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
