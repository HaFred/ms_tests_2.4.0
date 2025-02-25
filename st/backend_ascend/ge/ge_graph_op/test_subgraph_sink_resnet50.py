# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
import numpy as np
import os
import subprocess
import shutil
import mindspore.nn as nn
from mindspore import Tensor, lazy_inline
from mindspore.ops import operations as P
import mindspore.context as context
from mindspore.nn import TrainOneStepCell, WithLossCell
from mindspore.nn.optim import Momentum
from tests.mark_utils import arg_mark


def weight_variable(shape):
    ones = np.ones(shape).astype(np.float32)
    return Tensor(ones * 0.01)


def weight_variable_0(shape):
    zeros = np.zeros(shape).astype(np.float32)
    return Tensor(zeros)


def weight_variable_1(shape):
    ones = np.ones(shape).astype(np.float32)
    return Tensor(ones)


def conv3x3(in_channels, out_channels, stride=1, padding=0):
    """3x3 convolution """
    weight_shape = (out_channels, in_channels, 3, 3)
    weight = weight_variable(weight_shape)
    return nn.Conv2d(in_channels, out_channels,
                     kernel_size=3, stride=stride, padding=padding, weight_init=weight, has_bias=False, pad_mode="same")


def conv1x1(in_channels, out_channels, stride=1, padding=0):
    """1x1 convolution"""
    weight_shape = (out_channels, in_channels, 1, 1)
    weight = weight_variable(weight_shape)
    return nn.Conv2d(in_channels, out_channels,
                     kernel_size=1, stride=stride, padding=padding, weight_init=weight, has_bias=False, pad_mode="same")


def conv7x7(in_channels, out_channels, stride=1, padding=0):
    """1x1 convolution"""
    weight_shape = (out_channels, in_channels, 7, 7)
    weight = weight_variable(weight_shape)
    return nn.Conv2d(in_channels, out_channels,
                     kernel_size=7, stride=stride, padding=padding, weight_init=weight, has_bias=False, pad_mode="same")


def bn_with_initialize(out_channels):
    shape = (out_channels)
    mean = weight_variable_0(shape)
    var = weight_variable_1(shape)
    beta = weight_variable_0(shape)
    gamma = weight_variable_1(shape)
    bn = nn.BatchNorm2d(out_channels, momentum=0.1, eps=0.0001, gamma_init=gamma,
                        beta_init=beta, moving_mean_init=mean, moving_var_init=var)
    return bn


def bn_with_initialize_last(out_channels):
    shape = (out_channels)
    mean = weight_variable_0(shape)
    var = weight_variable_1(shape)
    beta = weight_variable_0(shape)
    gamma = weight_variable_0(shape)
    bn = nn.BatchNorm2d(out_channels, momentum=0.1, eps=0.0001, gamma_init=gamma,
                        beta_init=beta, moving_mean_init=mean, moving_var_init=var)
    return bn


def fc_with_initialize(input_channels, out_channels):
    weight_shape = (out_channels, input_channels)
    bias_shape = (out_channels)
    weight = weight_variable(weight_shape)
    bias = weight_variable_0(bias_shape)

    return nn.Dense(input_channels, out_channels, weight, bias)


