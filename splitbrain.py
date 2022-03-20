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

def compute_sub_cls(G):
  G = G.copy()

  # Next, find leaf nodes of the program symbols. Iteratively remove them
  # from the graph until at the final state.
  def _find_leaf_nodes(graph):
    return [v for v, d in graph.out_degree() if d == 0]

  CLs = []

  while len(G) > 0:
    symbols = []
    leaves = _find_leaf_nodes(G)
    for leaf in leaves:
      G.remove_node(leaf)
      symbols.append(leaf)

    CLs.append(symbols)

  return CLs