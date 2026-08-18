# OS roadmap

**Status:** adopted direction, 2026-07-26. This file records what the OS is being improved toward
and in what order. It is not an implementation claim: every section below says plainly whether the
work is BUILT or PLANNED. It arms no deadline by itself, and nothing here is a commitment until it
appears as a `**Due:**` line in the file that owns the work.

**A note on the paths in this file.** Planned scripts are named in plain text, without backticks,
on purpose. `repo-doctor`'s dead-pointer check tests every backticked path-shaped span for existence
on disk, and a path that is planned is not rot. If you do need to backtick one, the sanctioned
remedy is a scoped, dated entry in `.repo-doctor-allow` (`<check-id> <path>::<token-glob>`), not a
looser check. The commented example at the bottom of that file is exactly this case.

---

## Objective

Improve agent accuracy, client-artifact reliability, and operational follow-through, without adding
a database, a dashboard, a generalized workflow engine, or automation of a motion nobody has proven
by hand.

The governing loop:

`current truth -> commitment -> artifact -> hard validation -> outcome -> decision`

Artifacts and decisions are the parts this repo already handles well. The gaps that cost real money
are the other three: truth that is compact enough to actually be read, a commitment clock with no
blind spots, and validators that fail closed.

---

## 1. Keep the canonical core compact

**BUILT.**

`knowledge/memory.md` is loaded every session, so its size is a cost every session pays, and a fact
buried at the bottom of a large file is a fact agents answer without. It holds current state and
pointers only: current business state, stable operating facts, current client states, the next
priorities, and a pointer to the file that owns each depth topic. Dated narrative and superseded
explanation move into the owning topic file.

Two floors enforce it, both in `repo-doctor`, both soft, both scoped to that one file:

- `core-bloat` - a size ceiling and a maximum line length.
- `core-restatement` - a currency figure inside a pointer block. A pointer names **where** a value
  lives. The moment it names the value, there are two owners and one of them is going stale.

Scoped narrowly on purpose. A repo-wide version of either floor opens with a wall of hits on files
nobody is cleaning up today, and a check that is loud about unrelated work gets switched off inside
a week. Floors land attached to a real cleanup, never pre-emptively.

---

## 2. Keep one commitments clock

**BUILT.**

- The `Due:` line lives in the file that owns the commitment. There is no second hand-maintained
  register, because two registers means one of them is wrong and nobody knows which.
- `scripts/horizon` is the only aggregate view, generated on demand.
- Every promise to a client, a counterparty or yourself gets its owner-local line at the moment it
  is made, not at the moment it is remembered.
- A `Due:` line is resolved by striking it through with the dated outcome, never deleted. The
  resolution is the record.

The grammar has exactly one owner, `scripts/clock_grammar.py`, loaded by `horizon`, `money` and
`repo-doctor`. It used to exist as three hand-copies, and one edit widened exactly one of them, so
`money` began rejecting the rollover shape `horizon` accepted. That is the general failure of copied
rules: they do not drift loudly, they drift into disagreement.

The shape that hole hid, and the reason a mid-line token counts at all:

```
~~**Due:** <old date> - what was promised~~ **Due:** <new date> - the same thing, moved
```

One resolved token and one live token on one line. A line-start anchor cannot see the second, and a
"skip any line containing a strikethrough" rule cannot see it either, so one dead date hid a live
overdue one from the clock, from the blind-spot check, and from the chronic-slip check at once. The
fixture pair in section 9 is what keeps all three consumers agreeing about it.

---

## 3. Put contracts in front of client-facing generators

**BUILT for invoices, PARTLY BUILT for proposals.**

Invoice validation covers required fields, the ledger number, dates, currency, bill-to identity,
line-item arithmetic, and instalment totals against the contract total.

Proposal validation covers required fields plus a recorded verification receipt in the data sidecar:

```json
"verification": {
  "fact_check": "passed",
  "price_attack": "passed",
  "checked_at": "YYYY-MM-DD"
}
```

