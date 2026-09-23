#!/usr/bin/env python3
"""Build position_element ops from perform-editing-operations richtexts response."""
import json
import sys

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
SLIDE_HEIGHT = 1350
TEXT_LEFT = 108

data = json.load(sys.stdin)
ops = []
for rt in data["richtexts"]:
    idx = rt["page_index"]
    if idx < 2:
        continue
    height = rt["containerElement"]["dimension"]["height"]
    ops.append(
        {
            "type": "position_element",
            "element_id": ELEMENT_IDS[idx - 1],
            "top": (SLIDE_HEIGHT - height) / 2,
            "left": TEXT_LEFT,
        }
    )
print(json.dumps(ops, ensure_ascii=False))
