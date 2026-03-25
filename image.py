from fastapi import APIRouter, HTTPException, Request

from image_shared import generate_image, require_auth_session
from image_library import get_user_images_library, register_download
from chat_shared import get_auth_user_from_session

from db import get_db_conn

router = APIRouter()


@router.post("/tool/image_generate")
async def tool_image_generate(request: Request, payload: dict):
    require_auth_session(request)

    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")

    url = generate_image(prompt)
    if not url:
        raise HTTPException(status_code=500, detail="Image generation failed")

    return {
        "tool": "image_generate",
        "prompt": prompt,
        "url": url,
    }

@router.get("/images/library")
def get_images_library(session_id: str):
    images = get_user_images_library(session_id)
    return {"images": images}

@router.post("/images/download")
def download_image(payload: dict):
    session_id = payload.get("session_id")
    image_url = payload.get("image_url")

    conn = get_db_conn()
    try:
        user = get_auth_user_from_session(conn, session_id)
        if not user:
            return {"allowed": False}

        cur = conn.cursor()

        # check subscription
        cur.execute("""
            SELECT subscription_status
            FROM auth_users
            WHERE id = %s
        """, (user["id"],))

        sub = cur.fetchone()["subscription_status"]

        if sub != "free":
            return {"allowed": True}

        # free → max 1
        cur.execute("""
            SELECT COUNT(*) as cnt
            FROM image_downloads
            WHERE user_id = %s AND image_url = %s
        """, (user["id"], image_url))

        count = cur.fetchone()["cnt"]

        if count >= 1:
            return {"allowed": False}

        cur.execute("""
            INSERT INTO image_downloads (user_id, image_url)
            VALUES (%s, %s)
        """, (user["id"], image_url))

        conn.commit()

        return {"allowed": True}

    finally:
        conn.close()

@router.get("/images/library")
def get_images_library(session_id: str):
    conn = get_db_conn()
    try:
        user = get_auth_user_from_session(conn, session_id)
        if not user:
            return {"images": []}

        rows = get_user_images_library(conn, user["id"])

        images = []
        for r in rows:
            content = r["content"]

            if content.startswith("[IMAGE]"):
                url = content.replace("[IMAGE]", "").strip()
            elif content.startswith("[USER_IMAGE]"):
                url = content.replace("[USER_IMAGE]", "").strip()
            else:
                continue

            images.append({
                "url": url,
                "created_at": r["created_at"]
            })

        return {"images": images}

    finally:
        conn.close()