A document may be generated as a draft without a complete receipt. It must not be labeled final or
send-ready until the contract passes. `repo-doctor`'s `sidecar-trace` check reads the same sidecar
and requires a scope trace, so the price-attack pass has something to attack.

Still open here: the proposal contract is enforced by the skill's own steps rather than by a
validator that can fail closed on its own. Until that lands, the mandatory fresh-context gates in
the skill are the control, and they are only as good as the operator's refusal to skip them on a
"quick" job.

---

## 4. One full quality command

**PLANNED.** Not built. Nothing in the repo references it as if it exists.

A single scripts/check entry point, composing the controls that already exist rather than replacing
them:

- `scripts/repo-doctor` (full mode)
- `scripts/horizon`
- the clock grammar self-check
- JSON parse of every data sidecar
- python and node syntax over every script
- office and PDF package validation
- `git diff --check`
- backup-age warning from the marker
- the guardrail-fixture runner from section 9

It is the pre-push and pre-send gate. The pre-commit path stays fast and stays narrow: a gate that
adds ten seconds to every commit teaches people to commit less often, which is worse than the
defect it catches.

---

## 5. Tighten default context boundaries

**BUILT as doctrine, PLANNED as tooling.**

Default read order: `CLAUDE.md`, then `knowledge/memory.md`, then the owning topic file, then
`ai/DECISIONS.md` plus `ai/ERRORS.md` and `ai/TOMBSTONES.md` when the task touches money, a
client-facing artifact or a superseded number, then the relevant current output.

Excluded by default unless the task explicitly needs them: the quarantined inbox, superseded drafts,
historical research working directories.

If context-selection misses keep happening, the next step is a small scripts/context router that
prints the authoritative paths for a topic. Not a vector store. Simple routing has not yet been
proven insufficient, and a retrieval layer over a repo this size is a way to make a solved problem
interesting.

---

## 6. A five-task golden benchmark

**PLANNED.**

One representative fixture and an invariant-based rubric for each of:

1. Produce a fact-grounded proposal.
2. Generate a ledger-valid invoice.
3. Answer a current client-state question.
4. Produce a daily plan from live commitments.
5. Research and adjudicate a disputed claim.

Score factual and current-state accuracy, source use, price correctness, forbidden claims, and
output validity. Never snapshot exact prose: prose changes for good reasons and a snapshot test
punishes that.

Run the pack after any change to `CLAUDE.md`, to the canonical memory structure, to a core skill, to
a generator, or to a validator. One builder plus one fresh-context critic is the default.

---

## 7. Close the recovery prerequisites

**BUILT.**

- Encrypted off-site backup of the local-only set, with an in-run restore proof, and one drill done
  by hand with the passphrase typed from the password manager rather than read from the Keychain.
  Owner and detail: `knowledge/ops/tools-and-stack.md` section 7.
- `business-profile-creator` repaired rather than disabled. The defect was a blank-slate rebuild:
  the interview template overwrote a richer stored profile, silently dropping every field the
  interview did not ask about, and nobody noticed until a downstream draft was missing a positioning
  line no one remembered writing. The repair is a read-existing-and-merge step, a field-level diff
  before writing, and a non-canonical output path for profiles of other businesses. That ruling
  lives here and the skill cites it.

---

## 8. The ratchet rule

**LIVE.** It is process, not code, so it applies from the moment it is written down.

A session that fixes a class of quality problem ends by adding the floor check that makes that class
un-reintroducible, wherever a mechanical check is possible. Cleanups without ratchets are rented,
not owned: the same defect walks back in through the next tired session, and the second cleanup
costs the same as the first.

Two constraints keep this from turning into check sprawl:

- **A new check traces to a real entry in `ai/ERRORS.md`, or to a hazard named in that file's
  Hazards section.** No speculative process. A check invented for a defect nobody has ever hit is a
  false positive generator with a good story.
- **Floors land attached to a real cleanup, and start as narrow as the cleanup was.** See section 1
  for what happens to a floor that opens loud.

The rule is wired as one bullet in `CLAUDE.md` under "Improving this OS". This file is where its
mechanism is specified.

