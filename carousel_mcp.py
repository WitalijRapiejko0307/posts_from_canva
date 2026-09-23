#!/usr/bin/env python3
"""Helper for carousel MCP workflow: extract heights and build payloads."""
import json
import sys
from pathlib import Path

from run_batch import heights_from_richtexts, position_payload, text_payload


def main() -> None:
    cmd = sys.argv[1]
    if cmd == "heights":
        data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        heights = heights_from_richtexts(data["richtexts"])
        print(json.dumps(heights))
    elif cmd == "position-from-response":
        cid = int(sys.argv[2])
        tx = sys.argv[3]
        data = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
        heights = heights_from_richtexts(data["richtexts"])
        print(json.dumps(position_payload(tx, cid, heights), ensure_ascii=False))
    elif cmd == "text":
        cid = int(sys.argv[2])
        tx = sys.argv[3]
        print(json.dumps(text_payload(tx, cid), ensure_ascii=False))


if __name__ == "__main__":
    main()
