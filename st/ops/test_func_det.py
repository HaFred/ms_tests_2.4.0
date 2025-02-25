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
from tests.mark_utils import arg_mark
import numpy as np
import pytest
import mindspore.common.dtype as mstype
import mindspore.nn as nn
import mindspore.ops as ops
from mindspore import Tensor
from mindspore import context


class Net(nn.Cell):
    def construct(self, x):
        return ops.det(x)


@arg_mark(plat_marks=['platform_ascend', 'platform_gpu', 'cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level2',
          card_mark='onecard', essential_mark='unessential')
@pytest.mark.parametrize('mode', [context.GRAPH_MODE, context.PYNATIVE_MODE])
def test_det(mode):
    """
    Feature: ops.det(x)
    Description: Verify the result of ops.det(x)
    Expectation: success
    """
    context.set_context(mode=mode)
    net = Net()
    x = Tensor([[1.5, 2.0], [3, 4.6]], dtype=mstype.float32)
    output = net(x)
    expected = np.array(0.9)
    assert np.allclose(output.asnumpy(), expected)
