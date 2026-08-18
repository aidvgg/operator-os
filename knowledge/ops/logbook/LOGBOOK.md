# Daily logbook - single source of truth for the daily operating ledger

> **This file is the cursor plus the append-only record of the operator's days.** Any session, any model, any time, reads this file before running `/plan` or `/eod` and uses the date under **LAST LOGGED** to know where the sequence is. Append one row per day. Never overwrite a past row. A genuinely missed workday is `SKIPPED`, a force-majeure miss is `EXCUSED` (protocol 7 and 8 below). This is the mechanism that keeps the record honest across a hundred separate chats, and git is the audit trail.

> **Capture is NOT here.** Task capture lives in the operator's own inbox (task app, paper, whatever it already is). This logbook is the *accountability, stats and journal* layer on top: **Sam speaks, the acting agent writes.** Never let it become a second inbox that has to be hand-maintained.

## LAST LOGGED

```
2026-08-01 (Sat, W31), LOGGED (weekend, voluntary). Planned 4 effective / Done 4, 100%. Streak 7 workdays, unchanged: Saturday is an off-day, so it counts in days-logged and completion and is streak-neutral. 4 units: the Acme Phase 3 proposal generated to PDF and passed through pdf-check; the two mandatory gates run in fresh context (fact-check, price-attack) with one wording change taken from the price-attack; the proposal SENT on Sam's explicit go at 14:05; plus an unplanned outbound block, 5 conversations, which entered both sides of the count per the unplanned-work convention. Habits: deep-work not raised (weekend convention), outbound-5 hit for the first time in the record and marked. Detail: days/2026-08-01.md.

Previous: 2026-07-31 (Fri, W31), LOGGED. Planned 4 / Done 4, 100%. Streak 7 workdays. Beacon Health intake diagnostic finished and delivered, then invoiced as NL-2026-003 with the number taken off the ledger rather than guessed; the Acme Phase 3 proposal data assembled from the roadmap file; the outbound block ran, 3 conversations logged. Habits: deep-work marked (sixth consecutive workday), post missed which ends a 2-day run, outbound-5 missed at 3. Detail: days/2026-07-31.md.
```

*(After logging a day: rewrite this block for that date, append the row to the Entries table, recompute `STATS.md`. Nothing else advances the cursor.)*

*(Template note, delete with the demo rows: the record deliberately stops at Sat 2026-08-01 with Mon 2026-08-03 unlogged, so the first `/plan` you run on a fresh clone has real work to do. Either the day gets closed from what actually happened, or it gets a `SKIPPED` row and breaks the streak. Both are correct. Back-filling a plan to protect the number is the one thing that is not.)*

## Logging protocol (read before every /plan and /eod)

1. **Read this file.** The date the sequence is at is in the `LAST LOGGED` block above. Do not derive it any other way, and never recall it from conversation.
2. **One row per calendar day.** A day appears at most once in the Entries table. A weekend off-day needs no row at all; the DOW column keeps the gap unambiguous. A voluntarily logged weekend day gets a normal row (protocol 7), it just carries no streak credit.
3. **`/plan` (morning):** draft 3 to 6 motion-tagged tasks with Sam, write today's planned checklist into `days/YYYY-MM-DD.md` (always when tasks are mirrored to the calendar, so the event ids are recorded; otherwise the table row is enough), and insert the Entries row with `Done=0`, `Completion=-`, `Status=OPEN`.
4. **`/eod` (evening):** mark what shipped, move unfinished tasks to carried with their first-planned date and days-slipped, compute Planned / Done / Completion / Focus-by-motion, fill in the Entries row, set `Status=LOGGED`, advance `LAST LOGGED`, then **recompute `STATS.md`** from the full table. That is the one sanctioned write back into `knowledge/`.
5. **Never overwrite history.** A past day's numbers are frozen. If a workday was genuinely missed (could have worked, chose not to), add its row marked `SKIPPED` with Planned and Done blank. Do not back-fill a plan to save a streak. Git makes any back-fill visible, and the honesty case collapses the first time it is gamed.
6. **Focus hours are self-reported estimates**, not clocked. They are directional, for spotting the concentration pattern, not stopwatch time-tracking. An unreported figure is recorded as unreported, never estimated on the operator's behalf.
7. **Weekends are off-days.** Sat and Sun are not workdays: no row needed, never `SKIPPED`, and the streak carries Fri to Mon untouched. Planning or logging a weekend is allowed, and such a day counts in days-logged and completion but is **streak-neutral** (no credit, no break). A weekend day is a workday only if Sam declares it one **in advance**, recorded at declaration time in the prior day's file or that day's `/plan`. Never granted retroactively at `/eod`.
8. **Excused misses are streak-neutral.** A workday missed for a force-majeure reason (illness, travel or holiday, disaster, a birth or a death) gets a row marked `EXCUSED (<reason>)` with Planned and Done blank. Like a weekend it carries the streak through instead of breaking it, and it does **not** count in days-logged or completion, because no work happened. That is the one way it differs from a logged weekend day, which does count. Honesty guardrail: the reason comes from that enumerated set and is recorded at the time, never invented later to rescue a streak. A miss with no such reason is `SKIPPED` and still breaks the streak.

