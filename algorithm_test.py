from re import X
from absl.testing import absltest
from splitbrain import SplitbrainV2
from splitbrain import statistics
import graphdef_utils
import program_graph_pb2


class SplitbrainTest(absltest.TestCase):

  def assertSummaryASumsAcrossB(self, A, B, name):
    x = 0
    for CL in A:
      x += getattr(CL, name)
    self.assertEqual(getattr(B, name), x)

  def test_fib(self):
    graphdef = graphdef_utils.load_graphdef_from_file(
        "testdata/example_graph.textproto")
    G = graphdef_utils.make_graph_from_proto(graphdef)
    algorithm = SplitbrainV2()
    CLs = algorithm.run(G)
    self.assertEqual(CLs, [['fib', 'my_error'], ['do_fib']])

    stats_pb = statistics.evaluate(G, CLs, graphdef)
    self.assertLen(stats_pb.split_changelist, len(CLs))

    # This is a little confusing, but the goal is to confirm that the number
    # of nodes, lines changed, etc... is equal between the source program graph
    # and the individual summary records.
    for prop in [
        "lines_added",
        "lines_changed",
        "lines_removed",
    ]:
      self.assertSummaryASumsAcrossB(stats_pb.split_changelist,
                                     stats_pb.original_changelist, prop)
      self.assertSummaryASumsAcrossB(graphdef.symbol,
                                     stats_pb.original_changelist, prop)

    self.assertSummaryASumsAcrossB(stats_pb.split_changelist,
                                   stats_pb.original_changelist,
                                   "number_of_nodes")

  def test_SplitbrainV1_only_uses_bazel(self):
    """Tests that SplitbrainV1 fails when faced with non-Bazel data.
    
    This is because the algorithm has a special edge-case and can only function
    upon Bazel data.
    """
    nodedef = program_graph_pb2.NodeDef()
    nodedef.kind = program_graph_pb2.NodeDef.Kind.SYMBOL
    graphdef = program_graph_pb2.GraphDef()
    graphdef.symbol.append(nodedef)
    self.assertFalse(splitbrain.SplitbrainV1().is_valid(graphdef))


if __name__ == '__main__':
  absltest.main()
