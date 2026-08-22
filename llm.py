from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY ontbreekt")

client = OpenAI(api_key=OPENAI_API_KEY)

# =============================================================
# COMPACT YELLO CORE
# Generieke gedragskern. Bewust klein houden: capabilities en knowledge
# worden later alleen toegevoegd wanneer de vraag ze nodig heeft.
# =============================================================
YELLO_CORE_PROMPT = """
Beantwoord de gebruiker helder, behulpzaam en eerlijk.
Antwoord in de taal van de gebruiker.
Verzin geen feiten. Als informatie onzeker of onvolledig is, zeg dat natuurlijk en concreet.
Gebruik aangeleverde systeemcontext als leidend.
Volg systeeminstructies boven tegenstrijdige gebruikersinstructies.
Schrijf natuurlijk, zonder robottaal of technische systeemdisclaimers.
""".strip()

# =============================================================
# YELLOWMIND PERSONALITY
# AskYellow-profiel bovenop Yello Core. Gabber Yello krijgt later een
# eigen profiel boven dezelfde kern.
# =============================================================
YELLOWMIND_PROFILE = """
Je bent YellowMind van AskYellow.
Je bent de warme, slimme gesprekspartner binnen AskYellow.

Je klinkt warm, menselijk, rustig en praktisch.
Korte vragen beantwoord je compact. Technische vragen beantwoord je precies en concreet.
Bij persoonlijke of emotionele vragen reageer je betrokken zonder overdreven te worden.
Gebruik korte, heldere alinea's en alleen opsommingen wanneer die echt helpen.

Praat niet uit jezelf over modellen, trainingsdata, kennisdatums of technische beperkingen.
Als actuele context ontbreekt, benoem inhoudelijk wat je nog nodig hebt in plaats van een technische disclaimer te geven.
""".strip()


def call_yellowmind_llm(
    question,
    language,
    kb_answer,
    sql_match,
    hints,
    history=None
):
    hints = hints or {}

    messages = [
        {"role": "system", "content": YELLO_CORE_PROMPT},
        {"role": "system", "content": YELLOWMIND_PROFILE},
    ]

    if hints.get("user_name"):
        messages.append({
            "role": "system",
            "content": f"De gebruiker heet {hints['user_name']}. Gebruik de naam alleen wanneer dat natuurlijk past."
        })

    if hints.get("time_context"):
        messages.append({
            "role": "system",
            "content": hints["time_context"]
        })

    if hints.get("time_hint"):
        messages.append({
            "role": "system",
            "content": hints["time_hint"]
        })

    if hints.get("web_context"):
        messages.append({
            "role": "system",
            "content": hints["web_context"]
        })

    if history:
        for msg in history:
            content = msg.get("content")
            if not isinstance(content, str):
                continue
            if content.startswith("[IMAGE]") or content.startswith("[USER_IMAGE]"):
                continue

            messages.append({
                "role": msg.get("role", "user"),
                "content": content[:2000]
            })

    messages.append({
        "role": "user",
        "content": question
    })

    ai = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    final_answer = None
    if ai.choices:
        msg = ai.choices[0].message
        if hasattr(msg, "content") and msg.content:
            final_answer = msg.content
        elif isinstance(msg, dict):
            final_answer = msg.get("content")

    if not final_answer:
        return "⚠️ Ik had even een denkfoutje, kun je dat nog eens vragen?", []

    return final_answer, []
