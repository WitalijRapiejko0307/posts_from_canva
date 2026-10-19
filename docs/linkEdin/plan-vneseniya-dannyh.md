# Plan: enter LinkedIn publish data in Canva

**Document date:** 18.10.26

Repeatable checklist for filling the LinkedIn schedule/publish panel on designs that are **already open** in the browser (one tab per design, user logged in). Captions were prepared in the prior run [`plan-podgotovki-teksta.md`](plan-podgotovki-teksta.md); use **`POST_COUNT` from that run**. JSON lives at [`../../material/linkEdin/captions.json`](../../material/linkEdin/captions.json). Ids `1..POST_COUNT` must match open Canva design tabs **in the same order** (tab order = id order). The **parent confirms** id ↔ tab mapping before anyone types.

Set **Parameters** before the run. Everything else in **Fixed inputs** stays the same from run to run.

---

## Parameters

| Parameter | This run | Meaning |
|-----------|----------|---------|
| `POST_COUNT` | _from text-prep run_ | Number of designs/tabs in this batch; must equal `captions.length` in JSON |

---

## Fixed inputs

| What | Value |
|------|--------|
| LinkedIn account | `vitali_rapeika` |
| Publish format | **Video** (not Post, not Story) |
| Caption source | `captions[].caption` in [`../../material/linkEdin/captions.json`](../../material/linkEdin/captions.json) |
| Id ↔ tab rule | Tab 1 → caption `id` 1, … tab `POST_COUNT` → caption `id` `POST_COUNT` |

---

## Steps

**Role split (fixed):** The **parent** owns the browser and performs **all** `user-chrome-devtools` actions (`list_pages`, `select_page`, `click`, `fill`, `type_text`, `take_snapshot`). **Composer 2.5 sub-agents do not click.** After the parent fills one tab, the parent takes a snapshot (or pastes a short snapshot description) and launches **one** Composer 2.5 sub-agent to **verify only** that tab’s UI state.

1. **Count tabs.** Run `list_pages`. Keep only Canva design tabs for this batch. Count must equal `POST_COUNT`. If not, **stop** and reconcile with the user.
2. **Map ids.** Assign tab `1..POST_COUNT` to caption id `1..POST_COUNT`. Parent states the mapping; user confirms before step 3.
3. **Per tab: fill (parent) → check (sub-agent).** For each id in order:
   - Parent: `select_page` for that tab, open Share / schedule / publish panel, set format **Video**, pick account **`vitali_rapeika`** if shown, enter caption with `type_text` (no clipboard paste), **do not** click Publish.
   - Parent: `take_snapshot` (or paste snapshot text into the sub-agent prompt).
   - Parent: launch **one** Composer 2.5 sub-agent with the template below. Sub-agent returns **only**: format is Video (yes/no), caption text read back (first 80 chars), **Publish was not clicked** (yes/no).
   - If check fails, parent fixes UI and re-runs check for that tab before moving on.

   **Sub-agent instruction template (parent fills placeholders):**

   ```
   Tab id: TAB_ID
   Expected caption starts with: EXPECTED_START
   Full caption from JSON (for reference): CAPTION

   You receive a snapshot description of the LinkedIn publish panel only. Do not browse.
   Verify: (1) format is Video, (2) visible caption starts with EXPECTED_START, (3) Publish/Schedule was not clicked yet.
   Reply in three lines: Video yes/no | first 80 chars of caption you see | Publish not clicked yes/no
   ```

4. **Fill rules (parent, every tab).** Same as step 3 UI work:
   - Share or the schedule/publish panel already used for this design type.
   - Set format to **Video**.
   - Account **`vitali_rapeika`** if an account picker is visible.
   - Put the caption into the caption field with **`type_text`**. Do **not** use Control+V.
   - Do **not** click Publish in this step.
5. **Publish (parent, after all tabs pass check).** On each design tab, click **Publish** once. Do **not** wait for the publishing spinner or completion. One click per tab; no second publish click.

---

## Checklist

- [ ] Canva design tab count = `POST_COUNT`
- [ ] Each tab: format **Video**
- [ ] Each tab: caption matches JSON for that `id` (prefix check + sub-agent PASS)
- [ ] Each tab: account **`vitali_rapeika`** when picker present
- [ ] Publish clicked **once per tab**, **after** all fills and checks
- [ ] No Publish click during fill/check step; no duplicate Publish click

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
| Composer 2.5 sub-agent | Task / sub-agent | Check one tab from snapshot text only |

---

## Pitfalls

| Pitfall | What goes wrong | Guard |
|---------|-----------------|--------|
| Wrong format **Post** (or Story) | LinkedIn gets wrong asset type | Explicitly set **Video**; sub-agent checks format |
| Caption from another `id` | Mismatched copy on wrong design | Tab order = id order; confirm mapping; `EXPECTED_START` from JSON |
| Clipboard paste (Control+V) | Wrong or partial text | **`type_text` only** |
| Publish before check | Irreversible or unchecked publish | Sub-agent confirms Publish **not** clicked; Publish only in step 5 |
| Waiting for publish spinner | Wastes time; not required | One Publish click per tab; do not wait |
| Tab count ≠ `POST_COUNT` | Wrong batch | Stop at step 1 |

---

## Sub-agents

| Setting | Value |
|---------|--------|
| Model | **Composer 2.5** |
| Count | **One sub-agent per design** (per check pass) |
| Browsing | **None** — snapshot description from parent only |

**Parent prompt (≤ 5 lines):** id `N`; verify format **Video**; caption starts with `{first ~40 chars from JSON}`; **Publish not clicked**; paste snapshot below.

**Sub-agent reply:** `PASS` or `FAIL` plus **one sentence** (what failed or confirmation). No extra prose, no tool use.
