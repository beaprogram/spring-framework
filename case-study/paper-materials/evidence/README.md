# Preserved experiment evidence

These are copies of selected original CI artifacts from 17 October 2026, published with the documentation on 27 October. No experiment was rerun to create this bundle. The canonical explanation is [case study details](../../README.md).

Each stage contains its original `dcode-result.json`, `DependencyGraph.graphml`, `upstream-check.log`, and a ZIP of the original JUnit XML files. The upstream architecture failure report is also preserved: nonempty for the violation stage, empty for baseline and repair. XML files were repacked without changing their bytes; binary Gradle caches and unrelated analyzer outputs are omitted.

[Provenance](provenance.json) records artifact names, original member paths, full commits, individual XML hashes and derived test totals. [Controlled mutation diff](controlled-mutation.diff) was generated from the two recorded source commits; it is a derived comparison, not a new experiment.

Run `python3 verify.py` from this directory. The verifier uses only Python's standard library, checks the checksum manifest and XML hashes, recounts test results, compares the three dependency graphs and checks active DCode gate results. It does not contact DCode or run the analyzer. A checksum establishes file integrity against this bundle's manifest, not independent authenticity of the original CI run.

Original CI runs: [baseline](https://github.com/beaprogram/spring-framework/actions/runs/39037227075), [violation](https://github.com/beaprogram/spring-framework/actions/runs/39037674985), [repair](https://github.com/beaprogram/spring-framework/actions/runs/39038043397). CI downloads can have different access or retention requirements; the subset here remains inspectable from the public repository.
