# Daily logbook - single source of truth for the daily operating ledger

> **This file is the cursor plus the append-only record of the operator's days.** Any session, any model, any time, reads this file before running `/plan` or `/eod` and uses the date under **LAST LOGGED** to know where the sequence is. Append one row per day. Never overwrite a past row. A genuinely missed workday is `SKIPPED`, a force-majeure miss is `EXCUSED` (protocol 7 and 8 below). Git is the audit trail.

> **Capture is NOT here.** Task capture lives in the operator's own inbox (task app, paper, whatever it already is). This logbook is the *accountability, stats and journal* layer on top: **{{FIRST_NAME}} speaks, the acting agent writes.** Never let it become a second inbox.

## LAST LOGGED

```
No day logged yet. Logbook opened {{TODAY}}. The first /plan you run opens the first row.
```

*(After logging a day: rewrite this block for that date, append the row to the Entries table, recompute `STATS.md`. Nothing else advances the cursor.)*

## Logging protocol (read before every /plan and /eod)

1. **Read this file.** The date the sequence is at is in the `LAST LOGGED` block above. Do not derive it any other way, and never recall it from conversation.
2. **One row per calendar day.** A day appears at most once in the Entries table. A weekend off-day needs no row at all.
3. **`/plan` (morning):** draft 3 to 6 motion-tagged tasks with {{FIRST_NAME}}, write today's planned checklist into `days/YYYY-MM-DD.md` when tasks are mirrored to the calendar, and insert the Entries row with `Done=0`, `Completion=-`, `Status=OPEN`.
4. **`/eod` (evening):** mark what shipped, move unfinished tasks to carried with their first-planned date and days-slipped, compute Planned / Done / Completion / Focus-by-motion, fill in the Entries row, set `Status=LOGGED`, advance `LAST LOGGED`, then **recompute `STATS.md`** from the full table.
5. **Never overwrite history.** A past day's numbers are frozen. A genuinely missed workday gets its row marked `SKIPPED` with Planned and Done blank. Do not back-fill a plan to save a streak.
6. **Focus hours are self-reported estimates**, not clocked. An unreported figure is recorded as unreported, never estimated on the operator's behalf.
7. **Weekends are off-days.** Sat and Sun are not workdays: no row needed, never `SKIPPED`, and the streak carries Fri to Mon untouched. A logged weekend day counts in days-logged and completion but is streak-neutral. A weekend day is a workday only if {{FIRST_NAME}} declares it one **in advance**.
8. **Excused misses are streak-neutral.** A workday missed for a force-majeure reason (illness, travel or holiday, disaster, a birth or a death) gets a row marked `EXCUSED (<reason>)` with Planned and Done blank. It does not count in days-logged or completion. The reason is recorded at the time, never invented later.

## Motion tags

Every task carries exactly one tag, so the focus split is computed rather than guessed. The tag set is closed on purpose.

- `[client]` - paid client delivery: builds, calls, deliverables, client messages
- `[outbound]` - sourcing, sends, conversations, prospect briefs
- `[content]` - posts and other content that feeds outbound
- `[retainer]` - the standard or productized offer: packaging, the one-pager, retainer conversations
- `[ops]` - entity, tooling, backups, admin, the OS itself

## Entries (append-only, one row per day)

| Date | DOW | Wk | Planned | Done | Completion | Focus h | Top motion | Status |
|---|---|---|--:|--:|--:|--:|---|---|
