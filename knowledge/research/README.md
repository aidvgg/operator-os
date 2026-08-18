# knowledge/research

Distilled conclusions only. Not raw runs, not transcripts, not everything that was read.

## The split, and why it exists

| Where | What lives there | Lifespan |
|---|---|---|
| `outputs/research/` | The run: phase artifacts, the claim tables with URLs and verbatim passages, fetched source bodies, `STATE.md`. One directory per run slug. | As long as the run is being audited. Prunable after. |
| `knowledge/research/` | The one page a decision actually rests on: the conclusion, the claims it stands on with their tier and date, and what would overturn it. | Until it is superseded or goes stale. |

A run produces a lot of paper. Almost none of it is worth reading again. What is worth reading
again is the conclusion plus the handful of claims it balances on, because that is the only part
a future session needs in order to either use it or knock it down.

The rule that keeps the two apart: **a page arrives here only after the run's stress-test phase
and an explicit write-back sanction.** `skills/research-doctrine` holds no write licence into
`knowledge/` on purpose. Its decide-phase artifact carries a write-back plan (enumerated edits,
banners, tombstones, Stale-after lines); Sam sanctions it; the parent session executes it. A
conclusion that promotes itself is a conclusion nobody audited.

## What a page here must carry

1. **`**Stale after:** YYYY-MM-DD` with a word on why**, if any claim can rot. Web-sourced
   pricing, platform mechanics, vendor capability, eligibility rules: all perishable. `repo-doctor`
   flags an expired page so staleness announces itself. Re-verify or supersede, never just bump
   the date.
2. **The decision it feeds**, named in the first block. Research with no decision attached is
   reading, and reading does not belong in `knowledge/`.
3. **Source tiers carried through from the run.** P1 (primary or issuing authority), P2 (reputable
   secondary that cites its primary), P3 (blog, forum, aggregator, undated page). A claim keeps the
   tier it earned; nothing upgrades on the way here.
4. **A confidence number and a one-line basis on every load-bearing claim.** The claims the
   recommendation rests on, plus every number, date and named capability.
5. **"What would change this conclusion"**, written as things you could actually observe. A
   conclusion with no falsifier is a preference.
6. **The write-back that was executed**, so a reader can tell which curated files already moved.

**URLs and verbatim passages stay in the run artifact, not here.** This page carries the tier, the
as-of date and the basis. That is deliberate: a curated page that copies fifty URLs rots into a
link-checking chore, and the run directory is where an auditor goes anyway. If the run has been
pruned and the claim is being reused for something load-bearing, re-verify it rather than trusting
the tier label alone.

## Naming

`<topic>-<YYYY-MM-DD>.md`. The date is the day the conclusion was reached, not the day the file
was tidied. A research conclusion's age is the first thing a reader needs and the last thing
anyone remembers to state.

## Rules that bite in this directory

- **No numbers this directory owns.** A research page cites the owner file for any price
  (`knowledge/business/outbound-offer.md` for the productized offer, the client's roadmap for an
  engagement). Restate one here and you have made a second copy of a live number in the tree where
  people go looking for arguments.
- **Never delete a page that stopped being true.** Put a `**SUPERSEDED - see <path>**` banner at
  the top, or `**DEAD - <why>**` if nothing replaced it, and leave the reasoning in place. Half the
  value of an old scan is showing what you believed then and why it was wrong.
- **A conclusion the file cannot support gets demoted, not softened.** If the run capped a claim at
  low confidence, the conclusion says so out loud instead of rounding it up in the summary.

## What is here now

- `smb-ops-tooling-scan-2026-07-24.md` - what small and mid-size businesses already use for the
  problems Northwind Labs solves, and whether the offer should be framed as replacement or as
  glue. **Stale after 2027-09-01** (demo date).

*(Worked-example content. Delete the scan, keep the conventions above.)*
