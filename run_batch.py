#!/usr/bin/env python3
"""Generate payloads and track carousel creation state."""
import json
import sys
from pathlib import Path

from build_ops import ELEMENT_IDS, PAGES, SLIDE_HEIGHT, TEXT_LEFT, text_ops

SOURCE_DESIGN_ID = "DAHVJ1CkcSc"
DATE_PREFIX = "15.09.26"
STATE_FILE = Path("carousel_state.json")


def heights_from_richtexts(richtexts: list) -> dict[int, float]:
    return {
        rt["page_index"]: rt["containerElement"]["dimension"]["height"]
        for rt in richtexts
        if rt["page_index"] >= 2
    }


def position_ops_from_heights(heights: dict[int, float]) -> list[dict]:
    return [
        {
            "type": "position_element",
            "element_id": ELEMENT_IDS[idx - 1],
            "top": (SLIDE_HEIGHT - heights[idx]) / 2,
            "left": TEXT_LEFT,
        }
        for idx in sorted(heights)
    ]


def text_payload(transaction_id: str, cid: int) -> dict:
    data = json.loads(Path("carousel.json").read_text(encoding="utf-8"))
    carousel = next(c for c in data["carousels"] if c["id"] == cid)
    return {
        "transaction_id": transaction_id,
        "operations": text_ops(carousel, cid),
        "page_index": 1,
        "pages": PAGES,
        "user_intent": f"Apply carousel {cid} text to all 8 slides",
    }


def position_payload(transaction_id: str, cid: int, heights: dict[int, float]) -> dict:
    return {
        "transaction_id": transaction_id,
        "operations": position_ops_from_heights(heights),
        "page_index": 2,
        "pages": PAGES,
        "user_intent": f"Center text on slides 2-8 for carousel {cid}",
    }


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"completed": {}, "source_design_id": SOURCE_DESIGN_ID}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    cmd = sys.argv[1]
    state = load_state()

    if cmd == "init":
        payloads_dir = Path("payloads_batch")
        payloads_dir.mkdir(exist_ok=True)
        for cid in range(1, 14):
            data = json.loads(Path("carousel.json").read_text(encoding="utf-8"))
            carousel = next(c for c in data["carousels"] if c["id"] == cid)
            ops = text_ops(carousel, cid)
            (payloads_dir / f"c{cid}_text_ops.json").write_text(
                json.dumps(ops, ensure_ascii=False), encoding="utf-8"
            )
        print("Generated text ops for carousels 1-13")

    elif cmd == "text-payload":
        cid = int(sys.argv[2])
        tx = sys.argv[3]
        print(json.dumps(text_payload(tx, cid), ensure_ascii=False))

    elif cmd == "position-payload":
        cid = int(sys.argv[2])
        tx = sys.argv[3]
        heights = json.loads(sys.argv[4])
        heights = {int(k): v for k, v in heights.items()}
        print(json.dumps(position_payload(tx, cid, heights), ensure_ascii=False))

    elif cmd == "mark-done":
        cid = int(sys.argv[2])
        design_id = sys.argv[3]
        edit_url = sys.argv[4]
        state["completed"][str(cid)] = {"design_id": design_id, "edit_url": edit_url}
        save_state(state)
        print(f"Marked carousel {cid} done")

    elif cmd == "urls":
        for cid in sorted(state.get("completed", {}), key=int):
            print(state["completed"][cid]["edit_url"])

    elif cmd == "pending":
        done = {int(k) for k in state.get("completed", {})}
        print([i for i in range(1, 14) if i not in done])

    elif cmd == "heights-json":
        data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        heights = heights_from_richtexts(data["richtexts"])
        print(json.dumps(heights))


if __name__ == "__main__":
    main()
