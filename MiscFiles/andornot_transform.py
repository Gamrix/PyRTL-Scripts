import pyrtl


def and_inverter_synth(block=None):
    """
    Transforms a decomposed block into one consisting of ands and inverters in place
    :param block: The block to synthesize
    """
    def and_inv_op(net):
        if net.op in '~|&rwcsm@':
            return True

        def arg(num):
            return net.args[num]

        dest = net.dests[0]
        if net.op == '^':
            all_1 = arg(0) & arg(1)
            all_0 = ~arg(0) & ~arg(1)
            dest <<= all_0 & ~all_1
        elif net.op == 'n':
            dest <<= ~(arg(0) & arg(1))
        else:
            raise pyrtl.PyrtlError("Op, '{}' is not supported in and_inv_synth".format(net.op))

    pyrtl.net_transform(and_inv_op, block)
