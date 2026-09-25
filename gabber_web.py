"""Guarded web-search routing for Gabber Yello."""

import re

from websearch import do_websearch


_EXPLICIT = (
    "zoek op internet", "zoek eens op", "zoek dit op", "google dit",
    "kun je dit opzoeken", "kun je online zoeken", "check online",
)
_INTERNET_REQUEST = re.compile(
    r"\b(zoek(?:en)?|vind(?:en)?|opzoek(?:en)?|check(?:en)?)\b.{0,45}\b(internet|online|web)\b"
    r"|\b(internet|online|web)\b.{0,45}\b(zoek(?:en)?|vind(?:en)?|opzoek(?:en)?|check(?:en)?)\b",
    re.IGNORECASE,
)

_CURRENT = (
    "laatste nieuws", "nieuwste nieuws", "meest recente", "actueel",
    "vandaag bekend", "deze week bekend", "net bekendgemaakt",
    "huidige agenda", "aankomende optredens", "treedt op", "treed op",
    "wanneer is het", "wanneer vindt", "is er nog", "bestaat nog",
    "dit weekend", "komend weekend", "aankomend weekend", "volgend weekend",
    "aankomende feesten", "komende feesten", "feestjes dit weekend", "feesten dit weekend",
)

# Only factual misses get an automatic internet fallback. Personal memories,
# opinions and casual conversation must stay a conversation instead of turning
# every message into a Google query.
_FACTUAL_QUESTION = re.compile(
    r"^(?:weet (?:je|jij)\s+)?(?:"
    r"wat (?:is|was|betekent)|wanneer|"
    r"waar (?:is|was|staat|ligt|vindt|speelt|draait)|welke (?:artiest|dj|track|plaat|versie|editie|datum)|"
    r"door wie|van wie|hoeveel|hoe heet|klopt het dat"
    r")\b",
    re.IGNORECASE,
)
_SCENE_FACT = re.compile(
    r"\b(track|plaat|nummer|release|remix|mashup|artiest|dj|liveact|label|"
    r"feest|festival|hardcorefestival|club|locatie|line-?up|optreden|editie|hardcore|gabber|hardstyle)\b",
    re.IGNORECASE,
)
_PERSONAL_OR_OPINION = re.compile(
    r"\b(ik vind|vind jij|volgens jou|favoriet|mijn herinnering|weet je nog|"
    r"wat denk je|hoe voel|anekdote|verhaal van mij|bij ons|onze familie)\b",
    re.IGNORECASE,
)
_SHORT_UNKNOWN_PERSON = re.compile(
    r"^(?:weet (?:je|jij)\s+)?wie (?:is|was)\s+[\w.'’-]+(?:\s+[\w.'’-]+){0,2}\??$",
    re.IGNORECASE,
)


def should_search_web(message: str, has_official_mhjh_context: bool) -> bool:
    q = " ".join((message or "").strip().split())
    q_lower = q.lower()

    # A direct request always wins, even when MHJH knowledge is available.
    if any(trigger in q_lower for trigger in _EXPLICIT) or _INTERNET_REQUEST.search(q):
        return True

    # Personal opinions and memories stay conversational.
    if _PERSONAL_OR_OPINION.search(q):
        return False

    # Current/recent questions always require a fresh web check, even when
    # reviewed MHJH knowledge also contains an older fact about the subject.
    if any(trigger in q_lower for trigger in _CURRENT):
        return True

    # Reviewed MHJH knowledge remains the primary source for historical facts.
    if has_official_mhjh_context:
        return False

    # A bare nickname/name is ambiguous: ask for context once instead of
    # searching the wrong person (for example: "Wie is Dof?").
    if _SHORT_UNKNOWN_PERSON.fullmatch(q):
        return False

    # Automatic emergency exit for a sufficiently specific factual scene
    # question for which our reviewed knowledge returned no match.
    return bool(
        len(q.split()) >= 5
        and _FACTUAL_QUESTION.search(q)
        and _SCENE_FACT.search(q)
    )


