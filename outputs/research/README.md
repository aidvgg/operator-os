# outputs/research/

Research runs. One folder per question, produced by `skills/research-doctrine` for anything a
decision will rest on. A quick lookup does not need a folder. A question whose answer will change
what you charge, who you sell to, or what you build does.

**Layout: `outputs/research/<slug>/`**

- `STATE.md` - which phase the run is in and what is still open. Written first, updated every phase.
- `phase-<letter>-<YYYY-MM-DD>.md` - one artifact per phase, appended, never overwritten. The
  phases exist so gathering, verifying and deciding cannot silently blur into each other.
- `sources/` - what was actually fetched, so a claim can be re-checked without re-running the web.
- `local/` - **gitignored.** Fetched pages routinely carry public contact phone numbers, which trip
  `repo-doctor`'s secrets check and block the commit. That is the check working. Redact them in the
  committed copy with a `[REDACTED-PUBLIC-PHONE]` marker and keep the unredacted values here. The
  committed report cites this path; the live URL stays the authority.

## Rules that make a run worth re-reading

- **Label every claim with its source tier.** P1 primary, P2 credible secondary, P3 weak or
  single-source. An unlabeled claim is an opinion wearing a citation's clothes.
- **The citation audit runs before the decide phase, always.** Deciding first and auditing after is
  how a run reaches the conclusion it started with.
- **A research run has no `knowledge/` write licence.** The decide phase emits a write-back plan
  listing the edits the findings imply. The operator sanctions it, and only then does anything land
  in `knowledge/`.
- **Perishable pages declare their expiry near the top**, as a bold `Stale after:` line with a
  `YYYY-MM-DD` date and a word on why. Vendor pricing, platform mechanics and eligibility rules all
  move. `repo-doctor` flags an expired page so staleness announces itself. Re-verify or supersede
  it. Do not just push the date out.
- **Kill a dead run properly.** A bold `DEAD` banner at the top saying why, in the same session it
  is ruled dead. A run that quietly stops being updated reads as current forever.

Research that a decision was actually made on gets promoted to `knowledge/research/`. Everything
that stayed exploratory stays here.
