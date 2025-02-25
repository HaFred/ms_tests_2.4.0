from tests.mark_utils import arg_mark
import numpy as np
import pytest
import mindspore
import mindspore.context as context
from mindspore import Tensor
from mindspore.common.api import jit
import mindspore.nn as nn
from mindspore.ops.operations.math_ops import NextAfter


class NextAfterNet(nn.Cell):
    def __init__(self):
        super(NextAfterNet, self).__init__()
        self.nextafter = NextAfter()

    @jit
    def construct(self, x, y):
        return self.nextafter(x, y)


def nextafter_graph(x1, x2):
    context.set_context(mode=context.GRAPH_MODE, device_target='CPU')
    net_msp = NextAfterNet()
    out_msp = net_msp(Tensor(x1), Tensor(x2))
    return out_msp


def nextafter_pynative(x1, x2):
    context.set_context(mode=context.PYNATIVE_MODE, device_target='CPU')
    net_msp = NextAfterNet()
    out_msp = net_msp(Tensor(x1), Tensor(x2))
    return out_msp


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_nextafter_float64_graph():
    """
    Feature: ALL To ALL
    Description: test cases for nextafter
    Expectation: the result match to tensorflow
    """
    x = np.array([0.0]).astype(np.float64)
    y = np.array([0.1]).astype(np.float64)
    out_tf = np.array([5.e-324]).astype(np.float64)
    out_msp = nextafter_graph(x, y)
    assert out_msp.asnumpy() == out_tf


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_nextafter_float64_pynative():
    """
    Feature: ALL To ALL
    Description: test cases for nextafter
    Expectation: the result match to tensorflow
    """
    x = np.array([0.0]).astype(np.float64)
    y = np.array([0.1]).astype(np.float64)
    out_tf = np.array([5.e-324]).astype(np.float64)
    out_msp = nextafter_pynative(x, y)
    assert out_msp.asnumpy() == out_tf


@arg_mark(plat_marks=['cpu_linux', 'cpu_windows', 'cpu_macos'], level_mark='level1', card_mark='onecard',
          essential_mark='unessential')
def test_nextafter_cpu_dynamic_shape():
    """
    Feature: test nextafter op in cpu.
    Description: test the ops in dynamic shape.
    Expectation: expect correct shape result.
    """
    context.set_context(mode=context.PYNATIVE_MODE, device_target='CPU')
    net = NextAfterNet()
    x_dyn = Tensor(shape=[None, None], dtype=mindspore.float32)
    y_dyn = Tensor(shape=[None, None], dtype=mindspore.float32)
    net.set_inputs(x_dyn, y_dyn)
    x = np.array([[0.0], [0.1]]).astype(np.float32)
    y = np.array([[0.1], [0.2]]).astype(np.float32)
    output = net(Tensor(x, mindspore.float32), Tensor(y, mindspore.float32))
    expect_shape = (2, 1)
    assert output.asnumpy().shape == expect_shape
