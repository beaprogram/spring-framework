# Spring Expression architecture compliance experiment

The study covers `spring-expression/src/main/java` at the upstream revision
`49adc91c7e41eaafb52fc11e1210989894bda1f3`, not the entire Spring Framework.
The repository was selected through a saved GitHub GraphQL shortlist of 20
popular Java repositories. Exact query/results are retained in the research
evidence outside this checkout.

Spring's `ArchitectureRules.SpringSlices` groups the first four package
segments and prohibits cycles. In this module those groups are the Expression
API, Common utilities, and SpEL implementation. Existing SpEL-to-Common
dependencies justify a controlled test of the reverse direction. A DCode
Common-to-SpEL denial operationalizes that constraint; it is not a verbatim
maintainer rule and does not establish tool equivalence with ArchUnit.

Keep one fixed architecture definition for baseline, deliberate violation, and
repair. The violation adds a Common convenience method that instantiates a
SpEL parser, with functional tests. Repair removes the controlled change;
it does not retain the added convenience API.

The workflow runs functional tests, records the upstream module checks,
extracts production-source dependencies with a hash-pinned analyzer, uploads
using the actual commit SHA, and enforces the active DCode gate. Upstream
checks are recorded separately so a failure there cannot prevent recording
the DCode verdict; their failures are still enforced before job completion.
Artifacts are retained even on gate failure. Do not interpret a successful
upload with an inactive gate as a passing architecture result.

GitHub configuration: `DCODE_API_KEY` is a secret; `DCODE_PROJECT_ID` and
`DCODE_ENFORCE_ARCH` are variables. Enforcement is `false` only for bootstrap
and `true` for all final experiment stages. Never put credentials in source.

Limitations: one module and controlled mutation, source-only graph, analyzer
trial limit, no external/runtime/Kotlin/test-class graph coverage. Other Spring
modules are build dependencies only. This is not whole-framework validation
or an estimate of accuracy on naturally occurring architectural defects.
