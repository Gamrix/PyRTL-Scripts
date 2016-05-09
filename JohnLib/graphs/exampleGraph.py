from __future__ import absolute_import

from JohnLib.graphs import graphBase

import pyrtl
from pyrtl.rtllib import adders


def make_example_graph():
    in1, in2 = pyrtl.Input(8, 'in1'), pyrtl.Input(8, 'in2')
    out = pyrtl.Output(9, 'output')
    out <<= adders.kogge_stone(in1, in2)

    pyrtl.synthesize()
    pyrtl.optimize()

    graphBase.show_graph()


if __name__ == '__main__':
    make_example_graph()
