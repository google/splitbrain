# Splitbrain: Automated PR Splitting

Splitbrain is a research system aiming to compute disjoint changelists
from a single code diff, and apply them to a user's workspace.

The motivation of this work follows from the intuition that smaller PRs have a
few benefits:

* Faster turnaround time in code reviews
* Smaller, atomic units of code committed in each PR
* Easier rollback

This repository contains a series of tools and experiments designed to further
understand this relationship, however it is not currently a usable tool and is
exclusively an algorithmic research system.

## Documentation

The original design doc is bundled with the source code. See [`docs/DESIGN.md`](docs/DESIGN.md) for details.

## Building

Splitbrain uses [bazel](http://bazel.build) as it's build system.

Quick start:

```
bazel build //... && bazel test //...
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

## License

Apache 2.0; see [`LICENSE`](LICENSE) for details.

## Disclaimer

This project is not an official Google project. It is not supported by
Google and Google specifically disclaims all warranties as to its quality,
merchantability, or fitness for a particular purpose.
