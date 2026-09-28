# Project guide — Lithuanian construction regulations

## 1. Purpose

This repository is a long-term research and reference workspace for Lithuanian construction law, with primary focus on **Statybos techniniai reglamentai (STR)**.

The objective is to answer practical construction-regulation questions accurately and auditably.

For substantive questions, research should identify:

- the applicable STR or other legal act;
- the exact point, subpoint, appendix, table or note;
- the relevant wording or a concise quotation;
- how the provision applies to the factual situation;
- important exceptions and dependencies;
- the effective date / applicable edition;
- an official-source link.

A plausible answer is not enough. The result should be independently verifiable against the applicable Lithuanian legal text.

## 2. Persistent workspace

Repository:

https://github.com/DenisTimofijuk/statybos-techniniai-reglamentai

Important files:

- `AGENTS.md` — short AI/session entry point;
- `PROJECT_GUIDE.md` — this detailed operating guide;
- `data/str-catalog.json` — machine-readable STR catalog and validity metadata;
- `knowledge/REGULATION_MAP.md` — topic-to-regulation routing map;
- `knowledge/COMMON_DECISION_PATHS.md` — recurring multi-regulation research paths;
- `knowledge/TRANSITIONS_2027.md` — known future regulatory transition information;
- `scripts/search_catalog.py` — local catalog lookup helper;
- `scripts/check_vtpsi.py` — VTPSI freshness checker;
- `scripts/audit_knowledge.py` — deterministic/mechanical repository-hygiene checker;
- `maintenance/KNOWLEDGE_AUDIT.md` — semantic audit/refactoring workflow and trigger rules;
- `maintenance/audit-state.json` — maintenance timestamps and concrete unresolved audit items;
- `.github/workflows/check-vtpsi.yml` — automated freshness monitoring;
- `.github/workflows/knowledge-audit.yml` — monthly/manual mechanical hygiene audit.

Treat the repository as persistent project memory, but not as the legal authority.

Use project/chat history as **working context**. Use this repository for **durable, reusable knowledge** that should survive individual conversations. Important research should not depend on the model vaguely remembering an earlier chat.

## 3. Official source hierarchy

### Primary legal sources

1. **e-TAR / Teisės aktų registras**
   - https://www.e-tar.lt/

2. **e-Seimas**
   - https://e-seimas.lrs.lt/

Use them for:
- legal text;
- consolidated editions;
- amendments;
- effective dates;
- repeals;
- transition provisions.

### Official administrative source

3. **VTPSI**
   - https://vtpsi.lrv.lt/

Canonical STR index:

https://vtpsi.lrv.lt/lt/teisine-informacija/teises-aktai-2/statybos-techniniai-reglamentai/

Use VTPSI for:
- the current STR inventory;
- official explanations and guidance;
- inspection/administrative material.

VTPSI guidance does not override the legal act itself.

### Secondary sources

Commercial databases, blogs, professional articles, forums and summaries may help discovery or interpretation, but must not be the sole authority for a final legal conclusion when primary material is available.

## 4. Freshness baseline

The repository was initialized from the VTPSI page showing:

**Atnaujinimo data: 2026-09-11**

The baseline date is recorded in `data/str-catalog.json`.

For current-law questions:

1. check the live VTPSI page;
2. compare its `Atnaujinimo data` with the repository baseline;
3. if newer, treat the catalog as potentially stale;
4. identify additions, removals, renamed acts and affected consolidated editions;
5. update the repository after verification.

Do not assume a search result or amendment document is the latest consolidated edition.

## 5. Research workflow

### Step 1 — establish the facts and relevant date

Identify facts that can materially change the legal result, such as:

- date of design/work/event;
- building or structure type;
- current and intended use;
- construction category;
- dimensions;
- location and land-plot context;
- protected-area or cultural-heritage status;
- type of works;
- whether the question concerns design, permitting, execution, completion or use.

Do not ask for information that would not materially change the answer. When reasonable, state an assumption and proceed.

### Step 2 — classify before applying requirements

Typical classification issues include:

- new construction vs reconstruction vs repair;
- building vs engineering structure;
- special / non-complex / other category;
- residential vs public vs industrial use;
- existing building vs proposed building;
- project design vs construction execution vs building use.

Do not jump directly to a numeric distance, dimension or document requirement before confirming the legal category.

### Step 3 — route to candidate regulations

Use:

- `data/str-catalog.json`;
- `knowledge/REGULATION_MAP.md`;
- `knowledge/COMMON_DECISION_PATHS.md`;
- repository search;
- official-source search.

Many questions depend on more than one regulation.

### Step 4 — determine the applicable edition

Check:

- effective date;
- amendment history;
- repeal date;
- transitional provisions;
- whether a newer regulation is published but not yet effective.

Distinguish current law, future published law and historical law.

