# MiniFlow - lesson 2 Udacity CarND


class Node(object):
    def __init__(self, inbound_nodes=[]):
        # nodes from which this node receives values
        self.inbound_nodes = inbound_nodes
        # node to which this node passes Values
        self.outbound_nodes = []

        # for each inbound node here, add this node as an outbound node to that node
        for n in self.inbound_nodes:
            n.outbound_nodes.append(self)
        # A calculated value
        self.value = None

    def forward(self):
        raise NotImplemented


class Input(Node):
    def __init__(self):
        # An Input node has no inbound nodes,
        # so no need to pass anything to the Node instantiator.
        Node.__init__(self)

        # NOTE: Input node is the only node where the value
        # may be passed as an argument to forward().

        # All other node implementations should get the value
        # of the previous node from self.inbound_nodes
        #
        # Example:
        # val0 = self.inbound_nodes[0].value

    def forward(self, value=None):
        # Overwrite the value if one is passed in
        if value is not None:
            self.value = value



class Add(Node):
    def __init__(self, x,y,z):
        Node.__init__(self, [x,y,z])

    def forward(self):
        o = 0
        for n in self.inbound_nodes:
            o += n.value

        self.value = o


class Linear(Node):
    def __init__(self, inputs, weights, bias):
        Node.__init__(self, [inputs, weights, bias])

    def forward(self):
        pass


def topological_sort(feed_dict):
    # Sort generic nodes in topological order using Khan's algorithim...
    input_nodes = [n for n in feed_dict.keys()]

    G = {}
    nodes = [n for n in input_nodes]
    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in G:
            G[n] = {'in': set(), 'out': set()}
        for m in n.outbound_nodes:
            if m not in G:
                G[m] = {'in': set(), 'out': set()}
            G[n]['out'].add(m)
            G[m]['in'].add(n)
            nodes.append(m)

    L = []
    S = set(input_nodes)
    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Input):
            n.value = feed_dict[n]

        L.append(n)
        for m in n.outbound_nodes:
                G[n]['out'].remove(m)
                G[m]['in'].remove(n)
                # if no other incoming edges add to S
                if len(G[m]['in']) == 0:
                    S.add(m)
    return L


def forward_pass(output_node, sorted_nodes):
    """
    Performs a forward pass through a list of sorted nodes.

    Arguments:

        `output_node`: A node in the graph, should be the output node (have no outgoing edges).
        `sorted_nodes`: A topologically sorted list of nodes.

    Returns the output Node's value
    """

    for n in sorted_nodes:
        n.forward()

    return output_node.value