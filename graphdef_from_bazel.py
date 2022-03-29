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


if __name__ == '__main__':
  app.run(main)