---

## 9. Guardrail fixtures: tests that the checks still fire

**PLANNED.** This section is the specification. It is the owner of the fixture contract, and
`CLAUDE.md`, `scripts/repo-doctor`, `scripts/horizon` and `scripts/clock_grammar.py` all point here.

### 9.1 Why this exists

The enforcement layer currently has zero tests. A rotted regex, a renamed path, a check that quietly
returns before its loop, or a rename that leaves a scan pointed at a directory that no longer exists:
any of these makes a check stop firing while every run stays green.

**A guardrail that silently stops firing is worse than no guardrail.** No guardrail leaves you
careful. A dead guardrail leaves you confident, and confidence is what makes people skip the manual
read. Every green run after the rot is a false negative being counted as evidence, and the longer
the streak, the more the next release trusts it.

This is not hypothetical in this family of tooling. The one incident in `ai/ERRORS.md` that reached
a client with a broken file was a verification method that had silently stopped verifying: text
extraction passed a file that was not a real document, because extraction reads bytes rather than
opening the package. The check ran. The check returned green. The check had not verified anything.
"Guardrail rot" is a named hazard in the same file, and this section is the control it points at.

### 9.2 The contract

**Every check id in `scripts/repo-doctor` gets exactly two fixtures.**

- A **positive fixture**: a known-bad input the check MUST reject. It proves the check still fires.
- A **negative fixture**: a known-good input the check MUST pass. It proves the check has not been
  widened into something that flags ordinary work.

Both halves are load-bearing. A suite made only of known-bad inputs is passed perfectly by a check
that flags everything, and a check that flags everything is switched off within a week, which is rot
with extra steps and a paper trail. The negative fixture is what makes a false-positive fix
provable instead of a matter of taste.

**Choose the negative fixture as close to the positive one as the rule allows.** A known-good input
from the far side of the repo proves nothing. The near miss is the whole test: it is the shape
someone will try to "fix" the check into rejecting, or the shape a widened check will start
rejecting by accident.

**A check without a fixture pair is assumed rotted.** Not "untested". Rotted. The runner enumerates
check ids from `repo-doctor` itself (a planned `scripts/repo-doctor --print-checks` inventory flag)
and fails on any id absent from the fixture manifest. That is what makes the assumption mechanical
rather than aspirational: add a check without fixtures and the next full run is red, naming your
check.

### 9.3 Where fixtures live

**Outside the live tree.** A sibling directory next to the repo, `../operator-os-fixtures/`, never a
subdirectory of it. Three reasons, in order of how expensive they are to learn the hard way:

1. Several fixtures are deliberately toxic by construction: a wire-block-shaped string, a corrupt
   office package, a retired value written plainly, an absolute home path in an executable. Inside
   the tree, every one of those HARD-fails every ordinary commit and push. The obvious repair, an
   exclusion path inside the doctor, is a hole cut in the gate for the benefit of the tests, and a
   hole cut for a good reason is still a hole.
2. `CLAUDE.md`'s "Agents and the live tree" rule already bars probe files next to live ones. A
   fixture is a probe with a long life and a filename that looks legitimate.
3. Running from outside exercises the doctor the way a real commit does: by path, through the same
   entry point, with no privileged knowledge of its internals.

The honest cost: an out-of-tree directory is not carried by the clone, and a fixture set nobody can
find is a suite nobody runs. So the **manifest is committed and the fixtures are materialized**. The
repo holds a text manifest describing each fixture, its check id, its expected verdict and the
reason it exists; the runner builds the toxic files into the sibling directory at run time and
deletes them after. No toxic byte is ever stored in git, and a fresh clone can still run the suite
with one command.

### 9.4 First fixture pairs

The pairs below are the starting set. They are chosen by blast radius: the checks whose silent death
would cost a client, cash, or a secret.

