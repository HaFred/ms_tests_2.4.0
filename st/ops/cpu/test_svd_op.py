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
import numpy as np
from mindspore.ops.operations import linalg_ops, array_ops
from mindspore.ops.primitive import constexpr

import mindspore
from mindspore import context, ops, nn, Tensor
from tests.mark_utils import arg_mark

context.set_context(mode=context.GRAPH_MODE, device_target='CPU')
RTOL = 1.e-5
ATOL = 1.e-6

k_0 = Tensor(0, mindspore.int32)
matmul = ops.MatMul()
batch_matmul = ops.BatchMatMul()
transpose = ops.Transpose()


@constexpr
def make_zero_matrix(shape, dtype):
    return Tensor(np.zeros(shape), dtype)


def matrix_diag(diagonal, shape):
    assist_matrix = make_zero_matrix(shape, ops.DType()(diagonal))
    return array_ops.MatrixSetDiagV3()(assist_matrix, diagonal, k_0)


class SvdNet(nn.Cell):

    def __init__(self, full_matrices=False, compute_uv=True):
        super(SvdNet, self).__init__()
        self.svd = linalg_ops.Svd(full_matrices=full_matrices,
                                  compute_uv=compute_uv)

    def construct(self, a):
        return self.svd(a)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_dynamic_shape():
    """
    Feature: test svd op in cpu.
    Description: test the ops in dynamic shape.
    Expectation: expect correct shape result.
    """
    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')
    net = SvdNet(True, True)
    a_dyn = Tensor(shape=[None, None], dtype=mindspore.float32)
    net.set_inputs(a_dyn)
    a = Tensor([[1, 2], [-4, -5], [2, 1]], dtype=mindspore.float32)
    s, u, v = net(a)
    expect_s_shape = (2,)
    expect_u_shape = (3, 3)
    expect_v_shape = (2, 2)
    assert s.asnumpy().shape == expect_s_shape
    assert u.asnumpy().shape == expect_u_shape
    assert v.asnumpy().shape == expect_v_shape


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_net1():
    """
    Feature: Svd
    Description: test cases for svd: m >= n and full_matrices=False, compute_uv=False
    Expectation: the result match to numpy
    """
    a = np.random.rand(3, 2)
    tensor_a = Tensor(a, dtype=mindspore.float32)
    mscp_svd_net = SvdNet(False, False)
    s, _, _ = mscp_svd_net(tensor_a)
    n_s = np.linalg.svd(a, full_matrices=False, compute_uv=False)
    assert np.allclose(n_s, s.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_net2():
    """
    Feature: Svd
    Description: test cases for svd: m >= n and full_matrices=True, compute_uv=True
    Expectation: the result match to numpy
    """
    a = np.random.rand(3, 2)
    tensor_a = Tensor(a, dtype=mindspore.float64)
    mscp_svd_net = SvdNet(True, True)
    s, u, v = mscp_svd_net(tensor_a)

    output = matmul(u, matmul(matrix_diag(s, (3, 2)), transpose(v, (1, 0))))
    assert np.allclose(a, output.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_net3():
    """
    Feature: Svd
    Description: test cases for svd: m >= n and full_matrices=False, compute_uv=True
    Expectation: the result match to numpy
    """
    a = np.random.rand(3, 2)
    tensor_a = Tensor(a, dtype=mindspore.float32)
    s, u, v = ops.svd(tensor_a, False, True)
    output = matmul(u, matmul(matrix_diag(s, (2, 2)), transpose(v, (1, 0))))
    assert np.allclose(a, output.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_net4():
    """
    Feature: Svd
    Description: test cases for svd: m < n and full_matrices=True, compute_uv=True
    Expectation: the result match to numpy
    """
    a = np.random.rand(2, 3)
    tensor_a = Tensor(a, dtype=mindspore.float64)
    s, u, v = ops.svd(tensor_a, True, True)
    output = matmul(u, matmul(matrix_diag(s, (2, 3)), transpose(v, (1, 0))))
    assert np.allclose(a, output.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_net5():
    """
    Feature: Svd
    Description: test cases for svd: inputs shape is (a, b, m, n), m > n
    Expectation: the result match to numpy
    """
    a = np.random.rand(5, 5, 3, 2)
    tensor_a = Tensor(a, dtype=mindspore.float32)
    s, u, v = ops.svd(tensor_a, True, True)

    output = batch_matmul(
        u,
        batch_matmul(matrix_diag(s, (5, 5, 3, 2)), transpose(v, (0, 1, 3, 2))))
    assert np.allclose(a, output.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
def test_svd_net6():
    """
    Feature: Svd
    Description: test cases for svd: specific input 3*2
    Expectation: the result match to numpy
    """
    a = np.array([[1, 2], [-4, -5], [2, 1]])
    tensor_a = Tensor(a, dtype=mindspore.float32)
    s, u, v = linalg_ops.Svd(full_matrices=True, compute_uv=True)(tensor_a)
    output = matmul(u, matmul(matrix_diag(s, (3, 2)), transpose(v, (1, 0))))
    assert np.allclose(a, output.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_svd_vmap1():
    """
    Feature: Svd
    Description: test cases for svd: vmap
    Expectation: the result match to numpy
    """
    a = np.random.rand(5, 3, 3)
    tensor_a = Tensor(a, dtype=mindspore.float32)
    net = SvdNet(True, True)
    svd_vmap = ops.vmap(net, (0,), 0)
    s, u, v = svd_vmap(tensor_a)
    output = batch_matmul(
        u, batch_matmul(matrix_diag(s, (5, 3, 3)), transpose(v, (0, 2, 1))))
    assert np.allclose(a, output.asnumpy(), rtol=RTOL, atol=ATOL)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_svd_vmap2():
    """
    Feature: Svd
    Description: test cases for svd: vmap
    Expectation: the result match to numpy
    """
    a = np.random.rand(5, 3, 3)
    tensor_a = Tensor(a, dtype=mindspore.float32)
    net = SvdNet(True, False)
    svd_vmap = ops.vmap(net, (0,), 0)
    s, _, _ = svd_vmap(tensor_a)
    n_s = np.linalg.svd(a, full_matrices=True, compute_uv=False)
    assert np.allclose(n_s, s.asnumpy(), rtol=RTOL, atol=ATOL)
