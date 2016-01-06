from __future__ import division
import pyrtl
a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
out = pyrtl.Output(1, 'out')

# a_or_b = a | b
a_or_b = ~(~a & ~b)
a_nand_b = ~(a & b)
out <<= a_or_b & a_nand_b

trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=trace)

for i in range(4):
    a_in = i % 2
    b_in = i // 2
    sim.step({a: a_in, b: b_in})
    assert(a_in ^ b_in == trace.trace[out][i])

trace.render_trace()
