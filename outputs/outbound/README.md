# outputs/outbound/

Everything the outbound motion produces except the offer itself and the message copy, both of
which live under `knowledge/` and `templates/`.

**Layout:**

- `prospect-gate.md` - **the owner of the qualification rules.** Who is in the corridor, the hard
  kills, the scored tells, the ladder, and the verdict vocabulary at each of the three moments.
  `skills/prospect-brief` applies it and never restates or invents a rule.
- `briefs/<slug>-<YYYY-MM-DD>.md` - one decision-ready brief per prospect: who they are, the gate
  walked in order with the evidence for every tell, a pain-bank match, and opener prep.
- Batch triage files - a run of profiles with per-prospect verdicts. These hold verdicts, never
  rules. If a triage file starts explaining a rule, the rule has two owners and one of them is
  already wrong.

## What does not live here

| Thing | Owner |
|---|---|
| The offer, its price, the qualification bar, the copy freeze flag | `knowledge/business/outbound-offer.md` |
| The actual message wording | `templates/message-templates.md` |
| Sending limits and platform-safety envelope | `knowledge/business/linkedin-safety-rules.md` |
| The pains you lead with | `knowledge/pain-points/pain-point-bank.md` |
| What counts as a conversation, and the gate it counts toward | `knowledge/business/outbound-offer.md` |
| The running count of conversations had | `knowledge/ops/logbook/` |

## Two standing rules

**Nothing in this folder sends anything.** `skills/prospect-brief` writes briefs and prepares
copy. The operator sends, by hand, on that specific message. That is item 7 of the pre-send
checklist and no clean set of checks replaces it.

**No agent writes into an external tracker.** Outreach trackers, CRMs and sheets that live outside
this repo are the operator's to update by hand. An agent that inherited the wrong working
directory once rebuilt a live tracker file from a stale source and destroyed it, and the read rail
has stayed read-only since.

Paste blocks in this folder are scanned for banned dashes by `repo-doctor`, same as
`outputs/content/`. Filled outbound copy belongs in a fence so the check can see it.
