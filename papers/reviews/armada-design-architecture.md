# Adversarial architecture review: Cro in the Measurement Armada

Reviewed 2026-10-02. Inputs: [current design](../../docs/design.md) and the operator's original `Measurement_Armada_Architecture_Notes.pdf`, pages1–13. The original PDF SHA256 is `37c8edba3f921b08e0c8736a0849afb2ca2b75f7a295eb97d0378f04c2276c83`; a fresh extraction exactly matched `context/design/measurement-armada.txt`. This review concerns architecture and scientific handoffs, not a derivation or runtime-code review. No design or runtime files were edited.

**Final assessment: all seven findings are resolved at the architecture level. No remaining blocker was found within this review scope.** The revised design defines a bounded conventional campaign and coherent scientific handoffs. This clears these architectural findings for the next mathematical specification; it does not establish the deferred derivations, numerical algorithms or implementation behavior.

## Final integration check

The original findings below are retained with their initial line references; those line numbers precede the integration edits. A final scoped re-read checked the actual revised design, including its bounded campaign, joint fitting state, observation records and provenance exports.

| Finding | Final status | Resolution in current design |
| --- | --- | --- |
|1 — Forecast versus repair|Resolved|Design Comparison and Acquisition, lines454–466: structural prospective repair is separate from a numerical forecast, which requires declared component scenarios/prior/acquisition assumptions. |
|2 — Fisher/runtime round trip|Resolved|Proposal record and lines468–475: Fisher returns an actual assignment; Cro checks returned incidence before execution; runtime preserves selection/observations and the preceding result. |
|3 — Bounded milestone|Resolved|Worked Campaign explicitly labels supplied arithmetic and does not claim fitting or a completed loop. First Bounded Campaign, lines575–614, chooses scalar Gaussian one-prompt coverage followed by checked second-prompt acquisition and expanded balanced EMS refit. Explicit prerequisites exclude general sparse fitting, intervals/allocation, multivariate/ordinal/temporal families and production runtime. |
|4 — Initial fitter ownership|Resolved|Estimation Contracts, lines252–257: Cro initially owns its G-specific first estimators behind the reusable inference contract; each fit has one implementation/method identity. Ras ownership is scoped to response-model scale/severity/linking, while Cro can retain Gaussian rater means. |
|5 — Version/joint-source provenance|Resolved|Results and Armada Interoperability, lines488–500: references resolve exact input versions; derived/adjudicated observations retain parents/roles; exports retain shared stochastic sources, joint draw indexing/approximation and transformations. GUM distinguishes totals from contributions and cannot assume missing joint relationships independent. |
|6 — Observation support/time/visibility|Resolved|Study and Observation Records now require supported point/category/interval/censoring representations, bounds, point time or window with units and protocol/mechanism versions. Mechanism references resolve allowed evidence/visibility; unsupported record kinds may be rejected explicitly. |
|7 — Mean/effect fit state|Resolved|Estimation and Projection retain fitted mean/effect state and joint dependence; projection retains mean structure and response thresholds/links. Joint draw collections contain the state required for the requested projection. Concrete parameter layouts and family derivations remain specification work. |

No remaining architecture blocker was identified within the original seven findings. The bounded milestone's mathematical specification must still establish the precise supported prompt-conditional quantity, which aliases the chosen two-prompt assignment resolves, the EMS derivations and the meaning of any signed estimates. The revised text explicitly retains those obligations and does not require every component to become separately identified. The initial family is partial in prompt coverage, not arbitrary incomplete-cell inference. This is an appropriate scope restriction, not a hidden expansion of support.

The rereview made no changes to design or runtime files. The original finding descriptions remain as the integration history and their proposed acceptance conditions remain useful inputs to the later specification and implementation plan.

Here P1 means a decision needed before planning the stated end-to-end milestone. P2 means an interface weakness to resolve before the affected shared record or extension is implemented. These are proposed-design findings, not assertions of bugs in the published0.1.0 calculator.

## 1. P1 — Projection candidates and information-acquisition probes need distinct contracts

