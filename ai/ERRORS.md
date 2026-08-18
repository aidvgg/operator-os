# ERRORS.md - incidents that reached Sam or a client

One row per incident. The bar for a row is that the mistake **left the workspace**: it reached Sam
as a claim they acted on, or it reached a client. A mistake caught in draft is not an entry, it is a
Tuesday.

**Every rule and every check in this repo must trace to a row here, or to a hazard named in the
Hazards section below. No speculative process.** That rule lives in `CLAUDE.md` under "Improving
this OS", and it is the only thing between a working OS and a pile of ceremony nobody follows. If
you cannot point at the row a new check exists for, do not add the check.

Rows are append-only and never rewritten to read better. The Control column is the useful half: it
is what a future session greps to find out whether a class of failure already has a floor under it.
The ratchet rule says a session that fixes a class of problem ends by putting that floor in, where
a mechanical check is possible, and states plainly when it is not. A control that can only ever be
procedural should say so in its own cell, so nobody later mistakes a habit for a guardrail.

Keep the rows blunt. This file is the one place in the repo where the writing is allowed to be
unflattering, and softening a row is how the lesson gets lost.

| Date | What happened | Reached | Root cause | Control that now prevents it |
|---|---|---|---|---|
| 2026-07-11 | A price from a superseded proposal was quoted in a client message. The number had been replaced days earlier and the message still went out carrying the dead one. | Client | The dead number lived in four files and only one was updated when the price changed. Nothing forced the other three to die with it, so three current-sounding copies of a wrong price sat in the tree waiting to be grabbed. | **One owner per state fact**: a price lives in its owner file and every satellite links to it instead of restating it. Mechanical floor: `ai/TOMBSTONES.md` plus the `tombstones` check in `scripts/repo-doctor`, HARD in `knowledge/`, `.claude/`, `.agents/`, `.github/`, `templates/`, `skills/` and root-level markdown, soft in `outputs/`. Honest limit: the check only knows a value is dead once somebody writes the tombstone row, so the same-session ripple is still a human obligation. The check makes the ripple stick, it does not start it. |
| 2026-07-22 | A generated `.docx` opened as plain text on the client's machine. They said so in writing before Sam noticed. | Client | The generator wrote text and gave it a `.docx` name. The only verification step extracted the text back out and confirmed the words were there, which a malformed file passes trivially. A verification method that cannot fail is not a verification method. | `scripts/docx-check` is mandatory in the pre-send checklist: zip integrity, a full XML parse of every part, a document and body root check, non-empty extracted text, and a real open test. Wired into `scripts/repo-doctor` as the `office-xml` HARD check, so a fake office file cannot even be committed. `scripts/pdf-check` is the same gate for PDFs. Standing rule: a generated file is not delivered until something that is not the generator can open it. |
| 2026-07-29 | An agent wrote into the live repo instead of a throwaway clone and overwrote a working file. Recovered from the last commit, so nothing was lost, but the session was. | Sam | The agent trusted an inherited working directory to tell it where it was, and its output path was relative to that. The generator it ran also carried one machine's absolute home path, so its own anti-clobber guard was reading the live tree while the agent believed it was in a scratch copy. | The **"Agents and the live tree"** rule in `CLAUDE.md`: `git -C <abs>` for every git call, explicit `cwd=` on every subprocess, absolute paths in shell, explicit-path staging and never `git add -A`, probes and fixtures in a throwaway clone outside the repo. Mechanical half: `machine-path`, HARD in `scripts/` and `.githooks/`, so no committed executable may hardcode one machine's home directory; derive the root from `git rev-parse --show-toplevel` instead. Procedural half stays procedural: no check can know whether an agent verified its own working directory. |
| 2026-07-30 | A Phase 3 proposal draft reached Sam pricing infrastructure that was already live and already paid for as if it were new build, alongside two line items nobody had asked for. Caught before it went out, so it reached Sam and not the client. | Sam | Scope was assembled from what the repo knew rather than from what the client asked for. Delivered work sitting in the roadmap read as available scope, and internal residuals, the things Sam had privately decided ought to be done next, got promoted into a priced deliverable without anyone deciding to sell them. Nothing in the drafting step forced a line to name where it came from. | **Scope discipline** in `skills/proposal-creator/SKILL.md`: every scope line must trace to a client ask, and already-delivered infrastructure is never re-billed. Mechanical floor: the mandatory `DEFINITION OF DONE` section, and the `scopeTrace` sidecar, where each line carries `line`, `origin` and `evidence`, enforced by the `sidecar-trace` check in `scripts/repo-doctor`. The sidecar is handed to `price-attack` in fresh context, so a line marked `already live, not billable` that is still priced gets caught by a reviewer who was not in the room when it was drafted. Honest limit: `origin` is written by the same drafter, so the sidecar catches an unexamined line, not a dishonest one. |

