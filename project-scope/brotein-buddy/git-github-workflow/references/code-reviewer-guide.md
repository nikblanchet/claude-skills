# Code Reviewer Agent — Invocation Guide

The `code-reviewer` subagent runs under a **strict blinding contract**: it sees the diff and the existing codebase, nothing else. It never reads the PR description, planning docs, or commit messages, because authorial intent measurably biases the review.

Canonical policy source: BroteinBuddy `CLAUDE.md`, "Process before every merge" step 4 and "Notes on the critique steps". This guide is the mechanics; that file is the policy.

## When to Invoke

In the merge workflow, the code review runs at step 4 — after local checks pass, before any merge consideration.

1. `npm test` passes.
2. `npm run lint` is clean.
3. `npm run build` succeeds.
4. Spawn a fresh `code-reviewer` subagent in a clean session.

Do not invoke before tests pass — a reviewer chewing on a broken build produces noise, not signal.

## What the Reviewer Sees (and What It Doesn't)

The contract is enumerated, not principled. There is no judgment call about whether a given input "counts" as intent.

### Allow-list (read freely)

Inputs and actions that produce factual answers about the code as it exists on disk:

- The diff: `git diff main..HEAD`.
- Any file in the working tree outside the deny-list.
- Dependency source under `node_modules/`.
- Test / type-check / build runs: `npm test`, `npm run lint`, `npm run build`.
- Web searches for library and API documentation.

### Deny-list (forbidden inputs)

Authorial intent and out-of-band context:

- `gh pr view` — the PR description and comment thread.
- Anything under `.planning/` or `.scratch/`.
- `git log main..HEAD` and `git show` on any commit on the branch.
- The conversation transcript that produced the code.
- Prior fresh-context reviews of the same PR.

### Backstop clause

If the reviewer feels it needs something from the deny-list to make a judgment, **that itself is a finding**: "intent is not legible from the diff and codebase alone." It is not a license to read the forbidden input. A guide that depends on the reviewer's discipline is a guide that has already failed; redact at the source.

## Why This Definition of Blind

Three sources motivate the contract.

1. **Mitropoulos, Alexopoulos, Alexopoulos, and Spinellis (March 2026), "Measuring and Exploiting Contextual Bias in LLM-Assisted Security Code Review"** (arxiv 2603.18740v2). In their bias-injection study, redacting the PR description before passing the PR to an automated reviewer recovered detection in 12 of 17 missed cases (70%). Adding explicit instructions to ignore commit metadata recovered 4 more, raising overall detection to 16 of 17 (94%). The paper's conclusion: "Programmatically redacting bias elements is the safest approach" — instruction-based debiasing leaks because reviewers reference metadata anyway. Hence: redact at the source (this guide), do not rely on telling the model to ignore what it has been shown.

2. **McAleese et al. (2024), "LLM Critics Help Catch LLM Bugs" (CriticGPT, OpenAI)**. LLM critics catch real bugs that human reviewers miss. The wrinkle is calibration: context-rich critics carry a measurably higher false-positive rate, and false positives erode trust faster than missed bugs do. A blinded reviewer that finds fewer fake issues is more useful than a context-rich reviewer that finds more total issues but mixes in confident-sounding noise.

3. **Anthropic's Claude Code best practices** make the same point about fresh context: a reviewer without the author's framing won't be biased toward rationalizing the code it just saw produced. The rule generalizes beyond Claude-authored code — any account of why the code looks the way it does primes the reviewer to rationalize rather than scrutinize.

Note the **deliberate asymmetry** with `teacher-mentor-guide.md` in this same directory: the teaching-mentor subagent is given the PR description, planning docs, commit history, and prior code reviews precisely because its job is to author an educational record of the final delivered state. That subagent needs intent. The code reviewer does not. Different stage of the workflow, different blinding.

## First Review vs Subsequent Reviews

Default: one pass.

A second pass is permitted **only if the first surfaced structural objections that materially reshaped the PR** — a new file added, a function rewritten, a design choice reversed. A second pass is not appropriate when the only changes since pass one are tidying nits or fixing typos; those don't need a fresh review.

**Hard cap: two passes per PR.** A third pass is a sign the PR is wrong-sized; split it or accept the current state.

Each pass is its own fresh-context subagent invocation in a clean session. The harness does not carry prior conversation, including prior reviews, into a new subagent — "fresh context" already implies it, and no separate rule is needed.

## Exit Signal

When the reviewer finds nothing meriting attention, it must explicitly say **"No material issues."** (capital N, period). That phrase is the green light.

The absence of findings is not the same as the presence of approval. A reviewer that returns a blank list might have failed to find issues for reasons unrelated to PR quality. The explicit signal forces the reviewer to commit.

Do not reward critics that invent issues to justify their turn. A correct review with nothing to flag is a useful review.

## Invocation

The invocation prompt has three load-bearing parts: the blinding contract, the output format, and the exit-signal requirement.

```
Review this PR. Read only the diff and the existing codebase on disk.

DO NOT read:
- The PR description or comments (do not run `gh pr view`).
- Anything under `.planning/` or `.scratch/`.
- The branch's commit messages (do not run `git log main..HEAD` or `git show`).
- Any prior review of this PR.

You MAY:
- Read `git diff main..HEAD`.
- Read any file in the working tree outside the deny-list above.
- Read dependency source under `node_modules/`.
- Run `npm test`, `npm run lint`, `npm run build`.
- Search the web for library and API documentation.

If you feel you need something from the deny-list to make a judgment,
return that as a finding ("intent is not legible from the diff and codebase
alone"). Do not read the forbidden input.

Return findings as a numbered list. Each finding has:
- severity: `blocker` | `concern` | `nit`
- summary: one sentence
- detail: a short paragraph

If you find no material issues, your response must explicitly state:
"No material issues."

This is pass 1 of at most 2.
```

For a second pass — only when the first triggered structural changes — use the same prompt with the last sentence replaced by:

```
This is pass 2 of 2. The diff has changed since pass 1; review the current
diff fresh. Do not look up pass 1's findings.
```

## Agent Output Location

Save the review to:

```
.scratch/code-review-pr-{pr-number}-pass-{n}-{timestamp}.md
```

Example: `.scratch/code-review-pr-100-pass-1-2026-05-21T14:30:00-0700.md`.

`.scratch/` is gitignored. Note the asymmetry: the reviewer **writes** its output here as the only permitted interaction with the directory, but the deny-list still forbids **reading** anything under `.scratch/` (including its own past output or another reviewer's). The file is for the human's reference between iterations, not for a subsequent reviewer to consume.
