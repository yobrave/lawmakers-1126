import json
import os
from pathlib import Path

CFG = {
    "artifact": "entry.txt",
    "limit": 320,
    "default_out": "out",
}


def pipeline(root: Path):
    raw = (root / CFG["artifact"]).read_text(encoding="utf-8").strip()
    size = len(raw)
    if size < 1 or size > CFG["limit"]:
        raise SystemExit(f"gate says 1..{CFG['limit']}, got {size}")
    out_root = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or CFG["default_out"])
    out_root.mkdir(parents=True, exist_ok=True)
    dest = out_root / CFG["artifact"]
    dest.write_bytes(raw.encode("utf-8"))
    return size, dest


if __name__ == "__main__":
    n, where = pipeline(Path(__file__).resolve().parent)
    print(json.dumps({"chars": n, "limit": CFG["limit"], "wrote": str(where)}))
