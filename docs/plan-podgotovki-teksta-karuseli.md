# Plan: prepare carousel text from a Google Doc

**Document date:** 02.10.26

Repeatable cycle: take the next batch of posts above the stop marker, rewrite each as a carousel, write the JSON files, and move the marker. The next stage is [`plan-sozdaniya-karuseli.md`](plan-sozdaniya-karuseli.md).

Set **Parameters** before the cycle. Everything else in **Fixed inputs** stays the same from run to run.

---

## Parameters

Fill this table at the start of the cycle. Do not assume defaults from a previous run.

| Parameter | This run | Meaning |
|-----------|----------|---------|
| `POST_COUNT` | 10 | How many complete posts to take this cycle |
| `SLIDE_COUNT` | 8 | Slides per carousel, including hook and closing CTA |

---

## Fixed inputs

| What | Value |
|------|--------|
| Document | Google Doc **Text for carousel** |
| ID | `1WkjF2NtZGwx0ThzfoTtKg64bZfe33PSJHkBscxDHPEs` |
| URL | `https://docs.google.com/document/d/1WkjF2NtZGwx0ThzfoTtKg64bZfe33PSJHkBscxDHPEs/edit` |
| Marker | `🟢 STOP 🟢` |
| Account in the CTA | `@vitali_rapeika` |
| Caption length | at most **300** characters |
| Slide text | [`material/carousel.json`](../material/carousel.json) |
| Captions | [`material/description.json`](../material/description.json) |

**Post shape in the document:** hook headline → body → call to action (subscribe, comment, or save, usually including `@vitali_rapeika`).

---

## 1. Open the document

1. MCP `user-chrome-devtools`: `list_pages`.
2. If the doc tab is already open, `select_page` and bring it to the front.
3. If not, `navigate_page` to `https://docs.google.com/document/d/1WkjF2NtZGwx0ThzfoTtKg64bZfe33PSJHkBscxDHPEs/edit`.
4. The browser is already open in the project working folder. Do not start a new Chrome session.

The Docs editor does not expose the document body through DOM `innerText`. Read the file through Google Drive MCP:

```
read_file_content  fileId: 1WkjF2NtZGwx0ThzfoTtKg64bZfe33PSJHkBscxDHPEs
```

---

## 2. Find the marker

1. Find exactly one `🟢 STOP 🟢` in the file text.
2. If the emoji is corrupted in the Drive export, normalize it and search by the stable text inside the marker, checking neighboring lines.
3. The working area is **only the text above the marker**. Leave posts below the marker untouched.

---

## 3. Select the posts above the marker

Walk **upward** from the marker and take `POST_COUNT` complete posts. A post boundary is:

- **start:** a hook headline (often its own line or a bold paragraph);
- **end:** a CTA — subscribe, comment, save, or `@vitali_rapeika`.

JSON order is **top to bottom** in the document:

| id | Position in the batch |
|----|------------------------|
| 1 | highest of the selected posts |
| `POST_COUNT` | closest to the marker |

Skip drafts, fragments, poems without a CTA, and blocks without a headline. They do not count toward `POST_COUNT`.

---

## 4. Rewrite each post as a carousel

Each post becomes `SLIDE_COUNT` slides. Do not number the slides inside the text (`1.`, `2.`, and similar).

| Slide | What to write |
|-------|----------------|
| 1 | Rewritten hook (caps plus a subtitle on a new line is fine) |
| 2 … `SLIDE_COUNT` − 1 | Short subtitle plus a paragraph. Keep the meaning; change the wording |
| `SLIDE_COUNT` | Close the thought and ask to follow `@vitali_rapeika`. The CTA must match the post |

Match the tone of the current carousel file: direct, concrete, no bureaucratic phrasing.

The Instagram caption is a separate rewritten text, at most **300** characters, and ends with a follow of `@vitali_rapeika`.

---

## 5. Write slides to `carousel.json`

1. Open [`material/carousel.json`](../material/carousel.json).
2. **Delete every current entry** in the `carousels` array.
3. Write this cycle’s carousels in the same structure:

```json
{
  "carousels": [
    {
      "id": 1,
      "slides": [
        { "slide_number": 1, "text": "..." },
        { "slide_number": 2, "text": "Subtitle\nParagraph..." }
      ]
    }
  ]
}
```

- `id`: 1 … `POST_COUNT`
- each carousel has exactly `SLIDE_COUNT` objects in `slides`
- `slide_number`: 1 … `SLIDE_COUNT`
- line breaks inside a slide are `\n`

---

## 6. Write captions to `description.json`

1. Open [`material/description.json`](../material/description.json).
2. **Delete every current entry** in the `descriptions` array.
3. Write this cycle’s captions in the same structure:

```json
{
  "descriptions": [
    { "id": 1, "text": "..." }
  ]
}
```

Caption `id` equals carousel `id`. Each `text` is at most **300** characters.

---

## 7. Move the marker up by this batch

After the JSON is written, the marker must sit **above** the batch just processed. Those posts count as done. The next cycle again takes `POST_COUNT` complete posts immediately above the marker.

**How to move it in Google Docs (chrome-devtools):**

1. `Control+F` → find `🟢 STOP 🟢` (must be **1 of 1**).
2. Cut only that line (`Home` → `Shift+End` → `Control+X`). Do not use `Control+A`.
3. Find the headline of the top post in this batch (a unique phrase).
4. Place the cursor at the start of that headline → `Enter` → insert the marker.
5. Do not paste with `Control+V` if the clipboard may have been overwritten (Docs find and `fill` replace the clipboard). Type `🟢 STOP 🟢` with `type_text` on the empty line above the headline.
6. Do not use `Control+H` regex to insert `\n`. Docs often inserts the literal characters `\n\n` instead of a paragraph break.

Check after Docs saves (`read_file_content` again):

- there is one marker;
- unprocessed posts are above it;
- the post with id 1 of this batch is immediately below it;
- the marker is gone from its previous place.

---

## 8. Checks before the next stage

- [ ] Exactly one `🟢 STOP 🟢`
- [ ] `POST_COUNT` complete posts taken from above the marker
- [ ] Each carousel has `SLIDE_COUNT` slides and no item numbering in the text
- [ ] The last slide asks to follow `@vitali_rapeika`
- [ ] `material/carousel.json` contains only this batch (previous entries removed)
- [ ] `material/description.json` has `POST_COUNT` texts, each ≤ 300 characters, ids match
- [ ] The marker moved up by this batch, and the paragraph before the first post is clean

Next: [`plan-sozdaniya-karuseli.md`](plan-sozdaniya-karuseli.md) — Canva copies, text on slides, Instagram prep **without publishing**.

---

## Tools

| Step | Tool |
|------|------|
| Open or find the Docs tab | `list_pages`, `select_page`, `navigate_page` (`user-chrome-devtools`) |
| Read the document | `read_file_content` (`plugin-google-drive-google-drive`) |
| Find, cut, or insert the marker | `press_key`, `fill`, `type_text` (`user-chrome-devtools`) |
| Check how the marker looks | `take_screenshot` |
| Write texts | edit `material/carousel.json` and `material/description.json` |

---

## Pitfalls

| Problem | What to do |
|---------|------------|
| Docs does not return text via `innerText` | Read with Drive `read_file_content` |
| `Control+V` pasted the wrong fragment | Do not trust the clipboard; `type_text` on an empty line |
| Regex replace of `\n` produced the characters `\n\n` | Delete the literals and break the paragraph with `Enter` |
| Two markers | Keep one, above the top post of this batch |
| A block next to the marker has no CTA | Do not count it; take the next complete block with a headline and a close |
