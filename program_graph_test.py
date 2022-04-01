from absl.testing import absltest
import graphdef_utils
import networkx as nx


class ProgramGraphTest(absltest.TestCase):

  def test_merge_from_proto(self):
    graphdef = graphdef_utils.load_graphdef_from_file(
        "testdata/example_graph.textproto")

    G1 = nx.DiGraph()
    G1.add_nodes_from(["fib", "my_error", "do_fib"])
    G1.add_edge("fib", "fib")  # self loops.
    G1.add_edge("do_fib", "my_error")
    G1.add_edge("do_fib", "fib")
    G1.remove_edges_from(nx.selfloop_edges(G1))

    G2 = graphdef_utils.make_graph_from_proto(graphdef)

    self.assertTrue(nx.is_isomorphic(G1, G2))


if __name__ == '__main__':
  absltest.main()
