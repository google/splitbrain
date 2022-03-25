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
    'Control': program_graph_pb2.Statistics.Algorithm.Control,
}


def evaluate_cl(
    G: nx.Graph, symbols: list, all_symbols: list,
    graphdef: program_graph_pb2.GraphDef) -> program_graph_pb2.Statistics.CL:
  stats_pb.average_node_connectivity = nx.average_node_connectivity(G)
  stats_pb.edge_connectivity = nx.edge_connectivity(G)
  stats_pb.number_of_nodes = G.number_of_nodes()
  stats_pb.number_of_edges = G.number_of_edges()
  stats_pb.number_of_sub_cls = len(changelists)
  return None


def evaluate(G: nx.Graph, changelists: list,
             graphdef: program_graph_pb2.GraphDef,
             algorithm: str) -> program_graph_pb2.Statistics:
  # TODO(cameron): Pass in GraphDef, use to compute CL-level stats.
  # TODO(cameron): Compute diff stats *between* CLs also. Add tests for this.
  stats_pb = program_graph_pb2.Statistics()
  stats_pb.algorithm = ALGORITHM_TO_ENUM_MAP.get(
      algorithm, program_graph_pb2.Statistics.Algorithm.UNKNOWN)

  symbols = [symbol for symbols in changelists]

  for CL_symbols in changelists:
    stats_pb.split_changelist.append(
        evaluate_cl(G.subgraph(CL_symbols), CL_symbols, symbols.graphdef))

  stats_pb.original_changelist = evaluate_cl(G, symbols, symbols, graphdef)

  return stats_pb
