# Fonts for the invoice generator

Three latin-subset variable woff2 files.
`skills/invoice-creator/scripts/generate-invoice-html.js` reads them off disk and inlines each
one as a base64 `@font-face` src, so a generated invoice renders identically on a machine that
has never installed these fonts.

| File | Family | Used for |
|---|---|---|
| `SpaceGrotesk-var-latin.woff2` | Space Grotesk | display type, headings, the wordmark |
| `InterTight-var-latin.woff2` | Inter Tight | body copy |
| `JetBrainsMono-var-latin.woff2` | JetBrains Mono | labels, amounts, the wire table |

## Licence

All three are licensed under the **SIL Open Font License 1.1**. They are redistributed with this
template, so the licence and the copyright notices are part of what ships:

- Licence text: `skills/FONT-LICENSES/OFL-1.1.txt`
- Provenance, copyright notices, versions, what the subsets contain: `skills/FONT-LICENSES/NOTICE-fonts.md`

The canonical copy lives up there rather than in this directory on purpose. The same three fonts
also ship under `skills/proposal-creator/assets/fonts/`, byte-identical. If the only licence copy
sat inside a skill folder, deleting a skill you do not use would strip the licence off binaries
that are still being redistributed by the other one.

Replacing these fonts means updating `skills/FONT-LICENSES/NOTICE-fonts.md` too. A notice that
describes fonts the repo no longer ships is worse than no notice, because it reads as verified.
