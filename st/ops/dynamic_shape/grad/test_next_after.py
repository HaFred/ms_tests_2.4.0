from tests.mark_utils import arg_mark
import numpy as np
import pytest
import mindspore as mp
from mindspore import nn, context, Tensor
from mindspore.ops.operations.math_ops import NextAfter
from .test_grad_of_dynamic import TestDynamicGrad


class NetNextAfter(nn.Cell):
    def __init__(self):
        super(NetNextAfter, self).__init__()
        self.nextafter = NextAfter()

    def construct(self, x1, x2):
        return self.nextafter(x1, x2)


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos', 'platform_gpu'], level_mark='level2',
          card_mark='onecard', essential_mark='unessential')
def test_dynamic_nextafter_shape():
    """
    Feature: NextAfter Grad DynamicShape.
    Description: Test case of dynamic shape for NextAfter grad operator on CPU, GPU and Ascend.
    Expectation: success.
    """
    context.set_context(mode=context.PYNATIVE_MODE)
    test_dynamic = TestDynamicGrad(NetNextAfter())
    x1 = Tensor(np.asarray([0.0]), mp.float32)
    x2 = Tensor(np.asarray([0.1]), mp.float32)
    test_dynamic.test_dynamic_grad_net([x1, x2])


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos', 'platform_gpu'], level_mark='level2',
          card_mark='onecard', essential_mark='unessential')
def test_dynamic_nextafter_rank():
    """
    Feature: NextAfter Grad DynamicRank.
    Description: Test case of dynamic rank for NextAfter grad operator on CPU, GPU and Ascend.
    Expectation: success.
    """
    context.set_context(mode=context.PYNATIVE_MODE)
    test_dynamic = TestDynamicGrad(NetNextAfter())
    x1 = Tensor(np.asarray([0.0]), mp.float32)
    x2 = Tensor(np.asarray([0.1]), mp.float32)
    test_dynamic.test_dynamic_grad_net([x1, x2], True)
