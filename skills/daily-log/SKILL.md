---
name: daily-log
description: "Canonical workflow for the operator's daily logbook: plan the day, stand up, log the day end to end, and roll up a weekly retro. Provider discovery aliases and capability fallbacks are owned by ai/AGENT_ROUTES.json. Reads the cursor from knowledge/ops/logbook/LOGBOOK.md, appends one row per day, recomputes STATS.md, and speaks a plain-text accountability diff. The operator speaks; the acting agent writes. This is not a capture inbox."
---

# Daily operating logbook

Maintains a plain-markdown daily ledger that gives the operator the three things a task app cannot: a per-day saved journal, plan-vs-done accountability, and task statistics. Modeled exactly on the invoice machinery. `LOGBOOK.md` is the cursor plus the append-only table (the `INVOICE-LEDGER.md` analog), `STATS.md` is the recomputed rollup (the `SUMMARY.md` analog).

## Discovery and capabilities

Before dispatching a mode, read this skill's entry in `ai/AGENT_ROUTES.json`. That registry is the single owner of natural-language aliases, structured first-turn actions, required and optional capabilities, and structured fallback actions when a runtime has no calendar or repository-write tool. Generated provider entrypoints point to this file and project those action ids into fixed instructions; they do not own workflow procedure.

## Hard rules

