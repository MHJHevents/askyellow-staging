from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from chat_engine.db import get_conn
from core.time_context import build_time_context, build_llm_time_hint
from core.askyellow_context import get_relevant_askyellow_context
from core.capability_router import detect_capability

from chat_shared import (
    store_message_pair,
    get_user_history,
    get_auth_user_from_session,
    build_welcome_message,
    get_history_for_llm,
    get_available_history_days,
    get_user_history_by_day,
    get_user_images,
)

from image_shared import (
    generate_image,
    analyze_uploaded_image,
    edit_uploaded_image,
    detect_uploaded_image_operation,
    read_and_validate_upload,
)

from llm import call_yellowmind_llm

router = APIRouter()

TIME_CONTEXT_TRIGGERS = (
    "vandaag", "gisteren", "morgen", "datum", "tijd", "hoe laat",
    "welke dag", "deze week", "vorige week", "volgende week",
    "dit jaar", "vorig jaar", "volgend jaar", "recent", "actueel",
    "momenteel", "nu", "jaarwisseling",
)


def _needs_time_context(text: str) -> bool:
    q = (text or "").lower()
    return any(trigger in q for trigger in TIME_CONTEXT_TRIGGERS)


@router.get("/chat/history")
def chat_history(session_id: str, day: str | None = Query(default=None)):
    conn = get_conn()
    try:
        user = get_auth_user_from_session(conn, session_id)

        if not user:
            return {
                "available_days": [],
                "messages": [],
                "today": [],
                "yesterday": [],
                "welcome": None,
            }

        user_id = user["id"]
        first_name = user.get("first_name")

        if day == "list":
            return {
                "available_days": get_available_history_days(conn, user_id)
            }

        if day == "images":
            return {
                "images": get_user_images(conn, user_id)
            }

        if day and day not in ("today", "yesterday"):
            messages = get_user_history_by_day(conn, user_id, day)
            return {
                "day": day,
                "messages": messages,
                "available_days": get_available_history_days(conn, user_id),
            }

        today_messages = get_user_history(conn, user_id, "today")
        yesterday_messages = get_user_history(conn, user_id, "yesterday")

        return {
            "available_days": get_available_history_days(conn, user_id),
            "today": today_messages,
            "yesterday": yesterday_messages,
            "welcome": build_welcome_message(first_name),
        }
    finally:
        conn.close()


@router.post("/chat")
def chat(payload: dict):
    session_id = payload.get("session_id")
    message = payload.get("message", "").strip()
    wants_image = payload.get("wants_image", False)

    if not session_id or not message:
        raise HTTPException(status_code=400, detail="session_id of message ontbreekt")

    # Capability routing stays cheap and deterministic. The cold Shopper owns
    # actionable product-search requests; YellowMind owns normal conversation.
    if not wants_image and detect_capability(message) == "shopper":
        return {
            "type": "search",
            "query": message,
            "capability": "shopper",
        }

    conn = get_conn()
    try:
        history = get_history_for_llm(conn, session_id)
        user = get_auth_user_from_session(conn, session_id)
    finally:
        conn.close()

    hints = {}

    if user and user.get("first_name"):
        hints["user_name"] = user["first_name"]

    if _needs_time_context(message):
        hints["time_context"] = build_time_context()
        hints["time_hint"] = build_llm_time_hint()

    if wants_image:
        image_url = generate_image(message)

        if not image_url:
            raise HTTPException(status_code=500, detail="Afbeelding genereren mislukt")

        store_message_pair(session_id, message, "[IMAGE]" + image_url)
        return {
            "type": "image",
            "url": image_url
        }

    kb_answer = get_relevant_askyellow_context(message)

    answer, _ = call_yellowmind_llm(
        question=message,
        language="nl",
        kb_answer=kb_answer,
        sql_match=None,
        hints=hints,
        history=history
    )

    if not answer:
        answer = "⚠️ Ik kreeg geen inhoudelijk antwoord terug."

    store_message_pair(session_id, message, answer)
    return {"reply": answer}


@router.post("/chat/image")
async def chat_with_uploaded_image(
    session_id: str = Form(...),
    message: str = Form(""),
    file: UploadFile = File(...),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id ontbreekt")

    image_bytes, mime_type = await read_and_validate_upload(file)

    conn = get_conn()
    try:
        history = get_history_for_llm(conn, session_id)
    finally:
        conn.close()

    operation = detect_uploaded_image_operation(message)
    user_log_text = f"[USER_IMAGE]{message or 'uploaded image'}"

    if operation == "edit":
        prompt = (message or "").strip() or "Maak van deze afbeelding een nette karikatuur."

        image_src = edit_uploaded_image(
            image_bytes=image_bytes,
            mime_type=mime_type,
            prompt=prompt,
        )

        store_message_pair(session_id, user_log_text, f"[IMAGE]{image_src}")
        return {
            "type": "image",
            "mode": "edit",
            "url": image_src,
            "reply": "Hier is je bewerkte afbeelding."
        }

    answer = analyze_uploaded_image(
        image_bytes=image_bytes,
        mime_type=mime_type,
        question=message,
        history=history,
    )

    store_message_pair(session_id, user_log_text, answer)
    return {
        "type": "vision",
        "mode": "analyze",
        "reply": answer,
    }


@router.post("/chat/reset")
def reset_chat(payload: dict):
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400)

    conn = get_conn()
    try:
        user = get_auth_user_from_session(conn, session_id)
        cur = conn.cursor()

        if user:
            cur.execute(
                """
                UPDATE conversations
                SET ended_at = NOW()
                WHERE user_id = %s
                  AND ended_at IS NULL
                """,
                (user["id"],)
            )
        else:
            cur.execute(
                """
                UPDATE conversations
                SET ended_at = NOW()
                WHERE session_id = %s
                  AND ended_at IS NULL
                """,
                (session_id,)
            )

        conn.commit()
    finally:
        conn.close()

    return {"ok": True}
