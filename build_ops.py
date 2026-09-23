#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ELEMENT_IDS = [
    "PBXKvc9WHMF2pStF-LBYyfNb2hnYbXzW2",
    "PBbHwq2nRppzN66r-LBM5fsw0CpRzPjDs",
    "PBPy5QcnWvRjtDtj-LBnjMCpqlxBq8S6R",
    "PB5wTSCmZCbvlD2s-LBN7sV0vqXBVpMWw",
    "PBGD7w5fDxNpQmKY-LBYXjTDjVLMJvpMk",
    "PBqrXVst3Z9MYfKd-LBxdr8sB07F3X8bD",
    "PBnQ3htq5JjfzRCR-LB6rp2xPKhgDKbVN",
    "PBnl4PhMp6SZldZc-LBxCqQWqXfvVhZX6",
]
PAGES = [
    {"page_id": "PBXKvc9WHMF2pStF", "page_number": 1, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBbHwq2nRppzN66r", "page_number": 2, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBPy5QcnWvRjtDtj", "page_number": 3, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PB5wTSCmZCbvlD2s", "page_number": 4, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBGD7w5fDxNpQmKY", "page_number": 5, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBqrXVst3Z9MYfKd", "page_number": 6, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBnQ3htq5JjfzRCR", "page_number": 7, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
    {"page_id": "PBnl4PhMp6SZldZc", "page_number": 8, "dimension": {"width": 1080, "height": 1350}, "is_responsive": False, "is_empty": False, "is_editable": True},
]
SLIDE_HEIGHT = 1350
TEXT_LEFT = 108


def text_ops(carousel, cid):
    ops = [{"type": "update_title", "title": f"15.09.26 - {cid}"}]
    for i, slide in enumerate(carousel["slides"]):
        eid = ELEMENT_IDS[i]
        ops.append({"type": "replace_text", "element_id": eid, "text": slide["text"]})
        if i >= 1:
            ops.append({"type": "format_text", "element_id": eid, "formatting": {"font_size": 46, "text_align": "center"}})
    return ops


def position_ops(heights):
    return [
        {
            "type": "position_element",
            "element_id": ELEMENT_IDS[idx - 1],
            "top": (SLIDE_HEIGHT - h) / 2,
            "left": TEXT_LEFT,
        }
        for idx, h in sorted(heights.items())
    ]


def main():
    cid = int(sys.argv[1])
    mode = sys.argv[2]
    data = json.loads(Path("carousel.json").read_text(encoding="utf-8"))
    carousel = next(c for c in data["carousels"] if c["id"] == cid)
    if mode == "text":
        print(json.dumps(text_ops(carousel, cid), ensure_ascii=False))
    elif mode == "position":
        heights = json.loads(sys.argv[3])
        print(json.dumps(position_ops(heights), ensure_ascii=False))


if __name__ == "__main__":
    main()
