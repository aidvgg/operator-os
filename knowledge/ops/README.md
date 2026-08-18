# knowledge/ops/

The operating machinery the business runs on, as opposed to what it sells (`knowledge/business/`),
who it sells to (`knowledge/clients/`), or how it sounds (`knowledge/voice/`).

Three things live here.

`tools-and-stack.md` - the live tool stack and the **owner of the recurring cost lines**. Every
number that leaves the account each month is written once, in that file. `scripts/money` keeps a
hardcoded copy for its burn math and each entry there cites the file by name, so a cost change is
edited there first and mirrored second. It also holds the machine-side setup (document pipeline,
scheduled jobs, backup, secrets posture) and a dated log of reversible tool choices.

`os-roadmap.md` - the improvement direction for the OS itself, and the **owner of the
guardrail-fixture specification** that `CLAUDE.md`'s ratchet rule points at. It is a roadmap, not
a status claim: every item says plainly whether it is built or planned, and it arms no deadline by
itself.

`logbook/` - the daily operating ledger: plan, log, accountability, stats. Maintained only by
`skills/daily-log` through `/plan`, `/standup`, `/eod` and `/weekly`. `LOGBOOK.md` carries the
`LAST LOGGED` cursor and one append-only row per day, `STATS.md` is the recomputed rollup, `days/`
holds per-day detail, `reviews/` the weekly retros, `HABITS.md` the tracked set. This is the
accountability and stats layer, not a capture inbox: capture stays in the operator's task manager,
and the acting agent writes the logbook rather than the operator maintaining a second list by hand.

## What does not live here

- Prices. Client engagement prices live in that client's roadmap file under `knowledge/clients/`;
  the productized offer's price lives in `knowledge/business/outbound-offer.md`. One owner each,
  and this tree points at them rather than restating them.
- Rulings. A decision that must not be re-argued is a row in `ai/DECISIONS.md`. A reversible tool
  choice is a dated line in `tools-and-stack.md`. The difference is whether re-opening it is a
  waste of a session or an ordinary Tuesday.
- Cash. `knowledge/business/invoices/SUMMARY.md` is the sole cash authority. Ops owns the cost
  side only, and only the recurring part of it.

## Local-only by design

Personal and financial-rail material is deliberately absent from git. Tax paperwork, statements,
banking notes, issued invoices and anything carrying a live account value live in gitignored paths
(`personal/`, `outputs/ops/`, `outputs/invoices/`, and the wire block in
`knowledge/business/invoices/PAYMENT-DETAILS.md`, whose committed sibling is a placeholder
template). A shared clone must not carry any of it.

Committed files may **cite** those paths. They may never **restate** their contents: name the fact
class, not the counterparty, the identifier or the number. A pointer into a local-only path is
therefore expected to dangle on a fresh clone, and `repo-doctor` skips gitignored tokens in its
dead-pointer scan for exactly that reason.

Off-site coverage for the local-only set is `scripts/backup-sensitive`, described in
`tools-and-stack.md`. A file being absent from git is not the same as it being backed up.
