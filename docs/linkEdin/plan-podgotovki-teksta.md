# Plan: prepare LinkedIn captions from chat posts

**Document date:** 18.10.26

Repeatable cycle: the user pastes source posts in the chat. Uniqualize each into one LinkedIn caption and write `captions.json`. No Google Doc, no stop marker, no browser, no carousel slides.

Set **Parameters** before the cycle. Everything else in **Fixed inputs** stays the same from run to run.

---

## Parameters

Fill this table at the start of the cycle. Do not assume defaults from a previous run.

| Parameter | This run | Meaning |
|-----------|----------|---------|
| `POST_COUNT` | _user states_ | How many captions to produce this cycle |

---

## Fixed inputs

| What | Value |
|------|--------|
| Source | Posts the user pastes in the chat for this cycle. Exactly `POST_COUNT` complete posts, in paste order |
| Output file (repo-relative) | [`material/linkEdin/captions.json`](../../material/linkEdin/captions.json) |
| Output file (absolute) | `/home/wentel/CursorProjects/Canva/material/linkEdin/captions.json` |
| Account to mention in the close | `@vitali_rapeika` |
| Link placement | The registration or site link goes in the **first comment**, not in the profile header. If the source says the link is in the profile, the caption still points to the first comment. Do not tell people to look in the profile header. |
| Caption length | At most **3000** characters (LinkedIn post limit). Prefer a readable post, not a wall of text. Hard max 3000 |

---

## 1. Read the user message

1. Read the user message for this cycle.
2. Take exactly `POST_COUNT` source posts in the order given.
3. If the user gave fewer or more than `POST_COUNT`, stop and ask. Do not invent posts.
4. Treat each pasted block as one complete post. Preserve order for JSON `id` assignment.

---

## 2. Uniqualize each post

The parent agent does **not** rewrite the text itself.

For each source post:

1. Start one **Gemini 3 flash** sub-agent.
2. Pass the English prompt below **unchanged**, then the source post and the plan constraints from **Append after the prompt**.
3. Check the result against the **Contract for each caption** below.
4. If the sub-agent returned `[need a fact]`, do not write that into JSON. Pull the detail from the source or keep the source wording for that line.
5. Continue until all `POST_COUNT` captions pass the contract.

### Contract for each caption

- Same facts as the source. Do not invent numbers, promises, names, or events.
- Direct, concrete tone. Suitable for LinkedIn (professional, first person or the source voice). Not an Instagram carousel. No slide numbering.
- One post, not a thread of slides.
- Open with a strong first line. Keep the meaning of the source. Remove filler.
- End with a reason, then a light CTA that fits the post (comment, or follow `@vitali_rapeika` when the source asks to follow). Do not add a follow CTA if the source has no follow ask; if the source has a follow/subscribe ask, use `@vitali_rapeika`.
- If the source points to a registration or site link, the caption says that link is in the **first comment**. Do not place that link in the caption body, and do not send people to the profile header.
- At most **3000** characters.
- If a concrete detail is missing, the sub-agent may mark `[need a fact]`. The parent must not write `[need a fact]` into the JSON.

### Gemini prompt

Pass the prompt below unchanged, then the source post and the append block.

```
You are an editor of strong LinkedIn posts.

Rewrite the source post into one LinkedIn caption.
Keep every fact. Invent nothing. If a specific detail is missing, write [need a fact].
Open with one strong line that states the point. Then the body: the problem or observation, the non-obvious point, a concrete takeaway. Short paragraphs. No hashtags. No emoji spam. No clichés, cheap clickbait, or exaggeration.
Close with a reason, then one natural action that matches the source (comment, or follow). No pressure and no new promises.
Return only the finished caption. No title, no labels, no slide numbers.
```

**Append after the prompt:**

```
Plan constraints:
- Return exactly one caption.
- At most 3000 characters.
- If the source asks people to follow or subscribe, the last lines ask to follow @vitali_rapeika, reason first, then the action.
- If the source points to a registration or site link, the caption says the link is in the first comment. Do not put the URL in the caption. Do not say the link is in the profile or the profile header.
- Do not use hashtags.
```

---

## 3. Write JSON

1. Open [`material/linkEdin/captions.json`](../../material/linkEdin/captions.json) (create the file and directory if missing).
2. **Delete every current entry** in the `captions` array.
3. Write **only** this cycle’s captions:

```json
{
  "captions": [
    { "id": 1, "caption": "..." }
  ]
}
```

- `id`: 1 … `POST_COUNT`, same order as the user pasted the posts
- `caption`: the uniqualized LinkedIn post

---

## Checklist before done

- [ ] `POST_COUNT` captions
- [ ] ids 1 … `POST_COUNT`
- [ ] each caption ≤ 3000 characters
- [ ] no `[need a fact]` in any caption written to JSON
- [ ] facts match the source
- [ ] file contains only this batch (previous entries removed)
- [ ] no hashtags
- [ ] a registration or site link is pointed to the first comment, not the profile header, and the URL is not inside the caption

---

## Tools

| Step | Tool |
|------|------|
| Read source posts | Parent reads the user message in chat |
| Rewrite each post | Gemini sub-agent with the prompt in step 2 |
| Write captions | Parent edits `material/linkEdin/captions.json` |

---

## Pitfalls

| Problem | What to do |
|---------|------------|
| Fewer posts than `POST_COUNT` | Stop and ask the user; do not invent posts |
| More posts than `POST_COUNT` | Stop and ask which `POST_COUNT` to use, or ask for a corrected count |
| Leftover captions from the previous run | Clear the `captions` array before writing this batch |
| Hashtags added by the sub-agent | Remove hashtags before writing JSON |
| Invented facts in the rewrite | Reject or fix from the source; do not publish invented details |
| `[need a fact]` left in output | Resolve from the source; never write the marker into JSON |
| Link sent to the profile header | People look in the wrong place | The caption says the link is in the first comment. Do not write “in the profile” or put the URL in the caption |
