# Copyright 2024 Huawei Technologies Co., Ltd
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
from mindspore.mint import cummin
from mindspore import ops, Tensor
import mindspore as ms
from tests.st.utils import test_utils
from tests.st.ops.dynamic_shape.test_op_utils import TEST_OP


def generate_random_input(shape, dtype):
    return np.random.randn(*shape).astype(dtype)


@test_utils.run_with_cell
def cummin_forward_func(x, axis):
    return cummin(x, axis)


@test_utils.run_with_cell
def cummin_backward_func(x, axis):
    return ops.grad(cummin_forward_func, (0))(x, axis)


@test_utils.run_with_cell
def cummin_vmap_func(x, axis):
    return ops.vmap(cummin_forward_func, in_axes=(0, None), out_axes=(0, None))(x, axis)


@pytest.mark.level0
@pytest.mark.env_onecard
@pytest.mark.platform_arm_ascend_training
@pytest.mark.parametrize('mode', ['pynative', 'KBK'])
@pytest.mark.parametrize("dtype", [np.int8, np.int16, np.int32, np.int64, np.uint8,
                                   np.float64, np.float32, np.float16])
def test_mint_cummin(mode, dtype):
    """
    Feature: cummin ops.
    Description: test ops cummin forward.
    Expectation: output right results.
    """
    x = Tensor(np.array([[3, 1, 4, 1], [1, 5, 9, 2]]).astype(dtype))
    axis = -2
    expect_values = np.asarray([[3, 1, 4, 1], [1, 1, 4, 1]]).astype(dtype)
    expect_indices = np.asarray([[0, 0, 0, 0], [1, 0, 0, 0]]).astype(np.int64)
    expect_grad = np.asarray([[1, 2, 2, 2], [1, 0, 0, 0]]).astype(dtype)
    if mode == 'pynative':
        ms.context.set_context(mode=ms.PYNATIVE_MODE)
        output = cummin_forward_func(x, axis)
        output_grad = cummin_backward_func(x, axis)
    elif mode == 'KBK':
        ms.context.set_context(mode=ms.GRAPH_MODE)
        op_froward = ms.jit(cummin_forward_func, jit_config=ms.JitConfig(jit_level="O0"))
        output = op_froward(x, axis)
        op_backward = ms.jit(cummin_backward_func, jit_config=ms.JitConfig(jit_level="O0"))
        output_grad = op_backward(x, axis)
    assert np.allclose(output[0].asnumpy(), expect_values)
    assert np.allclose(output[1].asnumpy(), expect_indices)
    assert np.allclose(output_grad.asnumpy(), expect_grad)


@pytest.mark.level1
@pytest.mark.env_onecard
@pytest.mark.platform_arm_ascend_training
@pytest.mark.parametrize("context_mode", [ms.PYNATIVE_MODE])
@pytest.mark.parametrize("dtype", [np.int8, np.int16, np.int32, np.int64, np.uint8,
                                   np.float64, np.float32, np.float16])
def test_cummin_vmap(context_mode, dtype):
    """
    Feature: Vmap.
    Description: test vmap of op cummin.
    Expectation: expect correct result.
    """
    ms.context.set_context(mode=context_mode)
    np_array = np.array([[[1, 2, 3, 4], [5, 6, 7, 8]]]).astype(dtype)
    x = Tensor(np_array)
    axis = -1
    nest_vmap = ops.vmap(ops.vmap(cummin_forward_func, in_axes=(0, None)), in_axes=(0, None))
    values, indices = nest_vmap(x, axis)
    expect_values = np.array([[[1, 1, 1, 1], [5, 5, 5, 5]]]).astype(dtype)
    expect_indices = np.array([[[0, 0, 0, 0], [0, 0, 0, 0]]]).astype(np.int64)
    assert (values.asnumpy() == expect_values).all()
    assert (indices.asnumpy() == expect_indices).all()


@pytest.mark.level1
@pytest.mark.env_onecard
@pytest.mark.platform_arm_ascend_training
def test_cummin_dynamic():
    """
    Feature: cummin ops.
    Description: test ops cummin forward.
    Expectation: output right results.
    """
    ms.context.set_context(mode=ms.PYNATIVE_MODE)
    test_cell = test_utils.to_cell_obj(cummin_forward_func)
    input1 = Tensor(generate_random_input((3, 4, 5), np.float32))
    axis1 = 1
    input2 = Tensor(generate_random_input((2, 3, 5, 4), np.float32))
    axis2 = -2
    TEST_OP(test_cell, [[input1, axis1], [input2, axis2]], "cummin", disable_mode=["GRAPH_MODE"])
