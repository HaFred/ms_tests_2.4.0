# Copyright 2020-2022 Huawei Technologies Co., Ltd
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
import numpy as np
import pytest

import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.common.api import jit
from mindspore.ops import operations as P
from mindspore.ops.composite import GradOperation

context.set_context(mode=context.GRAPH_MODE, device_target='CPU')


class Grad(nn.Cell):
    def __init__(self, network):
        super(Grad, self).__init__()
        self.grad = GradOperation(get_all=True, sens_param=True)
        self.network = network

    @jit
    def construct(self, input_, output_grad):
        return self.grad(self.network)(input_, output_grad)


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.ops = P.Square()

    def construct(self, x):
        return self.ops(x)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize('dtype', [np.int32, np.int64, np.float32, np.float64])
def test_net(dtype):
    """
    Feature: ALL To ALL
    Description: test cases for Square
    Expectation: the result match to numpy
    """
    x = np.random.randn(2, 3, 3, 4).astype(dtype)
    y_expect = x * x
    net = Net()
    out = net(Tensor(x))
    diff = out.asnumpy() - y_expect
    err = np.ones(shape=y_expect.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == y_expect.shape
    sens = np.random.randn(2, 3, 3, 4).astype(dtype)
    backword_net = Grad(Net())
    output = backword_net(Tensor(x), Tensor(sens))
    print(len(output))
    print(output[0].asnumpy())
