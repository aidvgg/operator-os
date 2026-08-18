# outputs/ - product, not truth

Everything the OS generates lands here: proposals, invoices, posts, outbound briefs, research
runs. One rule governs the whole tree.

**An output is a snapshot of what was true when it was generated. It is never an authority.**

A price in a sent proposal, a status in an old brief, a figure in last month's research note: all
of it is historical the moment the file is written. The live value lives in the owner file under
`knowledge/`. When an output and its owner disagree, the owner wins and the output is not
"corrected", because rewriting what actually went to a client falsifies the record.

That is what "disposable relative to `knowledge/`" means. Delete this whole tree and the business
still knows who its clients are, what they were charged, what was decided and why. Delete
`knowledge/` and the repo is a folder of old PDFs.

## The map

| Path | What lands here | Produced by |
|---|---|---|
| `outputs/proposals/` | Client proposals, quotes and SOWs, plus the data sidecar each was generated from | `skills/proposal-creator` |
| `outputs/invoices/` | Issued invoices. **Local-only, gitignored.** See the carve-outs below | `skills/invoice-creator` |
| `outputs/content/` | X posts, LinkedIn posts, threads, seeds | Hand-written against `knowledge/voice/` |
| `outputs/outbound/` | The prospect gate, per-prospect briefs, outbound drafts | `skills/prospect-brief` |
| `outputs/research/` | Research runs, one folder per question | `skills/research-doctrine` |
| `outputs/profiles/` | Business profiles for anyone who is not this business | `skills/business-profile-creator` |
| `outputs/ops/` | Backup logs, machine notes, anything operational. **Local-only, gitignored** | Scripts and sessions |

Each committed subdirectory carries its own `README.md`. Read it before adding a file to it.

The two local-only directories, `outputs/invoices/` and `outputs/ops/`, carry no README and do not
exist on a fresh clone. That is not an oversight. Git cannot re-include a file underneath an
ignored directory, and both paths are in `repo-doctor`'s HARD protected set, so a README committed
there would be blocked twice over. The rule for both is the row above and this paragraph. They get
created the first time something writes into them.

## The local-only carve-outs

Three paths in this tree are deliberately never committed. The reason is the same each time: the
file is structurally unsafe to publish, not merely private.

- **`outputs/invoices/`** - an issued invoice embeds the live wire block from
  `knowledge/business/invoices/PAYMENT-DETAILS.md` by design, because a client cannot pay an
  invoice that omits it. That makes a generated invoice not committable, ever. Your cloud drive
  is the archive. The committed record of an invoice is the ledger row and the per-invoice record
  under `knowledge/business/invoices/`, which carry the number, the amount and the status but no
  bank values.
- **`outputs/ops/`** - operational exhaust: backup logs, machine-local notes, receipts. None of it
  is business machinery and all of it is what a shared clone must not carry.
- **`outputs/research/*/local/`** - a research run pulls contact details out of public sources.
  The committed report cites this path, the local folder holds the unredacted values, and the two
  never merge.

`scripts/repo-doctor` enforces all three as protected paths and blocks the commit if one gets
staged, including with `git add -f`. It derives them from `.gitignore` and unions that with a floor
hardcoded in the script, which covers `outputs/invoices/` and `outputs/ops/`, so a botched ignore
edit cannot silently unprotect those two.

**Committed files may cite these paths. They may never restate what is in them.** A pointer that
dangles on a fresh clone is intentional. Naming the fact class is fine; naming the counterparty,
the ID or the number is not.

## Conventions that keep this tree readable

- **Name files `<slug>-<YYYY-MM-DD>.md`.** The date is when it was generated, not when it was
  sent. Two versions of the same thing get two files, not an edit.
- **Never hand-edit a generated document.** Change the input and regenerate. A hand-patched PDF
  and its data sidecar disagree the moment you save, and the sidecar is what the verification
  gates read.
- **Prove the format before it leaves.** `scripts/pdf-check` on any `.pdf`, `scripts/docx-check`
  on any `.docx`. A generator that writes text and names it `.docx` produces a file that opens as
  garbage on the client's machine, which has happened here once and is now the reason both checks
  are mandatory in the `CLAUDE.md` pre-send checklist.
- **These READMEs hold no live state.** No dated status lines, no "awaiting X". `repo-doctor`
  warns on it. A README that carries state becomes a second owner of it, and the second owner is
  always the stale one.

## Tombstones are soft here, and that is on purpose

`repo-doctor` blocks a retired value HARD under `knowledge/`, `.claude/`, `templates/` and
`skills/`, but only warns on a hit in `outputs/`. A proposal that quoted a number before it was
superseded is a true record of what was quoted, and the fix is a banner, not a rewrite. The
warning still names the file, so you find out before someone copies the dead figure forward.

## Promoting an output into knowledge

A deliverable that produced a fact does not teach the business anything until the fact is written
to its owner file, in the same session.

- An invoice is issued -> the ledger, `SUMMARY.md` and the per-invoice record are updated.
- A proposal is accepted -> the client roadmap file gets the phase, the price and the status.
- A research run reaches a conclusion a decision rests on -> the decide phase emits a write-back
  plan, the operator sanctions it, and the fact lands in `knowledge/`.
- A prospect brief finds a pain the bank does not hold -> the bank gets a candidate entry.

Nothing in this tree writes to `knowledge/` on its own. The write licences are listed in
`CLAUDE.md` and they are narrow.
