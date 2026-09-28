# Agent entry point

This repository is the persistent research workspace for Lithuanian **Statybos techniniai reglamentai (STR)** and related construction law.

If you are an AI assistant starting a new project session, **start here**.

## Required startup

1. Read **`PROJECT_GUIDE.md`** before substantive regulatory research.
2. Use **`data/str-catalog.json`** and **`knowledge/REGULATION_MAP.md`** to locate likely STRs.
3. Use **`knowledge/COMMON_DECISION_PATHS.md`** for questions that span several regulations.
4. Check **`knowledge/TRANSITIONS_2027.md`** when the relevant date is near or after 2027-01-01.
5. For current-law questions, verify the live VTPSI index/update date and the applicable consolidated official text.
6. Use **`maintenance/KNOWLEDGE_AUDIT.md`** when a knowledge-base audit, documentation-hygiene review or structural refactor is needed.

## Authority rule

The repository is a research/indexing layer, not the legal authority.

Use this hierarchy:

1. e-TAR / Teisės aktų registras
2. e-Seimas
3. VTPSI
4. Secondary sources only for discovery/cross-checking

If repository material conflicts with an official current source, **the official source wins** and the repository should be corrected.

## Answer standard

A substantive answer should normally contain:

- a clear practical conclusion;
- STR / legal-act number and title;
- exact point, subpoint, appendix, table or note;
- a short quotation where useful;
- explanation of how the provision applies;
- relevant exceptions/dependencies;
- effective-date context;
- official-source link.

Do not answer current legal questions from memory alone.

## Maintenance rule

The repository should improve through use, but **not every new fact belongs in persistent knowledge**.

Persist a finding only when it is reusable and has been verified well enough to improve future research, such as:

- a regulatory change or effective-date correction;
- a confirmed cross-reference;
- a corrected official source;
- a transition rule;
- a recurring decision path;
- a durable interpretation or research shortcut that is clearly distinguished from legal text.

Before persisting regulatory knowledge:

1. verify the controlling source using the official-source hierarchy;
2. record enough provenance to re-check the finding later;
3. distinguish verbatim legal requirements from interpretation or administrative guidance;
4. preserve applicable effective-date / historical context;
5. avoid turning user-specific facts, unsupported assumptions, or tentative reasoning into project knowledge.

### Audit/refactoring trigger

Invoke a **scoped** knowledge audit automatically when normal research reveals a material repository-maintenance problem, including:

- repository knowledge contradicting an official source;
- duplicate/competing canonical entries;
- stale routing or cross-references;
- current/future/historical regimes becoming mixed;
- an important regulation changing status or a transition date becoming operative;
- several related findings that should be consolidated into a reusable decision path.

Do not run a full repository refactor after every question. Use the smallest scope that fixes the discovered problem. For substantive legal inconsistencies, verify official sources before changing durable knowledge.

A user can explicitly trigger a full audit with requests such as **"run the knowledge-base audit"** or **"audit/refactor the project knowledge"**.

For the full workflow, provenance fields, classification rules, historical/future-law handling, citation precision and repository-maintenance policy, read **`PROJECT_GUIDE.md`**. For audit levels, procedure and completion criteria, read **`maintenance/KNOWLEDGE_AUDIT.md`**.
