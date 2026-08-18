---
name: prospect-brief
description: "Turn a name or a profile URL into a decision-ready brief on an outbound prospect: profile, site and social read in parallel via the agent-hands scripts, the qualification ladder in outputs/outbound/prospect-gate.md applied as written, a pain-bank match, and opener prep. Trigger on 'brief this prospect', 'triage these accepts', 'screen this batch', 'is this inbound worth a reply'. Use for post-accept triage (ICP/SKIP), pre-send screening (SEND/FILL/KILL), and inbound triage (corridor/unknown/DQ). Output goes to outputs/outbound/briefs/. No knowledge write licence, no send authority."
---

# prospect-brief

**What this is:** one command that turns a name or a profile URL into a decision-ready brief on a
prospect: who they are, what they run, whether they pass the gate, what to say in the opener, and
what they will likely push back with. It replaces the tab-hopping that otherwise sits between a
prospect landing in your outreach list and a message actually going out.

**When to run it:**
- **Post-accept triage.** A connection was accepted and needs an `ICP` / `SKIP` verdict before you
  spend real time on a personalized opener.
- **Pre-send screening.** A batch of profiles needs `SEND` / `FILL` / `KILL` verdicts before
  connection requests go out.
- **Inbound triage.** Someone replied, commented, or asked for a lead magnet and needs
  `corridor` / `unknown` / `DQ` before anything is spent on them.

State which moment you are in before you start, because they yield different verdict vocabularies
and the output must carry the right one.

**The gate always emits SEND / FILL / KILL.** The table translating those three into each moment's
vocabulary, and the rule governing the FILL row, are owned by `outputs/outbound/prospect-gate.md`.
Read them there and apply them exactly as written.

They are deliberately not restated here. This skill is the satellite, the gate is the owner, and a
satellite copy of a rule is the copy that goes stale the first time the gate is tuned. That is the
one-owner rule in `CLAUDE.md` applied to a rule rather than to a number. If this file and the gate
ever disagree, the gate wins and this file is what gets corrected.

**The reachability check does not run post-accept.** It exists to avoid spending a read on a profile
you cannot reach, and the connection already went through. Record it as "moot, already accepted" and
move on to the first scoring layer.

## Hard rules

1. **This skill never sends anything.** It writes a brief. The CLAUDE.md pre-send checklist, item 7,
   binds: the operator sends, on that specific artifact, however clean the checks came back.
2. **It never composes new outreach copy while a copy freeze holds.** When the outbound motion has
   frozen its copy (the freeze and its release condition are declared in
   `knowledge/business/outbound-offer.md`), the opener, the follow-up and any delivery message are
   read VERBATIM from `templates/message-templates.md` and only the bracket slots are filled. If a
   brief seems to need a new line of copy, the answer is that it does not. A freeze exists so the
   reply rate is measuring one message, not a hundred small rewrites.
3. **`outputs/outbound/prospect-gate.md` owns the qualification rules.** Read it every run and apply
   its ladder as written. Never invent a scoring weight, never add a kill it does not name. It is a
   boolean ladder, not a point score. Do not paste the rulebook into a brief; DO name each tell that
   fired with the evidence that fired it, which is what makes the verdict auditable. Naming a tell is
   citing the rule, not restating the rulebook.
4. **Never disqualify on a number no profile shows.** Revenue, headcount and client volume are call
   qualifiers, not connect filters. A profile page shows none of them, so pushing a financial
   qualifier upstream of the calendar disqualifies people on a guess. If a brief wants to estimate
   revenue, it stops and says unknown.
5. **Tooling is not a disqualifier.** A prospect already paying for a tool in the category has
   already priced the pain. So has the owner who built their own janky internal system. Both are
   tells that they take the problem seriously, not reasons to walk away.
6. **Only hard kills kill. Tells score.** A single tell is a note, never a verdict. Record the tell
   count next to the verdict so the ratio stays auditable.
7. **Prices come from the authority.** If a brief names a number it comes from
   `knowledge/business/outbound-offer.md`, or from the client roadmap file when the number is a
   client engagement's. Check `ai/TOMBSTONES.md` before writing any price: retired figures are
   blocked by `repo-doctor` for a reason, and a dead price in a prospect brief is one copy-paste
   away from being quoted at someone.
8. **Write briefs to `outputs/outbound/briefs/<slug>-<YYYY-MM-DD>.md`, never to `knowledge/`.** A
   brief is a deliverable, not state. It has no `knowledge/` write licence.

## Inputs

Minimum: a profile URL or slug. Useful extras if known: their X handle, their company website, and
which moment (post-accept, pre-send, inbound) this is.

## Steps

**0. Check whether the repo already ruled on this person.** `grep -ril "<name>"` and the profile slug
across `outputs/outbound/` and `knowledge/`. Earlier triage artifacts hold per-prospect verdicts that
no tool surfaces. A brief that silently re-derives a settled verdict wastes a cycle; one that silently
contradicts it is the stale-satellite failure the one-owner rule exists to prevent. If a prior verdict
exists, the brief RECONCILES with it: agree and say so, or disagree and say exactly which new evidence
moved it.

**1. Gather, in parallel.** These are independent reads, so run them concurrently:
- `scripts/li-fetch <url-or-slug> --json` for the profile: headline, current company, about,
  experience, education, follower and connection counts.
