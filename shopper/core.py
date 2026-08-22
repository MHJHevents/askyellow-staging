"""Shopper Core orchestration.

The Shopper is intentionally cold: it decides whether to ask one useful
question, give neutral buying guidance, or produce a concrete search query.
It never invents products or prices.
"""

from search_v2.query_builder import ai_build_search_decision
from search_v2.state import add_message, get_conversation


def process_shopper_input(session_id: str, query: str) -> dict:
    query = (query or "").strip()
    if not session_id or not query:
        return {"action": "error", "message": "session_id en query zijn verplicht"}

    add_message(session_id, "user", query)
    conversation = get_conversation(session_id)
    decision = ai_build_search_decision(conversation)

    if not decision["is_ready_to_search"]:
        question = decision["clarification_question"]
        add_message(session_id, "assistant", question)
        return {
            "action": "ask",
            "question": question,
            "confidence": decision["confidence"],
        }

    if decision["response_mode"] == "advice":
        # Advice stays deliberately minimal in Shopper Core. Rich conversational
        # advice belongs to YellowMind; Shopper's job is to converge on search.
        proposed = decision.get("proposed_query") or query
        return {
            "action": "search",
            "query": proposed,
            "confidence": decision["confidence"],
        }

    proposed = decision["proposed_query"]
    add_message(session_id, "assistant", proposed)
    return {
        "action": "search",
        "query": proposed,
        "confidence": decision["confidence"],
    }
