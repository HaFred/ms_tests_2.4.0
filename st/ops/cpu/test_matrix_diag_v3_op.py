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

import pytest
import numpy as np
import mindspore.nn as nn
from mindspore import dtype as mstype
from mindspore import Tensor
from mindspore import context
from mindspore.ops.operations.array_ops import MatrixDiagV3


class Net(nn.Cell):
    def __init__(self, align):
        super(Net, self).__init__()
        self.op = MatrixDiagV3(align)

    def construct(self, x, k, num_rows, num_cols, padding_value):
        output = self.op(x, k, num_rows, num_cols, padding_value)
        return output


def benchmark(diagonal, expect, align="RIGHT_LEFT", k=None, num_rows=None, num_cols=None, padding_value=None,
              error=1e-7):
    if k is None:
        k = 0
    if num_rows is None:
        num_rows = -1
    if num_cols is None:
        num_cols = -1
    if padding_value is None:
        padding_value = 0
    ms_diagonal = Tensor(diagonal)
    ms_k = Tensor(k, dtype=mstype.int32)
    ms_num_rows = Tensor(num_rows, dtype=mstype.int32)
    ms_num_cols = Tensor(num_cols, dtype=mstype.int32)
    ms_padding_value = Tensor(padding_value, dtype=ms_diagonal.dtype)
    output = Net(align)(ms_diagonal, k=ms_k, num_rows=ms_num_rows, num_cols=ms_num_cols, padding_value=ms_padding_value)
    np.testing.assert_allclose(output.asnumpy(), expect, rtol=error, atol=error)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize("data_shape", [(8,)])
@pytest.mark.parametrize("data_type", [np.int32, np.int64, np.float32, np.float64])
def test_matrix_diag_v1(data_shape, data_type):
    """
    Feature: MatrixDiagV3 operator.
    Description: Compatible with np.diag.
    Expectation: The result matches numpy.
    """
    context.set_context(mode=context.PYNATIVE_MODE, device_target='CPU')
    diagonal = np.random.randint(100, size=data_shape).astype(data_type)
    expect = np.diag(diagonal)
    benchmark(diagonal, expect)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize("data_type", [np.uint32, np.uint64, np.int8, np.int16])
def test_matrix_diag_v3_1(data_type):
    """
    Feature: MatrixDiagV3 operator.
    Description: A specific case 1/2/3.
    Expectation: success.
    """
    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')
    # Case 1
    diagonal = np.array([[1, 2, 3, 4],
                         [5, 6, 7, 8]]).astype(data_type)
    expect = np.array([[[1, 0, 0, 0],
                        [0, 2, 0, 0],
                        [0, 0, 3, 0],
                        [0, 0, 0, 4]],
                       [[5, 0, 0, 0],
                        [0, 6, 0, 0],
                        [0, 0, 7, 0],
                        [0, 0, 0, 8]]]).astype(data_type)
    benchmark(diagonal, expect)
    # Case 2
    diagonal = np.array([[1, 2, 3],
                         [4, 5, 6]]).astype(data_type)
    k = 1
    expect = np.array([[[0, 1, 0, 0],
                        [0, 0, 2, 0],
                        [0, 0, 0, 3],
                        [0, 0, 0, 0]],
                       [[0, 4, 0, 0],
                        [0, 0, 5, 0],
                        [0, 0, 0, 6],
                        [0, 0, 0, 0]]]).astype(data_type)
    benchmark(diagonal, expect, k=k)
    # Case 3
    diagonal = np.array([[[0, 8, 9],
                          [1, 2, 3],
                          [4, 5, 0]],
                         [[0, 2, 3],
                          [6, 7, 9],
                          [9, 1, 0]]]).astype(data_type)
    k = (-1, 1)
    expect = np.array([[[1, 8, 0],
                        [4, 2, 9],
                        [0, 5, 3]],
                       [[6, 2, 0],
                        [9, 7, 3],
                        [0, 1, 9]]]).astype(data_type)
    benchmark(diagonal, expect, k=k)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize("data_type", [np.uint8, np.uint16, np.float16])
def test_matrix_diag_v3_2(data_type):
    """
    Feature: MatrixDiagV3 operator.
    Description: A specific case 4/5/6.
    Expectation: success.
    """
    context.set_context(mode=context.PYNATIVE_MODE, device_target='CPU')
    # Case 4
    diagonal = np.array([[[8, 9, 0],
                          [1, 2, 3],
                          [0, 4, 5]],
                         [[2, 3, 0],
                          [6, 7, 9],
                          [0, 9, 1]]]).astype(data_type)
    k = (-1, 1)
    expect = np.array([[[1, 8, 0],
                        [4, 2, 9],
                        [0, 5, 3]],
                       [[6, 2, 0],
                        [9, 7, 3],
                        [0, 1, 9]]]).astype(data_type)
    benchmark(diagonal, expect, k=k, align="LEFT_RIGHT")
    # Case 5
    diagonal = np.array([1, 2]).astype(data_type)
    expect = np.array([[0, 0, 0, 0],
                       [1, 0, 0, 0],
                       [0, 2, 0, 0]]).astype(data_type)
    benchmark(diagonal, expect, k=-1, num_rows=3, num_cols=4)
    # Case 6
    expect = np.array([[9, 9],
                       [1, 9],
                       [9, 2]]).astype(data_type)
    benchmark(diagonal, expect, k=-1, num_rows=3, padding_value=9)
