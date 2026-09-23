#!/usr/bin/env python3
import json
from pathlib import Path

ELEMENT_IDS = [
    "PBXKvc9WHMF2pStF-LBYyfNb2hnYbXzW2",
    "PBbHwq2nRppzN66r-LBM5fsw0CpRzPjDs",
    "PBYR9b5mqCw63srK-LBDsPG3BTLsWsHf4",
    "PBCpBj1RSBLDv6Gn-LBPzl1zdT2DXssh1",
    "PBtDh7gBKWzF5tCJ-LB0FvgjhkDM2v3Lp",
    "PBSD56NpD8Z65xrv-LBwP3399V5TBSrtP",
    "PBkdxZtbndDn9W8w-LBFF9WCdYpPKX78V",
    "PBnl4PhMp6SZldZc-LBxCqQWqXfvVhZX6",
]
PAGES = [
    {"page_id": "PBXKvc9WHMF2pStF", "page_number": 1, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBbHwq2nRppzN66r", "page_number": 2, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBYR9b5mqCw63srK", "page_number": 3, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBCpBj1RSBLDv6Gn", "page_number": 4, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBtDh7gBKWzF5tCJ", "page_number": 5, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBSD56NpD8Z65xrv", "page_number": 6, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBkdxZtbndDn9W8w", "page_number": 7, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBnl4PhMp6SZldZc", "page_number": 8, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
]
SLIDE_HEIGHT = 1350
TEXT_LEFT = 108


def text_ops(carousel, cid):
    ops = [{"type": "update_title", "title": f"14.09.26 - {cid}"}]
    for i, slide in enumerate(carousel["slides"]):
        eid = ELEMENT_IDS[i]
        ops.append({"type": "replace_text", "element_id": eid, "text": slide["text"]})
        if i >= 1:
            ops.append({"type": "format_text", "element_id": eid, "formatting": {"font_size": 46, "text_align": "center"}})
    return ops


def position_ops(heights):
    ops = []
    for page_idx, height in heights.items():
        eid = ELEMENT_IDS[page_idx - 1]
        ops.append({"type": "position_element", "element_id": eid, "top": (SLIDE_HEIGHT - height) / 2, "left": TEXT_LEFT})
    return ops


def main():
    data = json.loads(Path("carousel.json").read_text(encoding="utf-8"))
    out_dir = Path("payloads")
    out_dir.mkdir(exist_ok=True)
    for carousel in data["carousels"]:
        cid = carousel["id"]
        if cid == 1:
            continue
        payload = {
            "carousel_id": cid,
            "text_operations": text_ops(carousel, cid),
            "pages": PAGES,
        }
        (out_dir / f"carousel_{cid}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"carousel_{cid}.json")


if __name__ == "__main__":
    main()
