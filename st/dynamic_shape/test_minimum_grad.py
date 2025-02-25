# Copyright 2023 Huawei Technologies Co., Ltd
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
import pytest
from tests.st.utils import test_utils
from tests.mark_utils import arg_mark

from mindspore import ops
from mindspore.common.api import _pynative_executor
import mindspore as ms


@test_utils.run_with_cell
def minimum_grad_forward_func(x1, x2, grads):
    return ops.auto_generate.MinimumGrad(grad_x=True, grad_y=True)(x1, x2, grads)


@test_utils.run_with_cell
def minimum_grad_vmap_func(x1, x2, grads):
    return ops.vmap(minimum_grad_forward_func, in_axes=0, out_axes=0)(x1, x2, grads)


@arg_mark(plat_marks=['platform_ascend', 'platform_gpu', 'cpu_linux'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize("context_mode", [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
@pytest.mark.parametrize("data_type", [np.float32])
@test_utils.run_test_with_On
def test_minimum_grad_op_forward(context_mode, data_type):
    """
    Feature: Ops.
    Description: test op minimum_grad forward.
    Expectation: expect correct result.
    """
    ms.context.set_context(mode=context_mode)
    x1 = ms.Tensor(np.array([1, 2, 4]).astype(data_type))
    x2 = ms.Tensor(np.array([2, 4, 3]).astype(data_type))
    grads = ms.Tensor(np.array([1., 2., 3.]).astype(data_type))
    out = minimum_grad_forward_func(x1, x2, grads)
    expect_out = np.array([[1., 2., 0.], [0., 0., 3.]]).astype(np.float32)
    np.testing.assert_allclose(out[0].asnumpy(), expect_out[0], rtol=1e-3)
    np.testing.assert_allclose(out[1].asnumpy(), expect_out[1], rtol=1e-3)


@arg_mark(plat_marks=['platform_ascend', 'platform_gpu', 'cpu_linux'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize("context_mode", [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
@pytest.mark.parametrize("data_type", [np.float32])
@test_utils.run_test_with_On
def test_minimum_grad_op_vmap(context_mode, data_type):
    """
    Feature: test vmap function.
    Description: test minimum_grad op vmap.
    Expectation: expect correct result.
    """
    ms.context.set_context(mode=context_mode)
    x1 = ms.Tensor(np.array([[3, 5, 11], [7, 5, 6]]).astype(data_type))
    x2 = ms.Tensor(np.array([[6, 6, 8], [3, 2, 7]]).astype(data_type))
    grads = ms.Tensor(np.array([[1., 2., 3.], [1., 2., 3.]]).astype(data_type))
    out = minimum_grad_vmap_func(x1, x2, grads)
    expect_out = np.array([[[1., 2., 0.], [0., 0., 3.]], [[0., 0., 3.], [1., 2., 0.]]]).astype(np.float32)
    np.testing.assert_allclose(out[0].asnumpy(), expect_out[0], rtol=1e-3)
    np.testing.assert_allclose(out[1].asnumpy(), expect_out[1], rtol=1e-3)


@arg_mark(plat_marks=['platform_ascend', 'platform_gpu', 'cpu_linux'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize("context_mode", [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
@test_utils.run_test_with_On
def test_minimum_grad_op_dynamic_shape(context_mode):
    """
    Feature: minimum_grad ops.
    Description: test ops minimum_grad dynamic shape tensor input.
    Expectation: expect correct result.
    """
    ms.context.set_context(mode=context_mode)
    x1_dyn = ms.Tensor(shape=[None], dtype=ms.float32)
    x2_dyn = ms.Tensor(shape=[None], dtype=ms.float32)
    grads_dyn = ms.Tensor(shape=[None], dtype=ms.float32)
    test_cell = test_utils.to_cell_obj(ops.auto_generate.MinimumGrad())
    test_cell.set_inputs(x1_dyn, x2_dyn, grads_dyn)
    x1 = ms.Tensor(np.array([1, 2, 4]).astype(np.float32))
    x2 = ms.Tensor(np.array([2, 4, 3]).astype(np.float32))
    grads = ms.Tensor(np.array([1., 2., 3.]).astype(np.float32))
    out = test_cell(x1, x2, grads)
    expect_out = np.array([[1., 2., 0.], [0., 0., 3.]]).astype(np.float32)
    np.testing.assert_allclose(out[0].asnumpy(), expect_out[0], rtol=1e-3)
    np.testing.assert_allclose(out[1].asnumpy(), expect_out[1], rtol=1e-3)

    x1_2 = ms.Tensor(np.array([3, 6, 2]).astype(np.float32))
    x2_2 = ms.Tensor(np.array([7, 5, 9]).astype(np.float32))
    grads_2 = ms.Tensor(np.array([3., 5., 2.]).astype(np.float32))
    out_2 = test_cell(x1_2, x2_2, grads_2)
    expect_out_2 = np.array([[3., 0., 2.], [0., 5., 0.]]).astype(np.float32)
    np.testing.assert_allclose(out_2[0].asnumpy(), expect_out_2[0], rtol=1e-3)
    np.testing.assert_allclose(out_2[1].asnumpy(), expect_out_2[1], rtol=1e-3)


@arg_mark(plat_marks=['platform_gpu', 'cpu_linux'], level_mark='level0', card_mark='onecard',
          essential_mark='essential')
@pytest.mark.parametrize("context_mode", [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
@test_utils.run_test_with_On
def test_minimum_grad_op_dynamic_rank(context_mode):
    """
    Feature: minimum_grad ops.
    Description: test ops minimum_grad dynamic rank tensor input.
    Expectation: expect correct result.
    """
    ms.context.set_context(mode=context_mode)
    x1_dyn = ms.Tensor(shape=None, dtype=ms.float32)
    x2_dyn = ms.Tensor(shape=None, dtype=ms.float32)
    grads_dyn = ms.Tensor(shape=None, dtype=ms.float32)
    test_cell = test_utils.to_cell_obj(ops.auto_generate.MinimumGrad())
    test_cell.set_inputs(x1_dyn, x2_dyn, grads_dyn)
    x1 = ms.Tensor(np.array([1, 2, 4]).astype(np.float32))
    x2 = ms.Tensor(np.array([2, 4, 3]).astype(np.float32))
    grads = ms.Tensor(np.array([1., 2., 3.]).astype(np.float32))
    out = test_cell(x1, x2, grads)
    expect_out = np.array([[1., 2., 0.], [0., 0., 3.]]).astype(np.float32)
    np.testing.assert_allclose(out[0].asnumpy(), expect_out[0], rtol=1e-3)
    np.testing.assert_allclose(out[1].asnumpy(), expect_out[1], rtol=1e-3)

    x1_2 = ms.Tensor(np.array([3, 6, 2, 7]).astype(np.float32))
    x2_2 = ms.Tensor(np.array([7, 5, 9, 2]).astype(np.float32))
    grads_2 = ms.Tensor(np.array([3., 5., 2., 2.]).astype(np.float32))
    out_2 = test_cell(x1_2, x2_2, grads_2)
    expect_out_2 = np.array([[3., 0., 2., 0.], [0., 5., 0., 2.]]).astype(np.float32)
    np.testing.assert_allclose(out_2[0].asnumpy(), expect_out_2[0], rtol=1e-3)
    np.testing.assert_allclose(out_2[1].asnumpy(), expect_out_2[1], rtol=1e-3)


@arg_mark(plat_marks=['platform_gpu'], level_mark='level1', card_mark='onecard', essential_mark='unessential')
@pytest.mark.parametrize("context_mode", [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
@pytest.mark.parametrize("data_type", [np.complex64])
@test_utils.run_test_with_On
def test_minimum_grad_op_dtype_check(context_mode, data_type):
    """
    Feature: Ops.
    Description: test op minimum_grad forward.
    Expectation: expect correct result.
    """
    ms.context.set_context(mode=context_mode)
    x1 = ms.Tensor(np.array([1, 2, 4]).astype(data_type))
    x2 = ms.Tensor(np.array([2, 4, 3]).astype(data_type))
    grads = ms.Tensor(np.array([1., 2., 3.]).astype(data_type))
    with pytest.raises(TypeError):
        _ = minimum_grad_forward_func(x1, x2, grads)
        _pynative_executor.sync()