**Location:** design lines255–265 and365–386; diagram lines86–89. **Original:** Armada pages2,4–5 and12.

The projection contract correctly rejects a new procedure whose necessary components are confounded in the pilot. The acquisition section then says Cro evaluates a proposed pilot's precision objectives, but does not distinguish a future **measurement replication** from an **experiment that obtains information needed to estimate the model**.

Consider the stated exclusive system–judge pilot. The desired judge-generalized coefficient can be unsupported. If every candidate passes through the existing projection-support gate and requires that coefficient as its objective, a useful crossed-overlap pilot also has no admissible objective. The architecture can report why the pilot failed, yet has no defined path to select the observation that repairs it. Supplying arbitrary values for the unidentifiable components would solve the programming problem by inventing evidence.

**Fix:** distinguish two operations at the scientific boundary:

- D-study evaluation predicts score error/dependability under a stated replication model and compatible component information.
- Acquisition evaluation checks what information a proposed observation assignment can add. A structural repair may be supported by its change to the identifiable combinations without having a numerical expected-precision or information-gain value. A numerical utility requires an explicitly sourced external component scenario, prior or inference/acquisition model.

An acquisition proposal must say which target/alias or unsupported projection it addresses, what observations/overlap are required, and whether its utility is structural, conditional on supplied assumptions, or statistically estimated. Preserve that distinction in candidate statuses. Do not claim that increased rank implies a particular precision gain, or that overlap alone identifies all covariance components.

**Acceptance:** a confounded pilot produces a justified repair request with unknown quantitative gain, rather than either a fabricated coefficient or an empty “no candidates” answer. Under explicitly supplied external assumptions it can additionally produce a labeled quantitative comparison.

## 2. P1 — The Fisher/runtime handoff omits the return-and-recheck step and proposal record

**Location:** design ownership table lines34–39, minimum records lines109–118, diagram lines87–89, acquisition lines381–386. **Original:** Armada page6's explicit Probe proposal record, pages5 and12.

The diagram combines “Campaign acquisition and Fisher assignment” after optimization, whereas Fisher must establish a realizable assignment before a count-based prediction becomes an executable recommendation. The text permits actual incidence or a validated assignment distribution, but no handoff states what happens when Fisher realizes a different topology, rejects the request, or returns an assignment whose dependence/overlap invalidates the initial projection. The minimum vocabulary also lacks the probe-proposal record required by the original architecture.

**Fix:** name the request/return protocol without choosing a package or serialization technology:

1. Cro returns a procedure/repair request tied to a particular study and fit, with target, sampling assumptions, required incidence properties and Cro's conditional evaluation.
2. Fisher returns the concrete assignment or an explicitly supported assignment distribution, feasibility status, realized costs and any deviations.
3. Cro recompiles/rechecks that returned assignment and reevaluates supported quantities; disagreement invalidates or revises the initial candidate evaluation.
4. The runtime records the accepted proposal, selection rationale/policy and evidence available at selection, executes it, and returns observations with those assignment identities. Changed conditions create a new recorded study revision.

The runtime owns selection and execution; Fisher owns construction; Cro owns the measurement-model check and projection. A rejected or changed assignment is a normal result, not implicit permission to execute the original count-only recommendation.

**Acceptance:** an assignment with the same nominal counts but exclusive pairing cannot inherit the crossed candidate's G/Phi. A repaired assignment receives its own reevaluation before execution. Proposal and returned observations can be traced through one round trip without reading a prose log to reconstruct the links.

## 3. P1 — The worked example does not demonstrate the proposed first milestone

**Location:** design lines423–477, especially427,434 and461–462. **Original:** Armada page12, stage1 and the first demanding milestone.

“The pilot estimates” seven components is followed by an explicit statement that these are supplied illustrative parameters. The table therefore demonstrates the existing projection arithmetic, not fitting a pilot. The exclusive-pairing branch describes a potential repair but supplies neither an actual candidate assignment nor a completed acquisition/refit round trip. The statement that this “realizes” the campaign milestone overstates the example.

