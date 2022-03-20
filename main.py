"""Entry-point for SplitBrain inference.

Reads in a program graph and generates output symbols. See splitbrain.py for
the algorithm itself.

Usage:
  ./splitbrain.py --input_graph=example_graph.textproto
"""

import os
import networkx as nx
import program_graph_pb2
import splitbrain
import statistics

from absl import app
from absl import flags
from google.protobuf import text_format

FLAGS = flags.FLAGS

flags.DEFINE_string('input_path', None, 'Path to input GraphDef.')
flags.mark_flag_as_required('input_path')
flags.DEFINE_bool('enable_statistics', False,
                  'If true, capture statistics for this session.')
flags.DEFINE_string(
    'output_dir', None,
    'Directory to write output artefacts (e.g. statistics pb) to.')


VALID_ALGORITHMS = {
  'Control': splitbrain.NullAlgorithm,
  'SplitbrainV2': splitbrain.SplitbrainV2,
}
flags.DEFINE_multi_enum(
    'algorithms', ['SplitbrainV2'], VALID_ALGORITHMS.keys(),
    'Multi string list of algorithms to run, e.g. SplitbrainV2.')


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
      raise Exception("input path of %s is invalid" % (FLAGS.input_path))
    graphdef = _load_graphdef_from_file(FLAGS.input_path)

    G = _make_graph_from_proto(graphdef)
    print("Loaded graphdef into memory: %s" % G)

    for algorithm_name in FLAGS.algorithms:
      print("\nRunning algorithm: %s" % algorithm_name)
      algorithm = VALID_ALGORITHMS[algorithm_name]()

      CLs = algorithm.run(G)
      for changelist in CLs:
        print('Changelist: ' + str(changelist))

      if FLAGS.enable_statistics:
        if FLAGS.output_dir is None:
          raise Exception(
            "output_dir cannot be empty if --enable_statistics.")
        print('Writing statistics to disk.')
        stats_pb = statistics.evaluate(G, CLs)
        output_path = os.path.join(FLAGS.output_dir, 'statistics.proto')
        with open(output_path, 'wb') as f:
          f.write(stats_pb.SerializeToString())


if __name__ == '__main__':
  app.run(main)
