from __future__ import print_function
import pyrtl
from pyrtl import *


def add_resets_bad(reset_wire):
    no_reset = ~ reset_wire

    def add_reset(orig_reg):
        orig_input = WireVector(len(orig_reg))
        no_reset_mask = no_reset.sign_extend(len(orig_reg))
        orig_reg <<= orig_input & no_reset_mask
        return orig_input, orig_reg

    wire_transform(add_reset, Register, tuple())


def add_resets(reset_wire):
    no_reset = ~ reset_wire

    def add_reset(orig_net):
        if orig_net.op != "r":
            return True

        orig_input, orig_reg = orig_net.args[0], orig_net.dests[0]
        no_reset_mask = no_reset.sign_extended(len(orig_input))
        orig_reg.reg_in = None  # to allow for a new reg assignment to occur
        orig_reg.next <<= orig_input & no_reset_mask

    net_transform(add_reset)


def test_add_reset():
    i0 = pyrtl.Input(5, "in0")
    i1 = pyrtl.Input(5, "in1")
    o = pyrtl.Output(5, "out")
    reg = pyrtl.Register(5)
    reset = pyrtl.Input(1, "reset")

    reg.next <<= i0 & i1
    o <<= reg

    add_resets(reset)

    sim = pyrtl.Simulation()
    sim.step({i1: 5, i0: 7, reset: 0})
    sim.step({i1: 5, i0: 7, reset: 1})
    assert(sim.inspect(o) == 5)
    sim.step({i1: 0b01101, i0: 0b01110, reset: 0})
    assert(sim.inspect(o) == 0)
    sim.step({i1: 0b01101, i0: 0b01110, reset: 0})
    assert(sim.inspect(o) == 0b01100)
    print("test is a success")

if __name__ == '__main__':
    test_add_reset()
