# Plan: enter YouTube publish data in Canva

**Document date:** 18.10.26

Repeatable checklist for filling the YouTube publish panel on designs that are **already open** in the browser (one tab per design, user logged in). Metadata was prepared in the prior run [`plan-podgotovki-teksta.md`](plan-podgotovki-teksta.md); use **`POST_COUNT` from that run**. JSON lives at [`../../material/YouTUbe/data.json`](../../material/YouTUbe/data.json). Ids `1..POST_COUNT` must match open Canva design tabs **in the same order** (tab order = id order). Each row has `title`, `description`, and `tags` (array of plain strings, no `#`).

**Start here:** designs are open; do **not** search Canva, copy designs, edit slides, or open new tabs.

Set **Parameters** before the run. Everything else in **Fixed inputs** stays the same from run to run.

---

## Parameters

| Parameter | Meaning |
|-----------|---------|
| `POST_COUNT` | Number of design tabs in this batch; must equal `videos.length` in JSON (from the text-prep run) |

---

## Fixed inputs

| Field | Rule |
|-------|------|
| **Title** | From `videos[].title` for that `id` |
| **Description** | From `videos[].description` for that `id` |
| **Tags** | From `videos[].tags`; enter as plain text, **no `#` character** |
| **Visibility** | **Public** |
| **Publish** | Click **Publish** once per tab **after** all tabs pass check (step 5) |

---

## Steps

**Role split (fixed):** The **parent** owns the browser and performs **all** `user-chrome-devtools` actions (`list_pages`, `select_page`, `click`, `fill`, `type_text`, `take_snapshot`). **Composer 2.5 sub-agents do not browse or click.** After the parent fills one tab, the parent pastes what it sees and launches **one** Composer 2.5 sub-agent to **verify only** that tab’s UI state.

1. **Count tabs.** Run `list_pages`. Keep only Canva design tabs for this batch. Count must equal `POST_COUNT`. If not, **stop** and reconcile with the user.
2. **Map ids.** Tab `1` → JSON `id` `1`, … tab `POST_COUNT` → JSON `id` `POST_COUNT`. Parent states the mapping before filling.
3. **Per tab: fill (parent) → check (sub-agent).** For each id in order: parent completes step 4 for that tab, then pastes **title**, **first line of description**, **tags**, and **visibility** (from snapshot or read-back). Launch **one** Composer 2.5 sub-agent with the template below. Sub-agent returns **PASS** or **FAIL** and **one sentence**. If **FAIL**, parent fixes and re-checks that tab before continuing.
4. **Fill rules (parent, every tab).** Open Share / YouTube publish panel for that design. Set **Title** from JSON `title`; **Description** from JSON `description`; **Tags** from JSON `tags` joined or entered as plain text with **no `#`**; **Visibility** to **public**. Use **`type_text`** (and `fill` where appropriate). Do **not** use Control+V. Do **not** click **Publish** in this step.

   The YouTube form sits in a nested Canva iframe. Title, description, and buttons such as **Visibility** and **Tags** accept `fill` / `click`. The **Public** / **Private** / **Unlisted** accessibility radios do not: they have no clickable box, and clicking the radio times out with “did not become interactive”. Click the visible circle or label beside **Public** (the sibling the verbose snapshot marks ignored), then read the snapshot back and confirm `radio "Public" checked`.
5. **Publish (parent, after all tabs PASS).** On each design tab, click **Publish** once. Do **not** wait for publishing to finish. One click per tab; no second publish click.

**Sub-agent instruction template (parent fills placeholders):**

```
Tab id: ID
Expected title: TITLE
Expected description starts with: DESCRIPTION_START
Expected tags (no #): TAGS
Expected visibility: VISIBILITY
```

---

## Checklist

- [ ] Canva design tab count = `POST_COUNT`
- [ ] Tab order matches JSON `id` `1` … `POST_COUNT`
- [ ] Each tab: title, description, tags (no `#`), visibility **public**
- [ ] Each tab: Composer 2.5 check **PASS** before any Publish click
- [ ] Text entry via **`type_text`** / `fill` only (no clipboard paste)
- [ ] **Publish** clicked **once per tab**, **after** all fills and checks
- [ ] No waiting for publish completion

---

## Tools

| Tool | Namespace | Who uses it |
|------|-----------|-------------|
| `list_pages` | user-chrome-devtools | Parent |
| `select_page` | user-chrome-devtools | Parent |
| `click` | user-chrome-devtools | Parent |
| `fill` | user-chrome-devtools | Parent |
| `type_text` | user-chrome-devtools | Parent |
| `take_snapshot` | user-chrome-devtools | Parent |
| Composer 2.5 sub-agent | Task / sub-agent | Check one tab from parent read-back only |

---

## Sub-agents

| Setting | Value |
|---------|--------|
| Model | **Composer 2.5** |
| Count | **One sub-agent per design** (per check pass) |
| Browsing | **None** — title, description start, tags, visibility from parent only |

**Sub-agent reply:** `PASS` or `FAIL` plus **one sentence**. No extra prose, no tool use.

---

## Pitfalls

| Pitfall | What goes wrong | Guard |
|---------|-----------------|--------|
| Wrong folder spelling | JSON not found or wrong batch | Path is `material/YouTUbe/` (capital **T** and **U**), not `YouTube` |
| `#` in tags | Invalid or wrong tags on YouTube | Strip `#`; tags are plain strings from JSON |
| Visibility left **private** | Video not public | Set **public**; sub-agent checks visibility |
| Click lands on the visibility radio | Click times out; visibility stays **Private** | Do not click the `radio "Public"` node. Click the visible circle or label next to it, then confirm `checked` in a new snapshot |
| Publish before check | Unchecked or wrong metadata live | No Publish in step 4; Publish only in step 5 after all **PASS** |
| Tab count ≠ `POST_COUNT` | Wrong id ↔ design mapping | Stop at step 1 |
| Clipboard (Control+V) | Wrong or partial text | **`type_text` only** |
