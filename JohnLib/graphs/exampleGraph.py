from __future__ import absolute_import

from JohnLib.graphs import graphBase

import pyrtl
from pyrtl.rtllib import adders


def make_example_graph():
    in1, in2 = pyrtl.Input(8, 'in1'), pyrtl.Input(8, 'in2')
    out = pyrtl.Output(9, 'output')
    out <<= adders.ripple_add(in1, in2)

    graphBase.show_graph()


if __name__ == '__main__':
    make_example_graph()
