import networkx as nx
import program_graph_pb2

from google.protobuf import text_format


def load_graphdef_from_file(path: str) -> program_graph_pb2.GraphDef:
  graphdef = program_graph_pb2.GraphDef()
  with open(path, 'r') as f:
    text_format.Parse(f.read(), graphdef)
  return graphdef


def make_graph_from_proto(graphdef: program_graph_pb2.GraphDef) -> nx.Graph:
  graph = nx.DiGraph()
  graph.add_nodes_from([symbol.name for symbol in graphdef.symbol])

  for symbol in graphdef.symbol:
    for edge in symbol.u_edge:
      graph.add_edge(symbol.name, edge)

  graph.remove_edges_from(nx.selfloop_edges(graph))
  return graph
