"""Program to generate GraphDef proto from a Bazel repository.

A sibling script called gen_bazel_bindings.sh should be used to invoke this
program.

Usage:
  ./gen_bazel_bindings.py --input_graph=path/to/query.proto \
      --output_graph=path/to/output.proto
"""

import os
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input_proto",
                    None,
                    "Path to input proto from blaze query output.",
                    required=True)
flags.DEFINE_string("output_proto",
                    None,
                    "Path to output proto (splitbrain GraphDef).",
                    required=True)


def _is_valid_workspace(modified_files) -> bool:
    return len(modified_files) > 0


def main(argv):
  del argv

  print("main")


if __name__ == '__main__':
  app.run(main)
