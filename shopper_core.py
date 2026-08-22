"""Cold Shopper Core for AskYellow.

This module owns only search-decision logic. It can ask one useful follow-up
question or produce a concrete search query. It never invents products,
prices, availability, or affiliate claims.
"""

from search_v2.query_builder import ai_build_search_decision
from search_v2.state import add_message, get_conversation


def analyze_shopper(session_id: str, query: str) -> dict:
    session_id = (session_id or "").strip()
    query = (query or "").strip()

    if not session_id or not query:
        return {"action": "error", "message": "session_id en query zijn verplicht"}

    add_message(session_id, "user", query)
    conversation = get_conversation(session_id)
    decision = ai_build_search_decision(conversation)

    if not decision.get("is_ready_to_search"):
        question = decision.get("clarification_question") or "Kun je één belangrijk detail toevoegen?"
        add_message(session_id, "assistant", question)
        return {
            "action": "ask",
            "question": question,
            "confidence": decision.get("confidence", 0.0),
        }

    proposed_query = (decision.get("proposed_query") or query).strip()
    add_message(session_id, "assistant", proposed_query)

    return {
        "action": "search",
        "query": proposed_query,
        "confidence": decision.get("confidence", 0.0),
    }