### Step 5 — read provisions in context

Do not rely on an isolated sentence.

Check:

- scope/applicability;
- definitions;
- parent points and subpoints;
- exceptions;
- tables and table notes;
- appendices;
- cross-references;
- transition clauses.

When citing a table value, identify the relevant table, row/category, column and applicable notes.

### Step 6 — verify cross-references

If an STR refers to another STR, statute, hygiene norm, fire-safety rule, planning rule, Civil Code provision, special land-use condition or another act, inspect that source when it materially affects the result.

### Step 7 — answer clearly

Separate:

1. legal requirement;
2. exact source/reference;
3. practical interpretation;
4. exceptions/dependencies;
5. effective-date context.

Do not present an interpretation as if it were verbatim legislation.

## 6. Answer format

For substantive legal questions, prefer this order:

### Conclusion

Give the practical result first.

### Legal basis

State:
- STR / legal-act code and title;
- exact point/subpoint/table/appendix;
- official source.

### Relevant wording

Use a short direct quotation when it materially establishes the rule.

### Application

Explain how the provision maps to the user's facts.

### Exceptions / dependencies

Identify facts or other rules that could change the conclusion.

### Date

State the applicable edition/effective-date context when relevant.

Avoid burying the answer under a document dump.

## 7. Citation precision

Avoid vague references such as only naming the STR when a specific provision exists.

Prefer the exact:
- point;
- subpoint;
- appendix;
- table;
- row/category;
- note.

Do not quote a table cell without the context needed to know when it applies.

Keep direct quotations concise and use them only to establish the controlling rule.

## 8. STR is not the entire legal system

A construction question may also depend on:

- Statybos įstatymas;
- Teritorijų planavimo įstatymas;
- Specialiųjų žemės naudojimo sąlygų įstatymas;
- Civilinis kodeksas;
- fire-safety regulations;
- hygiene norms;
- cultural-heritage law;
- protected-area rules;
- municipal planning documents;
- detailed/general plans;
- land-use designation;
- servitudes;
- infrastructure protection zones.

If STR alone cannot establish the answer, research the other controlling source instead of forcing the question into an STR.

## 9. Important 2027 transition

**STR 2.02.12:2026 „Pastatai“** becomes effective on **2027-01-01**.

It replaces several older building-design STRs. Details are maintained in:

`knowledge/TRANSITIONS_2027.md`

For facts through 2026-12-31, do not prematurely apply STR 2.02.12:2026.

For facts from 2027-01-01 onward, check STR 2.02.12:2026 before relying on the legacy building-design regulations.

When the relevant date is ambiguous and the regimes differ, explain both.

## 10. Historical questions

For past events, research the law effective on the relevant date.

Do not automatically apply current rules retroactively.

Check:
- the applicable edition;
- amendments already in force on that date;
- transition provisions;
- repeals/replacements.

If historical text cannot be verified confidently, state the limitation.

## 11. Future-law questions

When a regulation is published but not yet effective:

- label it as future law;
- give its effective date;
- distinguish it from current requirements.

Never describe future law as already binding.

## 12. Uncertainty and interpretation

Do not guess legal requirements.

Distinguish:

- explicit legal rule;
- interpretation;
- administrative guidance;
- professional practice;
- unresolved or fact-dependent issue.

If a missing fact changes the answer, explain exactly which fact matters.

Do not turn common practice into a legal obligation without a source.

## 13. Check user assumptions

Treat proposed legal conclusions as hypotheses.

Common assumptions to verify include:

- the user has chosen the correct STR;
- a permit is automatically unnecessary;
- neighbour consent alone makes construction compliant;
- an old regulation is still current;
- a structure is non-complex merely because it is small;
- repair/reconstruction classification depends only on cost;
- a setback/distance is universally fixed.

Correct a faulty premise before building the rest of the answer around it.

## 14. Repository maintenance

The repository should improve through use, but persistence is a **quality-controlled step**, not an automatic dump of every conversation.

### 14.1 What should be persisted

Commit reusable findings such as:

- new/repealed/replaced STRs;
- effective-date changes;
- transition rules;
- important cross-references;
- recurring decision paths;
- corrected official URLs;
- normalized metadata;
- useful retrieval/checking tooling;
- durable interpretation notes that materially improve future research and are clearly identified as interpretation rather than legal text.

A finding is a good persistence candidate when it is likely to help future questions beyond the immediate user's facts.

### 14.2 Persistence gate

Before storing regulatory knowledge, verify that:

1. the finding is reusable rather than merely case-specific;
2. the controlling rule has been checked against the official-source hierarchy;
3. the relevant legal edition/effective date has been established;
4. material exceptions, transition rules and cross-references have been checked;
5. legal text, administrative guidance and interpretation are clearly distinguished;
6. the new information does not merely duplicate an existing repository entry;
7. the update makes future retrieval or reasoning materially better.

