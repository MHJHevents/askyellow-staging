"""Selective MHJH and Hardcore knowledge loader for Gabber Yello.

Small operational JSON blocks and reviewed Hardcore Markdown sections are
retrieved locally. Only relevant excerpts enter the model prompt, keeping both
answers and token use under control.
"""

from functools import lru_cache
import json
from pathlib import Path
import re
import unicodedata

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "gabber_yello" / "knowledge"
HARDCORE_DIR = KNOWLEDGE_DIR / "hardcore"
KNOWLEDGE_FILES = (
    "mhjh.json",
    "gabber_yello.json",
    "event.json",
    "mijnmhjh.json",
    "lootjesjacht.json",
    "arcade.json",
    "lineup.json",
    "tickets.json",
    "whitehouse.json",
    "partyinfo.json",
    "merch.json",
    "resale.json",
    "partybus.json",
)

STOPWORDS = {
    "de", "het", "een", "en", "of", "van", "voor", "met", "naar", "is",
    "zijn", "wat", "wie", "waar", "hoe", "welke", "dat", "dit", "die",
    "ik", "jij", "je", "mij", "mijn", "er", "om", "op", "in", "te",
}


def _normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", (text or "").lower())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def _terms(text: str) -> set[str]:
    return {word for word in _normalize(text).split() if len(word) >= 3 and word not in STOPWORDS}


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


@lru_cache(maxsize=1)
def _load_hardcore_sections():
    sections = []
    if not HARDCORE_DIR.exists():
        return tuple()

    for path in sorted(HARDCORE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        current_title = path.stem
        current_lines = []

        def store_section():
            body = "\n".join(current_lines).strip()
            if body:
                searchable = f"{current_title}\n{body}"
                sections.append({
                    "title": current_title,
                    "body": body,
                    "normalized": _normalize(searchable),
                    "terms": _terms(searchable),
                    "file": path.name,
                })

        for line in text.splitlines():
            if line.startswith("## "):
                store_section()
                current_title = re.sub(r"^##\s+(?:\d+\.\s*)?", "", line).strip()
                current_lines = []
            elif line.startswith("# "):
                continue
            else:
                current_lines.append(line)
        store_section()

    return tuple(sections)


def _hardcore_matches(message: str, limit: int = 4) -> list[str]:
    normalized = _normalize(message)
    query_terms = _terms(message)
    if not normalized or not query_terms:
        return []

    scored = []
    for order, section in enumerate(_load_hardcore_sections()):
        title_normalized = _normalize(section["title"])
        title_terms = _terms(section["title"])
        overlap = query_terms & section["terms"]
        if not overlap:
            continue

        score = len(overlap) * 3
        score += len(query_terms & title_terms) * 8
        if title_normalized and title_normalized in normalized:
            score += 20
        if normalized in section["normalized"]:
            score += 6
        scored.append((score, -order, section))

    scored.sort(reverse=True, key=lambda item: (item[0], item[1]))
    excerpts = []
    used_chars = 0
    for score, _, section in scored[:limit]:
        if score < 3:
            continue
        excerpt = f"### {section['title']}\n{section['body']}"
        # Hard cap prevents one broad question from producing a giant prompt.
        if used_chars + len(excerpt) > 12000:
            remaining = 12000 - used_chars
            if remaining < 500:
                break
            excerpt = excerpt[:remaining].rsplit("\n", 1)[0]
        excerpts.append(excerpt)
        used_chars += len(excerpt)
        if used_chars >= 12000:
            break
    return excerpts


def get_relevant_mhjh_context(message: str):
    q = _normalize(message)
    if not q:
        return None

    scored_blocks = []
    for order, block in enumerate(_load_mhjh_knowledge()):
        score = 0
        for keyword in block.get("keywords", []):
            key = _normalize(keyword)
            if key and f" {key} " in f" {q} ":
                score += max(1, len(key.split()))
        if score > 0:
            scored_blocks.append((score, -order, block))

    scored_blocks.sort(reverse=True, key=lambda item: (item[0], item[1]))
    operational = [
        item[2].get("answer", "")
        for item in scored_blocks[:2]
        if item[2].get("answer")
    ]
    hardcore = _hardcore_matches(message)

    combined = operational + hardcore
    return "\n\n".join(combined) if combined else None