## Hazards

Failure classes that have been seen, reasoned about, or nearly landed, but have not yet produced an
incident row. They exist so that "no speculative process" stays honest: a check may trace to a
hazard here instead of to an incident, but only if the hazard is written down first, with the
evidence that makes it real rather than imagined. A hazard with no in-family precedent and no
near-miss behind it does not belong in this section.

- **Guardrail rot: a check that silently stops firing.** The enforcement layer is the part of this
  repo with the least testing, and its failure mode is silence. A rotted regex, a renamed path, a
  parse loop that returns zero rows, a scanner whose input list quietly excludes the files it was
  written for: every one of those leaves the run green while the guardrail is off. This is not
  speculative, and the 2026-07-22 row above is the in-family precedent: it **is** a verification
  method that silently stopped verifying, in a place where the output went to a client. Controls
  that exist today, each of which is a hand-built answer to one instance of the shape: the tombstone
  ledger reports its own absence or an unparseable table (`tombstones-source`) instead of scanning
  nothing quietly; the tombstone exemption rules run their own cases in band on every invocation
  (`tombstone-selfcheck`); `scripts/clock_grammar.py` self-checks its invariants on load, and is the
  single owner of the Due and Stale grammar precisely because hand-copied grammars drift apart;
  `backup-sensitive` proves a restore before it will write its own success marker, because comparing
  ciphertext checksums only ever proved transport (`backup-unproven`); `sessionstart-mute` checks
  that the session hook still actually surfaces the doctor's output; the agent-adapter pair
  (`agent-adapters` and `agent-adapter-check-broken`) refuses the generator's own clean claim until
  the live generator has also rejected a stale surface and a dropped alias in a disposable tree,
  because a padded no-op that keeps the marker strings and prints the clean sentinel passes every
  source-shape test there is; and the allow file expires its own entries, so an exception cannot
  outlive the thing it excused. The real control is the **guardrail-fixture suite** specified in
  `knowledge/ops/os-roadmap.md`: known-bad fixtures plus a runner that asserts each check still
  flags its own fixture. Until that exists, every check here is trusted rather than tested, and the
  ratchet rule in `CLAUDE.md` is what keeps the gap from growing.
  The shape has a second face worth naming, because it is not a check at all. `ai/AGENT_ROUTES.json`
  is the one registry that generates `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md` and
  the thin Claude commands. A generated view that drifts from its registry leaves every check green
  while one model reads different policy from the others: the planning phrase that routes a Claude
  session into the daily-log skill routes a different agent into a generic intake instead, and
  nothing in the tree objects. Green run, guardrail off, wearing a discovery surface rather than a
  scanner.
- **Clock blindness: a deadline that exists only as prose.** `scripts/horizon` reads structured
  tokens on purpose, because free-text date mining is an alarm swamp. The cost of that choice is
  that a commitment written as an ordinary sentence, or parked in a table column, is invisible to
  the clock, and the OS reports zero overdue while a real date sails past. Money in has the same
  hole as promises out: an invoice with a payment date recorded only in a register column is a
  receivable nobody is watching. Controls: the `**Due:** YYYY-MM-DD - <what>` convention, owned by
  the file that owns the commitment; `horizon-blind`, soft in `scripts/repo-doctor`, which flags
  past-dated deadline-shaped prose in `knowledge/` with no matching Due token; `scripts/money`
  failing when an open invoice row has no armed Due line under `knowledge/business/invoices/`; and
  `clock-chronic`, which surfaces anything overdue a week or more at commit time so a date nobody
  moves cannot age quietly. The related shape on the decisions ledger is `clock-ignored`: a review
  row whose Review-on cell holds neither a date nor an explicit `Gate: <condition>` can never be
  nagged by `horizon`, so `decision-undated` names it every session instead, while a `Gate:` row
  stays visible under horizon's EVENT GATES. Resolving a Due line means
  striking it with the outcome, never deleting it, or the record of what was promised disappears
  with the reminder.
  The third face is a fact with an expiry rather than a date to act on. A page of web-sourced
  pricing, platform limits or eligibility rules is true the week it is written and quietly false
  later, and nothing in the tree objects unless the page declares its own shelf life. It is the same
  hole as the other two: the clock can only see what somebody armed. Control: the
  `**Stale after:** YYYY-MM-DD` line on perishable pages, and `stale-page` in `scripts/repo-doctor`,
  which reads only that declared token and never mines prose for a date, and which names a
  calendar-invalid value out loud rather than leaving a page that can never expire looking healthy.
  Stated limit: a perishable page that never declares itself is invisible to this too, so the
  declaring habit is the control and the check is only its floor.
