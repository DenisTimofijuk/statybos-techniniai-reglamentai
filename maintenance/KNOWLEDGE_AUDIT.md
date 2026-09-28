# Knowledge audit and documentation hygiene

This workflow keeps the repository useful as it grows.

It is deliberately split into **mechanical checks** and **semantic/legal review**. Mechanical tooling may detect structural problems. It must not decide what Lithuanian law means.

## 1. When to invoke this workflow

Run a **full audit** when the user explicitly asks for a knowledge-base audit, documentation hygiene review, repository refactor, or similar maintenance work.

Also invoke an appropriately scoped audit during normal research when one or more of these conditions appears:

- repository knowledge conflicts with an official source;
- several related reusable findings have accumulated and should be consolidated;
- duplicate or competing knowledge entries are discovered;
- an important regulation changes legal status;
- a transition date is reached or is about to change the applicable regime;
- an existing routing/decision path repeatedly fails to find the controlling rule;
- stale cross-references or inconsistent effective-date information are discovered;
- a repository area has become materially harder to use because knowledge is fragmented.

Do **not** run a repository-wide semantic refactor after every research question. Prefer the smallest audit scope that solves the detected maintenance problem.

## 2. Audit levels

### Level 1 — mechanical

Examples:

- malformed JSON;
- catalog count mismatch;
- duplicate regulation codes;
- missing required catalog fields;
- broken repository-local references;
- invalid audit-state structure;
- obvious duplicate source URLs;
- missing expected maintenance files.

May be checked by scripts.

### Level 2 — documentation structure

Examples:

- duplicate or competing notes;
- stale routing entries;
- orphaned knowledge;
- the same rule maintained in several places without a canonical entry;
- research paths that no longer match repository structure;
- case-specific notes that should be generalized or removed.

Requires semantic review, but usually not new legal interpretation.

### Level 3 — semantic/legal consistency

Examples:

- contradictory interpretations;
- legal text and interpretation blurred together;
- administrative guidance presented as binding legislation;
- current and historical rules mixed together;
- incorrect or incomplete cross-references;
- a conclusion whose effective-date context is unclear.

Requires verification against official sources before substantive changes are committed.

### Level 4 — regulatory change

Examples:

- new, amended, repealed or replaced legal acts;
- published future law becoming effective;
- transition provisions becoming operative;
- a changed official source that invalidates repository routing or conclusions.

Requires current official-source verification and updates to every affected index, transition note, decision path and knowledge entry.

## 3. Full audit procedure

### Step A — establish audit scope and state

1. Read `AGENTS.md` and `PROJECT_GUIDE.md`.
2. Read `maintenance/audit-state.json`.
3. Inspect repository structure and recent relevant knowledge changes.
4. Decide whether the audit is full-repository or scoped to a topic/area.

### Step B — run mechanical checks

Run:

```bash
python scripts/audit_knowledge.py
```

Use `--strict` when a non-zero exit code is useful for CI or a manual validation gate:

```bash
python scripts/audit_knowledge.py --strict
```

The script may flag candidates for review. A warning is not proof that the underlying knowledge is wrong.

### Step C — check freshness

For current-law maintenance, also run:

```bash
python scripts/check_vtpsi.py
```

If the VTPSI index differs from the committed baseline, investigate the actual regulatory changes before altering the catalog.

### Step D — semantic review

Review at least these questions:

1. Are there duplicate or competing canonical explanations?
2. Are topic-to-regulation routes still accurate?
3. Are recurring multi-regulation questions represented in `knowledge/COMMON_DECISION_PATHS.md`?
4. Are current, future and historical rules clearly separated?
5. Are transition dates and replacement relationships internally consistent?
6. Are legal rules, administrative guidance, interpretation and research paths clearly labeled?
7. Do persisted interpretations still have recoverable official legal support?
8. Are there useful findings stranded in the wrong file or duplicated across several files?
9. Are obsolete entries preserved only where historical context is useful?
10. Does any repository note make a broader claim than its source supports?

### Step E — official-source verification

Before modifying substantive legal knowledge because of a Level 3 or Level 4 finding:

1. verify the applicable legal text in e-TAR where possible;
2. use e-Seimas as the next official legal source;
3. check VTPSI for the current STR inventory and official administrative guidance;
4. establish the applicable effective date and consolidated edition;
5. inspect amendments, repeal/replacement provisions and transition rules;
6. preserve exact provision references and source URLs in the updated knowledge.

Do not "clean up" a legal discrepancy by choosing whichever repository wording looks more plausible.

### Step F — refactor conservatively

Prefer:

- one canonical entry plus cross-references;
- explicit current/future/historical status;
- small, focused changes;
- preserving provenance;
- updating routing/index files when canonical knowledge moves;
- deleting duplication only after confirming nothing unique is lost.

Avoid cosmetic mass rewrites that create large diffs without improving retrieval or correctness.

### Step G — update audit state

After a completed audit, update `maintenance/audit-state.json`.

For a full semantic audit, set `last_full_audit`.

For a mechanical-only run, set `last_mechanical_audit`.

For VTPSI freshness verification, set `last_vtpsi_check`.

Record unresolved maintenance items only when they are concrete and useful for a future session.

## 4. Automatic behavior during normal research

The assistant should automatically invoke a **scoped** version of this workflow when an audit trigger in Section 1 is encountered and repository write access is available.

Automatic maintenance must follow these constraints:

- do not interrupt a simple user question with unnecessary repository-wide work;
- fix a discovered contradiction or stale route when it materially affects future answers;
- verify substantive legal changes before committing them;
- do not silently convert uncertainty into durable knowledge;
- keep maintenance commits focused and explain material repository changes to the user.

## 5. Scheduled maintenance

The repository includes `.github/workflows/knowledge-audit.yml`.

It runs the mechanical audit on a monthly schedule and supports manual dispatch.

The scheduled workflow is intentionally non-mutating. It detects structural hygiene problems but does not autonomously rewrite legal knowledge.

A semantic/full audit remains an AI-assisted research task governed by this document and `PROJECT_GUIDE.md`.

## 6. Audit completion standard

A full audit is complete when:

- mechanical checks have been reviewed;
- currentness has been checked where applicable;
- identified Level 3/4 findings have been verified against official sources;
- duplicate/stale knowledge has been consolidated or explicitly left with a reason;
- routing and cross-references reflect any moved/changed knowledge;
- provenance and effective-date context remain recoverable;
- `maintenance/audit-state.json` has been updated.

The objective is not to make the repository prettier. It is to make future regulatory research **more correct, faster to route, easier to verify, and harder to misapply**.
