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
"""
Test stop device api
"""
import os
from mindspore._c_expression import _stop_device
import mindspore.context as context
import mindspore.nn as nn
from mindspore.ops import operations as P
from mindspore import Tensor
from tests.mark_utils import arg_mark


class Net(nn.Cell):
    def __init__(self):
        super(Net, self).__init__()
        self.ops = P.Abs()

    def construct(self, x):
        return self.ops(x)

def train():
    context.set_context(mode=context.GRAPH_MODE, device_target='Ascend')
    net = Net()
    net(Tensor(2.0))


@arg_mark(plat_marks=['platform_ascend910b'], level_mark='level1', card_mark='allcards', essential_mark='unessential')
def test_stop_device():
    """
    Feature: Test stop device interface.
    Description: Test stop_device interface.
    Expectation: The interface stop_device can work successfully.
    """
    train()
    env_dic = os.environ
    device_id = int(env_dic.get('DEVICE_ID').lower()) if env_dic.get('DEVICE_ID') else 0
    _stop_device(device_id)
    try:
        train()
    except RuntimeError as e:
        assert str(e).find('ForceStopError') != -1