- The company website. The profile record usually names a company but no domain, so **resolve the
  domain by search and confirm the site is actually theirs before scoring a word of it.** Guessing
  `<company>.com` is how a brief ends up scoring a parked domain-sale page as "no team, no sites, no
  process" and killing a live prospect on it. This is a known failure of the guess, not a caution
  about one: a parked domain one letter away from the live one reads as a dead business. Once
  verified: what they sell and to whom, how many sites or locations the copy names, whether a change
  signal is visible (an ops or admin role open, a new location, a system switch), and whether the
  copy describes a process a person is holding together by hand.
- `scripts/x-fetch <handle>` if an X handle is known. Recent posts are the highest-signal read for
  what they actually complain about.

Record what you could NOT resolve. A brief that hides its gaps is worse than a short one.

**When the roles panel comes back empty.** The profile provider returns null position and experience
fields on some profiles, and `scripts/li-fetch` says so explicitly instead of printing a bare dash.
That panel is load-bearing twice over: the "is this actually the owner" kill and the second-current-role
tell both read it. A null panel is a gap in the record, never evidence of a thin profile. Resolve the
title another way, in this order: the record's current-company object, the search-engine-indexed
profile title, the employer's own about or team page (is the prospect listed, and who is named as
founder), then any prior repo triage. If none of them resolve who this person works for, say the
verdict is deferred rather than guessing. The wrong-person kill is the highest-frequency kill in any
gate and the most expensive one to get wrong in either direction.

**Read activity, not authored posts, for dormancy.** `li-fetch` prints these as separate blocks. The
posts array holds authored articles that are often years old on a daily-active account; the activity
block carries dated likes and comments. Scoring dormancy off authored posts turns "active yesterday"
into "six years dead". Also ignore the country subdomain in a profile URL as a location signal: it
reflects the provider's exit node, not the prospect, and the same profile can come back under three
different country subdomains in three consecutive calls, which is why `li-fetch` canonicalizes it.

**2. Run the gate.** Open `outputs/outbound/prospect-gate.md` and walk it in the order it defines:
reachability first, then the hard kills (any hit kills, and you name which row fired), then the scored
tell sections, then the final ladder, first match wins. Report the verdict with the exact ladder line
that produced it, plus the per-section tell counts.

Where a kill row turns on a judgment call, ask the question the gate itself asks, out loud, and record
the answer with its evidence. A kill that was reached by reading the row's intent is auditable; one
that was reached by pattern-matching the row's title is not.

**3. Map the pain.** `knowledge/pain-points/pain-point-bank.md` and its `.csv` twin are the source.
Name the one or two entries whose mechanism matches what this prospect actually runs, and say why. Do
not force a match: "no bank entry fits, the nearest is X and here is how it differs" is a real answer
and more useful than a stretch. The bank is authoritative and read-only here; never edit it to fit a
prospect.

**4. Prepare the opener.** Only for a post-accept `ICP` verdict.
- Render the locked opener from `templates/message-templates.md` verbatim, with the bracket slots
  filled. Do not rewrite a single word of it while the freeze holds.
- Add delivery notes for THIS prospect: what they run, and the one specific thing worth knowing so the
  message reads like it was made for them rather than read off a card. The copy is fixed; the
  personalization lives in the detail you cite, not in new sentences.
- Name the likely objections and quote the send-safe response from whichever file the outbound motion
  keeps them in. If no owner file carries a response for an objection you expect, say so plainly. Do
  not write new objection handling here.

**5. Write the brief** to `outputs/outbound/briefs/<slug>-<YYYY-MM-DD>.md` using the template below,
then tell the operator the verdict in one line. Do not paste the whole brief into chat.

## Output template

```
# <Name> - prospect brief <YYYY-MM-DD>

**Moment:** post-accept triage | pre-send screening | inbound triage
**Verdict:** <ICP|SKIP> or <SEND|FILL|KILL> or <corridor|unknown|DQ>
**Gate verdict:** <SEND|FILL|KILL>, translated by the mapping table
**Produced by:** hard kill row <n>, converted by ladder line 1  /  or: ladder line <n>
**Prior repo verdict:** <none found | the verdict, its file:line, and agree/disagree>

## Who
<one paragraph: person, company, what they actually sell, to whom>
Profile: <url> | Site: <url or none found> | X: <handle or none found>

## Gate
Reachability: <pass | gated, do not spend a read | moot, already accepted>
Hard kills: <clean | row N fired, the evidence>
Tells by section: <section> n | <section> n | ...
  <one line per tell, with the evidence that produced it>
Sections failing: <list or none>
Steelman: <if a hard kill decided it, score the tells anyway on the most generous reading
  and say where that path lands. A verdict that survives its own steelman is worth more
  than one that was never tested, and it costs one paragraph.>

## Pain match
<bank entry name and why it fits, or the honest near-miss>

## Opener prep (ICP verdicts only)
Locked copy, slots filled:
<verbatim from the owner file>
Delivery notes: <what to know so the message is for them>
Likely objections: <objection -> quoted send-safe line, or "no owner line exists">

## Unresolved
<what could not be read, and what it would change if known>
```

## What this skill must never do

- Send, DM, connect, comment, or post. It has no send authority, ever.
- Write into an outreach tracker, CRM or sheet that lives outside this repo. Those are the operator's
  to write by hand. An agent that inherited the wrong working directory once overwrote a live tracker
  file, and the read rail has stayed read-only since.
- Write into `knowledge/`. It has no write licence there.
- Invent a revenue estimate, a headcount, or a client count that no source states.
- Produce new opener, follow-up, or delivery copy while the freeze holds.
- Quote a price that is not in `knowledge/business/outbound-offer.md` or the client's roadmap file.
