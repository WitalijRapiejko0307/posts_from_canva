# Plan: create Instagram carousels in Canva

**Document date:** 02.10.26

Text for this cycle is already in [`material/carousel.json`](../material/carousel.json) and [`material/description.json`](../material/description.json), prepared by [`plan-podgotovki-teksta-karuseli.md`](plan-podgotovki-teksta-karuseli.md).

Use the same `POST_COUNT` and `SLIDE_COUNT` as in that text-prep run. Do not assume 5 posts or 8 slides.

---

## Parameters

Taken from the text-prep cycle. Do not invent new counts here.

| Parameter | Meaning |
|-----------|---------|
| `POST_COUNT` | How many carousels to build (ids `1` … `POST_COUNT` in the JSON files) |
| `SLIDE_COUNT` | Slides per carousel, including the hook and the closing CTA |

---

## Fixed inputs

| What | Value |
|------|--------|
| Source designs | latest Instagram-post carousels in Canva |
| Copy name | `{source title} {today}` with date **DD.MM.YY** (example: source `09.09.26`, today `10.09.26` → copy **`10.09.26`**) |
| Slide size | 1080 × 1350 px |
| Text block width | 864 px |
| Font on slides 2 … `SLIDE_COUNT` | **52**, center aligned |
| Account | **vitali_rapeika** |
| Slide text | [`material/carousel.json`](../material/carousel.json) |
| Captions | [`material/description.json`](../material/description.json) |

Slide 1 is the hook. The last slide is the CTA, including `@vitali_rapeika`.

---

## 1. Find the source design

1. Open Canva through MCP.
2. Search the latest Instagram-post designs: `search-designs` with `sort_by: modified_descending` and `limit: 3–5`.
3. Pick a design that has **`SLIDE_COUNT` slides**. It is usually the most recently modified carousel.

Repeat for each of the `POST_COUNT` carousels. Each copy needs its own source with `SLIDE_COUNT` slides.

---

## 2. Create a copy

1. Call `copy-design` with the source `design_id`.
2. Name the copy `{source title} {today}` using **DD.MM.YY**.
3. The original stays unchanged. All edits go into the copy.

---

## 3. Replace text on the slides

Read slide strings from `material/carousel.json` for this carousel `id`.

1. Call `start-editing-transaction` for the copy id.
2. Keep `transaction_id` and the `pages` array.
3. For each slide, call `perform-editing-operations`:

| Slide | Action |
|-------|--------|
| 1 | `replace_text` — hook from `slides` where `slide_number` is 1 |
| 2 … `SLIDE_COUNT` | `replace_text` — that slide’s `text` |
| 2 … `SLIDE_COUNT` | `format_text` — `font_size: 52`, `text_align: center` |

Batch operations (for example three slides at a time) when one request is too large.

---

## 4. Center text blocks (slides 2 … `SLIDE_COUNT`)

1. After the text replace, take the text-block **height** from the API response (`dimension.height`).
2. Position:
   - **Horizontal:** `left = (1080 - 864) / 2 = 108` (block width 864 px).
   - **Vertical:** `top = (1350 - height) / 2` (slide height 1350 px).
3. Call `position_element` for every slide from 2 through `SLIDE_COUNT`.

---

## 5. Save the design

1. Call `commit-editing-transaction` with the same `transaction_id`.
2. Keep the finished design URL (`edit_url` from `copy-design`, or the URL after commit).
3. Repeat sections 1–5 until all `POST_COUNT` copies are saved.

---

## 6. Open every carousel in Chrome

After every copy is saved, open **each** finished carousel in Chrome — one tab per design URL **without** `/edit` at the end.

- If the API returned `edit_url` like `https://www.canva.com/design/{id}/edit`, drop the `/edit` suffix and open `https://www.canva.com/design/{id}`.
- A link with `/edit` on the id is **not readable**: the server returns **404**.
- MCP `user-chrome-devtools`: `list_pages`, then `new_page` for each carousel URL (without `/edit`).
- Expectation: the Canva session is already logged in, and the tab shows the design (`canva.com/design/…`), not the login screen.

---

## 7. Prepare the Instagram post (do not publish)

For each open carousel:

1. **Share → Instagram**. Format = **Post**, account **vitali_rapeika**.
2. Canva inserts one page by default. You need **`SLIDE_COUNT` slots**:
   - slot 1 → Page 1;
   - slots 2 … `SLIDE_COUNT`: **Add image → Choose a page → Page N**.
3. When adding a page, **do not wait for the slide to load**. Assign every carousel page for posting immediately.
4. Check: the panel has `SLIDE_COUNT` slots, “Page 1” through “Page `SLIDE_COUNT`”, and no empty “Choose a page”.
5. **Caption** — from [`material/description.json`](../material/description.json): `text` of the entry with the same `id` as the carousel. Enter it with `type_text`. **Do not publish.**

---

## 8. Checklist before posting

- [ ] `POST_COUNT` copies exist, one per id in `material/carousel.json`
- [ ] Slide 1: hook matches the JSON, no typos, quotation marks intact
- [ ] Slides 2 … `SLIDE_COUNT`: full text inserted
- [ ] Font on slides 2 … `SLIDE_COUNT`: **52**
- [ ] Text on slides 2 … `SLIDE_COUNT`: **centered** horizontally and vertically
- [ ] Last slide: CTA and `@vitali_rapeika`
- [ ] Design saved (`commit-editing-transaction` finished)
- [ ] Copy named with today’s date: **`DD.MM.YY`** (or `{source} {date}`)
- [ ] Every carousel is open in a Chrome tab
- [ ] Each carousel has pages 1 … `SLIDE_COUNT` set for an Instagram Post
- [ ] Caption filled from `material/description.json` (matching `id`)
- [ ] **Publish** has not been clicked

---

## 9. Publish to Instagram

For each open carousel:

1. **Click Publish.**
2. **Do not wait** for the post to finish publishing.

---

## Tools

| Step | Tool |
|------|------|
| Find a design | `search-designs` |
| Copy | `copy-design` |
| Start editing | `start-editing-transaction` |
| Replace, format, position | `perform-editing-operations` |
| Save | `commit-editing-transaction` |
| Discard a draft | `cancel-editing-transaction` |
| Open carousels in Chrome | `list_pages`, `new_page` (`user-chrome-devtools`) |
| Share → Instagram, slots, caption | `click`, `fill`, `type_text` (`user-chrome-devtools`) |
