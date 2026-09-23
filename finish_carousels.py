#!/usr/bin/env python3
"""Generate MCP payloads for remaining carousels 8-13."""
import json
from pathlib import Path

from run_batch import heights_from_richtexts, position_payload, text_payload

DM = json.loads(Path("design_map.json").read_text())
TX = json.loads(Path("tx_map.json").read_text())


def main() -> None:
    for cid in range(8, 14):
        cid_s = str(cid)
        tx = TX[cid_s]
        text = text_payload(tx, cid)
        Path(f"/tmp/c{cid}_mcp_text.json").write_text(
            json.dumps({k: text[k] for k in ["transaction_id", "operations", "page_index", "pages", "user_intent"]},
                       ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"c{cid}: tx={tx} design={DM[cid_s]['design_id']} url={DM[cid_s]['edit_url']}")


if __name__ == "__main__":
    main()
