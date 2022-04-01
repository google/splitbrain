# google/splitbrain

load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")

py_proto_library(
  name = "program_graph_py_proto",
  srcs = ["program_graph.proto"],
  srcs_version = "PY2AND3",
  deps = [
  ],
)

py_library(
  name = "splitbrain",
  srcs = [
    "splitbrain.py",
    "statistics.py",
    "graphdef_utils.py",
  ],
)

py_binary(
  name = "graphdef_from_bazel",
  srcs = ["graphdef_from_bazel.py"],
  deps = [":splitbrain"],
)

py_binary(
  name = "main",
  srcs = ["main.py"],
  deps = [":splitbrain"],
)

py_test(
  name = "splitbrain_benchmark",
  srcs = ["splitbrain_benchmark.py"],
  deps = [":splitbrain"],
)

filegroup(
    name = "testdata",
    srcs = glob(["testdata/*.textproto"])
)

py_test(
  name = "splitbrain_test",
  srcs = ["splitbrain_test.py"],
  deps = [":splitbrain"],
  data = [":testdata"]
)

py_test(
  name = "graphdef_utils_test",
  srcs = ["graphdef_utils_test.py"],
  deps = [":splitbrain"],
  data = [":testdata"]
)
