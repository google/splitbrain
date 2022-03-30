"""Entry-point for SplitBrain inference.

Reads in a program graph and generates output symbols. See splitbrain.py for
the algorithm itself.

Usage:
  ./splitbrain.py --input_graph=example_graph.textproto
"""

import os
from re import A
import networkx as nx
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
    'SplitbrainV1': splitbrain.SplitbrainV1,
}

FLAGS = flags.FLAGS

flags.DEFINE_string('input_path', None, 'Path to input GraphDef.')
flags.mark_flag_as_required('input_path')
flags.DEFINE_bool('enable_statistics', False, 'Captures data for this session.')
flags.DEFINE_bool('textproto', False, 'Writes output data as textproto format.')
flags.DEFINE_string('output_dir', None,
                    'Directory to write output (e.g. statistics).')
flags.DEFINE_string('cl_identifier', 'unknown', 'UID for source CL in stats.')
flags.DEFINE_bool('dot', False, 'Outputs CLs as a DOT visualisation.')
flags.DEFINE_bool('quiet', False,
                  'Suppress textual output. Note: Pair with --git or --dot.')
flags.DEFINE_bool('git', False, 'Outputs CLs as a stream of git commands.')
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


def _make_git_from_cls(CLs: list, graphdef: program_graph_pb2.GraphDef) -> str:
  # TODO(cameron): Ensure cannot build if doesn't fit constraints.
  # TODO(cameron): Move to another file, add tests.

  out = "git rebase -i <oldsha1>\n"  # TODO(cameron): Pass in via CLI.
  out += "git reset HEAD^\n"
  for CL in CLs:
    for symbol in CL:
      del symbol
      filepath = "path/to/file"  # TODO(cameron): Grab from symbol table.
      out += f"git add {filepath}\n"
    commit_message = "SplitBrain Commit!!!"  # TODO(cameron): Generate description.
    out += f"git commit -m {commit_message}\n"

  out += "git rebase --continue"
  return out


def main(argv):
  del argv

  if not os.path.exists(FLAGS.input_path):
    raise Exception("input path of %s is invalid" % (FLAGS.input_path))
  graphdef = graphdef_utils.load_graphdef_from_file(FLAGS.input_path)

  G = graphdef_utils.make_graph_from_proto(graphdef)
  if not FLAGS.quiet:
    print("Loaded graphdef into memory: %s" % G)

  for algorithm_name in FLAGS.algorithms:
    algorithm = VALID_ALGORITHMS[algorithm_name]()
    if not algorithm.is_valid(graphdef):
      continue

    CLs = algorithm.run(G)
    if not FLAGS.quiet:
      print("Executed algorithm: %s\nChangelists:" % algorithm_name)
      for changelist in CLs:
        print('---> CL: ' + str(changelist))

    if FLAGS.enable_statistics:
      if FLAGS.output_dir is None:
        raise Exception("output_dir cannot be empty if --enable_statistics.")
      if not FLAGS.quiet:
        print('Writing statistics to disk.')
      stats_pb = statistics.evaluate(G,
                                     CLs,
                                     graphdef,
                                     algorithm=algorithm_name,
                                     cl_identifier=FLAGS.cl_identifier)
      _write_statistics_to_disk(FLAGS.output_dir,
                                stats_pb,
                                algorithm=algorithm_name,
                                textproto=FLAGS.textproto)

    if FLAGS.dot:
      print(_make_dot_from_graph(G))
    if FLAGS.git:
      print(_make_git_from_cls(CLs, graphdef))


if __name__ == '__main__':
  app.run(main)