The capability table places campaign integration after sparse fitting, coherent uncertainty/allocation and multivariate/extended models. It calls itself a dependency map but does not declare which of those branches are prerequisites for the first partial-rating milestone. A planner could interpret all of them as required and defer learning the shared contracts until most of the fleet exists.

**Fix:** label the current example as a supplied-component illustration. Add a bounded milestone definition: one observation family, one explicit partial-design family, one supported target, one deliberate alias, one repair request, one realized assignment, one new observation batch and reevaluation. State dependencies explicitly; general multivariate/ordinal/temporal fitting and a production campaign database should not become prerequisites merely because they appear earlier in a table.

A tractable candidate is a one-prompt pilot with multiple objects and judges: report supported prompt-conditional quantities, retain the alias blocking a new-prompt target, obtain another prompt with the required object/judge coverage, then check and refit the expanded design. The exact estimability and estimator rules require the forthcoming mathematical specification. Alternatively select a named incomplete Gaussian family if the first milestone truly requires unbalanced fitting. Do not call it arbitrary unfamiliar-incidence support.

The demonstration may use a small assignment provider and campaign runner under the stated contracts; it need not launch Fisher as a separate library. Acceptance should cover supported estimates, blocked projections, actual proposal feasibility, preserved IDs/provenance and a useful change in supported information. Independently reconciled calculations still supply the numerical oracle.

**Acceptance:** a reviewer can identify the initial observations, supported and unsupported questions, actual next observations and resulting change in conclusions. Supplied synthetic generating components remain reference evidence and are not passed to the fit as if inferred from the pilot.

## 4. P2 — Statistical ownership is clear conceptually, but estimator ownership needs one explicit decision

**Location:** design lines24–39,97–101 and219–235. **Original:** Armada pages3–4 and12.

The ownership table gives model fitting to “Shared inference”; later Cro proposes its own estimation module and constrained Gaussian engine. These can be compatible, but the document does not say whether that engine is Cro's implementation behind the shared estimator contract, a common service, or a second implementation alongside shared inference. The difference affects the first fitting API and subsequent Ras integration.

“Ras owns … modeled rater severity” is also too broad if read literally. A Gaussian G-study can estimate rater mean effects or retain a fixed-panel mean structure. Response-model severity on an identified latent scale belongs to Ras; it is not a prohibition on all rater mean terms in Cro.

**Fix:** choose the initial implementation owner while retaining a reusable estimator contract. For example, Cro owns its G-specific EMS logic and a bounded Gaussian fitting implementation; it exposes that through the common model/estimate contract, allowing shared inference to use or replace compatible numerical machinery later. Do not decide all package boundaries now. Scope Ras's ownership to response-model parameters/latent scale/linking and specify that a joint Ras–Cro model has one coherent joint estimation state rather than two independently fitted summaries being implicitly combined.

**Acceptance:** each first-milestone fit has one responsible implementation and one method identity. A future joint response/GT fit retains dependence between response-model and GT parameters rather than multiplying independent uncertainty summaries.

## 5. P2 — Provenance references need version and joint-source semantics

**Location:** design lines105–133,344–348 and394–403; GUM handoff line37. **Original:** Armada pages2,5–6 and8.

The design repeatedly requires provenance, stable identities and joint uncertainty. Those are good requirements. It does not yet state whether a reference names an immutable observation/design/model version or a mutable campaign entity. This matters for adaptive acquisition and for the promise that candidates share the same component uncertainty. Two exports from the same fit must remain one shared uncertainty source, not become independent contributions because they arrived in separate records.

**Fix:** require each fit/result/proposal to resolve the exact version of its study, observations/assignment, protocol, model and estimator configuration. The runtime remains responsible for the evidence ledger. Cro does not need to own a database, but its returned records need referential meaning sufficient to replay the calculation. Derived/adjudicated observations need parent/role references rather than merely a repeated evidence pointer.

For joint covariance or draws, preserve source identity, parameter/dimension ordering, scale transformations and shared draw indexing (or the identified joint approximation). The GUM export should identify which contributions share the same stochastic source and whether a contribution is a component contribution or an already aggregated total. Factor/evidence IDs alone do not define the cross-covariance of two derived quantities.

