from re import X
import networkx as nx
from absl.testing import absltest
import splitbrain
import statistics
import graphdef_utils


class SplitbrainTest(absltest.TestCase):

  def assertSummaryASumsAcrossB(self, A, B, name):
    x = 0
    for CL in A:
      x += getattr(CL, name)
    self.assertEqual(getattr(B, name), x)

  def test_fib(self):
    graphdef = graphdef_utils.load_graphdef_from_file(
        "data/example_graph.textproto")
    G = graphdef_utils.make_graph_from_proto(graphdef)
    algorithm = splitbrain.SplitbrainV2()
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


if __name__ == '__main__':
  absltest.main()
