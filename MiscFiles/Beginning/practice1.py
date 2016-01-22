import pyrtl

a = pyrtl.Input(1, "a")
b = pyrtl.Input(1, "b")

c = pyrtl.Output(1, "out")

wire = a & b
c <<= wire

d = pyrtl.Output(2, "concat")

d <<= pyrtl.concat(a, b)

sim = pyrtl.Simulation(tracer=pyrtl.SimulationTrace())

import random

sim_ins = {a: 0, b: 1}

sim.step(sim_ins)

for cycle in range(15):
    sim.step({
        a: random.choice([0, 1]),
        b: random.choice([0, 1]),
        # c: random.choice([0, 1])
    })

sim.tracer.render_trace(symbol_len=5, segment_size=5)

sim_inputs = {
    a:   '0010100111010000',
    b: '1100010000000000'
}

for cycle in range(len(sim_inputs[a])):
    sim.step({wire: int(value_array[cycle]) for wire, value_array
              in sim_inputs.items()})