def search_web_for_gabber(message: str, limit: int = 4) -> list[dict]:
    query = " ".join((message or "").split())[:300]
    if len(query) < 8:
        return []

    results = do_websearch(query)
    cleaned = []
    for item in results[:limit]:
        title = " ".join(str(item.get("title") or "").split())[:180]
        snippet = " ".join(str(item.get("snippet") or "").split())[:500]
        url = str(item.get("url") or "").strip()
        if not title or not url or not re.match(r"^https?://", url, re.IGNORECASE):
            continue
        cleaned.append({"title": title, "snippet": snippet, "url": url})
    return cleaned


def format_web_context(results: list[dict]) -> str | None:
    if not results:
        return None
    parts = []
    for index, item in enumerate(results, start=1):
        parts.append(
            f"[{index}] {item['title']}\n"
            f"{item['snippet']}\n"
            f"URL: {item['url']}"
        )
    return "\n\n".join(parts)


_EVENT_WORD = re.compile(
    r"\b(?:feest(?:en|je|jes|juhs)?|fesstjuhs|festival(?:s)?|evenement(?:en)?|optreden(?:s)?|uitgaan)\b",
    re.IGNORECASE,
)
_EVENT_PERIOD = re.compile(
    r"\b(?:dit|komend|aankomend|volgend)\s+weekend\b|"
    r"\b(?:vandaag|morgen|vanavond|deze\s+(?:vrijdag|zaterdag|zondag))\b",
    re.IGNORECASE,
)
_EVENT_DETAIL = re.compile(
    r"\b(?:line[\s-]?up|wie\s+(?:draait|speelt|staat)|welke\s+(?:dj|artiest)|"
    r"artiesten|namen|tickets?|kaartjes?|locatie|adres|hoe\s+laat|timetable|set[- ]tijden)\b",
    re.IGNORECASE,
)
_LOCATION_PATTERNS = (
    re.compile(r"\b(?:ik|we|wij)\s+(?:woon|wonen|woonachtig)\s+in\s+([a-zà-ÿ][a-zà-ÿ'’\-]*(?:\s+[a-zà-ÿ][a-zà-ÿ'’\-]*){0,3})", re.IGNORECASE),
    re.compile(r"\b(?:in de buurt van|omgeving van|regio)\s+([a-zà-ÿ][a-zà-ÿ'’\-]*(?:\s+[a-zà-ÿ][a-zà-ÿ'’\-]*){0,3})", re.IGNORECASE),
    re.compile(r"\bin\s+((?!(?:de|het|een|dit|deze|mijn|jouw)\b)[a-zà-ÿ][a-zà-ÿ'’\-]*(?:\s+[a-zà-ÿ][a-zà-ÿ'’\-]*){0,3})", re.IGNORECASE),
)
_LOCATION_STOP = {"dit", "deze", "komend", "aankomend", "volgend", "weekend", "vandaag", "morgen", "vanavond", "en", "maar", "want", "daar", "dus", "we", "wij", "ik", "is", "zijn", "er", "ook", "iets", "het", "de", "een", "hier", "in"}


def _is_upcoming_event_question(text: str) -> bool:
    return bool(_EVENT_WORD.search(text or "") and _EVENT_PERIOD.search(text or ""))


def _extract_location(text: str) -> str | None:
    q = " ".join((text or "").split())
    for pattern in _LOCATION_PATTERNS:
        match = pattern.search(q)
        if not match:
            continue
        words = []
        for word in match.group(1).strip(" ,.!?;:").split():
            cleaned = word.strip(" ,.!?;:")
            if cleaned.lower() in _LOCATION_STOP:
                break
            words.append(cleaned)
            if len(words) == 4:
                break
        if words:
            return " ".join(words).title()
    return None


