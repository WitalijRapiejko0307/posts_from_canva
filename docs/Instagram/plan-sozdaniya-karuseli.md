# Plan: prepare the Instagram post and publish

**Document date:** 02.10.26

The carousels for this cycle are already created by [`plan-podgotovki-teksta-karuseli.md`](plan-podgotovki-teksta-karuseli.md). **All 10 designs are already open in the browser** (one tab per design, URL without `/edit`).

Use the same `POST_COUNT` and `SLIDE_COUNT` as in that run. Do not assume 5 posts or 8 slides. This plan only prepares each post and clicks **Publish**.

**Sub-agents:** use **Composer 2.5**. Give each sub-agent clear instructions: which open tab, `SLIDE_COUNT`, the caption for that `id`, and the steps below. **One sub-agent = one post.** Enter text with `type_text`. The parent does not type captions or click Share itself.

Put this scope in every Composer instruction, unchanged:

```
Scope: do only this one open carousel: Share → Instagram, assign the pages, type the caption, click Publish. Do not study the history of previous iterations, earlier chats, or earlier batches. Do not open or follow any other plan, including plan-podgotovki-teksta-karuseli.md. Do not search the repo for other workflows. Do not rewrite slides or create a new design. Return when Publish is clicked.
```

---

## Parameters

Taken from the text-prep cycle. Do not invent new counts here.

| Parameter | Meaning |
|-----------|---------|
| `POST_COUNT` | How many open designs to post (ids `1` … `POST_COUNT`) |
| `SLIDE_COUNT` | Pages to assign on each post, including the hook and the closing CTA |

---

## Fixed inputs

| What | Value |
|------|--------|
| Designs | already open in Chrome, one tab each |
| Account | **vitali_rapeika** |
| Captions | [`material/Instagram/description.json`](../../material/Instagram/description.json) |

---

## 1. Prepare the Instagram post

For each open carousel, one Composer 2.5 sub-agent:

1. Select that design’s tab (`list_pages` → `select_page`).
2. **Share → Instagram**. Format = **Post**, account **vitali_rapeika**.
3. Canva inserts one page by default. You need **`SLIDE_COUNT` slots**:
   - slot 1 → Page 1;
   - slots 2 … `SLIDE_COUNT`: **Add image → Choose a page → Page N**.
4. When adding a page, **do not wait for the slide to load**. Assign every carousel page for posting immediately.
5. Check: the panel has `SLIDE_COUNT` slots, “Page 1” through “Page `SLIDE_COUNT`”, and no empty “Choose a page”.
6. **Caption** — `text` from `material/Instagram/description.json` for the same `id` as the carousel. **Input text using `type_text`.**

---

## 2. Publish

On that same open carousel:

1. **Click Publish.**
2. **Do not wait** for the post to finish publishing.

Repeat until every open design has been published by its own sub-agent.

---

## 3. Checklist

- [ ] All designs were already open in the browser before this plan started
- [ ] Each post was handled by its own **Composer 2.5** sub-agent
- [ ] Each carousel has pages 1 … `SLIDE_COUNT` set for an Instagram Post
- [ ] Caption filled with `type_text` from `material/Instagram/description.json` (matching `id`)
- [ ] **Publish** was clicked on every post
- [ ] Publishing was not awaited

---

## Tools

| Step | Tool |
|------|------|
| One post | **Composer 2.5** sub-agent with clear instructions |
| Find the open tab | `list_pages`, `select_page` (`user-chrome-devtools`) |
| Share → Instagram, slots | `click` (`user-chrome-devtools`) |
| Caption | `type_text` (`user-chrome-devtools`) — input text using `type_text` |
