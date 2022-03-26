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
import program_graph_pb2


class SplitbrainAlgorithm:
  """Base implementation of the SplitBrain algorithm."""

  def _find_leaf_nodes(self, graph):
    """Next, find leaf nodes of the program symbols.

    Iteratively remove them from the graph until at the final state.
    """
    return [v for v, d in graph.out_degree() if d == 0]

  def is_valid(self, graphdef: program_graph_pb2.GraphDef) -> bool:
    """Returns if the algorithm can run over the given graphdef."""
    return True

  def run(self, G: nx.Graph) -> list:
    raise NotImplementedError("Algorithm not implemented.")


class NullAlgorithm(SplitbrainAlgorithm):
  """Null algorithm which can act as experiment control group."""

  def run(self, G: nx.Graph) -> list:
    symbols = []
    for node in G.nodes:
      symbols.append(node)
    return [symbols]


class SplitbrainV1(SplitbrainAlgorithm):
  """Backport of SplitbrainV1 (internal) based on V2.
  
  V1 can only operate over the Bazel build graph, therefore it will fail if
  symbolic data is fed.
  """

  def is_valid(self, graphdef: program_graph_pb2.GraphDef) -> bool:
    for symbol in graphdef.symbol:
      if symbol.kind != program_graph_pb2.NodeDef.Kind.BUILD_TARGET:
        print("Error: SplitbrainV1 can only run across BUILD_TARGET graphs!")
        return False
    return True

  def run(self, G: nx.Graph) -> list:
    G = G.copy()
    CLs = []
    while len(G) > 0:
      symbols = []
      leaves = self._find_leaf_nodes(G)
      for leaf in leaves:
        G.remove_node(leaf)
        symbols.append(leaf)
      CLs.append(symbols)
    return CLs


class SplitbrainV2(SplitbrainAlgorithm):
  """Naive implementation of the generalised (V2) SplitBrain algorithm.
  
  TODO(cameron): Add clustering.
  """

  def run(self, G: nx.Graph) -> list:
    G = G.copy()
    CLs = []
    while len(G) > 0:
      symbols = []
      leaves = self._find_leaf_nodes(G)
      for leaf in leaves:
        G.remove_node(leaf)
        symbols.append(leaf)
      CLs.append(symbols)
    return CLs
