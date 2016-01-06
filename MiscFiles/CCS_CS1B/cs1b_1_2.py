from __future__ import division
import pyrtl
a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
out_a, out_b = (pyrtl.Output(1, 'out_' + i) for i in ("a", "b"))

parity = a ^ b
out_a <<= parity ^ a
out_b <<= parity ^ b

trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=trace)

for i in range(4):
    a_in = i % 2
    b_in = i // 2
    sim.step({a: a_in, b: b_in})
    # print("a = {}, b = {}".format(a_in, b_in))
    assert(a_in == sim.inspect(out_b))
    assert(b_in == sim.inspect(out_a))


trace.render_trace()

# b = a ^ b   # aka b_inter
# out_a = a ^b_inter
# out_b = out_a ^ b_inter


