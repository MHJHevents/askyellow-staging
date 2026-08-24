import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from openai import OpenAI, OpenAIError

router = APIRouter()

_INSTRUCTIONS = (
    "Gebruik de vaste mannelijke Ash-stem. Spreek natuurlijk Nederlands; probeer nadrukkelijk geen Haags "
    "accent te imiteren en overdrijf geen klinkers. Klink als een rauwe gabber van ongeveer veertig jaar: "
    "licht schor, droog, brutaal, direct en zeer duidelijk verstaanbaar. Gebruik de informele Haagse woorden "
    "precies zoals ze geschreven staan en laat het lokale gevoel uit woordkeuze, zinsbouw en droge timing komen. "
    "Geen nieuwslezer, geen toneel, geen karikatuur en niet gehaast. Geef de punchline lichte nadruk. "
    "Iedere regel is een losse korte reactie met een natuurlijke kleine pauze erna."
)
_LINES = """Nou dan. Laat maar zien.
Kom op pik. Gaan.
Hep je d'r zin in? Gaan dan.
Je mot erlangs, hè. Nie erdoor.
Beton. Ken gebeuren.
Nou pik. Dit leek bijna expres.
Tien! Straks mot ik nog aardig doen.
Twintig op rij. Geen ongeluk meer dit.
Dubbel kickie. Niet verslappuh nah.
Je hep meer bonks dan verstand.
Dat was geen landing, pik.
Godsamme. Nieuw record."""
_CACHE: bytes | None = None


@router.get("/internal/gabber-yello-ash-natural", include_in_schema=False)
def gabber_yello_ash_natural():
    global _CACHE
    if os.getenv("APP_ENV", "").lower() != "staging":
        raise HTTPException(status_code=404, detail="Not found")

    if _CACHE is None:
        try:
            audio = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="ash",
                input=_LINES,
                instructions=_INSTRUCTIONS,
                response_format="mp3",
            )
            _CACHE = audio.content
        except OpenAIError as exc:
            code = getattr(exc, "code", None) or exc.__class__.__name__
            status = getattr(exc, "status_code", None) or 502
            raise HTTPException(status_code=status, detail=f"OpenAI voice test failed: {code}") from exc

    return Response(
        content=_CACHE,
        media_type="audio/mpeg",
        headers={"Cache-Control": "private, max-age=300"},
    )
