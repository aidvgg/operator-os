# Vendored craft skills

Third-party reference skills for copy, page types, CRO, SEO, design and build. This file is the
provenance and licence record for every one of them; the standard it follows is
`skills/FONT-LICENSES/NOTICE-fonts.md` (what ships, upstream, licence, copyright, modifications).

**Primary source:** https://github.com/boraoztunc/skills at ref `11dd317` (upstream state
2026-07-28), ingested 2026-08-04. That repository is an aggregate: it collects skills from several
authors and adds some of its own. Its README `## License` section says `MIT`, but at `11dd317` and
at its HEAD as read on 2026-08-18 it ships no root `LICENSE` file, and GitHub's licence detector
reports the repository as `Apache-2.0` (it does carry `LICENSE-hyperframes`, `LICENSE-mengto-skills`,
`LICENSE-liamgvchi` and an `impeccable/NOTICE.md` under Apache-2.0 for sets this repo does not
ship). So "MIT" is the aggregate maintainer's stated intent, not a licence file this repo can
reproduce, and it is recorded below as exactly that. Nothing here asserts a settled MIT licence for
a skill whose only evidence is that README word.

**Honest status line:** per-skill upstream licences for the ten skills marked "aggregate README:
MIT (unconfirmed)" below are being confirmed. Any upstream author may ask for attribution to be
corrected or for a file to be removed by opening an issue on this repository, and it will be done.

To pull a skipped skill later: clone the aggregate into a scratch directory, copy the folder in,
add a row to the table below and add the name to the CLAUDE.md vendored-library line.

## Standing rules

- **Reference-tier.** First-party doctrine wins every conflict: precedence order, voice
  (`knowledge/voice/copy-rules.md`: no em dashes, dead-easy style, lowercase on X), pricing policy,
  send authority. Several of these files model em-dash-heavy marketing copy; never carry that style
  into anything we write.
- Consumed by reading `skills/<name>/SKILL.md` when the matching work starts, same as first-party
  skills. None has a `knowledge/` write licence, none has send authority, and none of their embedded
  numbers is our pricing (pricing authority lives where CLAUDE.md says it lives).
- Some descriptions cross-reference skills that were NOT ingested (email-sequence, signup-flow-cro,
  onboarding-cro, form-cro, popup-cro, ab-test-setup). Those refs are inert here; pull the skill only
  if the need turns real.
- `web-design-guidelines` fetches its rule list from a source URL at run time; it needs network.
- The vendored copy/SEO/CRO skills read `.claude/product-marketing-context.md` before asking
  questions. That file is a router to the owner files, never a data file.

## Provenance and licence, one row per vendored item (17 skills plus one binary)

Columns: upstream repository and path as evidenced; the ingest ref; the licence as evidenced (a
licence file in this tree, a frontmatter claim, an upstream repository's own licence, or only the
aggregate README word); whether an attribution or licence file for it is present in this tree.

