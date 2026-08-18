# knowledge/doctrine/

Operating doctrine. Two kinds of thing live here and nothing else.

1. **`knowledge/doctrine/principles.md`** - first-party operating principles, written by the operator in the operator's own words. The only doctrine file that ships in this folder.
2. **An adopted external framework**, one folder per framework at `knowledge/doctrine/<name>/`, fronted by a `CORE.md` router.

**This template ships the adopted-doctrine slot empty on purpose.** There is nothing here to delete and nothing to rename. Filling it is a deliberate act with a checklist, below, and most operators will never need to.

What does not belong here: live state (prices, deal stage, client posture), which lives in `knowledge/memory.md` and the client files. Perishable market research, which lives in `knowledge/research/` and carries a `Stale after:` line. Anything you have not read end to end.

---

## Reference is the default

Third-party material - a paid course, a mentor's framework, a book's method, a competitor's playbook - is **external reference** until a recorded decision says otherwise. Reference tier means four things:

- It is an **input**, never the business's voice. You do not repeat it to a client as your own position, and an agent does not carry its register into anything we write.
- It **never outranks a curated file**. Normal precedence holds: `CLAUDE.md` -> `knowledge/memory.md` -> topic files -> everything else. A reference page loses every conflict, and the conflict gets flagged rather than quietly averaged.
- It **routes nothing**. No skill reads it. No session is required to open it before deciding anything.
- It can sit in `knowledge/research/` or stay in `raw/`. It does not need this folder at all.

Most material should stay at reference tier forever. The test for promoting it is not "was it good". It is: are you willing to have every agent read it before every decision in a named domain, on every session, from now on. That is the actual cost of adoption, and it is paid in attention on every future task.

---

## Adoption is a recorded decision, not a mood

Adopt only when the framework has already changed how you decide and you are tired of re-explaining it from scratch. Then run this, in order.

1. **Name the domain in one sentence.** "This governs pricing, offer shape and outreach sequencing." If you cannot name which decisions route to it, you are not adopting a framework, you are impressed by one. Stop here.
2. **Name what it does not govern.** This list is usually longer than the first one, and it is the part that saves you a year from now. Delivery, hiring, tax, partnerships, whatever the source never actually addresses.
3. **Write the row in `ai/DECISIONS.md`.** The ruling, the falsifiable prediction, a review date. Adoption with no review date is a conversion rather than a decision, and conversions never get re-examined.
4. **Distil it yourself, in your own words**, into `knowledge/doctrine/<name>/`, one file per module. The licence rule below is why this is not optional, and the compression is where the understanding actually happens.
5. **Write `CORE.md` first**, to the contract below. Router, not summary.
6. **Add one routing line to `CLAUDE.md`**, naming the file to read and the decisions that must read it. Doctrine nobody is told to open is decoration.
7. **Run it backwards over rulings you have already made.** Take five live decisions and score them against the framework. If it endorses all five, it taught you nothing and belongs back at reference tier. If it contradicts one, argue that deviation once, write the argument down next to the audit, and never relitigate it session by session.

---

## The `CORE.md` contract

An adopted folder is read through its router, and the router carries these sections in this order.

| Section | What it holds |
|---|---|
| Source and licence | what this distils, where the source sits, whether you may redistribute it (usually no) |
| Adoption line | who adopted it, when, and the `ai/DECISIONS.md` row that records it |
| The model in one page | the framework compressed to what you would say out loud to a peer |
| Decision map | for each decision type, the file in this folder that owns it |
| The laws | deduped, checkable statements. Violating one is a flag in any session |
| Mapping to your motions | where this is native habitat, where it transfers partially, where it does not apply at all |
| Reading order | first to last, with a line on why each file comes when it does |
| **What this does NOT govern** | numbered, blunt, and the section you write hardest |

The last section is what earns the folder its place. A framework with no stated edges gets stretched into decisions it was never built for, and the stretch is invisible, because a doctrine page always sounds like doctrine.

Two more rules on the router:

- **Route before you quote.** If a number in the framework is channel-scoped, stage-scoped or a teaching example, say so at the point of use. A benchmark lifted from one channel and quoted at another is a wrong number wearing a citation.
- **The router restates nothing.** It points at the file that owns each thing. One owner per fact applies inside this folder exactly as it applies everywhere else.

---

## Doctrine is not state

Adopted doctrine is a lens, not a fact about today. Prices, client status, pipeline and next actions come from `CLAUDE.md` -> `knowledge/memory.md` -> the client file, in that order, always. Where a framework and this repo's operating contract disagree, the contract wins, and the disagreement gets written into the mapping section of `CORE.md` so nobody has to rediscover it.

Concretely: a doctrine page never carries a price, a deal stage or a client name. If one appears, that is state that wandered, and it will be stale inside a month.

---

## Do not commit what you cannot redistribute

Course PDFs, paid workshop material, a book's text, a purchased template pack: **none of it goes in git.** Most of it is licensed for your own use and nothing else, and this repo is a thing you clone onto a second machine, hand to a contractor, and back up to a cloud drive.

The rule:

- Source files stay in `raw/`, which is gitignored and quarantined.
- What gets committed is **your distillation, in your own words**. That is your work product, and it is the more useful artifact anyway.
- The source line in `CORE.md` states where the original lives and what the licence allows, so a future reader knows why the folder holds notes instead of chapters.

A distillation that is really a transcript is both a licence problem and a thinking problem. If you cannot say it shorter than the source said it, you have not finished reading it.

---

## Retiring an adopted framework

Same weight as adopting one, run in a single session:

1. Banner the folder's `CORE.md` with `**DEAD - <why>**` at the top.
2. Strike the routing line in `CLAUDE.md` rather than deleting it, so the history of why it was there survives.
3. Close the `ai/DECISIONS.md` row with the outcome.
4. Grep for files that still point at the folder and strike or repoint each one.

`repo-doctor`'s `dead-artifact-ref` check flags un-struck live-sounding references to a bannered file. That is the backstop for step 4, not a substitute for it.
