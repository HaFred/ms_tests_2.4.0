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

import numpy as np
import pytest

import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.ops.operations import _grad_ops as G


class NetEluGrad(nn.Cell):
    def __init__(self):
        super(NetEluGrad, self).__init__()
        self.eluGrad = G.EluGrad()

    def construct(self, x, dy):
        return self.eluGrad(dy, x)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_elu_grad_fp16():
    x = Tensor(np.array([[0.5, 2, 5.5], [4.5, -2, 0]]).astype(np.float16))
    dy = Tensor(np.array([[2, 1, 1.5], [-0.5, -1, -3]]).astype(np.float16))
    expect = np.array([[2, 1, 1.5], [-0.5, 1, -3]]).astype(np.float16)
    error = np.ones(shape=[2, 3]) * 1.0e-6

    context.set_context(mode=context.GRAPH_MODE, device_target="GPU")
    elu_grad = NetEluGrad()
    output = elu_grad(x, dy)
    diff = output.asnumpy() - expect
    assert np.all(diff < error)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_elu_grad_fp32():
    x = Tensor(np.array([[0.5, 2, 5.5], [4.5, -2, 0]]).astype(np.float32))
    dy = Tensor(np.array([[2, 1, 1.5], [-0.5, -1, -3]]).astype(np.float32))
    expect = np.array([[2, 1, 1.5], [-0.5, 1, -3]]).astype(np.float32)
    error = np.ones(shape=[2, 3]) * 1.0e-6

    context.set_context(mode=context.GRAPH_MODE, device_target="GPU")
    elu_grad = NetEluGrad()
    output = elu_grad(x, dy)
    diff = output.asnumpy() - expect
    assert np.all(diff < error)
