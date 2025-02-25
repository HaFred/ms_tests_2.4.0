# Copyright 2019-2022 Huawei Technologies Co., Ltd
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

import mindspore as ms
import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.ops import operations as P


class NetExp(nn.Cell):
    def __init__(self):
        super(NetExp, self).__init__()
        self.exp = P.Exp()

    def construct(self, x):
        return self.exp(x)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
@pytest.mark.parametrize("dtype", [np.bool_, np.int8, np.int16, np.int32, np.int64,
                                   np.uint8, np.uint16, np.uint32, np.uint64,
                                   np.float16, np.float32, np.float64,
                                   np.complex64, np.complex128])
@pytest.mark.parametrize("mode", [context.GRAPH_MODE, context.PYNATIVE_MODE])
def test_exp(dtype, mode):
    """
    Feature: test Exp op float32 on GPU
    Description: test Exp
    Expectation: success.
    """
    x0_np = np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(dtype)
    x1_np = np.random.uniform(-2, 2, 1).astype(dtype)
    x0 = Tensor(x0_np)
    x1 = Tensor(x1_np)
    expect0 = np.exp(x0_np)
    expect1 = np.exp(x1_np)
    error0 = np.ones(shape=expect0.shape) * 1.0e-3
    error1 = np.ones(shape=expect1.shape) * 1.0e-3

    context.set_context(mode=mode, device_target="GPU")
    exp = NetExp()
    output0 = exp(x0)
    diff0 = output0.asnumpy() - expect0
    assert np.all(diff0 < error0)
    assert output0.shape == expect0.shape
    output1 = exp(x1)
    diff1 = output1.asnumpy() - expect1
    assert np.all(diff1 < error1)
    assert output1.shape == expect1.shape


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_exp_dyn():
    """
    Feature: dynamic shape operator Exp on GPU
    Description: test dynamic shape of Exp
    Expectation: success or throw AssertionError exception.
    """
    x_np = np.random.uniform(-2, 2, 1).astype(np.float32)
    input_dyn = Tensor(shape=[None, ], dtype=ms.float32)

    context.set_context(mode=context.GRAPH_MODE, device_target="GPU")
    net = NetExp()
    net.set_inputs(input_dyn)
    out = net(ms.Tensor(x_np))
    expect = np.exp(x_np)
    error = np.ones(shape=expect.shape) * 1.0e-5
    diff = out.asnumpy() - expect
    assert np.all(diff < error)
