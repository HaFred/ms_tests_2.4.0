# Copyright 2022 Huawei Technologies Co., Ltd
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
import mindspore.ops.operations._grad_ops as P
from mindspore import Tensor
from mindspore.common.api import jit


class SparseSegmentSqrtNGradNet(nn.Cell):
    def __init__(self):
        super(SparseSegmentSqrtNGradNet, self).__init__()
        self.net = P.SparseSegmentSqrtNGrad()

    @jit
    def construct(self, grad, indices, segment_ids, output_dim0):
        return self.net(grad, indices, segment_ids, output_dim0)


def sparse_segment_sqrt_n_grad(loss):
    context.set_context(mode=context.GRAPH_MODE, device_target='GPU')
    grad_np = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], dtype=np.float32)
    indices_np = np.array([0, 0, 1, 2, 2, 3], dtype=np.int32)
    segment_ids_np = np.array([0, 1, 2, 2, 3, 3], dtype=np.int32)
    output_dim0_np = np.array(8, dtype=np.int32)
    grad_ms = Tensor(grad_np)
    indices_ms = Tensor(indices_np)
    segment_ids_ms = Tensor(segment_ids_np)
    output_dim0_ms = Tensor(output_dim0_np)
    net_ms = SparseSegmentSqrtNGradNet()
    out_ms = net_ms(grad_ms, indices_ms, segment_ids_ms, output_dim0_ms)
    expected = np.array([[6, 8, 10, 12],
                         [6.363961, 7.071068, 7.7781744, 8.485281],
                         [15.55635, 16.970562, 18.384777, 19.798988],
                         [9.192389, 9.899495, 10.606602, 11.313708],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]], dtype=np.float32)
    assert np.allclose(out_ms.asnumpy(), expected, loss, loss)


def sparse_segment_sqrt_n_grad_pynative(loss):
    context.set_context(mode=context.PYNATIVE_MODE, device_target='GPU')
    grad_np = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], dtype=np.float64)
    indices_np = np.array([0, 1, 1, 2, 3, 3], dtype=np.int64)
    segment_ids_np = np.array([0, 0, 1, 2, 2, 3], dtype=np.int64)
    output_dim0_np = np.array(8, dtype=np.int64)
    grad_ms = Tensor(grad_np)
    indices_ms = Tensor(indices_np)
    segment_ids_ms = Tensor(segment_ids_np)
    output_dim0_ms = Tensor(output_dim0_np)
    net_ms = SparseSegmentSqrtNGradNet()
    out_ms = net_ms(grad_ms, indices_ms, segment_ids_ms, output_dim0_ms)
    expected = np.array([[0.70710678, 1.41421356, 2.12132034, 2.82842712],
                         [5.70710678, 7.41421356, 9.12132034, 10.82842712],
                         [6.36396103, 7.07106781, 7.77817459, 8.48528137],
                         [19.36396103, 21.07106781, 22.77817459, 24.48528137],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]], dtype=np.float64)
    assert np.allclose(out_ms.asnumpy(), expected, loss, loss)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_sparse_segment_sqrt_n_grad_graph_float32_int32_int32():
    """
    Feature: ALL To ALL
    Description: test cases for SparseSegmentSqrtNGrad
    Expectation: the result match to tensorflow
    """
    sparse_segment_sqrt_n_grad(loss=1.0e-4)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
def test_sparse_segment_sqrt_n_grad_pynative_float64_int64_int64():
    """
    Feature: ALL To ALL
    Description: test cases for SparseSegmentSqrtNGrad
    Expectation: the result match to tensorflow
    """
    sparse_segment_sqrt_n_grad_pynative(loss=1.0e-5)
