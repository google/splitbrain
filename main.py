"""Entry-point for SplitBrain inference.

Reads in a program graph and generates output symbols. See splitbrain.py for
the algorithm itself.

Usage:
  ./splitbrain.py --input_graph=example_graph.textproto --output_dir=out

TODO(cambr): Implement.
"""

import os
import networkx
import splitbrain

from absl import app
from absl import flags
from google.protobuf import text_format

FLAGS = flags.FLAGS

flags.DEFINE_string('input_path', None, 'Path to input GraphDef.')
flags.mark_flag_as_required('input_path')


def _load_graphdef_from_file(path: str) -> str:
  graphdef = {}
  with open(path, 'r') as f:
    text_format.Merge(f.read(), graphdef)
  return "" 


def _make_graphdef_from_proto(proto: dict) -> networkx.Graph:
  return None


def main(argv):
  del argv

  if not os.path.exists(FLAGS.input_path):
    raise flags.FlagError("input path of %s is invalid".format(FLAGS.input_path))
  graphdef = _load_graphdef_from_file(FLAGS.input_path)
  graph = _make_graphdef_from_proto(graphdef)

  CLs = splitbrain.compute_sub_cls(graph)

  for changelist in CLs:
    print('Changelist: ' + str(changelist))


if __name__ == '__main__':
  app.run(main)