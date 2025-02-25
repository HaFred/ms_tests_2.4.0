# Copyright 2019-2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0(the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http:  // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
import mindspore.common.dtype as mstype
import mindspore.nn as nn
import numpy as np
import pytest
from mindspore.common.api import jit

from mindspore import Tensor, context
from mindspore.ops import operations as P
from tests.mark_utils import arg_mark

context.set_context(mode=context.GRAPH_MODE, device_target='CPU')


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.mul = P.Mul()

    @jit
    def construct(self, x, y):
        return self.mul(x, y)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_mul():
    x0 = Tensor(np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(np.float32))
    y0 = Tensor(np.random.uniform(-2, 2, (1, 1, 1, 1)).astype(np.float32))
    x1 = Tensor(np.random.uniform(-2, 2, (1, 3, 1, 4)).astype(np.float32))
    y1 = Tensor(np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(np.float32))
    x2 = Tensor(np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(np.float32))
    y2 = Tensor(2, mstype.float32)
    x3 = Tensor(2, mstype.float32)
    y3 = Tensor(2, mstype.float32)
    x4 = Tensor(np.random.uniform(-2, 2, (4)).astype(np.float32))
    y4 = Tensor(np.random.uniform(-2, 2, (4, 4)).astype(np.float32))
    mul = Net()
    out = mul(x0, y0).asnumpy()
    exp = x0.asnumpy() * y0.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x1, y1).asnumpy()
    exp = x1.asnumpy() * y1.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x2, y2).asnumpy()
    exp = x2.asnumpy() * y2.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x3, y3).asnumpy()
    exp = x3.asnumpy() * y3.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x4, y4).asnumpy()
    exp = x4.asnumpy() * y4.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_mul_int32():
    x0 = Tensor(np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(np.int32))
    y0 = Tensor(np.random.uniform(-2, 2, (1, 1, 1, 1)).astype(np.int32))
    x1 = Tensor(np.random.uniform(-2, 2, (1, 3, 1, 4)).astype(np.int32))
    y1 = Tensor(np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(np.int32))
    x2 = Tensor(np.random.uniform(-2, 2, (2, 3, 4, 4)).astype(np.int32))
    y2 = Tensor(2, mstype.int32)
    x3 = Tensor(2, mstype.int32)
    y3 = Tensor(2, mstype.int32)
    x4 = Tensor(np.random.uniform(-2, 2, (4)).astype(np.int32))
    y4 = Tensor(np.random.uniform(-2, 2, (4, 4)).astype(np.int32))
    mul = Net()
    out = mul(x0, y0).asnumpy()
    exp = x0.asnumpy() * y0.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x1, y1).asnumpy()
    exp = x1.asnumpy() * y1.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x2, y2).asnumpy()
    exp = x2.asnumpy() * y2.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x3, y3).asnumpy()
    exp = x3.asnumpy() * y3.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape

    out = mul(x4, y4).asnumpy()
    exp = x4.asnumpy() * y4.asnumpy()
    diff = np.abs(out - exp)
    err = np.ones(shape=exp.shape) * 1.0e-5
    assert np.all(diff < err)
    assert out.shape == exp.shape


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize('mode', [context.GRAPH_MODE, context.PYNATIVE_MODE])
def test_mul_tensor_api_modes(mode):
    """
    Feature: Test mul tensor api.
    Description: Test mul tensor api for Graph and PyNative modes.
    Expectation: The result match to the expect value.
    """
    context.set_context(mode=mode, device_target="CPU")
    x = Tensor([1.0, 2.0, 3.0], mstype.float32)
    y = Tensor([4.0, 5.0, 6.0], mstype.float32)
    output = x.mul(y)
    expected = np.array([4., 10., 18.], np.float32)
    np.testing.assert_array_equal(output.asnumpy(), expected)
