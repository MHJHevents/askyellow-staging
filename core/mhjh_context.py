"""Selective MHJH knowledge loader for Gabber Yello.

Loads small local JSON knowledge blocks and returns at most one relevant block.
No OpenAI call is used for retrieval, so irrelevant MHJH knowledge never enters
prompt context.
"""

from functools import lru_cache
import json
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "gabber_yello" / "knowledge"
KNOWLEDGE_FILES = (
    "event.json",
    "mijnmhjh.json",
    "lootjesjacht.json",
    "arcade.json",
    "lineup.json",
)


@lru_cache(maxsize=1)
def _load_mhjh_knowledge():
    blocks = []
    for filename in KNOWLEDGE_FILES:
        path = KNOWLEDGE_DIR / filename
        with path.open("r", encoding="utf-8") as handle:
            block = json.load(handle)
            block["_file"] = filename
            blocks.append(block)
    return tuple(blocks)


def get_relevant_mhjh_context(message: str):
    """Return the single best MHJH knowledge answer, or ``None``.

    Matching is intentionally local and deterministic: longer keyword matches
    score higher, and multiple matches accumulate. This keeps token use low and
    avoids pulling the entire MHJH library into every Gabber Yello request.
    """
    q = (message or "").lower().strip()
    if not q:
        return None

    best_block = None
    best_score = 0

    for block in _load_mhjh_knowledge():
        score = 0
        for keyword in block.get("keywords", []):
            key = keyword.lower().strip()
            if key and key in q:
                score += max(1, len(key.split()))

        if score > best_score:
            best_score = score
            best_block = block

    if not best_block:
        return None

    return best_block.get("answer")
