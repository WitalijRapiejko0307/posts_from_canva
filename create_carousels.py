#!/usr/bin/env python3
"""Build Canva editing operations for carousels from carousel.json."""

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

SLIDE_HEIGHT = 1350
TEXT_LEFT = 108


def build_text_operations(carousel: dict, title: str) -> list[dict]:
    ops = [{"type": "update_title", "title": title}]
    for i, slide in enumerate(carousel["slides"]):
        element_id = ELEMENT_IDS[i]
        ops.append(
            {
                "type": "replace_text",
                "element_id": element_id,
                "text": slide["text"],
            }
        )
        if i >= 1:
            ops.append(
                {
                    "type": "format_text",
                    "element_id": element_id,
                    "formatting": {"font_size": 46, "text_align": "center"},
                }
            )
    return ops


def build_position_operations(heights: dict[int, float]) -> list[dict]:
    ops = []
    for slide_idx in range(2, 9):
        element_id = ELEMENT_IDS[slide_idx - 1]
        height = heights[slide_idx]
        top = (SLIDE_HEIGHT - height) / 2
        ops.append(
            {
                "type": "position_element",
                "element_id": element_id,
                "top": top,
                "left": TEXT_LEFT,
            }
        )
    return ops


def main() -> None:
    data = json.loads(Path("carousel.json").read_text(encoding="utf-8"))
    date_prefix = "14.09.26"
    for carousel in data["carousels"]:
        cid = carousel["id"]
        title = f"{date_prefix} - {cid}"
        ops = build_text_operations(carousel, title)
        out = Path(f"ops/carousel_{cid}_text.json")
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(ops, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {out} ({len(ops)} operations)")


if __name__ == "__main__":
    main()
