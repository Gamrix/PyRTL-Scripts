from __future__ import division, print_function
import pyrtl
import numbers


def circuit_equivalence(equv_func, in_wires=None, out_wire=None, block=None, print_invalid=True):
    """
    Checks whether a circuit is equivalent to a python function

    :param equv_func: function to test circuit equivelence of. int args are passed
      in the order of the in_wires
    :param [Input] in_wires: wires for input (in order of args for equiv_func).
      default: all input wires, in their name's alphabetical order.
    :param Output out_wire: wire to use for output, default: find the only one
    :param Bool print_invalid:
    :return: bool
    """
    block = pyrtl.working_block(block)
    in_wires = _get_inputs(in_wires, block)
    out_wire = _get_output(out_wire, block)

    # now we get into the algorithm
    bits_to_test = sum(w.bitwidth for w in in_wires)

    sim = pyrtl.Simulation()
    for test_val in range(2**bits_to_test):
        vals = _create_seq_list(in_wires, test_val)
        sim.step({w: v for w, v in zip(in_wires, vals)})
        out_val = sim.inspect(out_wire)
        expected_val = equv_func(*vals)
        if not isinstance(expected_val, numbers.Integral):
            raise pyrtl.PyrtlError("Equv_func return %s, which is not an integer" %
                                   repr(expected_val))
        if out_val != expected_val:
            if print_invalid:
                situation_str = ', '.join(str(w) + ' = ' + str(v) for w, v in zip(in_wires, vals))
                print("in situation {}, got: {} expected: {}"
                      .format(situation_str, out_val, expected_val))
            return False
    return True


def _create_seq_list(wires, index):
    vals = []
    for wire in wires:
        wire_range = 2 ** wire.bitwidth
        vals.append(index % wire_range)
        index = index >> wire.bitwidth
    return vals


def _get_inputs(in_wires, block):
    if not in_wires:
        return sorted(block.wirevector_subset(pyrtl.Input), key=lambda w: w.name)
    return in_wires


def _get_output(out_wire, block):
    if out_wire is None:
        outs = block.wirevector_subset(pyrtl.Output)
        if len(outs) != 1:
            raise pyrtl.PyrtlError("If you don't have exactly one Outout wire, you must "
                                   "specify the Output wire to use")
        return outs.pop()
    elif isinstance(out_wire, pyrtl.WireVector):
        return out_wire
    else:
        raise pyrtl.PyrtlError("Invalid out_wire, %s" % str(out_wire))