| Name | Upstream repository and path | Ingest ref | Licence as evidenced | Attribution file in tree |
|---|---|---|---|---|
| `ogilvy` | boraoztunc/skills `ogilvy/` (aggregate; compiled from Ogilvy's 1972 and 1983 books, holder not named) | `11dd317` | frontmatter `license: MIT`, no copyright holder named | missing (frontmatter claim only) |
| `copywriting` | boraoztunc/skills `copywriting/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `copy-editing` | boraoztunc/skills `copy-editing/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `stop-slop` | github.com/hardikpandya/stop-slop (Hardik Pandya), via the aggregate | `11dd317` | frontmatter `license: MIT`, author self-attributed in frontmatter | frontmatter only; no licence text reproduced |
| `landing-page` | github.com/MengTo/Skills `agent-skills/web-design/landing-page/` (Meng To), via the aggregate | `11dd317` | MIT, licence text in tree | present: `LICENSE-mengto-skills`, `NOTICE-mengto.md` |
| `pricing-page` | github.com/MengTo/Skills `agent-skills/web-design/pricing-page/`, via the aggregate | `11dd317` | MIT, licence text in tree | present: `LICENSE-mengto-skills`, `NOTICE-mengto.md` |
| `product-proof-saas` | github.com/MengTo/Skills `agent-skills/web-design/product-proof-saas/`, via the aggregate | `11dd317` | MIT, licence text in tree | present: `LICENSE-mengto-skills`, `NOTICE-mengto.md` |
| `operational-enterprise-ai` | github.com/MengTo/Skills `agent-skills/web-design/operational-enterprise-ai/`, via the aggregate | `11dd317` | MIT, licence text in tree | present: `LICENSE-mengto-skills`, `NOTICE-mengto.md` |
| `page-cro` | boraoztunc/skills `page-cro/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `seo-audit` | boraoztunc/skills `seo-audit/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `schema-markup` | boraoztunc/skills `schema-markup/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `analytics-tracking` | boraoztunc/skills `analytics-tracking/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `visual-style-presets` | boraoztunc/skills `visual-style-presets/` (written by the aggregate's author to replace 19 upstream palette dumps) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `make-interfaces-feel-better` | boraoztunc/skills `make-interfaces-feel-better/` (aggregate; at HEAD the aggregate's `NOTICE-jakubkrehel.md` names a successor skill `better-ui` sharing this skill's `surfaces.md`, `animations.md`, `performance.md`, licensed under its `LICENSE-jakubkrehel`; that statement post-dates the ingest ref) | `11dd317` | aggregate README: MIT (unconfirmed); a later upstream notice points at a jakubkrehel licence not reproduced here | missing |
| `web-design-guidelines` | frontmatter `author: vercel`; the rule source it fetches at run time is github.com/vercel-labs/web-interface-guidelines (MIT per GitHub API, read 2026-08-18); the SKILL.md itself came via the aggregate | `11dd317` | upstream repository MIT; the wrapper's own licence: aggregate README MIT (unconfirmed) | missing |
| `tailwind-v4` | boraoztunc/skills `tailwind-v4/` (written for the aggregate to replace a v3-only upstream skill) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `app-store-screenshots` | boraoztunc/skills `app-store-screenshots/` (aggregate; earlier origin not recorded at ingest) | `11dd317` | aggregate README: MIT (unconfirmed) | missing |
| `app-store-screenshots/mockup.png` (binary, 95,347 bytes) | shipped inside the aggregate's `app-store-screenshots/` folder; the SKILL.md calls it "a pre-measured iPhone mockup"; author of the image not recorded anywhere upstream that was read | `11dd317` | unknown; covered only by the aggregate README word if at all | missing |

Ten skills carry the "aggregate README: MIT (unconfirmed)" mark: `copywriting`, `copy-editing`,
`page-cro`, `seo-audit`, `schema-markup`, `analytics-tracking`, `visual-style-presets`,
`make-interfaces-feel-better`, `tailwind-v4`, `app-store-screenshots`. Six of them
(`copywriting`, `copy-editing`, `page-cro`, `seo-audit`, `schema-markup`, `analytics-tracking`)
share a `version: 1.0.0` frontmatter shape and cross-reference each other, so they most likely
entered the aggregate as one set from a single earlier author; that origin was not recorded at
ingest and is not asserted here. If you redistribute this repo, or sell anything built on it, treat
those rows as open until the upstream licence is confirmed, and drop the folders you do not need.

## What each one is for

**Copy and positioning** (own site, lead magnets, outbound assets)
- `ogilvy` - Ogilvy's advertising principles: positioning, headlines, promises, long-form copy.
- `copywriting` - page-copy method for homepage / landing / pricing / feature pages.
- `copy-editing` - systematic multi-pass editing of existing marketing copy.
- `stop-slop` - strips predictable AI writing patterns. Where it and `knowledge/voice/copy-rules.md`
  differ, the first-party voice file wins.

**Page types** (own site rewrite, productizing an internal build, client-facing product pages)
- `landing-page` - single-intent landing IA, layout archetypes, headline formulas, SEO/AEO.
- `pricing-page` - value-metric pricing IA, plan design, FAQs, experiments.
- `product-proof-saas` - honest AI-product demo pages: real state models, no faked generation
  speed. Matches a positioning built on proof rather than claims.
- `operational-enterprise-ai` - enterprise-buyer IA: permissions, approvals, audit, rollback as a
  data model. For any client surface sold to a buyer who has to answer for it internally.

**CRO, SEO, measurement**
- `page-cro` - conversion review of marketing pages.
- `seo-audit` - technical / on-page SEO diagnosis.
- `schema-markup` - JSON-LD structured data for rich results and AEO.
- `analytics-tracking` - GA4 / GTM event and conversion tracking plans.

**Design and build** (client UIs, own site, polishing a shipped app)
- `visual-style-presets` - nine complete style directions with token blocks and one signature motif
  each; the direction-picker.
- `make-interfaces-feel-better` - design-engineering micro-detail principles, with typography /
  surfaces / animations / performance reference files.
- `web-design-guidelines` - terse file:line UI-code review against Vercel's Web Interface Guidelines.
- `tailwind-v4` - v4 CSS-first config, `@theme` tokens, v3-to-v4 migration diffs, dynamic-class
  safety.

**Store releases**
- `app-store-screenshots` - programmatic App Store screenshot pages in Next.js, with the bundled
  `mockup.png` phone frame. Trigger: a client mobile app going out to the stores.

## Deliberately skipped, with reasons

- `frontend-design`, `vercel-react-best-practices` - already provided as installed plugins in the
  Claude Code environment (frontend-design, vercel:react-best-practices); an in-repo second copy
  would drift against them.
- `content-strategy` - this repo owns content strategy in `knowledge/voice/`; a generic planner
  would fight settled doctrine.
- `adversarial-review` - covered by the built-in `/code-review` plus the installed review skills.
- HyperFrames family, 16 skills (hyperframes, -cli, -media, -registry, website-to-, remotion-to-,
  contribute-catalog, gsap, animejs, waapi, css-animations, lottie, three, typegpu, tailwind) -
  HTML-to-video framework; no programmatic-video motion today. Apache-2.0 under the aggregate's
  `LICENSE-hyperframes`. Revisit if video content stops being hand-recorded.
- One-trick visual effects (beautiful-shadows, glass-dark-ui, skeuomorphic-ui, container-lines,
  framed-grid-layout, corner-diagonals, css-border-gradient, progressive-blur,
  mesh-gradient-dark-blue-clean, liquid-metal-border, beam-glow-states, reveal-hover-effect,
  staggered-word-reveal, webgl-laser, thinking-orbs) - garnishes to pull one at a time once a build
  commits to a direction; `visual-style-presets` carries the direction decision.
  `shaders-cursor-ripples` additionally depends on a paid non-OSS library.
- `impeccable` (63-file command suite, Apache-2.0 under its own NOTICE upstream), `emil-design-eng`
  (679-line philosophy file), `apple-design` - overlap the kept design set and the installed
  frontend-design plugin.
- `programmatic-seo`, `competitor-alternatives` - no scaled-pages play and no named-competitor
  sales motion.
- `service-booking-flow` - consumer booking-funnel recipe; this operation sells back-office
  plumbing, not front-of-house booking pages.
- `documentary-brutalist-agency`, `editorial-portfolio-chapters` - site-genre recipes that fight a
  technical, infrastructure-shaped positioning.
- `minimal-zine-poster` - image generation via a separate provider API, off-stack.
- `linear-local-first-architecture`, `conductor-rewrite-performance` - solid engineering references
  with no local-first or desktop motion in flight; the nearest future consumer is client-app
  instant-feel work. Pull when that lands.
