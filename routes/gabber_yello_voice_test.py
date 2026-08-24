import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from openai import OpenAI, OpenAIError

router = APIRouter()

_BASE = (
    "Gebruik de vaste mannelijke Ash-stem. Spreek Nederlands als een rauwe Haagse gabber "
    "van ongeveer veertig jaar: licht schor, brutaal, droog, energiek en zeer duidelijk verstaanbaar. "
    "Geen nieuwslezer, geen toneelstem en niet gehaast. Iedere zin is een losse korte game-opmerking "
    "met een kleine pauze ertussen. "
)
_VARIANTS = {
    "light": _BASE + (
        "Geef de stem een subtiel Haags accent: iets plattere klinkers, ingeslikte woorduiteinden "
        "en een nuchtere Haagse cadans. Houd het natuurlijk en bescheiden."
    ),
    "medium": _BASE + (
        "Gebruik een duidelijk authentiek Haags accent. Maak woorden als ken, hep, mot, nie, d'r en pik "
        "hoorbaar Haags; slik eindletters licht in, gebruik een platte directe cadans en leg droge nadruk "
        "op de punchline. Blijf moeiteloos verstaanbaar en vermijd een overdreven typetje."
    ),
    "raw": _BASE + (
        "Ga vol voor een rauw volks Haags accent: sterk platte klinkers, ingeslikte eind-n, harde korte "
        "medeklinkers en een brutale directe gabbercadans. Klink alsof je langs de Haagse kust en op oude "
        "gabberfeesten bent opgegroeid. Nog steeds goed verstaanbaar; geen komedie of parodie."
    ),
}
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


@router.get("/internal/gabber-yello-ash-haags/{variant}", include_in_schema=False)
def gabber_yello_ash_haags(variant: str):
    if os.getenv("APP_ENV", "").lower() != "staging":
        raise HTTPException(status_code=404, detail="Not found")
    if variant not in _VARIANTS:
        raise HTTPException(status_code=404, detail="Unknown variant")

    if variant not in _CACHE:
        try:
            audio = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="ash",
                input=_LINES,
                instructions=_VARIANTS[variant],
                response_format="mp3",
            )
            _CACHE[variant] = audio.content
        except OpenAIError as exc:
            code = getattr(exc, "code", None) or exc.__class__.__name__
            status = getattr(exc, "status_code", None) or 502
            raise HTTPException(status_code=status, detail=f"OpenAI voice test failed: {code}") from exc

    return Response(
        content=_CACHE[variant],
        media_type="audio/mpeg",
        headers={"Cache-Control": "private, max-age=300"},
    )
