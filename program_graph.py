"""ProgramGraph is a high-level abstraction over a program.

See GraphDef and SymbolDef in program_graph.proto for more informationa about
the underlying data structure.

ProgramGraph adds additional features to the data structure such as loading
into a graph and precomputing the symbol table.
"""

import networkx as nx
import program_graph_pb2

class ProgramGraph:
  """In-memory implementation of a GraphDef protobuf."""

  def __init__(self):
    self._graph = nx.DiGraph()
    self._symbol_table = dict()

  def merge_from_proto(self, graphdef: program_graph_pb2.GraphDef):
    """Load a GraphDef into a ProgramGraph.
    
    Args:
      graphdef: Valid GraphDef protocol buffer. Self-loops in the graph will
        be removed.
    """
    G = nx.DiGraph()
    G.add_nodes_from([symbol.name for symbol in graphdef.symbol])
    for symbol in graphdef.symbol:
      self._symbol_table[symbol.name] = symbol
      for edge in symbol.u_edge:
        G.add_edge(symbol.name, edge)
    G.remove_edges_from(nx.selfloop_edges(G))
    self._graph = G