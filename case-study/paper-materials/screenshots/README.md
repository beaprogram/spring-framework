# Case study figures and screenshots

Use the [canonical case study](../../README.md) for the explanation and results.
Each retained image has a specific role; the detailed reconstruction is the main
architecture figure.

| Image | What it supports |
| --- | --- |
| [Detailed architecture](intended-architecture-detailed.svg) | All five Common members, selected neighboring types, the denied component rule, the introduced dependency and its existing return path. Explicitly labeled reconstruction from preserved membership and GraphML. |
| [Baseline report](baseline-report-2026-10-27.jpg) | Original saved baseline: selected commit, published v1, passed gate, zero violations and 516 edges. |
| [Violation overview](violation-overview-2026-10-27.jpg) | Selected violation commit, published v1, failed gate and one violation despite 99.8% aggregate compliance. |
| [Full violation report](violation-report-2026-10-27.jpg) | Original full report for inspecting the forbidden dependency and rule breakdown. The case-study page uses the cleaner overview; the PDF includes a labeled lower-report excerpt. |
| [Repair report](repair-report-2026-10-27.jpg) | Original saved repair: selected commit, published v1, passed gate, zero violations and 516 edges. |
| [Published membership capture](published-membership-2026-10-27.jpg) | Supporting UI provenance showing v1 and the five Common members. This crowded, collapsed canvas is not the main architecture explanation. |

Report validation dates remain 17 October 2026; these captures were taken on 27 October
by opening saved results. Capturing the screens did not rerun the experiment.

The former three-box architecture export, its redundant canvas capture, and the older
duplicate baseline capture are omitted from the current branch. Earlier Git snapshots
retain them; their removal does not alter the underlying experimental evidence.
