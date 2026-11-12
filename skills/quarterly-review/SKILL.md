---
name: quarterly-review
description: >-
  Prepare a family office quarterly or annual review from FamilyOFX: NAV and
  allocation, splits by entity and asset type, cash flows in the period, open
  commitments, and open tasks. Use when the user asks for a quarterly review,
  portfolio review, board pack, or "how did the office do this quarter".
---

# Quarterly review from FamilyOFX

Produce a review the principal can read in five minutes. Use only FamilyOFX data; say plainly when something is missing.

## Steps

1. **Period.** Agree the period. Default: the last full calendar quarter. Use `YYYY-MM-DD` dates.
2. **Position today.** Call `get_portfolio_summary`. Note `asOf`, the consolidated NAV, and the currency.
3. **Where the money sits.** Call `portfolio_analytics` with `view: breakdown` for `groupBy: legal_entity`, then `position_type`, then `currency`. Each set of groups adds up to the consolidated NAV.
4. **What moved.** Call `portfolio_analytics` with `view: cash_flows`, `interval: month`, and the period. Group the rows into money out (capital calls, buys) and money in (distributions, dividends, sells). Keep currencies separate.
5. **Private markets.** Use `positions` with action `top` and the summary's commitments to list funds with open commitments. For the two or three largest, call `cashflow_plans` with action `get` to show expected calls in the next quarter.
6. **Open items.** Call `tasks` with action `list` and keep tasks that are open or due in the next 30 days.
7. **Write the review:**
   - One paragraph: NAV, change drivers you can see in the data, anything unusual.
   - Tables: allocation by asset type and by entity (value and %), cash flows by month.
   - Upcoming: expected capital calls and due tasks.
   - Data gaps: holdings with no recent valuation, missing currency rates, or anything the tools did not return.
8. **Links.** Include record `url`s for any holding or task you name.

## Do not

- Do not compute a performance return. FamilyOFX stores valuations and flows; it does not return an IRR or TWR here. Say so if asked.
- Do not convert currencies yourself. Use the organisation-currency values the tools return.
- Do not create tasks unless the user asks. If they do, use `tasks_write` and give them the approval link.