- **House-style drift into send-ready copy.** Some rules are style, not incident: the em dash ban in
  `knowledge/voice/copy-rules.md` has no error row behind it and should not pretend to have one. It
  still earns a mechanical floor, because the failure mode is well understood even though it has not
  yet cost anything. Banned characters arrive by paste and by model output, a bulk sweep strips them
  once, and a later hand-edit quietly reintroduces a few into exactly the blocks that go out. A
  prose rule does not survive that cycle, which is the same shape as the guardrail-rot hazard above:
  a control that exists only as an instruction is a control nobody can prove is on. Control:
  `emdash-paste` in `scripts/repo-doctor`, scoped narrowly to fenced paste blocks under the send
  trees, so editorial prose, derivation notes and quoted third-party material stay untouched. Stated
  limit: copy that never becomes a file under `outputs/`, a message drafted in chat and sent
  straight from there, is outside every mechanical check, and the one-line ban in `CLAUDE.md` is all
  that covers it.
- **Credential and third-party contact shapes arriving through the work.** This repo already treats
  one class of value as never-commit: the wire block lives in a local-only
  `knowledge/business/invoices/PAYMENT-DETAILS.md`, gitignored, with `protected-paths` HARD behind
  it and the invoice skill holding a read licence only. That is the in-family precedent, and it is
  what makes this a hazard rather than an invented one. The class of value that must never enter git
  is established here, and exactly one member of it has a floor. The other members arrive through
  the work itself rather than through the money file: a client build that runs a managed database
  and a transactional mail provider hands Sam a service-role token and an api key, and a fetched
  research source carries a third party's direct phone number. Pasted into a client file, any of
  those commits clean unless something is watching for the shape. Controls: the provider-prefix,
  JWT, PEM and phone arms of `secrets` in `scripts/repo-doctor`, HARD, and every one of them is
  measured before it ships: the whole pattern list currently fires zero times across every text
  file in this tree, which is the only number that makes a HARD gate liveable. Stated limit, and a
  deliberate one: generic `password=` and `api_key=` shapes are NOT in that list, because they fire
  on ordinary workflow prose that names environment variables, and a check the operator learns to
  scroll past is a check that is off.
- **Snapshot drift: a restatement that outlives what it restated.** The 2026-07-11 row above is this
  hazard already realized in its most expensive form, and that is the evidence for the rest of it.
  What that row's control reaches is narrow: the tombstone ledger only knows a value is dead once
  somebody writes the row, so it covers copied *values* and nothing else. The same shape has faces
  the ledger cannot see. An artifact bannered dead and still cited in live-sounding text. The
  carry-over bucket in `knowledge/ops/logbook/STATS.md` whose as-of date has fallen behind the
  `knowledge/ops/logbook/LOGBOOK.md` cursor, which means closes have appended without the re-base
  step and every un-struck line in it is an unverified snapshot that the planning step reads as
  current. A "nothing outstanding" sentence in `knowledge/business/invoices/SUMMARY.md` sitting
  above a Register row that is still unpaid. A generated rollup, `knowledge/business/MONEY.md`,
  older than the file it rolls up, or generated in a prior calendar month so its trailing window has
  already moved under it. Controls: `dead-artifact-ref`, `carryover-stale`, `summary-openbalance`,
  `money-drift` and `money-monthstale`, all soft, all in `scripts/repo-doctor`, all surfaced every
  session by the SessionStart run. Soft on purpose: each is a freshness heuristic, and a HARD block
  on a heuristic trains `--no-verify`, which is the escape-hatch decay `.repo-doctor-allow` exists
  to prevent. Honest limit: every one of them compares a date or looks for a banner, so they catch a
  snapshot nobody re-based, never a snapshot re-based carelessly. The semantic half stays
  procedural.
- **A bounded core that stops being readable in one pass.** `CLAUDE.md` opens by telling every
  session to read `knowledge/memory.md` first, which makes that one file's size a cost paid before
  any session does anything else. Appending to it is free and reading it is not, so it grows in one
  direction unless something objects. The line-length half is the sharper one: verification here is
  grep-shaped, and a grep that truncates inside a single enormous line returns a fragment. A
  fragment reads as absence, and absence is what a fact-check acts on, so a quote that is really
  there can be reported missing and a correct claim can be ruled unsupported. Nothing has been ruled
  on that basis yet, which is exactly what keeps this a hazard and not a row. Control: `core-bloat`
  in `scripts/repo-doctor`, a byte ceiling and a maximum line length on that one file, soft and
  full-mode only, plus the eviction habit `knowledge/ops/os-roadmap.md` describes, where dated
  narrative moves to its owning topic file and leaves a pointer behind. Scoped to the core alone on
  purpose: a repo-wide version opens with a wall of hits on files nobody is cleaning up today, and a
  check that opens loud on unrelated work gets switched off inside a week. The pointer-region check
  that rides alongside it, `core-restatement`, is not this hazard. It belongs to the 2026-07-11 row,
  because a pointer carrying a figure is a number copied out of its owner file.