| Check | Known-bad, must be REJECTED | Known-good, must PASS |
|---|---|---|
| `secrets` | A committed file carrying an account-shaped or routing-shaped value | A file that cites the local-only wire file by path and names no value |
| `protected-paths` | The local-only wire file staged for commit | Its committed placeholder template staged |
| `tombstones` | A retired price written plainly in a `knowledge/` file | The same string struck through, with its row present in `ai/TOMBSTONES.md` |
| `office-magic` / `office-xml` | A text file renamed to `.docx` | A real generated `.docx` that opens as a package |
| `stale-page` | A page whose expiry date has passed | The same page carrying a future one |
| `dead-pointer` | A backticked path under a scanned top directory that is not on disk | A backticked command invocation with flags whose first word does exist |
| `horizon-blind` | A past-dated deadline written only as prose | The same date carried by a proper `Due:` token |
| clock grammar | A rollover line where one consumer sees the second token and another does not | `~~**Due:** <old>~~ **Due:** <new>` read as one resolved and one live, identically by `horizon`, `money` and `repo-doctor` |
| `money-stale` / `money-drift` | The cash register edited with the generated rollup left untouched | Register and freshly regenerated rollup together |
| `machine-path` | A script hardcoding an absolute home directory | The plist placeholder form the install step substitutes |
| `core-bloat` / `core-restatement` | An oversized core file, and a pointer block that restates a price | A core inside the floor whose pointer names only the owner file |
| `agent-adapters` | A generated view edited by hand | The same view regenerated from the route registry |
| `emdash-paste` | A send-ready copy block containing an em dash | The same copy with a comma or a single hyphen |
| `decision-undated` | A ruling whose review cell is neither a date nor a `Gate: <condition>` | A ruling carrying a real review date or an explicit `Gate:` cell |

The `decision-undated` pair is worth reading twice. A ruling reviewed "after 30 conversations" is
a legitimate shape, and the ledger spells it as `Gate: 30 real conversations logged`, which
`scripts/horizon` keeps visible under EVENT GATES without inventing a date. The same cell without
the `Gate:` prefix is the broken form the check names, because nothing can ever fire it. The
template ships the gate form, so a fresh clone is quiet here; strip the prefix to see the check
speak.

### 9.5 Running it, and keeping it honest

- The runner lives inside the section 4 quality command. Pre-push and pre-send, never pre-commit.
- **Success test:** deliberately break one guardrail, by renaming a path it watches or loosening one
  regex, and the next full run goes red and names that check. If it stays green, the suite is
  decoration.
- A fixture that starts failing is one of two things: a real regression, or a deliberate change to a
  check. A deliberate change updates the fixture **in the same commit as the check**, with the
  reason in the message. Adjusting a fixture until it goes green, in its own commit, with no
  explanation, is how a suite becomes a record of what the code currently does rather than a
  statement of what it must do.
- New check, new pair, same session. That is the ratchet rule of section 8 applied to the
  enforcement layer itself.

---

## 10. Explicit non-goals

- No knowledge database, no web dashboard, no vector store over the repo.
- No bidirectional sync between documents. One owner per fact, pointers everywhere else.
- No generalized agent-workflow platform.
- No large snapshot-test suite. Invariants, not prose captures.
- No additional canonical file duplicating facts an existing owner already holds.
- No larger agent count as a substitute for better routing or harder verification.

The target is a smaller, sharper operating system with fewer live-looking contradictions and harder
edges around money, commitments, client deliverables and recovery. Not a bigger one.

---

## 11. Status board

| Section | State |
|---|---|
| 1. Compact core | BUILT, floors live |
| 2. One commitments clock | BUILT |
| 3. Generator contracts | BUILT for invoices, proposal validator still lives in the skill's steps |
| 4. One full quality command | PLANNED |
| 5. Context boundaries | doctrine BUILT, router PLANNED and not yet needed |
| 6. Golden benchmark | PLANNED |
| 7. Recovery prerequisites | BUILT |
| 8. Ratchet rule | LIVE |
| 9. Guardrail fixtures | PLANNED, specified above |

Order of work: sections 4 and 9 together, because the runner needs a home. Then 6, which is the only
item that measures whether any of this improved the output rather than the plumbing. Section 5's
router waits for evidence that routing is actually the problem.
