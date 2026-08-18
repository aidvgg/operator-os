---
name: business-profile-creator
description: Update a business context profile by read-and-merge. For this operation it reads knowledge/business/operator-business-profile.json and knowledge/memory.md BEFORE asking anything, diffs field by field, and never blank-slate overwrites. Profiles for any other business write to outputs/, never knowledge/.
---

# Business Profile Creator

Create a structured business profile that captures your company's identity, offerings, positioning, and brand voice for use in AI-assisted content creation.

## Hard rules (this repo)

This started as a generic third-party interview template. It is repaired, not generic. These
five rules override every step below, including the interview script.

1. **Read before you ask.** Load `knowledge/business/operator-business-profile.json` and
   `knowledge/memory.md` in full BEFORE the first question. The existing profile is the baseline.
   The interview fills gaps and applies changes the operator states, nothing more.
2. **Diff, never replace.** Every field the operator does not change carries over byte for byte,
   including fields the question list below never asks about. Present a field-level diff (added /
   changed / unchanged) and get an explicit yes before writing. A blank-slate rebuild is a defect,
   not an option, and it is the specific failure this section exists to stop: a rebuilt profile
   silently drops every field the interview does not ask about, and nobody notices until a
   downstream draft is missing a positioning line nobody remembers writing
   (`knowledge/ops/os-roadmap.md` carries the ruling).
3. **Prices and positioning are mirrored here, never authored here.** Pricing authority is
   `knowledge/business/outbound-offer.md` for the outbound offer, plus the client roadmap file in
   `knowledge/clients/<client>/roadmap.md` for a client engagement. If an interview
   answer conflicts with the pricing authority, stop and flag it. Never write the conflict into
   the profile.
4. **Two output paths.** This operation's own profile writes to
   `knowledge/business/operator-business-profile.json`, which is a sanctioned `knowledge/`
   write and needs the operator's explicit ask. A profile for any other business (client
   onboarding, a new brand) writes to `outputs/profiles/<slug>-profile.json` and never touches
   `knowledge/`.
5. **Independent check before save.** Spawn the `fact-check` subagent with fresh context, passing
   only the draft JSON path. It re-derives every number, price, entity and date from canonical
   files. Fix failures and re-run until `VERDICT: PASS`. This skill does not validate its own
   output, which is what it used to do.

## When to Use This Skill

- Setting up a new writing system
- Onboarding a new client
- Updating business information after pivots or changes
- Creating context for a new brand or product line

## Interview Process

### Phase 1: Company Overview

Ask these questions one at a time, waiting for responses:

1. "What is your company/brand name?"
2. "In one sentence, what do you do?" (This becomes the tagline)
3. "Why does your company exist? What's the deeper purpose?" (Mission)
4. "Where is your company heading in the next 3-5 years?" (Vision)

### Phase 2: Value Proposition

5. "What's the #1 result or transformation you help people achieve?"
6. "How do you uniquely deliver this result? What's your method or approach?"
7. "What are 3 things that set you apart from alternatives?"

### Phase 3: Offerings

8. "List your paid products/services with brief descriptions and price points"
9. "What free resources do you offer (newsletter, lead magnets, community, etc.)?"

### Phase 4: Positioning

10. "How would you describe your market position (premium, accessible, etc.)?"
11. "What category do you compete in?"
12. "What's your specific niche or area of focus?"

### Phase 5: Brand Voice

13. "How would you describe your brand's personality in 3-5 words?"
14. "What's the overall tone of your communication?"
15. "What values do you want to demonstrate through your content?"

### Phase 6: Social Proof & Platforms

16. "What are your key metrics or achievements? (subscribers, clients, revenue, features)"
17. "What do clients commonly say about working with you?"
18. "What platforms are you active on? Include handles/URLs."

### Phase 7: Content Strategy

19. "What are your 3 main content topics or pillars?"
20. "What's your primary call-to-action for content?"

## Output Format

After gathering responses, generate a JSON file following this structure:

```json
{
  "business_profile": {
    "version": "1.0",
    "last_updated": "YYYY-MM-DD",
    "company_overview": {
      "name": "",
      "tagline": "",
      "mission": "",
      "vision": ""
    },
    "value_proposition": {
      "primary_value": "",
      "unique_mechanism": "",
      "key_differentiators": []
    },
    "offerings": {
      "products": [],
      "services": [],
      "free_resources": []
    },
    "positioning": {
      "market_position": "",
      "competitor_comparison": "",
      "category": "",
      "niche_focus": ""
    },
    "brand_voice_summary": {
      "personality": "",
      "tone": "",
      "values_demonstrated": []
    },
    "social_proof": {
      "key_metrics": [],
      "testimonial_themes": [],
      "notable_clients_or_features": []
    },
    "content_pillars": {
      "primary_topics": [],
      "content_mission": "",
      "content_style": ""
    },
    "calls_to_action": {
      "primary_cta": {},
      "secondary_ctas": []
    },
    "platforms": {}
  }
}
```

## Instructions

1. Begin with: "I'll help you create your business profile. This will take about 10-15 minutes. I'll ask questions one at a time - just answer naturally."

2. Ask questions conversationally, one at a time

3. If answers are vague, ask clarifying follow-ups

4. After all questions, generate the complete JSON

5. Save per hard rule 4: this operation's own profile goes to `knowledge/business/operator-business-profile.json` (canonical, sanctioned write, explicit ask only); any other business goes to `outputs/profiles/<slug>-profile.json`. Run hard rule 5's `fact-check` pass BEFORE saving, not after.

6. Provide a summary of the key elements captured

## Best Practices

- Keep the tone professional but friendly
- Help users articulate ideas they may struggle to express
- Suggest improvements or clarifications when answers are unclear
- Check that the profile captures the unique positioning. Validation itself is hard rule 5's fresh-context `fact-check` pass, never a self-review by this skill.
