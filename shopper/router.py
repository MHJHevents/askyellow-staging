from fastapi import APIRouter, HTTPException

from shopper.core import process_shopper_input

router = APIRouter(prefix="/shopper", tags=["shopper"])


@router.post("/analyze")
def analyze_shopper(payload: dict):
    session_id = (payload.get("session_id") or "").strip()
    query = (payload.get("query") or "").strip()

    if not session_id or not query:
        raise HTTPException(status_code=400, detail="session_id en query zijn verplicht")

    result = process_shopper_input(session_id, query)
    if result.get("action") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))

    return result
