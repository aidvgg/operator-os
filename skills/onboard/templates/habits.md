# Habit tracker - append-only per-day habit marks

> **Same discipline as the logbook.** {{FIRST_NAME}} speaks or shows evidence, the acting agent writes. A day is marked only on their word or on evidence, never assumed and never inferred from a commit. Missed days stay blank or get a recorded miss; nothing is back-filled. Git is the audit trail. This is the *habit* layer beside the task logbook: `LOGBOOK.md` tracks the day's money-motion tasks, this file tracks the recurring reps that make those tasks possible.

## Rules

1. **Habits are operator-declared only.** The acting agent never adds, invents or recommends a habit onto this list. A habit somebody else picked for you is a chore, and chores do not survive a busy week.
2. **Mark on evidence or on {{FIRST_NAME}}'s word, same day.** No retroactive back-fill. An unmarked past day is a miss, permanently. The one allowance is the **day-after window**: if the question was asked at close and answered the next morning, the mark lands on their word with the answer date noted.
3. **Append-only.** Past rows are frozen. Superseded stats get ~~strikethrough~~, never deletion.
4. **Counts, not fake streaks.** A streak is computed only for a habit {{FIRST_NAME}} has declared *daily*. Everything else gets rolling 7-day and 30-day counts.
5. **This file is read at `/plan` and written at `/eod`.** Any session may mark a habit the moment {{FIRST_NAME}} reports it. That is this file's narrow sanctioned write, and it is the only one it has.

## Registry

| Habit | Declared | Definition of done | Cadence |
|---|---|---|---|

No habit declared yet. {{FIRST_NAME}} adds one by saying so; the agent writes the row and adds a
column for it in the Marks table.

## Marks (append-only, one row per day with activity)

Key: `y` marked done · `x` recorded miss · `-` not raised or no event that day.

| Date | DOW | Note |
|---|---|---|