class ResidualBlock(nn.Cell):
    expansion = 4

    @lazy_inline
    def __init__(self,
                 in_channels,
                 out_channels,
                 stride=1):
        super(ResidualBlock, self).__init__()

        out_chls = out_channels // self.expansion
        self.conv1 = conv1x1(in_channels, out_chls, stride=1, padding=0)
        self.bn1 = bn_with_initialize(out_chls)

        self.conv2 = conv3x3(out_chls, out_chls, stride=stride, padding=0)
        self.bn2 = bn_with_initialize(out_chls)

        self.conv3 = conv1x1(out_chls, out_channels, stride=1, padding=0)
        self.bn3 = bn_with_initialize_last(out_channels)

        self.relu = P.ReLU()
        self.add = P.Add()

    def construct(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        out = self.add(out, identity)
        out = self.relu(out)

        return out


class ResidualBlockWithDown(nn.Cell):
    expansion = 4

    def __init__(self,
                 in_channels,
                 out_channels,
                 stride=1,
                 down_sample=False):
        super(ResidualBlockWithDown, self).__init__()

        out_chls = out_channels // self.expansion
        self.conv1 = conv1x1(in_channels, out_chls, stride=1, padding=0)
        self.bn1 = bn_with_initialize(out_chls)

        self.conv2 = conv3x3(out_chls, out_chls, stride=stride, padding=0)
        self.bn2 = bn_with_initialize(out_chls)

        self.conv3 = conv1x1(out_chls, out_channels, stride=1, padding=0)
        self.bn3 = bn_with_initialize_last(out_channels)

        self.relu = P.ReLU()
        self.downSample = down_sample

        self.conv_down_sample = conv1x1(in_channels, out_channels, stride=stride, padding=0)
        self.bn_down_sample = bn_with_initialize(out_channels)
        self.add = P.Add()

    def construct(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        identity = self.conv_down_sample(identity)
        identity = self.bn_down_sample(identity)

        out = self.add(out, identity)
        out = self.relu(out)

        return out


class MakeLayer0(nn.Cell):

    def __init__(self, block, in_channels, out_channels, stride):
        super(MakeLayer0, self).__init__()
        self.a = ResidualBlockWithDown(in_channels, out_channels, stride=1, down_sample=True)
        self.b = block(out_channels, out_channels, stride=stride)
        self.c = block(out_channels, out_channels, stride=1)

    def construct(self, x):
        x = self.a(x)
        x = self.b(x)
        x = self.c(x)

        return x


class MakeLayer1(nn.Cell):

    def __init__(self, block, in_channels, out_channels, stride):
        super(MakeLayer1, self).__init__()
        self.a = ResidualBlockWithDown(in_channels, out_channels, stride=stride, down_sample=True)
        self.b = block(out_channels, out_channels, stride=1)
        self.c = block(out_channels, out_channels, stride=1)
        self.d = block(out_channels, out_channels, stride=1)

    def construct(self, x):
        x = self.a(x)
        x = self.b(x)
        x = self.c(x)
        x = self.d(x)

        return x


class MakeLayer2(nn.Cell):

    def __init__(self, block, in_channels, out_channels, stride):
        super(MakeLayer2, self).__init__()
        self.a = ResidualBlockWithDown(in_channels, out_channels, stride=stride, down_sample=True)
        self.b = block(out_channels, out_channels, stride=1)
        self.c = block(out_channels, out_channels, stride=1)
        self.d = block(out_channels, out_channels, stride=1)
        self.e = block(out_channels, out_channels, stride=1)
        self.f = block(out_channels, out_channels, stride=1)

    def construct(self, x):
        x = self.a(x)
        x = self.b(x)
        x = self.c(x)
        x = self.d(x)
        x = self.e(x)
        x = self.f(x)

        return x


class MakeLayer3(nn.Cell):

    def __init__(self, block, in_channels, out_channels, stride):
        super(MakeLayer3, self).__init__()
        self.a = ResidualBlockWithDown(in_channels, out_channels, stride=stride, down_sample=True)
        self.b = block(out_channels, out_channels, stride=1)
        self.c = block(out_channels, out_channels, stride=1)

    def construct(self, x):
        x = self.a(x)
        x = self.b(x)
        x = self.c(x)

        return x


class ResNet(nn.Cell):

    def __init__(self, block, num_classes=100, batch_size=32):
        super(ResNet, self).__init__()
        self.batch_size = batch_size
        self.num_classes = num_classes

        self.conv1 = conv7x7(3, 64, stride=2, padding=0)

        self.bn1 = bn_with_initialize(64)
        self.relu = P.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, pad_mode="SAME")

        self.layer1 = MakeLayer0(block, in_channels=64, out_channels=256, stride=1)
        self.layer2 = MakeLayer1(block, in_channels=256, out_channels=512, stride=2)
        self.layer3 = MakeLayer2(block, in_channels=512, out_channels=1024, stride=2)
        self.layer4 = MakeLayer3(block, in_channels=1024, out_channels=2048, stride=2)

        self.pool = P.ReduceMean(keep_dims=True)
        self.fc = fc_with_initialize(512 * block.expansion, num_classes)
        self.flatten = nn.Flatten()

    def construct(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.pool(x, (-2, -1))
        x = self.flatten(x)
        x = self.fc(x)
        return x


def resnet50(batch_size, num_classes):
    return ResNet(ResidualBlock, num_classes, batch_size)


def train(net, data, label):
    learning_rate = 0.01
    momentum = 0.9

    optimizer = Momentum(filter(lambda x: x.requires_grad, net.get_parameters()), learning_rate, momentum)
    criterion = nn.SoftmaxCrossEntropyWithLogits(sparse=True)
    net_with_criterion = WithLossCell(net, criterion)
    train_network = TrainOneStepCell(net_with_criterion, optimizer)  # optimizer
    train_network.set_train()
    res = train_network(data, label)
    assert np.abs(np.sum(res.asnumpy()) - 73.68) < 0.01

@arg_mark(plat_marks=['platform_ascend910b'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_resnet50_lazyinline():
    """
    Feature: subgraph sink to GEGraphOp
    Description: Test subgraph sink to GEGraphOp
    Expectation: No exception.
    """
    os.environ['MS_DEV_DUMP_IR_PASSES'] = "hwopt_d_after_stream_assign"
    context.set_context(mode=context.GRAPH_MODE, jit_config={"jit_level": "O2"})
    ir_path = os.path.split(os.path.realpath(__file__))[0] +"/ir"
    context.set_context(save_graphs=2, save_graphs_path=ir_path)
    data = Tensor(np.ones([32, 3, 224, 224]).astype(np.float32) * 0.01)
    label = Tensor(np.ones([32]).astype(np.int32))
    net = resnet50(32, 10)
    train(net, data, label)

    # check if convert to GEGraphOp
    graph_file = f"{ir_path}/hwopt_d_after_stream_assign*.ir"
    graph_para = "GEGraphOp("
    graph_output = subprocess.check_output(
        ["grep -r '%s' %s | wc -l" % (graph_para, graph_file)],
        shell=True)
    graph_cnt = str(graph_output, 'utf-8').strip()
    assert graph_cnt == str(25)

    if os.path.exists(ir_path):
        shutil.rmtree(ir_path)
