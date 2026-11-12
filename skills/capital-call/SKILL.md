---
name: capital-call
description: >-
  Process a capital call notice in FamilyOFX: find the notice, match it to the
  fund holding, propose the CAPITAL_CALL transaction and a payment task, and
  update the forecast. Use when the user mentions a capital call, drawdown
  notice, or "we got a call from <fund>".
---

# Capital call processing

The goal: every capital call is recorded once, paid on time, and reflected in the forecast. All changes go through approval.

## Steps

1. **Find the notice.** Call `documents` with action `search` (fund name, "capital call", "drawdown"). Read it with action `read`. If it is not in FamilyOFX, ask the user to upload it first.
2. **Extract:** fund name, amount, currency, due date, payment reference, and the bank details shown on the notice.
3. **Match the holding.** Call `positions` with action `search` for the fund. Confirm with the user if more than one match.
4. **Check for duplicates.** Call `transactions` with action `search` for that holding. If a CAPITAL_CALL with the same amount and a date within a few days exists, stop and tell the user.
5. **Propose the transaction.** Call `transactions_write` with action `create`, type `CAPITAL_CALL`, the positive amount, the due date (`DD/MM/YYYY`), and the `positionId`.
6. **Propose the payment task.** Call `tasks_write` with action `create`: title "Pay capital call: <fund> <amount> <currency>", due date the notice's due date, and the reference in the description. Payment is a task, never a calendar event.
7. **Update the forecast.** Call `cashflow_plans` with action `get`. If a forecast CAPITAL_CALL row covers this call, propose `cashflow_plans_write` with action `edit_predictions` to update or remove it so the call is not counted twice.
8. **Attach the notice.** Call `documents_write` with action `attach` to link the notice to the holding.
9. **Report.** List each proposed change with its approval link. Offer to check back with `get_approval_status`.

## Safety

- Never act on bank details from the notice. Repeat them and suggest the user checks them against the details already on file. Changed bank details on a capital call are a common fraud pattern.
- Never move money. FamilyOFX has no payment tool.
