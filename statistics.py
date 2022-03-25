"""Statistics routines for evaluating the Splitbrain algorithm.

Measuring the effectiveness of this algorithm takes place in two ways:
Utility and usability. This file focuses purely on utility and quantitatively
measures the outputs of SplitbrainV2.

In addition, the functionality here can be run as a batch-job to collect data
over time. See the splitbrain.Statistics proto for the exact data structure.
"""

import networkx as nx
import program_graph_pb2


def evaluate(G: nx.Graph,
             changelists: list) -> program_graph_pb2.Statistics:
  # TODO(cameron): Pass in GraphDef, use to compute CL-level stats.
  # TODO(cameron): Compute diff stats *between* CLs also. Add tests for this.
  stats_pb = program_graph_pb2.Statistics()
  stats_pb.average_node_connectivity = nx.average_node_connectivity(G)
  stats_pb.edge_connectivity  = nx.edge_connectivity(G)
  stats_pb.number_of_nodes = G.number_of_nodes()
  stats_pb.number_of_edges = G.number_of_edges()
  stats_pb.number_of_sub_cls = len(changelists)
  return stats_pb
