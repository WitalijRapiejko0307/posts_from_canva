#!/usr/bin/env python3
import json
import sys
from pathlib import Path

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

if __name__ == "__main__":
    mode, cid, tx = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if mode == "text":
        ops = json.loads(Path(f"payloads/c{cid}_text.json").read_text(encoding="utf-8"))
        payload = {
            "transaction_id": tx,
            "operations": ops,
            "page_index": 1,
            "pages": PAGES,
            "user_intent": f"Apply carousel {cid} text content to all 8 slides",
        }
        print(json.dumps(payload, ensure_ascii=False))
    elif mode == "position":
        richtexts = json.loads(sys.stdin.read())
        from position_from_richtexts import ELEMENT_IDS, SLIDE_HEIGHT, TEXT_LEFT  # noqa: F401
        ops = []
        for rt in richtexts["richtexts"]:
            idx = rt["page_index"]
            if idx < 2:
                continue
            height = rt["containerElement"]["dimension"]["height"]
            ops.append({
                "type": "position_element",
                "element_id": ELEMENT_IDS[idx - 1],
                "top": (SLIDE_HEIGHT - height) / 2,
                "left": TEXT_LEFT,
            })
        payload = {
            "transaction_id": tx,
            "operations": ops,
            "page_index": 2,
            "pages": PAGES,
            "user_intent": f"Center text on slides 2-8 for carousel {cid}",
        }
        print(json.dumps(payload, ensure_ascii=False))
