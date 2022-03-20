import networkx as nx
import google_benchmark as benchmark
import splitbrain


@benchmark.register
def benchmark_fib(state):
  """Similar to test_fib."""
  G = nx.DiGraph()
  G.add_nodes_from(["fib", "my_error", "do_fib"])
  G.add_edge("fib", "fib")  # self loops.
  G.add_edge("do_fib", "my_error")
  G.add_edge("do_fib", "fib")
  G.remove_edges_from(nx.selfloop_edges(G))

  algorithm = splitbrain.SplitbrainV2()

  while state:
    algorithm.run(G)


if __name__ == '__main__':
  benchmark.main()
