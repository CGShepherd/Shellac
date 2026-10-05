# Project Shellac — Collaboration and Execution Guidance

This file defines the standing collaboration and execution policy for Project Shellac. It is process guidance, not electrical, mechanical, CAD, BOM, qualification, release, or manufacturing authority.

## 1. Default execution mode

Default to normal ChatGPT plus connected tools.

Do not use Codex or ChatGPT Work merely because Shellac contains software, Git, Python, KiCad, LTspice, automated tests, generated artefacts, or other repository-managed engineering material.

Use Codex or direct/local repository execution only when the user explicitly requests it.

## 2. Preferred workflow

Unless explicitly directed otherwise:

1. Analyse and review in the conversation.
2. Inspect connected evidence when useful.
3. Produce bounded, fail-closed scripts or patches for repository changes.
4. Let the user run local commands where direct execution is unnecessary.
5. Review the returned evidence before treating a change as qualified or closed.
6. Preserve configuration control throughout.

Prefer exact copy/paste Windows commands for local execution.

## 3. Authority and provenance

Do not silently modify historical authority or historical evidence.

Always distinguish between:

- current implemented authority;
- selected-next architecture that is not yet live product authority;
- historical or superseded provenance;
- qualification and assurance evidence.

A selected or preferred architecture must not be described as implemented until implementation evidence exists. Historical evidence must not override later current authority.

## 4. Fail-closed repository handling

Fail closed when repository state is ambiguous or when unexpected working-tree changes are present.

Do not overwrite, absorb, discard, stage, commit, or reinterpret unrelated changes merely to make a requested task proceed.

When a task assumes a governed baseline, verify the expected branch, expected baseline commit, local/remote relationship where relevant, and working-tree state before applying a repository change.

## 5. Release and routing gates

Keep routing, layout, BOM, manufacturing, and release gates explicit.

Do not infer that routing or another release gate is open merely because analysis or assurance work has begun.

Where a governed hold exists, preserve it until the explicitly governed blockers and assurance gates are satisfied.

## 6. Engineering review standard

Challenge engineering assumptions.

Distinguish measured or reproduced evidence from analytical inference, judgement, preference, and unresolved hypothesis.

Do not treat simulation limitations, model limitations, nominal-only results, surrogate results, or unexecuted bench work as closed evidence.

Apply the standing design philosophy of affordable performance: use tighter tolerance or superior component technology when calculated or measured impact justifies it; otherwise prefer the more economical technically adequate part.

Prefer defensive schematic and PCB decisions where they are cost-free or low-cost, but do not add unnecessary functionality, circuitry, options, or design complexity.

## 7. Substantial-response continuity

For substantial Shellac responses, end with:

`Confidence: NN%`

`Chat runway: ...`

Use the runway indication to preserve continuity. Begin preparing a continuation prompt when runway becomes Moderate, and proactively provide one when runway becomes Short or Critical.

## 8. One-off build and controlled recoverability

Shellac is expected to be a one-off or very-low-volume build, not a prototype intended to converge through repeated PCB revisions.

Do not use future prototype iteration as the default mitigation for a known pre-fabrication uncertainty. Close design-driving uncertainty before fabrication where practical. Where residual uncertainty cannot reasonably be closed and a board/mechanical respin would otherwise be the likely remedy, apply the controlled recoverability standard in `docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md`.

Defensive options must be tied to a specific uncertainty and must not materially degrade nominal performance. Avoid speculative option proliferation, especially in the low-level cartridge/SCH101 region.

## 9. Persistent cross-chat working state

`PROJECT_SHELLAC_WORKING_STATE.md` is the mandatory cross-chat execution-state index.

It is deliberately non-authoritative. Controlled current design/release authority wins if any conflict exists, and the working-state file must then be corrected before further major work.

Refresh the working-state file after every material review, qualification pass, governed repository transaction, commit/push, or critical-path change and before beginning the next major engineering phase.

A new Shellac chat should read `PROJECT_SHELLAC_WORKING_STATE.md` and this guidance before substantive work, then verify the actual repository baseline and consult specialist authority files as required.
