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
from mindspore import nn
from mindspore.ops import operations as P
from mindspore import Tensor
from mindspore import context
from .test_grad_of_dynamic import TestDynamicGrad


class LogMatrixDeterminantNet(nn.Cell):
    def __init__(self):
        super(LogMatrixDeterminantNet, self).__init__()
        self.log_matrix_determinant = P.LogMatrixDeterminant()

    def construct(self, input_x):
        output = self.log_matrix_determinant(input_x)
        return output


@arg_mark(plat_marks=['platform_gpu', 'cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level2',
          card_mark='onecard', essential_mark='unessential')
def test_dynamic_shape_log_matrix_determinant():
    """
    Feature: LogMatrixDeterminant Grad DynamicShape.
    Description: Test case of dynamic shape for LogMatrixDeterminant grad operator on CPU and GPU.
    Expectation: success.
    """
    context.set_context(mode=context.PYNATIVE_MODE)
    input_x = np.random.random((4, 4)).astype(np.float32)
    test_dynamic = TestDynamicGrad(LogMatrixDeterminantNet())
    test_dynamic.test_dynamic_grad_net(
        [Tensor(input_x)], False)


@arg_mark(plat_marks=['platform_gpu', 'cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level2',
          card_mark='onecard', essential_mark='unessential')
def test_dynamic_rank_log_matrix_determinant():
    """
    Feature: LogMatrixDeterminant Grad DynamicShape.
    Description: Test case of dynamic rank for LogMatrixDeterminant grad operator on CPU and GPU.
    Expectation: success.
    """
    context.set_context(mode=context.PYNATIVE_MODE)
    input_x = np.random.random((4, 4)).astype(np.float32)
    test_dynamic = TestDynamicGrad(LogMatrixDeterminantNet())
    test_dynamic.test_dynamic_grad_net(
        [Tensor(input_x)], True)
