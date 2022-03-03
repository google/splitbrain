"""Naive implementation of the generalised (V2) SplitBrain algorithm.

Computes the set of all possible commits from a symbol-graph. When squashed,
sub-commits should be equal to the original commit.

V1 (internal) was based upon file-level splits, operating against Bazel's BUILD
target graph. V2 (open-source) is a generalised graph search which iteratively
finds and extracts leaf nodes from a graph.

Vertices/edges in the V2 graph are abstract, and can represent files/imports,
symbols/calls or targets/srcs.

See main.py for running the algorithm against input data.
"""

import networkx as nx

# A program is modelled as a graph.
#
# def fib(n):
#   if n < 2:
#     return n
#   return fib(n-1) + fib(n-2)
#
# my_error = "Oh no! Over 1000."
#
# def do_fib(n):
#   if n >= 1000:
#     return my_error
#   return fib(n)
#
G = nx.DiGraph()
G.add_nodes_from(["fib", "my_error", "do_fib"])
G.add_edge("fib", "fib")  # self loops.
G.add_edge("do_fib", "my_error")
G.add_edge("do_fib", "fib")
G.remove_edges_from(nx.selfloop_edges(G))

# Next, find leaf nodes of the program symbols. Iteratively remove them
# from the graph until at the final state.
def find_leaf_nodes(graph):
  return [v for v, d in graph.out_degree() if d == 0]

CLs = []

while len(G) > 0:
  symbols = []
  leaves = find_leaf_nodes(G)
  for leaf in leaves:
    G.remove_node(leaf)
    symbols.append(leaf)

  CLs.append(symbols)

# Finally, print the CLs.
for changelist in CLs:
  print('Changelist: ' + str(changelist))