**Acceptance:** combining two results from one fit cannot silently treat their uncertainties as independent or count the same measurement-error contribution twice. Reanalysis after rubric or assignment revision can distinguish its inputs from the earlier result without overwriting it.

## 6. P2 — The observation contract loses information needed for censoring and temporal extensions

**Location:** design observation row114 and lines124–133,320–327. **Original:** Armada page6 specifies time **or interval**, visible information and observation-mechanism distinctions; pages7–8 add latency/exposure and evidence access.

“Value or explicit missing status” plus “time or occasion” can represent a point rating, but a status labeled censored does not specify its bound, a windowed sensor aggregate does not specify its integration window, and an occasion label does not specify elapsed time in units. Dependence declarations cannot reconstruct information absent from the observed record. Evidence access is described in prose but lacks a required reference to the actual observation mechanism/visibility configuration.

**Fix:** allow an observation to carry the typed support needed by its declared family: point value, category, interval/bound or other explicitly supported representation; point time or time window with units; and an observation-mechanism/version reference resolving exposure, permitted evidence and acquisition process where relevant. Cro need not reproduce trajectories or collect expert discussions. Unsupported record kinds can be rejected in the first engine while preserving them for a later supported model.

**Acceptance:** identical occasion labels with different elapsed times are not silently treated as identical temporal designs. Right-censoring at a known threshold cannot be ingested as an ordinary missing value or an exact observation at the threshold. Two ratings under different evidence visibility do not become equivalent solely because their rubric version matches.

## 7. P2 — Future multivariate/temporal adapters need fitted mean/effect state, not just component summaries

**Location:** design fit row117, shared inference row36, projection lines267–278, multivariate lines308–327; explicit future mean work at lines521–522.

The document acknowledges that some absolute multivariate targets require mean information, yet its fit handoff is described primarily as component values and joint component uncertainty. An adapter that returns only covariance components is insufficient for retained fixed effects, regressed scores, mean differences, drift/random slopes or some conditional-error targets. The observation model's mean structure is not the fitted mean state.

**Fix:** define the estimator result as an identified parameter/function state. It can include component estimates, fitted fixed/retained effects and relevant joint uncertainty, or explicitly record which pieces are unavailable. Parameter identities must include basis/scale/conditioning so a random intercept/slope covariance is not mistaken for a matrix across score dimensions. Supplied-component input remains a valid restricted input; requests requiring unavailable means/effects should be rejected with that reason.

**Acceptance:** future contrast/regressed/absolute requests cannot receive an apparently complete result from an input that contains only the covariance pieces they happen to need for one marginal reliability calculation. The first scalar kernel remains unchanged.

## Original decision boundary versus deliberately future work

These were the architecture decisions required before planning the bounded round trip; the final integration check above confirms they are now resolved: replication-versus-acquisition roles and result statuses; the proposal/assignment/recheck protocol; initial estimator owner; the selected partial-design/model family and milestone prerequisites; precise reference/version meaning for the records crossing that loop. These are architectural choices.

Still appropriate for later mathematical specifications: fixed/finite transformations; exact covariance identifiability criteria and tolerances; partial-identification bounds; general irregular score operators; constrained likelihood boundary algorithms; heterogeneous multivariate fitting; temporal/categorical models; confidence/credible interval methods; adaptive-selection validity; classification and conditional-error derivations. Their explicit deferral is not a finding. Also appropriately open: bindings, Arrow or other serialization technology, package extraction, production runtime, learned observers and learned inference/design.

## Strengths retained

The measurement study is a suitable Cro-owned analysis unit under the campaign-owned question and evidence ledger. Cro need not own the campaign's rival hypotheses, simulator or discussions. The target-first signal/error partition, observed-design/universe distinction, alias-preserving projection checks, method-specific uncertainty, scale boundaries and compositional capability checks all align with the original and acquired literature. The document correctly separates reliable observations from correctness, causal identification, calibration and validity; preserves first-pass versus adjudicated evidence; and keeps learned warnings separate from algebraic estimability. No wholesale architectural replacement is indicated.