1. **The cursor comes from the ledger.** `knowledge/ops/logbook/LOGBOOK.md` is the single source of truth for where the day sequence is. Read it first; use the `LAST LOGGED` date. Never recall it from conversation.
2. **The operator speaks, the acting agent writes.** This is the accountability and stats layer, never a capture surface. Capture stays in the operator's own task inbox (the layered-stack ruling is in `ai/DECISIONS.md`). Do not let this become a second inbox. **Never add, invent, or recommend net-new tasks onto the day's list** - only the tasks the operator states plus carried items go on the contract. Surfacing live context (open loops, the #1 risk, what is stale) is the job; populating the list with your own ideas is not. This is a standing correction, not a preference: an agent that seeds the list turns an accountability record into a wish list, and the plan-vs-done number stops meaning anything.
3. **Sanctioned-write licence (narrow):** this skill may write to exactly five paths and nothing else in `knowledge/`: `knowledge/ops/logbook/LOGBOOK.md`, `knowledge/ops/logbook/STATS.md`, `knowledge/ops/logbook/days/YYYY-MM-DD.md`, `knowledge/ops/logbook/reviews/YYYY-Www.md`, `knowledge/ops/logbook/HABITS.md` (the habit tracker; habits are operator-declared only, marked on their word or evidence the moment they report it, in any session, and the rules live in that file's header).
4. **Never overwrite history.** Past rows are frozen; a genuinely missed workday is `SKIPPED`, never back-filled. Do not game the streak. A force-majeure miss (illness, travel or holiday, disaster, a birth or a death) is `EXCUSED` instead: streak-neutral, reason recorded at the time, excluded from days-logged and completion. The full spec lives in `LOGBOOK.md` and `STATS.md`.
5. **Voice:** all spoken accountability output is plain text, no markdown, no justifying language, USD for any money. Never invent a deadline the operator has not verified.
6. **Weekends are off-days.** Sat and Sun are not workdays. Planning or logging on a weekend is allowed but optional; a logged weekend day counts in days-logged and completion stats but is **streak-neutral**, so it neither extends nor breaks the streak, which carries Fri to Mon. A weekend with no plan needs no row (never `SKIPPED`). A weekend day gets full workday status (streak credit, `SKIPPED` on a miss) only if the operator declares it a workday **in advance**. Record the declaration where it lands (the prior day's file, or the weekend day's `/plan`); never grant it retroactively at `/eod`.

## Commands

### `/plan` (morning) - the only-light write

0. **Close the previous OPEN day before planning a new one.** If the last row in `LOGBOOK.md` is still `Status=OPEN` and its date is in the past, run `/eod` for that day first, from its day file, the working tree and the operator's answers. Two OPEN rows make the cursor ambiguous, and a day closed days later from memory is a guess dressed as a record.
1. Read `LOGBOOK.md` (cursor), `STATS.md` (open loops and carried items), `HABITS.md` (habit status), and the `Current state` section of `knowledge/memory.md` (what is live: the client builds, the outbound gate, content). Run `scripts/horizon` (full) and put any OVERDUE or items due within 3 days in front of the operator. Horizon informs, it never auto-adds tasks (hard rule 2 still holds). When the runtime has calendar-read capability, pull today's calendar to see what is already booked and to anchor block times. When it does not, apply the registry fallback and continue planning.
   - **Follow the core's ownership pointers.** `knowledge/memory.md` carries **pointers, not state**, so its `Current state` section is where a lane's owner file is *named*, never where its numbers live. For every lane on today's contract, open that owner file and read it **before speaking or writing any number for that lane** (outbound -> `knowledge/business/outbound-offer.md`; clients -> `knowledge/clients/<client>/roadmap.md`; money -> `knowledge/business/invoices/SUMMARY.md`). This is not theory: a compression once moved a lane's state out of `memory.md` while this file's read list still named only `memory.md`, and the next close spoke two numbers the owner file had already resolved. **An owner file may also delegate work here explicitly** - a line like "the `STATS.md` closure rides the next daily-log pass" is an instruction, so read owner files for instructions, not just for figures.
   - **Prefer a generated number over a relayed one.** Where a script produces a lane's count, run the script: `scripts/horizon` for commitments, `scripts/money` for the money lane, and the read-only fetch scripts (`scripts/x-fetch`, `scripts/li-fetch`, `scripts/reddit-scan`) for anything sourced off-platform. Those scripts are read-only by construction, which is the point: a tool that only downloads cannot damage the thing it reads. A number someone read off a dashboard and relayed into chat is the one that drifts. The ownership rule above still binds: the owner file owns the lane's state and any narrative claim, the script owns only what it counted today, and a partial read is reported as partial rather than implied clean.
   - **Reconcile the working tree too: `git status --porcelain outputs/ knowledge/`.** This is the other half, and it catches a different failure: the pointer read finds committed state, this finds work that was never committed. Read every untracked or unstaged artifact belonging to a lane the logbook counts, and reconcile it against yesterday's close before speaking or writing any number. The operator runs parallel per-engagement chats, so **cross-lane work sitting uncommitted is the expected state, not an anomaly**; a close that reads only the logbook's own files will call a lane zero while its output sits right there in the tree. Reconciling is reading and correcting, never committing another lane's work into a foreign commit.
2. With the operator, draft **3 to 6 tasks**, each with a motion tag and a rough focus-hour estimate. Pull carried items from `STATS.md` first so they do not get dropped. **A carried item is a claim to verify, not state:** before it goes on the contract, check its premise against the owner file or artifact it cites. `STATS.md` restates, the topic files own, and carried lines have ridden onto the calendar already dead because nobody re-read the owner file that had resolved them. **The list is the operator's tasks plus carried items plus standing declared contracts only. Never seed it with tasks they did not state** (hard rule 2).
   - **Standing declared contracts carry automatically.** Where the operator has declared a recurring daily commitment, it goes on every workday's list without asking, and **that is not a rule-2 violation**: rule 2 bars the acting agent's *own* invented tasks, not the operator's standing ones. The live contract, its item list and its weekday rule are owned by `knowledge/memory.md`, with the ruling row in `ai/DECISIONS.md`. **Read the items there, do not carry a copy here.** This file used to restate them, which made it a third copy of an owned state fact sitting inside the skill that consumes it. The operator can suspend or amend the contract any day; the acting agent never quietly drops it.
3. **Sync the calendar when the capability exists, both ways.** Push out: mirror each planned task to the calendar as a time-blocked event, prefix the summary with the motion tag, colour by motion (`[client]`=7 Peacock, `[outbound]`=10 Basil, `[content]`=6 Tangerine, `[retainer]`=9 Blueberry, `[ops]`=8 Graphite), description `daily-log · [tag] · <carried or slip note>`. Pull in: read today's existing events first and anchor the blocks around the fixed ones (calls, appointments, anything external), and put an external meeting the operator did not mention in front of them rather than double-booking over it. Record each created event id in the day file's `## Calendar (synced)` section so `/eod` can reconcile. The write direction stays one-way: the acting agent writes tasks to the calendar, never types calendar items back into the logbook as tasks. If calendar or repository-write capability is absent, apply the registry fallback without blocking the plan.
4. Write today's planned checklist into `days/YYYY-MM-DD.md` (always create it when tasks are synced to the calendar, so the event ids are recorded; otherwise the table row alone is fine).
5. Insert the Entries row in `LOGBOOK.md`: `Done=0`, `Completion=-`, `Status=OPEN`.

### `/standup` (anytime) - read and nudge, NO writes

- Surface what is still `OPEN` today and every carried item by name with its days-slipped. Optionally name the next calendar item. Pure read; never writes.

### `/eod` (evening) - the real ritual, the one sanctioned write

1. **Open by re-running both `/plan` step 1 reconciles: the owner-file pointer read and `git status --porcelain outputs/ knowledge/`.** A lane's owner file may have moved on since the morning, and it is the authority on that lane's numbers. Then read every untracked or unstaged artifact belonging to a lane this file counts. A day's real output includes what parallel chats shipped and left uncommitted; a close that reads only the logbook's own files will under-count the day and speak a wrong number. Then walk today's planned tasks and mark each done or carried. Carried tasks keep their **first-planned date** and accrue **days-slipped**. Ask about any unmarked habit in `HABITS.md` and mark it (done, or left blank) on the operator's answer.
2. Compute: Planned, Done, Completion% (`done/planned`), focus hours split across the five motion buckets, top motion.
3. Update today's Entries row in `LOGBOOK.md`, set `Status=LOGGED`, advance `LAST LOGGED`.
4. **Recompute `STATS.md`** from the full Entries table (see the spec below). Create it on the first `/eod`. **Re-base the carry-over bucket against the owner files step 1 read:** a loop an owner file has resolved, struck, or declared dead does not carry forward as written. Strike it with the resolution in the same close, and put the status banner (`**DEAD - <why>**`) on the dead artifact itself so `repo-doctor`'s `dead-artifact-ref` check catches any pointer that survives. An un-re-based carry line will otherwise outlive its owner file's resolution by days and put a dead draft on the calendar as a live client task.
5. **Speak the accountability diff** in plain text. See Accountability below.

### `/weekly` (end of ISO week) - retro rollup

With no arguments, use the ISO week that just closed.

1. **Pull the business state (if the tooling exists):** run `scripts/horizon` (full mode) and `scripts/money`; read the `ai/DECISIONS.md` rows whose `Review on` date falls in or before this week; note any repo-doctor soft warnings and the `.backup-marker` age. Name every due decision row with a blank or pending Outcome, and its age in days. If this week's commits make an outcome knowable, say so and write the outcome into that row instead of carrying it another week. Skip cleanly any tool that is not built yet.
2. Read the last 7 rows plus any `days/` detail files, then write `reviews/YYYY-Www.md`: plan-vs-done, completion trend against the prior week, focus-by-motion split, the diversification rep count, carried-forward items, and the one pattern worth changing. Missing weekdays count as `SKIPPED`, never assumed-done; missing weekend rows are off-days, not skips (hard rule 6).
3. **Append a 5-line `## State of the business` block** to the weekly note, from step 1. Omit a line only if its source tool is not built yet.
   - **Overdue** - count of horizon OVERDUE items, the single worst one by name, and horizon's CHRONIC block. Anything chronic for a third consecutive weekly review is a capacity problem: say that plainly and propose retiring or re-scoping the commitment.
   - **Pipeline** - open proposals awaiting a client decision (count plus names).
   - **Money** - collected and outstanding delta against last week's `MONEY.md`.
   - **Decision reviews** - `DECISIONS.md` rows due this week that are still Outcome-blank.
   - **Risk** - one line: the single biggest live risk this week (concentration, a payment-rail problem, a slipping tripwire).
   Plain derived numbers, no charts, USD for money. Same discipline as `STATS.md`.
4. Report the retro path and the five State-of-the-business lines in plain text, no markdown.

## STATS.md spec (recomputed every `/eod`)

Short markdown, pure derived numbers, no charts. A header line of headline figures, then sections as bullet lists. Superseded numbers get strikethrough, never deletion, so the streak math stays auditable back to source rows through git. Keep it a **separate** file from `LOGBOOK.md` (the cursor stays tiny and authoritative, the rollup stays richly derived), which is the exact ledger-versus-SUMMARY split the invoices use.

Fields:
- **Days logged** (lifetime), **current streak**, **longest streak**, counted in **workdays** (consecutive non-`SKIPPED` Mon to Fri days, plus any weekend day the operator declared a workday in advance). Weekends are transparent: streak-neutral, carried through (hard rule 6).
- **Lifetime** planned, done, completion rate.
- **7-day** and **30-day** rolling completion %, the trend that matters more than the lifetime number.
- **Focus hours by motion**, last 7d and last 30d, the diversification lens. A month that is almost all `[client]` and almost no `[outbound]` or `[content]` mirrors the top-client concentration risk in *hours*, and `knowledge/memory.md` names that concentration as the #1 business risk.
- **Diversification rep count, last 7d** (outbound connects, calls held, content posts), the single number tracking whether rebalancing is actually happening.
- **Outbound gate progress:** calls held, closes, and proposals advanced, measured against the kill-or-go threshold. Read that threshold from `knowledge/business/outbound-offer.md`; never restate it here, because a second copy of a live threshold is a stale line waiting to happen.
- **Carry-over bucket:** every still-unfinished task with its first-planned date and days-slipped. This is the open-loops list `/plan` and `/standup` read from.

No revenue and no reply counts here. Those live in `knowledge/business/invoices/SUMMARY.md` and the outbound files. The logbook tracks controllable *inputs* only, the reps-versus-replies doctrine, and links out rather than duplicating.

## Accountability mechanic

At `/eod`, a plain-text plan-vs-done diff that bites because it is tied to the operator's own goals, not to generic nagging:
1. Name the specific carried task and exactly how many days it has slipped (git plus the table make slippage undeniable).
2. Connect a slip to the #1 risk `knowledge/memory.md` names, or to the outbound kill-or-go gate when relevant. Read the risk from that file rather than naming one here; a second copy of a live risk is a stale line waiting to happen, the same reason the gate threshold above is read and not restated. Accountability against their goals, not against a checkbox.
3. Flag controllable-input droughts (consecutive zero-outbound or zero-content days), the reps they control and keep deferring.

The streak is the only gamified element and it is honest: skipped workdays break it visibly in git, and weekends are neutral (hard rule 6). State it and move on. Never apologise for the work, never pad.

## What this skill does NOT do (deferred, do not pre-build)

- No Node generator, no rollup script. Appends and rollups are direct markdown edits. Add a script only if hand-recompute actually drifts, which mirrors how the invoice ledger was born out of a real numbering bug.
- No cron or scheduled agent in v1. Arm proactive morning and evening pings only after the manual loop has stuck for about two weeks. Validate, then automate.
- **The calendar mirror is ON wherever the runtime has calendar capability**, on the terms in `/plan` step 3: planned tasks are pushed out as blocks, external events are pulled in to anchor the day, and repo markdown stays authoritative because the calendar is a projection of it.
- A second mirror into a notes or wiki app stays deferred. One projection is a convenience; two are a sync problem.