def _weekend_dates(text: str, today=None) -> str:
    from datetime import date, datetime, timedelta
    from zoneinfo import ZoneInfo

    current = today or datetime.now(ZoneInfo("Europe/Amsterdam")).date()
    if not isinstance(current, date):
        current = date.today()
    saturday = current + timedelta(days=(5 - current.weekday()) % 7)
    if current.weekday() == 6:
        saturday = current - timedelta(days=1)
    if "volgend weekend" in (text or "").lower():
        saturday += timedelta(days=7)
    sunday = saturday + timedelta(days=1)
    return f"{saturday:%d-%m-%Y} en {sunday:%d-%m-%Y}"


def build_gabber_web_query(message: str, history: list[dict] | None = None, today=None) -> tuple[str, bool]:
    """Build a Dutch, local, date-anchored query for current party searches.

    A location correction can follow an event question, so use recent user turns
    only; earlier assistant answers are never copied into the search query.
    """
    user_turns = [
        item.get("content", "")
        for item in (history or [])[-12:]
        if item.get("role") == "user" and isinstance(item.get("content"), str)
    ]
    event_turns = [text for text in user_turns + [message or ""] if _is_upcoming_event_question(text)]
    current_location = _extract_location(message)
    is_event_detail = bool(event_turns and _EVENT_DETAIL.search(message or ""))
    followup_event = bool(event_turns and current_location and not _is_upcoming_event_question(message))
    if not _is_upcoming_event_question(message) and not followup_event and not is_event_detail:
        return " ".join((message or "").split())[:300], False

    event_text = (message or "") if _is_upcoming_event_question(message) else event_turns[-1]
    location = current_location
    if not location:
        for prior in reversed(user_turns):
            location = _extract_location(prior)
            if location:
                break
    location = location or "Nederland"
    region_suffix = "" if location.lower() == "nederland" else ", Nederland"
    period = _EVENT_PERIOD.search(event_text)
    period_label = period.group(0).lower() if period else "dit weekend"
    dates = _weekend_dates(event_text, today) if "weekend" in period_label else ""
    date_part = f" {dates}" if dates else ""
    topic = "line-up artiesten en speelgegevens" if is_event_detail else "feesten"
    query = f"hardcore gabber {topic} in {location}{region_suffix} {period_label}{date_part}"
    return query[:300], True



def find_mhjh_lineup_overlap(results: list[dict]) -> list[str]:
    """Return confirmed MHJH artists found in external event search results."""
    from pathlib import Path
    import json

    knowledge_path = Path(__file__).resolve().parent / "gabber_yello" / "knowledge" / "lineup.json"
    try:
        with knowledge_path.open("r", encoding="utf-8") as handle:
            artists = json.load(handle).get("confirmed_artists", [])
    except (OSError, ValueError, TypeError):
        return []

    event_results = []
    event_signal = re.compile(
        r"\b(?:line[\s-]?up|festival|gabber party|hardcore party|event|evenement|feest|optreden|agenda)\b",
        re.IGNORECASE,
    )
    for item in results or []:
        url = str(item.get("url") or "").lower()
        if "komttiedanhe.nl" in url or "mhjhevents.nl" in url:
            continue
        result_text = " ".join((
            str(item.get("title") or ""),
            str(item.get("snippet") or ""),
        ))
        if event_signal.search(result_text):
            event_results.append(result_text.lower())

    matches = []
    for artist in artists:
        name = str(artist.get("name") or "").strip()
        aliases = [name, *artist.get("aliases", [])]
        if name and any(
            re.search(r"(?<!\w)" + re.escape(str(alias).strip().lower()) + r"(?!\w)", result_text)
            for alias in aliases if str(alias).strip()
            for result_text in event_results
        ):
            matches.append(name)
    return matches



def get_official_mhjh_ticket_url() -> str | None:
    """Read the canonical ticket shop URL from reviewed MHJH knowledge."""
    from pathlib import Path
    import json

    knowledge_path = Path(__file__).resolve().parent / "gabber_yello" / "knowledge" / "tickets.json"
    try:
        with knowledge_path.open("r", encoding="utf-8") as handle:
            value = json.load(handle).get("official_ticket_url")
    except (OSError, ValueError, TypeError):
        return None
    return value if isinstance(value, str) and value.startswith("https://") else None
