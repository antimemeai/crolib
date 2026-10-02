# Measurement Armada design source

The operator supplied `~/projects/Measurement_Armada_Architecture_Notes.pdf` as
the broader direction for crolib on 2 October 2026. The 13-page sketch is titled
*The measurement armada*, working architecture v0.1, dated 2 October 2026. It
describes a campaign apparatus combining measurement libraries, simulation,
expert observations, conventional inference and a possible learned observer or
inference/design accelerator. It is an architecture proposal.

The original source is retained unchanged in ignored research storage at
`papers/downloads/design/measurement-armada-architecture-notes.pdf`. A reading
extraction is in ignored `context/design/measurement-armada.txt`. To restore the
local source, copy the operator's original PDF from the workspace location;
this is an operator-supplied document rather than a publicly downloadable work.
Its SHA256 is `37c8edba3f921b08e0c8736a0849afb2ca2b75f7a295eb97d0378f04c2276c83`.

## Design premises by page

| Pages | Premise used by crolib |
| --- | --- |
| 1–2 | A campaign investigates unresolved distinctions through observations and interventions; its output is a conditional characterization with uncertainty and a support envelope. |
| 3–4 | Cro owns G/D studies and dependability under an observation design; Fisher, Ras, GUM, validity and causal responsibilities have explicit handoffs. Shared numerical machinery can sit beneath scientific interfaces. |
| 5–6 | A common experimental loop preserves target, design, observation, model, result and proposal semantics. Interval interpretation and evidence authority survive serialization. |
| 7 | Simulation distinguishes hidden generating state from exposed observations and judgments. Identical exposed evidence can leave mechanisms unresolved. |
| 8 | Experts are an instrumented observation apparatus. Independent first-pass judgments, adjudication, evidence visibility and protocol versions remain distinct. |
| 9–10 | Typed learned outputs can be observers or computational accelerators. Schema validity, calibration, independence and identifiability remain separate; conventional fallback remains useful. |
| 11 | Agent and thermal campaigns share experimental structure while retaining different quantities, observation physics and warrants. |
| 12 | A demanding milestone is inference from an unfamiliar partial rating experiment that preserves ambiguity and selects a useful next observation. Package boundaries are settled through end-to-end campaigns. |
| 13 | Scientific neighbors and external citations are orientation, with explicit limits. The sketch does not audit crolib's current implementation. |

## Consequence for this repository

The proposed [crolib design](../docs/design.md) makes the measurement study the
central object and treats components and coefficients as conditional results.
It describes Cro's projection, uncertainty and allocation responsibilities and
the contracts connecting them to the Armada. This is our design inference from
the sketch and acquired corpus. It does not import the sketch's external claims
as validated implementation premises or select a dependency.

The existing 0.1.0 release remains a supplied-component crossed-design
calculator. Proposed broader capabilities are documented as future work.
