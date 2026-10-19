# YouTube metadata preparation plan

Repeatable workflow for a parent agent. The user pastes source post text in chat. Each post becomes one video row: title, description, tags. Output is JSON only. No Google Doc. No stop marker. No browser. No carousel.

---

## Parameters

| Parameter | Meaning |
|-----------|---------|
| `POST_COUNT` | How many videos (rows) to produce this cycle. The user states this number in chat. Do not reuse a default from a previous run. |

---

## Fixed inputs

| Input | Rule |
|-------|------|
| Source posts | Exactly `POST_COUNT` complete posts from the user message, in the order given. |
| Output path | Must be exactly `material/YouTUbe/data.json` (capital **T** and **U** in `YouTUbe`). Absolute: `/home/wentel/CursorProjects/Canva/material/YouTUbe/data.json` |
| Subscribe mention | When the source asks to subscribe or follow, use `@vitali_rapeika` in the description closing line. |

---

## Field limits

| Field | Limit |
|-------|-------|
| `title` | At most 100 characters. One clear line. No hashtags. No clickbait that invents facts. |
| `description` | At most 5000 characters. First 2 lines must stand alone (they show in search). Then the body. No hashtag block required. If the source asks to subscribe, close with a reason, then subscribe / follow `@vitali_rapeika`. |
| `tags` | Array of plain strings. No `#` anywhere. 5 to 12 tags. Each tag at most 30 characters. Tags come from the topic of the source. Do not invent unrelated trending tags. |

---

## Steps

1. Read the user message. Take exactly `POST_COUNT` posts in the given order. If the count does not match, stop and ask. Do not invent posts.
2. The parent does **not** rewrite. For each post, start one Gemini 3 flash sub-agent with the prompt below unchanged, plus the source post. Check the result, then continue.
3. Write JSON. Delete every current entry in the file. Write only this cycle’s rows.

---

## JSON shape

```json
{
  "videos": [
    {
      "id": 1,
      "title": "...",
      "description": "...",
      "tags": ["tag one", "tag two"]
    }
  ]
}
```

- `id` runs from `1` through `POST_COUNT`.

---

## Contract

- Facts only from the source. No invented numbers, promises, or events.
- If the model writes `[need a fact]`, the parent must not save that token. Use the source wording instead.
- Tags must not contain `#`.

---

## Gemini prompt

Send this block unchanged, then append the source post after it.

````
You are an editor of YouTube titles, descriptions, and tags.

From the source post, write:
1. title — one line, at most 100 characters. The point of the video. Specific. No hashtags. No ALL CAPS. Invent nothing.
2. description — the first two lines state the point so they work in search. Then short paragraphs: the problem or observation, the non-obvious point, the takeaway. At most 5000 characters. No hashtag list. Invent nothing. If a detail is missing, write [need a fact].
3. tags — 5 to 12 short phrases from the topic, each at most 30 characters. Plain text. No # character.

If the source asks people to subscribe or follow, the description ends with a reason, then a subscribe line that names @vitali_rapeika. No pressure. No new promises.

Return only this shape, with real line breaks between fields:
TITLE:
...
DESCRIPTION:
...
TAGS:
- tag
````

**Append block** (after the prompt, before or with the post):

```
Plan constraints:
- One title, one description, 5 to 12 tags.
- Title ≤ 100 characters. Description ≤ 5000 characters. Each tag ≤ 30 characters.
- Tags must not contain the # character.
- Use only facts from the source.
```

Then append the full source post for that video.

---

## Parent checks after each sub-agent

- Title length ≤ 100. Description length ≤ 5000. Each tag ≤ 30 characters.
- Tag count between 5 and 12. Strip `#` if present.
- Replace any `[need a fact]` with accurate wording from the source, or omit the unsupported clause.
- Subscribe line only if the source asked for subscribe/follow.

---

## Checklist

- [ ] User gave `POST_COUNT` and exactly that many posts in order.
- [ ] One Gemini sub-agent per post; parent did not rewrite body copy.
- [ ] All field limits satisfied.
- [ ] No `#` in tags; no `[need a fact]` left in saved JSON.
- [ ] Output path is `material/YouTUbe/data.json` (not `YouTube`).
- [ ] File contains only this cycle: full replace, no leftover rows.
- [ ] `id` values are `1` … `POST_COUNT`.

---

## Tools

| Tool | Use |
|------|-----|
| User message | Read `POST_COUNT` and source posts. |
| Gemini sub-agent | Uniqualize each post into TITLE / DESCRIPTION / TAGS. |
| Edit `material/YouTUbe/data.json` | Write the final JSON array for this cycle. |

---

## Pitfalls

| Pitfall | Avoid |
|---------|--------|
| Wrong folder spelling | Use `YouTUbe`, not `YouTube`. |
| Hashtags in tags | Plain strings only; no `#`. |
| Leftover rows | Replace entire file content each cycle. |
| Count mismatch | Stop and ask if posts ≠ `POST_COUNT`. |
| Invented facts | Only source facts; fix or drop `[need a fact]`. |
| Parent rewriting | Delegate copy to Gemini; parent validates and assembles JSON. |
