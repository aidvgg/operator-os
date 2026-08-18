# outputs/content/

Drafts and shipped copy for X and LinkedIn. No generator owns this folder. Content is written by
hand against `knowledge/voice/copy-rules.md` and `knowledge/voice/channel-voice.md`, with the
substance coming from `knowledge/pain-points/` and whatever the work actually produced that week.

**Layout:**

- `seeds/` - raw hooks and observations harvested from real sessions, one file each. A seed is a
  claim plus the receipt that earned it. Most never become posts.
- `<channel>-<slug>-<YYYY-MM-DD>.md` - a drafted or shipped post.

**Every post carries its receipt.** The value-beat rule in the voice files is hook, then substance:
a mechanism, the steps, or a number. A post that only names a problem is not finished. If the draft
cannot cite something that actually happened in the work, it is not a post yet, it is an opinion.

## Paste blocks and the dash check

Copy that is meant to be pasted goes in a fenced block. `repo-doctor` scans fenced blocks under
`outputs/content/` and `outputs/outbound/` for em and en dashes and blocks the commit on a hit,
because the ban is a hard rule of the house voice and prose reminders were not holding. Editorial
notes and derivation live outside the fences and are not scanned.

**A block under a heading that marks it as a posted record is skipped.** Mark it plainly, for
example `## posted 2026-08-01`, or strike the block through. Rewriting what actually went out to
satisfy a checker would falsify the record, which is why the exemption exists. A heading that
negates the marker (`## not posted yet`, `## draft, unshipped`) does not exempt anything.

**Nothing here posts itself.** A file in this folder is a draft until the operator posts it by
hand, and marking it as a record is a thing you do after, not before.
