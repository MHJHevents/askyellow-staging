import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from openai import OpenAI, OpenAIError

router = APIRouter()

_VOICES = {"cedar", "onyx", "ash"}
_PROMPT = (
    "Spreek Nederlands als een rauwe mannelijke Haagse gabber van ongeveer veertig jaar. "
    "Licht schor, brutaal, droog en energiek, maar zeer duidelijk verstaanbaar. "
    "Natuurlijk Haags ritme en accent; geen karikatuur, geen nieuwslezer, niet gehaast. "
    "Houd iedere zin als een losse korte game-opmerking met een kleine pauze ertussen."
)
_LINES = """Nou dan. Laat maar zien.
Muur, pik. Muur.
Beton. Ken gebeuren.
Kijk dan. Vijf op rij.
Tien! Nou word je irritant.
Twintig. Doe normaal joh.
Dubbel kickie. Niet verslappuh nah.
Honderd! Wat doe je?
Dat was geen landing, pik.
Godsamme. Nieuw record."""
_CACHE: dict[str, bytes] = {}


@router.get("/internal/gabber-yello-voice-test/{voice}", include_in_schema=False)
def gabber_yello_voice_test(voice: str):
    if os.getenv("APP_ENV", "").lower() != "staging":
        raise HTTPException(status_code=404, detail="Not found")
    if voice not in _VOICES:
        raise HTTPException(status_code=404, detail="Unknown voice")

    if voice not in _CACHE:
        try:
            audio = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=_LINES,
                instructions=_PROMPT,
                response_format="mp3",
            )
            _CACHE[voice] = audio.content
        except OpenAIError as exc:
            code = getattr(exc, "code", None) or exc.__class__.__name__
            status = getattr(exc, "status_code", None) or 502
            raise HTTPException(status_code=status, detail=f"OpenAI voice test failed: {code}") from exc

    return Response(
        content=_CACHE[voice],
        media_type="audio/mpeg",
        headers={"Cache-Control": "private, max-age=300"},
    )
