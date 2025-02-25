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
from tests.mark_utils import arg_mark

import pytest
import mindspore.context as context
import mindspore.nn as nn
from mindspore.ops import operations as P
from mindspore import Tensor
from mindspore.common import dtype as mstype

context.set_context(mode=context.GRAPH_MODE, device_target="GPU")


class Net(nn.Cell):
    def __init__(self, shape, seed=0, seed2=0):
        super(Net, self).__init__()
        self.uniformreal = P.UniformReal(seed=seed)
        self.shape = shape

    def construct(self):
        return self.uniformreal(self.shape)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_net():
    seed = 10
    shape = (3, 2, 4)
    net = Net(shape, seed=seed)
    output = net()
    assert output.shape == (3, 2, 4)


class DynamicShapeNet(nn.Cell):
    def __init__(self, seed=0, seed2=0):
        super(DynamicShapeNet, self).__init__()
        self.seed = seed
        self.uniformreal = P.UniformReal(seed=seed)

    def construct(self, input_shape):
        return self.uniformreal(input_shape)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_net_dynamic_shape():
    """
    Feature: op dynamic shape
    Description: set input_shape None and input real tensor
    Expectation: success
    """

    seed = 10
    shape = Tensor((3, 2, 4), mstype.int64)
    shape_dyn = Tensor(shape=[None], dtype=shape.dtype)
    net = DynamicShapeNet(seed)
    net.set_inputs(shape_dyn)
    output = net(shape)
    assert output.shape == (3, 2, 4)
