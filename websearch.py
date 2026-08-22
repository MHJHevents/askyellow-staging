# app/services/websearch_core.py
import os
import requests
from fastapi import APIRouter, HTTPException

from shopper_core import analyze_shopper

router = APIRouter()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# =====================================================
# INTERNE FUNCTIE (voor ask_handler / services)
# =====================================================

def do_websearch(query: str):
    query = (query or "").strip()
    if not query:
        return []

    if not SERPER_API_KEY:
        raise RuntimeError("SERPER_API_KEY ontbreekt op de server")

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    body = {"q": query}

    r = requests.post(url, json=body, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    results = []
    for item in data.get("organic", [])[:6]:
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("link"),
        })

    return results


# =====================================================
# SHOPPER CORE
# One cold entrypoint for direct search and YellowMind handoff.
# =====================================================

@router.post("/shopper/analyze")
def shopper_analyze(payload: dict):
    session_id = (payload.get("session_id") or "").strip()
    query = (payload.get("query") or "").strip()

    if not session_id or not query:
        raise HTTPException(status_code=400, detail="session_id en query zijn verplicht")

    result = analyze_shopper(session_id, query)
    if result.get("action") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))

    return result


# =====================================================
# ECHTE WEBSEARCH PROVIDER
# =====================================================

@router.post("/tool/websearch")
async def tool_websearch(payload: dict):
    query = (payload.get("query") or "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query missing")

    try:
        results = do_websearch(query)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Websearch error: {e}")

    return {
        "tool": "websearch",
        "query": query,
        "results": results,
    }
