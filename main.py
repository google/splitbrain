"""Entry-point for SplitBrain inference.

Reads in a program graph and generates output symbols. See splitbrain.py for
the algorithm itself.

Usage:
  ./splitbrain.py --input_graph=example_graph.textproto --output_dir=out

TODO(cambr): Implement.
"""

import os
import networkx as nx
import program_graph_pb2
import splitbrain

from absl import app
from absl import flags
from google.protobuf import text_format

FLAGS = flags.FLAGS

flags.DEFINE_string('input_path', None, 'Path to input GraphDef.')
flags.mark_flag_as_required('input_path')


def _load_graphdef_from_file(path: str) -> program_graph_pb2.GraphDef:
  graphdef = program_graph_pb2.GraphDef()
  with open(path, 'r') as f:
    text_format.Merge(f.read(), graphdef)
  return graphdef


def _make_graph_from_proto(graphdef: program_graph_pb2.GraphDef) -> nx.Graph:
  graph = nx.DiGraph()

  graph.add_nodes_from([symbol.name for symbol in graphdef.symbol])

  for symbol in graphdef.symbol:
    for edge in symbol.u_edge:
      graph.add_edge(symbol.name, edge)


  graph.remove_edges_from(nx.selfloop_edges(graph))

  return graph 


def main(argv):
  del argv

  if not os.path.exists(FLAGS.input_path):
    raise flags.FlagError("input path of %s is invalid".format(FLAGS.input_path))
  graphdef = _load_graphdef_from_file(FLAGS.input_path)

  G = _make_graph_from_proto(graphdef)
  print("Loaded graphdef into memory: %s".format(G))

  CLs = splitbrain.compute_sub_cls(G)
  for changelist in CLs:
    print('Changelist: ' + str(changelist))


if __name__ == '__main__':
  app.run(main)