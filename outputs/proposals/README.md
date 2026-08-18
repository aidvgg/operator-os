# outputs/proposals/

Client proposals, quotes and SOWs. Produced by `skills/proposal-creator`, which renders print HTML
to PDF through headless Chrome. Read that skill's `SKILL.md` before running it.

**Three files per proposal, and `skills/proposal-creator/SKILL.md` owns the names:**

- `<slug>-data.json` - the data sidecar, written first. It is the source of truth for the document.
- `<Client> - <Title>.html` - the self-contained render, kept for a quick visual pass.
- `<Client> - <Title>.pdf` - the artifact that goes to the client.

All three ship, and the HTML ships even though it is the big one (about 190 KB, because every font
is embedded so it opens correctly on a machine that has none of them). It is not a build leftover.
It is what the generator actually writes, and the PDF is printed from it, so it is the only copy you
can open, diff and re-print without Chrome. A folder holding the PDF alone leaves you unable to
tell a rendering bug from a data bug.

`<Title>` in the two filenames is the `projectTitle` with characters the filesystem treats specially
removed: `:` `/` `\` and a trailing `.`. The demo below is the case in point. Its title is
`Inventory-Sync Phase 3: Ops Dashboard` and the colon is in the document, on the cover, exactly as
written. It is not in the filename, because a colon in a macOS filename is displayed as a slash and
travels badly. Drop the character, never substitute a lookalike, and never let the document's title
drift to match the filename: the document is what the client reads.

The sidecar is not a build leftover. It carries `scopeTrace`, one entry per scope line recording
where that line came from: the client asked for it on a date, the operator added it, or it is
already live and not billable. `skills/proposal-creator` and the `price-attack` agent both read
those entries, so a scope line with no trace is a line nobody can defend in a pricing argument.
`repo-doctor` warns on a sidecar that does not parse, or whose `scopeTrace` is absent, empty or
off-schema.

**Prices in here are historical.** The live number for a client engagement is in
`knowledge/clients/<client>/roadmap.md`; the live number for the productized offer is in
`knowledge/business/outbound-offer.md`. A proposal states what was quoted that day. Never quote a
figure back out of this folder.

**Two verification gates are mandatory** and neither is optional for "quick" work: a fresh-context
`fact-check` on every proposal, and `price-attack` as well. Then `scripts/pdf-check` proves the
PDF is a real PDF. Then, and only then, the operator decides whether it goes.

Any demo file here belongs to the worked example. Delete it when you rebrand. The shipped demo
PDF is regenerated with `TZ=UTC` in front of the generator command, so its `CreationDate` carries
no local timezone offset; do the same before committing any PDF you intend to ship publicly (a
client deliverable does not need it).
