# Habit tracker - append-only per-day habit marks

> **Same discipline as the logbook.** Sam speaks or shows evidence, the acting agent writes. A day is marked only on their word or on evidence, never assumed and never inferred from a commit. Missed days stay blank or get a recorded miss; nothing is back-filled. Git is the audit trail. This is the *habit* layer beside the task logbook: `LOGBOOK.md` tracks the day's money-motion tasks, this file tracks the recurring reps that make those tasks possible.

## Rules

1. **Habits are operator-declared only.** The acting agent never adds, invents or recommends a habit onto this list. Same standing correction as tasks (daily-log hard rule 2). A habit somebody else picked for you is a chore, and chores do not survive a busy week.
2. **Mark on evidence or on Sam's word, same day.** No retroactive back-fill. An unmarked past day is a miss, permanently. The one allowance is the **day-after window**: if the question was asked at close and answered the next morning, the mark lands on their word with the answer date noted, which is different from inventing a mark from silence.
3. **Append-only.** Past rows are frozen. Superseded stats get ~~strikethrough~~, never deletion, so the counts stay auditable back to source rows through git.
4. **Counts, not fake streaks.** A streak is computed only for a habit Sam has declared *daily*. Everything else gets rolling 7-day and 30-day counts. A guilt-trip streak on a habit that was never meant to be daily is a number that lies.
5. **This file is read at `/plan` and written at `/eod`.** Any session may mark a habit the moment Sam reports it. That is this file's narrow sanctioned write, and it is the only one it has.

## Registry

| Habit | Declared | Definition of done | Cadence |
|---|---|---|---|
| `post` | 2026-07-20 | one post published on X or LinkedIn, live, not drafted | daily on workdays, streak computed |
| `outbound-5` | 2026-07-20 | five real conversations logged in a day, a reply that goes somewhere, not five sends | daily on workdays, streak computed |
| `deep-work` | 2026-07-20 | one uninterrupted 90-minute block, messages closed, one task only | daily on workdays, streak computed |
| `verify-timeline` | 2026-07-20 | every client-facing message that left today carried no date Sam had not personally checked | per event, count only, no streak |

`verify-timeline` is a discipline check rather than a rep, and it is on this list because the ruling behind it is settled in `ai/DECISIONS.md` and the failure behind that ruling is in `ai/ERRORS.md`. It is marked on days a client message actually went out, and left blank on days none did. Blank means "no event", not "missed".

## Marks (append-only, one row per day with activity)

Key: `y` marked done · `x` recorded miss · `-` not raised or no event that day.

| Date | DOW | post | outbound-5 | deep-work | verify-timeline | Note |
|---|---|---|---|---|---|---|
| 2026-07-20 | Mon | x | x | y | y | First day of the tracker. Phase 2 invoice message out, no dates in it. Outbound block ran late and produced 1 conversation. |
| 2026-07-21 | Tue | y | x | y | y | 1 post live (X). Marked at close on Sam's word after being written as a miss earlier that evening, see the correction note below. 2 conversations. |
| 2026-07-23 | Thu | x | x | x | y | The only deep-work miss in the record. Day went to a client fix and got sliced into fifteen-minute pieces. 1 conversation. |
| 2026-07-24 | Fri | y | x | y | - | **2 posts** in one day, the only doubled day so far. No client message went out, so `verify-timeline` has no event to judge. 3 conversations. |
| 2026-07-27 | Mon | x | x | y | y | 4 conversations, closest to the bar so far. Post missed on a day the block ran long. |
| 2026-07-28 | Tue | x | x | y | y | Phase 2 payment cleared, confirmation message out with no forward dates in it. 2 conversations. |
| 2026-07-29 | Wed | y | x | y | - | 1 post (X). 3 conversations. No client message left today, so `verify-timeline` has no event. |
| 2026-07-30 | Thu | y | x | y | y | 1 post (LinkedIn), and two of the day's four conversations came off it. Closest miss on `outbound-5` yet, 4 of 5. |
| 2026-07-31 | Fri | x | x | y | y | Post missed, ends a 2-day run. 3 conversations on a block that ran at 16:30. |
| 2026-08-01 | Sat | - | y | - | y | **`outbound-5` hit for the first time, 5 conversations**, on a weekend, on a block that ran first thing. `post` and `deep-work` not raised, weekend convention. Proposal sent, and the fact-check pulled an unverified three-week timeline out of it before it left, so `verify-timeline` reads y **because a gate caught it**, not because the draft never had it. Recorded that way on purpose. |

**Correction, 2026-07-21 row.** The row was first written with `post` as a miss and corrected the same evening when Sam confirmed the post was live. Corrections inside the day are normal. Corrections after the day are the thing rule 2 forbids, and the difference is a day, so it is worth being exact about which one this was.

**No row for 2026-07-22.** That workday is `SKIPPED` in `LOGBOOK.md`: no plan, no work, no habits raised. A blank row would imply four misses were recorded, and nothing was recorded, so the day gets no row at all and the counts below skip it.

## Stats (recomputed on each mark)

**`post`**, lifetime published: **5** (2026-07-21, 07-24 x2, 07-29, 07-30) · last 7d (Jul 26 to Aug 1): **2** · last 30d: **5** · current streak: **0**, broken by the Fri 07-31 miss · longest streak: **2** (07-29 to 07-30).
- Marked workdays: 4 hits, 5 misses, one skipped day with no row. That is a 44% hit rate on a habit declared daily.
- **Two posts against a weekly target of 5 in W31**, and the target is the one Sam set. The miss is named plainly in `reviews/2026-W31.md` rather than averaged away here.
- Both W31 posts landed midweek and both fed conversations the same day. Every content miss so far sits on a day the client lane ran past 17:00.

**`outbound-5`**, lifetime hits: **1** (2026-08-01) in 10 tracked days · last 7d: **1** · last 30d: **1** · current streak: **0** · longest streak: **0 workdays**.
- Read the shape honestly: **the only hit in the record sits on a weekend**, which is streak-neutral, so the workday streak has never started. Nine workdays have run the block and nine have come in under the bar, at 1, 2, 1, 3, 4, 2, 3, 4 and 3 conversations.
- Conversation totals themselves are in `STATS.md`, which owns the lifetime count and the gate progress. This file counts habit hits, not conversations, and does not restate that number.
- Nothing here says the bar is wrong. It says the bar has been hit once. If five is the wrong number, changing it is Sam's call and it gets recorded as a change, not as a quiet drift down to whatever happened.

**`deep-work`**, lifetime sessions: **8** · last 7d: **5** · last 30d: **8** · current streak: **6 workdays** (07-24 through 07-31, weekend carried through) · longest streak: **6**, the current one.
- One miss in the record, 2026-07-23, on the day a client fix cut the morning into pieces. It did not compound: Friday answered it.
- This is the healthiest habit on the list and it is also the least visible in the money numbers. Worth remembering when it becomes the first thing cut.

**`verify-timeline`**, client-facing days judged: **8** · slips that reached a client: **0** · caught pre-send: **1** (2026-08-01, an unverified three-week timeline pulled by the fact-check gate).
- No streak is claimed, per rule 4: this is per event, and the honest measure is slips, not consecutive days.
- **The one catch matters more than the eight clean days.** The draft carried the bad date and a fresh-context gate removed it. A working session that had been staring at the file all morning did not see it. That is the argument for keeping both gates mandatory, and it is why this row reads as a catch rather than a clean sheet.
