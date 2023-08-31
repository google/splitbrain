"""Extracts a GraphDef based on a Bazel workspace.

This tool launches the Bazel binary to extract some data from a workspace, and
processes the protocol buffer output to produce a GraphDef.

Usage:
  ./graphdef_from_bazel.py --input_dir=path/to/WORKSPACE \\
    --output_dir=path/to/out
"""

from absl import app
from absl import flags
import graphdef_utils
from third_party.bazel.src.main.protobuf import build_pb2 

FLAGS = flags.FLAGS
flags.DEFINE_string('input_path', None, 'Path to Bazel WORKSPACE file.')
flags.DEFINE_string('output_dir', None, 'Directory to write output to.')
flags.DEFINE_multi_string('modified_files', [],
                          'List of modified files to `bazel query` for.')
flags.DEFINE_bool('textproto', False,
                  'If true, writes output statistics as textproto format.')
flags.mark_flag_as_required('input_path')
flags.mark_flag_as_required('output_dir')


def main(argv):
  del argv

  with open(FLAGS.input_path) as f:
    pass

  # TODO(cameron): Load bazel proto using vendored dependency.
  # TODO(cameron): Filter on predicates: Must be a working change in the CL? Maybe keep transitive.
  # TODO(cameron): Find testdata based stuff and make changes bi-directional. Same with proto.
  # TODO(cameron): Merge bi-directional dependencies.
  # TODO(cameron): Import tests from internal.
  # TODO(cameron): Assert the graph is a DAG. Find and merge cycles.
  graphdef = program_graph_pb2.GraphDef()


if __name__ == '__main__':
  app.run(main)