# STR research protocol

This repository supports answers about Lithuanian statybos techniniai reglamentai (STR).

## Mandatory workflow for every substantive STR answer

1. **Identify the legal question and relevant date.** Do not assume today's edition applies to historical facts or future work.
2. **Locate candidate STRs** using `data/str-catalog.json` and `knowledge/REGULATION_MAP.md`.
3. **Check scope before requirements.** Read the regulation's purpose, applicability, definitions, exceptions and referenced documents.
4. **Verify the current consolidated text in an official source** (e-TAR / Teisės aktų registras or e-Seimas). The repository is an index, not the legal authority.
5. **Read the exact provision in context**, including parent point, subpoints, notes below tables, appendices and transition clauses.
6. **Cross-check referenced STRs / statutes** when the provision delegates a definition or requirement elsewhere.
7. Answer with:
   - STR code + title;
   - exact point/subpoint/appendix/table;
   - concise quotation of the controlling wording where useful;
   - practical interpretation separated from the quotation;
   - effective-date / edition note;
   - official-source link.
8. If official sources conflict with a cached/local note, **official source wins** and the repository must be updated.

## Source hierarchy

1. e-TAR / Teisės aktų registras
2. e-Seimas
3. VTPSI
4. Secondary databases only for discovery or cross-checking

Never present a secondary database as the sole authority for a legal requirement.

## Precision rules

- Never cite only a regulation title when a point number exists.
- Never quote a table cell without the table number, row context and applicable notes.
- Never collapse "may", "must", "prohibited", exceptions, or alternative conditions into the same meaning.
- Distinguish requirements for new construction, reconstruction, repair, change of use, and existing buildings.
- Distinguish building category, use/purpose, construction type, and land-plot constraints.
- If a value depends on dimensions, building group, fire class, use, location, protected area, cultural heritage status, or another trigger, state that trigger.
- When a rule is superseded on a future date, state both the current rule and the future rule if the user's date is ambiguous.

## Freshness gate

The baseline VTPSI index date is stored in `data/str-catalog.json`.

Before any answer where freshness matters:
- compare the live VTPSI page's **Atnaujinimo data** with the stored date;
- if newer, treat the catalog as stale;
- inspect additions/removals/title changes and affected official consolidated editions before answering.

## Known high-risk transition

`STR 2.02.12:2026 „Pastatai“` is published but becomes effective **2027-01-01**. Until then, the seven regulations marked `valid_until: 2026-12-31` in the catalog remain in force. Do not prematurely apply STR 2.02.12:2026 to 2026 situations.

## What counts as a good answer

A good answer is auditable: another engineer, architect, inspector or lawyer should be able to open the cited official text and reach the same conclusion from the cited clauses without guessing what was omitted.
