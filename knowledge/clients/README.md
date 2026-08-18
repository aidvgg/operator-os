# knowledge/clients/ - per-client context

One folder per client, slug-named after the client: `acme-retail/`, `beacon-health/`. Two files
carry the load.

| File | Owns | Never holds |
|---|---|---|
| `README.md` | the front page: who they are, the relationship, contact and cadence, standing rules, status today | phase prices, technical detail |
| `roadmap.md` | the engagement: phases, scope, **prices**, technical state, open risks, live `**Due:**` lines | relationship narrative |

A client with no priced work yet has only a `README.md`. The roadmap appears the day there are
phases and a number, not before. `beacon-health/` is that case right now, and its README says so
in the first line rather than leaving a reader to infer it.

## The price rule

**A client price lives in that client's `roadmap.md` and nowhere else.** Not in `memory.md`, not in
a proposal note, not in an agent file, not in a logbook entry, not restated "for convenience" in
the client's own README. Every copy of a price is a line that will be wrong the first time the
price moves, and the copy is always the one that reaches the client.

What a satellite file may do instead: name the owner file and say the shape. "Phase 3 is proposed
and undecided, price in `knowledge/clients/acme-retail/roadmap.md`" is a pointer. "Phase 3 is
proposed at $X" is a second owner. `repo-doctor`'s `core-restatement` check enforces exactly this
on `knowledge/memory.md`'s client pointer region, where any currency figure at all is a finding.
Everywhere else it is discipline.

### The seam with invoicing, because it looks like a violation and is not

Two different facts sit next to each other:

- The **roadmap** owns what a phase costs.
- The **invoice ledger** owns what was billed on a given invoice, and when it was paid.

They agree today, in both demo clients. They are still separate facts with separate owners. They
come apart the moment a phase is billed across two invoices, or a credit is issued, or a deposit is
taken. When they disagree, the ledger is right about cash and the roadmap is right about scope, and
the disagreement gets one line in each file naming the other. Do not resolve it by copying one
number over the other.

### When a price changes

Same session, no exceptions:

1. Change it in the roadmap, in struck form so the supersession is visible: `~~<old>~~ <new>`
   plus one clause on what moved.
2. Grep the dead value repo-wide. Banner or strike every current-sounding hit.
3. Add the dead string to `ai/TOMBSTONES.md`.

`repo-doctor` then blocks that string from reappearing un-struck. This is not paperwork. A re-price
that is not rippled sits un-bannered in every file that quoted it, and every one of those is a
wrong number waiting to be read out loud.

## Contacts are roles, not names

Record "the ops lead", "the practice manager", "the owner who signs". Not a person's name.

Two reasons. A name goes stale the day that person changes jobs, and it goes stale silently, in
however many files quoted it. And a client folder that reads as a dossier on a named individual is
the wrong artifact to be handing to an agent on every run. What actually drives a decision is the
role, the decision path, and the reply pattern, and all three survive turnover.

If a name is genuinely load-bearing for you, it belongs in your contact manager, not here.

## What never goes in a client folder

- Credentials of any kind. API tokens, SFTP keys, database passwords, portal logins. Reference the
  entry by name in your password manager and stop there.
- Wire and bank details. Those live only in the local-only
  `knowledge/business/invoices/PAYMENT-DETAILS.md`.
- Client data. Records, exports, samples. If a scope needs real data to reason about, reason about
  its schema and its counts instead.
- Anything you would not want read aloud to that client. These files feed agents and briefs, and
  candour about a relationship is different from a note you would be embarrassed by.

## This folder is what simulates the client

`.claude/agents/client-sim.md` grounds entirely on `knowledge/clients/<slug>/`, plus
`knowledge/business/invoices/SUMMARY.md` for what is outstanding. It carries no persona of its own
by design, because a persona baked into an agent prompt has no banner, no tombstone and no review
date. It builds the persona at run time from these files.

The practical consequence: anything you want rehearsed has to be written down. Reply pattern, price
posture, payment cadence, technical depth, who actually signs. If an axis is missing, the agent is
instructed to say `not in the files` rather than invent, which is correct behaviour and also a
prompt to go fix the grounding.

## Adding a client

1. Create `knowledge/clients/<slug>/README.md`. Front page only. Who they are, the problem in their
   words, contact and cadence, standing rules, status today.
2. Add one pointer line to the client region of `knowledge/memory.md`. The folder name and one
   clause on stage. No figures.
3. The day work is priced, write `roadmap.md` beside it and let it own the numbers.
4. Bill through `knowledge/business/invoices/INVOICE-LEDGER.md`. Read the next number, never guess
   one.

Multiple engagements with one client: keep `roadmap.md` as the file the rest of the OS points at,
since skills and agents cite that exact filename, and give each additional engagement its own file
beside it, listed in a table at the top of the README. Each engagement file owns its own prices.

## When a client ends

Banner the folder's README with `**DEAD - <why>**` or `**SUPERSEDED - see <path>**` on the first
line, in the same session the decision is made. `repo-doctor`'s `dead-artifact-ref` check then flags
live-sounding references to it elsewhere in the repo. Do not delete the folder: a finished
engagement is the evidence base for the next proposal, and a deleted one takes its pricing history
with it.

## Demo content

`acme-retail/` and `beacon-health/` are the worked example. They are here so a fresh clone can run
`scripts/money`, `scripts/horizon`, `client-sim` and the proposal skill end to end on day one.
Delete both folders once your own clients are in, and keep this page.
