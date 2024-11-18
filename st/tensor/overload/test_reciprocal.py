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
import pytest
from tests.mark_utils import arg_mark

import mindspore as ms
import mindspore.nn as nn


class Net(nn.Cell):
    def construct(self, x):
        return x.reciprocal()


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos', 'platform_gpu', 'platform_ascend',
                      'platform_ascend910b'],
          level_mark='level0',
          card_mark='onecard',
          essential_mark='unessential')
@pytest.mark.parametrize('mode', [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
def test_reciprocal_normal(mode):
    """
    Feature: reciprocal
    Description: Verify the result of reciprocal
    Expectation: success
    """
    ms.set_context(mode=mode, jit_config={"jit_level": "O0"})
    net = Net()
    x = ms.Tensor(np.array([1.0, 2.0, 4.0]), ms.float32)
    out = net(x)
    expect_out = np.array([1., 0.5, 0.25])
    assert np.allclose(out.asnumpy(), expect_out)
