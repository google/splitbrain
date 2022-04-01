"""Statistics routines for evaluating the Splitbrain algorithm.

Measuring the effectiveness of this algorithm takes place in two ways:
Utility and usability. This file focuses purely on utility and quantitatively
measures the outputs of SplitbrainV2.

In addition, the functionality here can be run as a batch-job to collect data
over time. See the splitbrain.Statistics proto for the exact data structure.
"""

import networkx as nx
import program_graph_pb2

ALGORITHM_TO_ENUM_MAP = {
    'SplitbrainV1': program_graph_pb2.Statistics.Algorithm.SPLITBRAIN_V1,
    'SplitbrainV2': program_graph_pb2.Statistics.Algorithm.SPLITBRAIN_V2,
    'Control': program_graph_pb2.Statistics.Algorithm.CONTROL,
}


def evaluate_cl(G: nx.Graph,
                symbol_table: dict) -> program_graph_pb2.Statistics.CL:
  """Processes CL graph and symbolic table to produce statistics.

  The goal here is simply to capture the relevant statistics, not make a
  judgement on the quality of the CL.

  The following metrics are captured:
  - Primary language (selects for majority of diff).
  - Graph complexity metrics (edge and node connectivity).
  - Diff metrics (total delta, add, rm).

  Args:
    G: GraphDef structure representing the CL.
    symbol_table: Dictionary structure from symbol name to NodeDef protobuf.

  Returns:
    Statistics protobuf suitable for further analysis.
  """
  cl_stats_pb = program_graph_pb2.Statistics.CL()
  cl_stats_pb.average_node_connectivity = nx.average_node_connectivity(G)

  if G.number_of_nodes() > 1:
    cl_stats_pb.edge_connectivity = nx.edge_connectivity(G)

  cl_stats_pb.number_of_nodes = G.number_of_nodes()
  cl_stats_pb.number_of_edges = G.number_of_edges()

  max_delta = 0
  primary_language = None

  for node in G.nodes:
    symbol = symbol_table[node]

    cl_stats_pb.lines_added += symbol.lines_added
    cl_stats_pb.lines_changed += symbol.lines_changed
    cl_stats_pb.lines_removed += symbol.lines_removed

    delta = symbol.lines_added + symbol.lines_changed + symbol.lines_removed
    if delta > max_delta:
      max_delta = delta
      primary_language = symbol.language

  # The primary language in this CL is the one with the maximum diff delta.
  cl_stats_pb.language = primary_language

  return cl_stats_pb


def evaluate(G: nx.Graph,
             changelists: list,
             graphdef: program_graph_pb2.GraphDef,
             algorithm="unknown",
             cl_identifier="unknown") -> program_graph_pb2.Statistics:
  """Processes all CLs and symbolic table to produce statistics.

  Args:
    G: Graph representation the original CL.
    changelists: List of strings with a direct mapping to NodeDefs.
    graphdef: Protobuf representation of the original CL.
    algorithm: Optional. Name of algorithm used, e.g. "SplitbrainV2".
    cl_identifier: Optional. Name of CL as unique ID.

  Returns:
    Statistics protobuf suitable for further analysis.
  """
  symbol_table = {}
  for symbol in graphdef.symbol:
    symbol_table[symbol.name] = symbol

  stats_pb = program_graph_pb2.Statistics()
  stats_pb.algorithm = ALGORITHM_TO_ENUM_MAP.get(
      algorithm, program_graph_pb2.Statistics.Algorithm.UNKNOWN)
  stats_pb.original_changelist.CopyFrom(evaluate_cl(G, symbol_table))
  stats_pb.cl_identifier = cl_identifier

  for CL in changelists:
    cl_stats_pb = evaluate_cl(G.subgraph(CL), symbol_table)
    stats_pb.split_changelist.append(cl_stats_pb)

  return stats_pb
