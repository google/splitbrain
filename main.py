"""Entry-point for SplitBrain inference.

Reads in a program graph and generates output symbols. See splitbrain.py for
the algorithm itself.

Usage:
  ./splitbrain.py --input_graph=example_graph.textproto
"""

import os
import program_graph_pb2
import splitbrain
import statistics
import graphdef_utils

from absl import app
from absl import flags
from google.protobuf import text_format
from networkx.drawing.nx_pydot import to_pydot

# Map of valid algorithmic names and associated classes.
VALID_ALGORITHMS = {
    'Control': splitbrain.NullAlgorithm,
    'SplitbrainV2': splitbrain.SplitbrainV2,
}

FLAGS = flags.FLAGS

flags.DEFINE_string('input_path', None, 'Path to input GraphDef.')
flags.mark_flag_as_required('input_path')
flags.DEFINE_bool('enable_statistics', False,
                  'If true, capture statistics for this session.')
flags.DEFINE_bool('textproto', False,
                  'If true, writes output statistics as textproto format.')
flags.DEFINE_string(
    'output_dir', None,
    'Directory to write output artefacts (e.g. statistics pb) to.')
flags.DEFINE_string(
    'cl_identifier', 'unknown',
    'Unique identifier for the source changelist in statistics.')
flags.DEFINE_bool(
  'dot', False,
  'If true, output the changeset as a DOT visualisation to stdout.')
flags.DEFINE_multi_enum(
    'algorithms', ['SplitbrainV2'], VALID_ALGORITHMS.keys(),
    'Multi string list of algorithms to run, e.g. SplitbrainV2.')


def _write_statistics_to_disk(output_dir: str,
                              stats_pb: program_graph_pb2.Statistics,
                              algorithm="splitbrain",
                              textproto=False):
  if textproto:
    file_extension = 'textproto'
    out = text_format.MessageToBytes(stats_pb)
  else:
    file_extension = 'binarypb'
    out = stats_pb.SerializeToString()
  filename = f'{algorithm}_statistics.{file_extension}'
  output_path = os.path.join(output_dir, filename)
  with open(output_path, 'wb') as f:
    f.write(out)


def _make_dot_from_graph(G: nx.Graph) -> str:
  return to_pydot(G).to_string()


def main(argv):
  del argv

  if not os.path.exists(FLAGS.input_path):
    raise Exception("input path of %s is invalid" % (FLAGS.input_path))
  graphdef = graphdef_utils.load_graphdef_from_file(FLAGS.input_path)

  G = graphdef_utils.make_graph_from_proto(graphdef)
  print("Loaded graphdef into memory: %s" % G)

  for algorithm_name in FLAGS.algorithms:
    print("\nRunning algorithm: %s" % algorithm_name)
    algorithm = VALID_ALGORITHMS[algorithm_name]()

    CLs = algorithm.run(G)
    for changelist in CLs:
      print('Changelist: ' + str(changelist))

    if FLAGS.enable_statistics:
      if FLAGS.output_dir is None:
        raise Exception("output_dir cannot be empty if --enable_statistics.")
      print('Writing statistics to disk.')
      stats_pb = statistics.evaluate(G, CLs, graphdef, algorithm=algorithm_name,
                                     cl_identifier=FLAGS.cl_identifier)
      _write_statistics_to_disk(FLAGS.output_dir,
                                stats_pb,
                                algorithm=algorithm_name,
                                textproto=FLAGS.textproto)

    if FLAGS.dot:
      print(_make_dot_from_graph(G))


if __name__ == '__main__':
  app.run(main)
