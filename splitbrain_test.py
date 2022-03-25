import networkx as nx
from absl.testing import absltest
import splitbrain


class SplitbrainTest(absltest.TestCase):

  def test_fib(self):
    # A program is modelled as a graph.
    #
    # def fib(n):
    #   if n < 2:
    #     return n
    #   return fib(n-1) + fib(n-2)
    #
    # my_error = "Oh no! Over 1000."
    #
    # def do_fib(n):
    #   if n >= 1000:
    #     return my_error
    #   return fib(n)
    #
    G = nx.DiGraph()
    G.add_nodes_from(["fib", "my_error", "do_fib"])
    G.add_edge("fib", "fib")  # self loops.
    G.add_edge("do_fib", "my_error")
    G.add_edge("do_fib", "fib")
    G.remove_edges_from(nx.selfloop_edges(G))

    algorithm = splitbrain.SplitbrainV2()
    CLs = algorithm.run(G)

    self.assertEqual(CLs, [['fib', 'my_error'], ['do_fib']])

    for changelist in CLs:
      print('Changelist: ' + str(changelist))


if __name__ == '__main__':
  absltest.main()
