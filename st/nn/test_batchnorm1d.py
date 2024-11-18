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

import mindspore as ms
import mindspore.nn as nn
from mindspore import Tensor
from tests.mark_utils import arg_mark


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.batchnorm1d = nn.BatchNorm1d(num_features=4)

    def construct(self, x):
        out = self.batchnorm1d(x)
        return out


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos', 'platform_ascend'],
          level_mark='level0',
          card_mark='onecard',
          essential_mark='essential')
@pytest.mark.parametrize('mode', [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
def test_batchnorm1d_para_customed_dtype(mode):
    """
    Feature: BatchNorm1d
    Description: Verify the result of BatchNorm1d specifying customed para dtype.
    Expectation: success
    """
    ms.set_context(mode=mode)
    net = Net()
    x = Tensor(np.array([[0.7, 0.5, 0.5, 0.6],
                         [0.5, 0.4, 0.6, 0.9]]).astype(np.float16))
    output = net(x)
    expect_output_shape = (2, 4)
    assert np.allclose(expect_output_shape, output.shape)


class ParaNet(nn.Cell):
    def __init__(self):
        super(ParaNet, self).__init__()
        self.batchnorm1d = nn.BatchNorm1d(num_features=4, dtype=ms.float32)

    def construct(self, x):
        out = self.batchnorm1d(x)
        return out


@arg_mark(plat_marks=['platform_gpu'], level_mark='level0', card_mark='onecard', essential_mark='essential')
@pytest.mark.parametrize('mode', [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
def test_batchnorm1d_para_customed_dtype_float32(mode):
    """
    Feature: BatchNorm1d
    Description: Verify the result of BatchNorm1d specifying customed para dtype float32 on GPU.
    Expectation: success
    """
    ms.set_context(mode=mode)
    net = ParaNet()
    x = Tensor(np.array([[0.7, 0.5, 0.5, 0.6],
                         [0.5, 0.4, 0.6, 0.9]]).astype(np.float32))
    output = net(x)
    expect_output_shape = (2, 4)
    assert np.allclose(expect_output_shape, output.shape)
