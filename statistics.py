'''Statistics routines for evaluating the Splitbrain algorithm.

Measuring the effectiveness of this algorithm takes place in two ways:
Utility and usability. This file focuses purely on utility and quantitatively
measures the outputs of SplitbrainV2.

In addition, the functionality here can be run as a batch-job to collect data
over time. See the splitbrain.Statistics proto for the exact data structure.
'''

import networkx as nx
import program_graph_pb2

ALGORITHM_TO_ENUM_MAP = {
    'SpltbrainV2': program_graph_pb2.Statistics.Algorithm.SPLITBRAIN_V2,
    'Control': program_graph_pb2.Statistics.Algorithm.CONTROL,
}


def compute_delta():
  pass


def evaluate_cl(G: nx.Graph, symbol_table: dict) -> program_graph_pb2.Statistics.CL:
  cl_stats_pb = program_graph_pb2.Statistics.CL()
  cl_stats_pb.average_node_connectivity = nx.average_node_connectivity(G)

  if G.number_of_nodes() > 1:
    cl_stats_pb.edge_connectivity = nx.edge_connectivity(G)

  cl_stats_pb.number_of_nodes = G.number_of_nodes()
  cl_stats_pb.number_of_edges = G.number_of_edges()

  for node in G.nodes:
    cl_stats_pb.lines_added += symbol_table[node].lines_added
    cl_stats_pb.lines_changed += symbol_table[node].lines_changed
    cl_stats_pb.lines_removed += symbol_table[node].lines_removed
  
  return cl_stats_pb


def evaluate(G: nx.Graph, changelists: list,
             graphdef: program_graph_pb2.GraphDef,
             algorithm: str) -> program_graph_pb2.Statistics:
  symbol_table = {}
  for symbol in graphdef.symbol:
    symbol_table[symbol.name] = symbol

  stats_pb = program_graph_pb2.Statistics()
  stats_pb.algorithm = ALGORITHM_TO_ENUM_MAP.get(
      algorithm, program_graph_pb2.Statistics.Algorithm.UNKNOWN)
  stats_pb.original_changelist.CopyFrom(evaluate_cl(G, symbol_table))

  for CL in changelists:
    cl_stats_pb = evaluate_cl(G.subgraph(CL), symbol_table)
    stats_pb.split_changelist.append(cl_stats_pb)

  return stats_pb
