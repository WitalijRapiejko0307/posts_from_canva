#!/usr/bin/env python3
"""Prepare MCP payload files for a carousel step."""
import json
import sys
from pathlib import Path

from run_batch import heights_from_richtexts, position_payload, text_payload


def main() -> None:
    cmd, cid, tx = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    out = Path(f"/tmp/c{cid}_{cmd}.json")
    if cmd == "text":
        payload = text_payload(tx, cid)
    elif cmd == "position":
        resp = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
        heights = heights_from_richtexts(resp["richtexts"])
        payload = position_payload(tx, cid, heights)
    else:
        raise SystemExit(f"unknown cmd {cmd}")
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
