# Copyright 2021 Huawei Technologies Co., Ltd
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
from tests.mark_utils import arg_mark

import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.ops import operations as P
from mindspore.ops.operations import _grad_ops as G


class NetSigmoidCrossEntropyWithLogits(nn.Cell):
    def __init__(self):
        super(NetSigmoidCrossEntropyWithLogits, self).__init__()
        self.loss = P.SigmoidCrossEntropyWithLogits()

    def construct(self, logits, labels):
        return self.loss(logits, labels)


class NetSigmoidCrossEntropyWithLogitsGrad(nn.Cell):
    def __init__(self):
        super(NetSigmoidCrossEntropyWithLogitsGrad, self).__init__()
        self.sigmoid_cross_entropy_with_logits_grad = G.SigmoidCrossEntropyWithLogitsGrad()

    def construct(self, logits, labels, dout):
        return self.sigmoid_cross_entropy_with_logits_grad(logits, labels, dout)


@arg_mark(plat_marks=['platform_ascend910b', 'platform_gpu'],
          level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_sigmoid_cross_entropy_with_logits():
    """
    Feature: test graph kernel SigmoidCrossEntropyWithLogits expander
    Description: SigmoidCrossEntropyWithLogits expander
    Expectation: the result match with the expected result
    """
    context.set_context(jit_level='O0')
    logits = Tensor(np.array([[1, 1, 2],
                              [1, 2, 1],
                              [2, 1, 1]]).astype(np.float32))
    labels = Tensor(np.array([[0, 0, 1],
                              [0, 1, 0],
                              [1, 0, 0]]).astype(np.float32))

    error = np.ones(shape=[3, 3]) * 1.0e-6

    context.set_context(mode=context.GRAPH_MODE, enable_graph_kernel=True)
    sigmoid_cross_entropy_with_logits = NetSigmoidCrossEntropyWithLogits()
    result_open_gk = sigmoid_cross_entropy_with_logits(logits, labels)

    context.set_context(mode=context.GRAPH_MODE, enable_graph_kernel=False)
    sigmoid_cross_entropy_with_logits_beta = NetSigmoidCrossEntropyWithLogits()
    result_close_gk = sigmoid_cross_entropy_with_logits_beta(logits, labels)
    diff = result_open_gk.asnumpy() - result_close_gk.asnumpy()
    assert np.all(abs(diff) < error)


@arg_mark(plat_marks=['platform_ascend910b', 'platform_gpu'],
          level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_sigmoid_cross_entropy_with_logits_grad():
    """
    Feature: test graph kernel SigmoidCrossEntropyWithLogitsGrad expander
    Description: SigmoidCrossEntropyWithLogitsGrad expander
    Expectation: the result match with the expected result
    """
    context.set_context(jit_level='O0')
    logits = Tensor(np.array([[1, 1, 2],
                              [1, 2, 1],
                              [2, 1, 1]]).astype(np.float32))
    labels = Tensor(np.array([[0, 0, 1],
                              [0, 1, 0],
                              [1, 0, 0]]).astype(np.float32))
    dout = Tensor(np.ones(shape=[3, 3]).astype(np.float32))

    error = np.ones(shape=[3, 3]) * 1.0e-6

    context.set_context(mode=context.GRAPH_MODE, enable_graph_kernel=True)
    sigmoid_cross_entropy_with_logits_grad = NetSigmoidCrossEntropyWithLogitsGrad()
    result_open_gk = sigmoid_cross_entropy_with_logits_grad(logits, labels, dout)

    context.set_context(mode=context.GRAPH_MODE, enable_graph_kernel=False)
    sigmoid_cross_entropy_with_logits_grad_beta = NetSigmoidCrossEntropyWithLogitsGrad()
    result_close_gk = sigmoid_cross_entropy_with_logits_grad_beta(logits, labels, dout)
    diff = result_open_gk.asnumpy() - result_close_gk.asnumpy()
    assert np.all(abs(diff) < error)
