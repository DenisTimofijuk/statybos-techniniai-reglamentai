# Statybos techniniai reglamentai — research workspace

This repository is a maintained knowledge base for Lithuanian **Statybos techniniai reglamentai (STR)** listed by the Valstybinė teritorijų planavimo ir statybos inspekcija (VTPSI).

Canonical index: https://vtpsi.lrv.lt/lt/teisine-informacija/teises-aktai-2/statybos-techniniai-reglamentai/

## Start here

For AI / ChatGPT project sessions:

1. **Read `AGENTS.md` first.**
2. It points to `PROJECT_GUIDE.md` for the complete research, citation and maintenance workflow.
3. Use the structured catalog and knowledge maps to route questions before researching official legal text.

## Baseline

- VTPSI page update date: **2026-09-11**
- Baseline captured: **2026-09-28**
- STR entries in the VTPSI list: **63**
- Current/future transition already tracked: **STR 2.02.12:2026 „Pastatai“**, effective **2027-01-01**

## Purpose

The repo is optimized for answering concrete questions with:

1. the relevant STR number and title;
2. the exact point / subpoint / appendix / table reference;
3. a short direct quotation where useful;
4. the effective-date context;
5. a link to the official source.

It is deliberately not a substitute for the official register. e-TAR / e-Seimas remains authoritative; local material is an index and research aid.

## Structure

- `AGENTS.md` — **single session/agent entry point**
- `PROJECT_GUIDE.md` — detailed research, citation, freshness and maintenance rules
- `data/str-catalog.json` — machine-readable VTPSI STR inventory and validity metadata
- `knowledge/REGULATION_MAP.md` — where to look by topic/problem
- `knowledge/COMMON_DECISION_PATHS.md` — recurring multi-regulation research paths
- `knowledge/TRANSITIONS_2027.md` — known upcoming changes and replacement rules
- `scripts/search_catalog.py` — local STR catalog lookup helper
- `scripts/check_vtpsi.py` — checks the VTPSI page update date and current STR inventory
- `scripts/audit_knowledge.py` — mechanical documentation/catalog hygiene checks
- `maintenance/KNOWLEDGE_AUDIT.md` — full/scoped semantic audit and refactoring procedure
- `maintenance/audit-state.json` — audit state and unresolved maintenance items
- `.github/workflows/check-vtpsi.yml` — scheduled freshness monitor
- `.github/workflows/knowledge-audit.yml` — monthly/manual mechanical knowledge audit

## Source hierarchy

1. **e-TAR / Teisės aktų registras** — primary legal source
2. **e-Seimas** — official legislation text/structure and consolidated editions
3. **VTPSI** — canonical STR inventory and administrative guidance
4. Secondary legal databases — discovery/cross-check only, never the sole authority for a final legal citation

## Freshness rule

Before relying on this repository for a date-sensitive answer, compare the live VTPSI page's **Atnaujinimo data** with the value stored in `data/str-catalog.json`.

If the dates differ, treat the repository as stale until the changed inventory/editions are reviewed.

> Legal texts change. An answer without an edition/effective-date check is merely a very organized way to be wrong.


## Knowledge maintenance

The repository uses a two-layer hygiene model:

- **mechanical checks** detect structural problems without interpreting law;
- **semantic/legal audits** consolidate and refactor knowledge only after appropriate official-source verification.

Run `python scripts/audit_knowledge.py` for a local mechanical check, or follow `maintenance/KNOWLEDGE_AUDIT.md` for a full audit. The mechanical audit also runs monthly in GitHub Actions and can be dispatched manually.

During ordinary research, the AI should invoke a **scoped** audit automatically when it encounters contradictions, stale routing, duplicated canonical knowledge, transition/status changes or similar maintenance debt. It should not perform repository-wide refactors merely because a new question was asked.
