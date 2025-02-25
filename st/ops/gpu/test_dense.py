# Copyright 2020 Huawei Technologies Co., Ltd
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

import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor

context.set_context(device_target="GPU")


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.dense = nn.Dense(2048, 1001)

    def construct(self, x):
        return self.dense(x)


class MultiLayerDense(nn.Cell):
    def __init__(self):
        super(MultiLayerDense, self).__init__()
        self.dense1 = nn.Dense(in_channels=256, out_channels=512)
        self.dense2 = nn.Dense(in_channels=512, out_channels=1024)

    def construct(self, x):
        x = self.dense1(x)
        x = self.dense2(x)
        return x


def test_net():
    x = np.random.randn(32, 2048).astype(np.float32)
    net = Net()
    output = net(Tensor(x))
    print(x)
    print(output.asnumpy())


def test_net_ND():
    x = np.random.randn(2, 332, 2048).astype(np.float32)
    net = Net()
    output = net(Tensor(x))
    print(x)
    print(output.asnumpy())


def test_net_multilayer():
    x = np.random.randn(16, 32, 256).astype(np.float32)
    net = MultiLayerDense()
    output = net(Tensor(x))
    print(x)
    print(output.asnumpy())
