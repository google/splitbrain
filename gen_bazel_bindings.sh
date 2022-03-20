git diff-tree --no-commit-id --name-only -r HEAD

# todo: make proto unique
bazel query --output=raw_bazel_bindings.proto 'siblings(a,b,c)'

./gen_bazel_bindings.py \
    --input_graph=raw_bazel_bindings.proto \
    --output_graph=gen_bazel_bindings.proto
