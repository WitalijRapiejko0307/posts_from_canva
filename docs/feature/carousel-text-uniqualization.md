# Feature: stronger carousel uniqualization (variant B)

**Status:** implemented in [`docs/plan-podgotovki-teksta-karuseli.md`](../plan-podgotovki-teksta-karuseli.md), step 4 and the checks in step 8.

**Target plan:** [`docs/plan-podgotovki-teksta-karuseli.md`](../plan-podgotovki-teksta-karuseli.md)

## What stays the same

The cycle does not change: posts above `🟢 STOP 🟢` → rewrite → `material/carousel.json` and `material/description.json` → move the marker.

- `POST_COUNT` and `SLIDE_COUNT` still come from **Parameters**.
- Steps 1–3 and 5–8 stay as written.
- Output is still the two JSON files in `material/`. No intermediate uniqualized payload.
- Last slide still asks to follow `@vitali_rapeika`.
- Instagram caption is still a separate text, at most 300 characters, ending with a follow of `@vitali_rapeika`.
- Slide text has no item numbering (`1.`, `2.`, and similar).

## What changes

Only **step 4**. Split it into a short contract (owned by the parent agent) and an English prompt (owned by a Gemini sub-agent). The parent does not rewrite the carousel itself. It launches Gemini once per post, checks the result against the contract, and writes JSON in steps 5–6.

If a slide contains `[need a fact]` (the prompt’s marker when the source has no concrete detail), the parent does not publish that placeholder. It pulls the missing detail from the source post or keeps the source wording for that line.

## Step 4 contract (parent)

Each post becomes exactly `SLIDE_COUNT` slides.

| Slide | Contract |
|-------|----------|
| 1 | One strong thought, at most 10 words. Caps plus a subtitle on a new line is fine |
| 2 … `SLIDE_COUNT` − 1 | One thought per slide, at most 40 words. Short subtitle plus a paragraph is fine |
| `SLIDE_COUNT` | Close the thought, then ask to follow `@vitali_rapeika`. The CTA must match the post. Reason first, then the action |

Also:

- Use only facts from the source post. Do not invent numbers, promises, or events.
- Tone stays direct and concrete.
- The caption is separate: at most 300 characters, ends with a follow of `@vitali_rapeika`.

## Gemini sub-agent

For each selected post, the parent starts a Gemini sub-agent and passes:

1. The prompt below, unchanged.
2. The source post text.
3. `SLIDE_COUNT`.
4. The CTA account `@vitali_rapeika`.
5. The three plan constraints appended after the prompt (slide count, account, caption). Those three lines are not in the editor brief; without them the JSON contract breaks.

Gemini returns only the finished slides plus one caption. The parent maps that text into the JSON shapes in steps 5 and 6.

### Prompt (pass in English)

```
You are an editor of strong social carousels.

1. First-slide text
Requirements: Up to 10 words. The hook is one strong thought. Options: contrast, an unexpected conclusion, a benefit, a myth, a hidden cause. The hook must stop the scroll and make the reader want to open the second slide. Specifics matter more than pretty phrasing. No clichés, cheap clickbait, or exaggeration. Do not invent facts, numbers, or promises.

2. Text for slides from 2 through the one before the last
Build a strong carousel on the topic you set in the first slide.
You already wrote the scroll-stopping hook. A recognizable problem. The main mistake or cause. A non-obvious conclusion that changes the view. A concrete solution.
An example of how to apply it.
A CTA that continues the carousel logically (you will write that separately).
One slide = one strong thought. Each slide should create interest in the next. The text is short, concrete, and easy to read on a phone.
For each of these slides: up to 40 words.
Use only the facts provided. If a specific detail is missing, write [need a fact]. Invent nothing.

3. CTA text (last slide)
Write a CTA for the last slide of the carousel.
Main takeaway: [what to remember]
Action: [save / send / write / get the material / go to the product / follow]
What the person gets: [result or material]
Requirements: The CTA continues the carousel logically. Reason first, then the action. No pressure, manipulation, or a bare "follow me". No new promises. Short, concrete, natural.

4. Edit the carousel text so it is stronger, sharper, and easier to read.
Strengthen: Remove repetition, filler, and long lead-ins. Replace abstractions with specifics from the source. Strengthen titles and opening lines.
One slide = one strong thought. Add contrast when it is already in the text.
Make the transitions logical. Keep the meaning, the facts, and the style of the original. Return only the finished text, slide by slide.
```

### Constraints to append (plan contract)

```
Plan constraints:
- Return exactly SLIDE_COUNT slides. Slide 1 is the hook. The last slide is the CTA.
- The last slide must ask to follow @vitali_rapeika. Keep the reason-then-action shape from section 3.
- Also return one Instagram caption, at most 300 characters, ending with a follow of @vitali_rapeika. The caption is not a slide.
- Do not number slides inside the text.
```

Replace `SLIDE_COUNT` with the number from **Parameters** before sending.

## Checks to add in step 8

- [ ] Each carousel was rewritten by the Gemini sub-agent with the prompt in this note
- [ ] Slide 1 is at most 10 words
- [ ] Slides 2 … `SLIDE_COUNT` − 1 are at most 40 words each
- [ ] No slide contains `[need a fact]`
- [ ] Facts in the slides are present in the source post

Existing checks in the plan stay in force.
