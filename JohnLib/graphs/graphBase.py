from __future__ import print_function
import pyrtl



# graph format
# format goals:
#   Trivial for user to set up
#   Easy for user to change visualizations
#   Interoperatablility between different formats supported, but could require some user intervention
#   Single pipeline for creating graphs - one interface
#   Keeps directed graph information


# building on net_graph

#########

# NETWORKX and D3 Support


# networkx d3 example https://github.com/networkx/networkx/blob/master/examples/javascript/force.py
# d3 pan and zoom example http://bl.ocks.org/stepheneb/1182434
# better d3 pan and zoom example: http://bl.ocks.org/robschmuecker/7880033
# d3 force directed graph example http://bl.ocks.org/d3noob/5141278
# d3 force zoom http://bl.ocks.org/d3noob/5141278


def networkx_graph(net_graph=None, net_attrs=None, edge_attr=None):
    import networkx
    graph = networkx.DiGraph()
    net_graph, net_attrs, edge_attr = _check_graph_items(net_graph, net_attrs, edge_attr)

    def add_node(net):
        attrs = {'name': str(net), 'fill': '#009999'}
        if net in net_attrs:
            attrs.update(net_attrs[net])
        graph.add_node(net, attrs)

    def add_edge(sNet, dNet, wire):
        attrs = {'name': str(wire)}
        attrs.update(edge_attr.get(wire, {}))
        attrs.update(edge_attr.get(sNet, {}).get(dNet, {}))
        graph.add_edge(sNet, dNet, attrs)

    for net in net_graph.keys():
        add_node(net)

    for sNet, dstInfo in net_graph.items():
        for dNet, wire in dstInfo.items():
            add_edge(sNet, dNet, wire)

    return graph


# D3 usage quick guide:
# In order to change properties of the

def str_convert_dict(dict, levels=1, cLLV=False, str_fun=str):

    conv_dict = {}
    if levels == 0:
        if cLLV:  # convert last layer vals
            return str_fun(dict)
        return dict

    conv_dict = {str_fun(k): str_convert_dict(v, levels - 1, cLLV, str_fun)
                 for k, v in dict.items()}

    return conv_dict


def convert_pyrtl_to_str(net_graph=None, net_attrs=None, edge_attr=None):

    conv_net_graph = str_convert_dict(net_graph, 2, True)
    conv_net_attrs = str_convert_dict(net_attrs, 1)
    conv_edge_attrs = str_convert_dict(edge_attr, 1)
    for key, val_dict in conv_edge_attrs:
        nets = set(n for n in val_dict.keys() if isinstance(n, pyrtl.LogicNet))
        for n in nets:
            val_dict[str(n)] = val_dict[n]
            del val_dict[n]
    return conv_net_graph, conv_net_attrs, conv_edge_attrs


def build_d3_json(netx_graph, file='force/force.json'):
    import json
    from networkx.readwrite import json_graph
    d = json_graph.node_link_data(netx_graph)
    with open(file, 'w') as f:
        json.dump(d, f)

    print('Wrote node-link JSON data to {}'.format(file))


def start_flask(folder='force'):
    import flask
    # Serve the file over http to allow for cross origin requests
    app = flask.Flask(__name__, static_folder=folder)

    @app.route('/<path:path>')
    def static_proxy(path):
        return app.send_static_file(path)

    print('\nGo to http://localhost:8000/force.html to see the example\n')
    app.run(port=8000)


def _check_graph_items(pyrtl_graph=None, net_attrs=None, edge_attr=None):
    if pyrtl_graph is None:
        from pyrtl.inputoutput import net_graph
        pyrtl_graph = net_graph(split_state=True)

    if net_attrs is None:
        net_attrs = {}
    if edge_attr is None:
        edge_attr = {}

    return pyrtl_graph, net_attrs, edge_attr



def show_graph(pyrtl_graph=None, net_attrs=None, edge_attr=None):
    import webbrowser
    graph_data = _check_graph_items(pyrtl_graph, net_attrs, edge_attr)
    conv_graph_data = convert_pyrtl_to_str(*graph_data)

    Ngraph = networkx_graph(*conv_graph_data)
    build_d3_json(Ngraph)
    start_flask()
    webbrowser.open("http://localhost:8000/force.html")
