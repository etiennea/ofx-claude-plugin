---
name: file-statement
description: >-
  File a bank, custodian, or fund statement that is already in FamilyOFX:
  identify the holding, record the valuation or import lines, attach the
  document, and set the reminder for the next statement. Use when the user says
  "file this statement", "process the latest statements", or "update NAVs from
  the statements".
---

# File a statement

## Steps

1. **Find it.** Call `documents` with action `search`. Recent uploads come first. Read the document with action `read`; follow `nextStartLine` until done.
2. **Identify** the institution, account or fund, statement date, currency, and closing value. A custodian statement may list many lines.
3. **Match holdings.** Call `positions` with action `search` for each account or fund. Ask the user rather than guess when there is no clear match.
4. **Record values.**
   - Up to 20 lines: one `transactions_write` call per holding with action `create`, type `Point in Time Valuation`, the closing value, and the statement date (`DD/MM/YYYY`). Include shares and price when stated. Do not edit NAV directly on the holding.
   - More than 20 lines (a full custodian statement): extract the lines and send them in one `batch_import_from_document` call, so the user reviews them as one approval.
5. **Attach.** Call `documents_write` with action `attach` to link the statement to the holding.
6. **Next statement.** For periodic fund reports, call `calendar_events_write` with action `remind_next_statement`.
7. **Report** what was proposed, with approval links, and any lines you could not match.

## Do not

- Do not create a new holding from a statement unless the user confirms. Propose it with `positions_write` action `create` only after they agree.
- Do not record the same statement twice. Check `transactions` for a valuation on the same date first.