## Motion tags

Every task carries exactly one tag, so the focus split is computed rather than guessed. The tag set is closed on purpose: five buckets fit in the head, and a sixth would be a category nobody reads.

- `[client]` - paid client delivery: builds, calls, deliverables, client messages
- `[outbound]` - sourcing, sends, conversations, prospect briefs (the controllable input)
- `[content]` - X and LinkedIn posts, the content engine that feeds outbound
- `[retainer]` - the productized offer: packaging, the one-pager, retainer conversations
- `[ops]` - entity, tooling, backups, admin, the OS itself

## Entries (append-only, one row per day)

| Date | DOW | Wk | Planned | Done | Completion | Focus h | Top motion | Status |
|---|---|---|--:|--:|--:|--:|---|---|
| 2026-07-20 | Mon | W30 | 5 | 4 | 80% | ~6 | client | LOGGED |
| 2026-07-21 | Tue | W30 | 4 | 3 | 75% | ~5.5 | client | LOGGED |
| 2026-07-22 | Wed | W30 | - | - | - | - | - | SKIPPED |
| 2026-07-23 | Thu | W30 | 4 | 2 | 50% | ~4 | client | LOGGED |
| 2026-07-24 | Fri | W30 | 5 | 4 | 80% | ~6 | outbound | LOGGED |
| 2026-07-27 | Mon | W31 | 5 | 3 | 60% | ~6 | outbound | LOGGED |
| 2026-07-28 | Tue | W31 | 4 | 4 | 100% | ~6.5 | client | LOGGED |
| 2026-07-29 | Wed | W31 | 4 | 2 | 50% | ~5 | outbound | LOGGED |
| 2026-07-30 | Thu | W31 | 5 | 4 | 80% | ~6 | client | LOGGED |
| 2026-07-31 | Fri | W31 | 4 | 4 | 100% | ~6 | client | LOGGED |
| 2026-08-01 | Sat | W31 | 4 | 4 | 100% | ~3.5 | client | LOGGED (weekend, voluntary) |

**Row notes (kept here so the table stays readable):**

- **2026-07-22 `SKIPPED`.** A workday with no plan and no work, and no force-majeure reason. It breaks the streak visibly, which is the point. The prior run ended at 2 workdays and the current one starts 07-23.
- **2026-08-01 reads 4 planned, and only 3 were planned.** The outbound block was unplanned and shipped, so it entered **both** the numerator and the denominator per the unplanned-work convention. Unplanned work is not free credit and it is not invisible. The denominator moves with the real contract, and it is never back-dated to flatter the rate.
- A day whose plan opened after most of the work had already happened gets `-` in Planned and `n/a` in Completion, and is excluded from both sides of every completion figure. No such day exists in this record yet.
