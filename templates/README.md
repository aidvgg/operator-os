# templates/

Reusable formats. A template is a shape with slots, never finished copy.

That distinction is the whole rule here. The moment a real price, a real date or a real client
name gets typed into a template it becomes a stale claim sitting in a file nobody re-reads,
and it will be pasted into a client message long after the real number moved. Live values live
in their owning file under `knowledge/` (one owner per state fact, see `CLAUDE.md`). Templates
point at the owner. They never restate the value.

What is here:

- `message-templates.md` - plain-text client and outbound skeletons. Phase-and-price framing,
  USD, slots in `[brackets]`.

How it plugs in: the task table in `CLAUDE.md` reads from `templates/` for proposals, content
and outbound. Filled output goes to `outputs/`, never back into this folder. Add a new format
here once you have written the same shape by hand twice.

One thing to know before you edit: `templates/` is a HARD surface for the tombstone check in
`scripts/repo-doctor`, the same tier as `knowledge/`. A retired value that reappears here is
blocked. That is deliberate. A dead price copied into a house format is a wrong number that
reaches a client months later, carrying the authority of a template.