If a potentially useful finding is still uncertain, **do not promote it into authoritative project knowledge yet**. Continue research or preserve it only in a clearly marked non-authoritative research note if such a note is genuinely useful.

### 14.3 Provenance requirements

For new or materially changed regulatory knowledge, preserve enough context to allow another researcher or future AI session to independently re-check it.

Where applicable, record:

- **legal act** — number and title;
- **provision** — exact point, subpoint, appendix, table, row/category or note;
- **source URL** — preferably e-TAR, then e-Seimas, with VTPSI for index/guidance context;
- **source type** — legal text, amendment, consolidated text, administrative guidance, etc.;
- **legal status** — current, future, historical, repealed/replaced where relevant;
- **effective from** — date from which the rule applies;
- **effective to / repeal date** — when relevant;
- **verified on** — date the official source was checked;
- **knowledge type** — explicit legal rule, cross-reference, administrative guidance, interpretation, research path or tooling note;
- **scope/conditions** — the classification or factual conditions under which the finding applies;
- **transition/exception notes** — when they materially affect application.

Not every file needs a rigid metadata block. Use the structure appropriate to the file, but do not omit provenance merely because prose is easier to write.

### 14.4 Legal text vs interpretation

Persistent notes must make the distinction obvious:

- **Legal rule**: directly supported by the applicable legal text.
- **Administrative guidance**: an official authority's explanation or practice; useful but not equivalent to legislation.
- **Interpretation**: reasoned application or synthesis derived from legal sources.
- **Research path**: a reliable method for locating or checking the controlling rule.

Do not rewrite an interpretation so that it reads like statutory wording.

When an interpretation is important enough to persist, preserve the underlying legal references that support it and note material uncertainty.

### 14.5 What should not be persisted as project knowledge

Do not store as durable knowledge:

- unsupported speculation;
- unverified claims from secondary sources;
- one user's private or case-specific facts unless generalized into a reusable rule without personal detail;
- assumptions made only to answer an incomplete question;
- conclusions whose applicable legal edition was not established;
- model-generated summaries with no recoverable source;
- duplicate notes that add no retrieval value.

### 14.6 Updating existing knowledge

Prefer improving an existing canonical entry over creating competing fragments.

When information becomes obsolete:

- preserve useful effective-date/history context rather than silently erasing it;
- mark replaced or historical rules clearly;
- update cross-references and routing maps that would otherwise send future research to stale material.

When an official source contradicts repository content, **correct the repository** and preserve enough context to understand why the earlier entry changed.

### 14.7 Maintenance behavior during normal research

Do not require the user to explicitly ask for repository maintenance every time.

After substantive research, independently evaluate whether the result passes the persistence gate. If it does and repository write access is available, update the appropriate file as part of the research workflow.

Keep repository changes focused. A legal answer should not trigger broad refactoring unless the research actually exposes a structural problem.

Official sources always override repository notes.

### 14.8 Knowledge audit and refactoring

Repository maintenance has two distinct layers:

1. **Mechanical audit** — deterministic structural checks performed by `scripts/audit_knowledge.py`.
2. **Semantic/legal audit** — AI-assisted review governed by `maintenance/KNOWLEDGE_AUDIT.md`, with official-source verification for substantive legal changes.

Automatically invoke a **scoped** semantic audit during normal research when a material hygiene trigger is discovered, such as:

- a repository entry contradicts an official source;
- duplicate or competing canonical explanations exist;
- routing/cross-references are stale or repeatedly fail;
- several related findings should be consolidated;
- current, future and historical regimes have become ambiguous;
- an important regulation changes status or a transition becomes operative.

Do not turn ordinary question answering into continuous repository-wide refactoring. Use the smallest audit scope that materially improves future research.

A user may explicitly request a full audit at any time. A full audit follows `maintenance/KNOWLEDGE_AUDIT.md` and updates `maintenance/audit-state.json` when completed.

The GitHub workflow `.github/workflows/knowledge-audit.yml` runs the mechanical audit monthly and on manual dispatch. It is intentionally **non-mutating**: scheduled automation detects structural problems but does not autonomously rewrite substantive legal knowledge.

## 15. New-session procedure

For every new project session involving Lithuanian construction regulation:

1. read `AGENTS.md`;
2. follow its pointer to this guide when substantive research is required;
3. route the question using the catalog/knowledge maps;
4. verify currentness when relevant;
5. verify controlling provisions using official sources;
6. answer with exact references and effective-date context;
7. evaluate new findings against the Section 14 persistence gate;
8. update the repository when verified reusable knowledge would improve future research;
9. if a maintenance trigger is encountered, apply the scoped workflow in `maintenance/KNOWLEDGE_AUDIT.md`.

The repository tells you where to look and what has already been learned. The official legal sources determine what the law actually says.
