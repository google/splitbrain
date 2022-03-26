# google/splitbrain

proto_library(
  name = "program_graph_proto",
  srcs = ["program_graph.proto"],
)

py_proto_library(
  name = "program_graph_py_proto",
  api_version = 2,
  deps = ["program_graph_proto"],
)

py_library(
  name = "lib",
  srcs = [
    "splitbrain.py",
    "statistics.py",
    "graphdef_utils.py",
  ],
)

py_binary(
  name = "cli",
  srcs = ["main.py"],
  deps = [":lib"],
)

py_test(
  name = "benchmark",
  srcs = ["splitbrain_benchmark.py"],
  deps = [":lib"],
)

py_test(
  name = "lib_test",
  srcs = ["splitbrain_test.py"],
  deps = [":lib"],
)
