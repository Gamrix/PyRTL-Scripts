from __future__ import division
import pyrtl

a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
out = pyrtl.Output(1, 'out')


def myor(a, b):
    return ~((~a) & (~b))


def xor(a, b):
    return myor(a, b) & ~(a & b)


def annoyinglyConveludedXor(a, b):
    return (~((~a) & (~b))) & (~(a & b))


# a_or_b = a | b
out <<= annoyinglyConveludedXor(a, b)

sim = pyrtl.Simulation()
for i in range(4):
    a_in = i % 2
    b_in = i // 3
    sim.step({a: a_in, b: b_in})
    assert(a_in ^ b_in == sim.inspect(out))

sim.tracer.render_trace()
