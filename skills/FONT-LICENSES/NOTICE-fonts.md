# Notice - fonts redistributed with this template

The document generators embed three font families into the HTML they render to PDF. Those
binaries are redistributed inside this repo, so the licence and the copyright notices have to
travel with them. All three are under the **SIL Open Font License 1.1**, whose full text sits
next to this file at [`skills/FONT-LICENSES/OFL-1.1.txt`](OFL-1.1.txt).

This is the same treatment the vendored MIT skills get in `skills/NOTICE-mengto.md` and
`skills/LICENSE-mengto-skills`. A binary you did not author is a thing you owe attribution for,
whether it is a markdown file or a woff2.

## What ships, and what covers it

| Family | Version in tree | Upstream project | Copyright notice, verbatim from the binary |
|---|---|---|---|
| Space Grotesk | 2.000 | github.com/floriankarsten/space-grotesk (Florian Karsten) | `Copyright 2020 The Space Grotesk Project Authors (https://github.com/floriankarsten/space-grotesk)` |
| Inter Tight | 3.004 | github.com/rsms/inter-tight (Rasmus Andersson) | `Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight)` |
| JetBrains Mono | 2.211 | github.com/JetBrains/JetBrainsMono (JetBrains s.r.o.) | `Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono)` |

Licence for all three: SIL Open Font License 1.1. Each binary points at
`https://scripts.sil.org/OFL` in its own `name` table (name ID 14), so the licence claim above
is the font's own claim, not a guess made from a download page.

The copyright column is the **holder statement of record**. Each project names its authors
collectively, so that string is what OFL condition 2 requires to be reproduced. The upstream
column names the person or company who runs the project, for provenance.

## Which files each notice covers

Six files, three families, two copies. The proposal and invoice generators each carry their own
`assets/` tree so a skill folder stays self-contained, so every family appears twice:

| Family | Files |
|---|---|
| Space Grotesk | `skills/proposal-creator/assets/fonts/SpaceGrotesk-var-latin.woff2`, `skills/invoice-creator/assets/fonts/SpaceGrotesk-var-latin.woff2` |
| Inter Tight | `skills/proposal-creator/assets/fonts/InterTight-var-latin.woff2`, `skills/invoice-creator/assets/fonts/InterTight-var-latin.woff2` |
| JetBrains Mono | `skills/proposal-creator/assets/fonts/JetBrainsMono-var-latin.woff2`, `skills/invoice-creator/assets/fonts/JetBrainsMono-var-latin.woff2` |

The two copies of each family are byte-identical, confirmed by sha256. If you update a font,
update both or the two document types drift apart in a way nobody notices until a client holds
a proposal and an invoice side by side.

## Why the canonical copy lives here and not in the skill folders

A licence stored only inside `skills/proposal-creator/` disappears the moment somebody deletes a
skill they do not use, and the binaries in the other skill folder are then redistributed with no
licence at all. So the licence lives one level up, in a directory that owns nothing else, and each
font directory carries a short `README.md` pointing back at it. Deleting a skill can then cost you
a pointer, never the licence.

## What the binaries are

Not the upstream originals. Each is a latin-subset variable font converted to woff2, which the
OFL permits (a Modified Version). Read out of the files themselves:

| Family | Glyphs | Variable axis | Codepoints mapped |
|---|---|---|---|
| Space Grotesk | 291 | `wght` 300 to 700, default 300 | 230 |
| Inter Tight | 482 | `wght` 100 to 900, default 400 | 231 |
| JetBrains Mono | 394 | `wght` 400 to 800, default 400 | 229 |

Two consequences worth knowing before you hit them.

**Latin only.** Roughly 230 codepoints each. A client name with a diacritic outside the subset,
or any non-latin script, renders as a missing glyph in the PDF. Check the output, do not assume.

**No Reserved Font Name.** None of the three declares one, verified by reading every `name` record
in all three files. That is why these subsets legitimately keep the names "Space Grotesk", "Inter
Tight" and "JetBrains Mono". Had any of them reserved its name, OFL condition 3 would require the
subset to be renamed, and the `@font-face` blocks in both generators would have to be renamed with
it.

## Swapping in your own display font

The generators name these families in their `@font-face` blocks
(`skills/proposal-creator/scripts/generate-proposal-html.js` and
`skills/invoice-creator/scripts/generate-invoice-html.js`), where the woff2 is read off disk and
inlined as base64. To use a font of your own, drop the woff2 in both `assets/fonts/` directories
and update both blocks.

If your replacement is not OFL, this notice stops describing what ships. Update the table, or the
repo is back to redistributing binaries whose licence nobody wrote down, which is the exact defect
this directory was created to close.
