import base64
import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import FileResponse
from meteofrance_api import MeteoFranceClient
from fonctions import get_forecast_for_city

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"], # Autorise toutes les méthodes HTTP
    allow_headers=["*"], # Autorise tous les en-têtes
)

# Configuration de l'API externe
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWI0MDFiNTQtNDA3ZS00YjliLWE2ZjQtODdhYzE2M2U0YTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.E4p5OS5QLYy2Tj7GTm-t9sWVsDA8UXUyKbHX1dUHE7U"
}

# Endpoint to generate weather bulletin
@app.get("/weather-bulletin/{city}")
async def weather_bulletin(city: str):
    url = "https://api.edenai.run/v2/text/generation"
    payload = {
        "providers": "openai,cohere",
        "text": f"fait moi un bulletin météo sous forme de phrase {get_forecast_for_city(city)}, noublie pas d'indiquer la température et de rappeler le nom de la ville et le jours de la prediction",
        "temperature": 0.2,
        "max_tokens": 250,
        "fallback_providers": ""
    }
    timeout = httpx.Timeout(10.0, read=None) # Ajustez le délai d'attente de lecture à None pour désactiver le délai d'attente de lecture
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
    except httpx.ConnectTimeout:
        raise HTTPException(status_code=504, detail="Délai d'attente de connexion dépassé.")
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Délai d'attente de lecture dépassé.")
    except httpx.WriteTimeout:
        raise HTTPException(status_code=504, detail="Délai d'attente d'écriture dépassé.")

    if response.status_code == 200:
        result = response.json()
        generated_text = result['openai']['generated_text']

        url_speech = "https://api.edenai.run/v2/audio/text_to_speech"
        payload_speech = {
            "providers": "google,amazon",
            "language": "fr-FR",
            "option": "FEMALE",
            "text": json.dumps(generated_text), # Convert the dictionary to a JSON string
            "fallback_providers": ""
        }
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url_speech, json=payload_speech, headers=headers)
        except httpx.ConnectTimeout:
            raise HTTPException(status_code=504, detail="Délai d'attente de connexion dépassé.")
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="Délai d'attente de lecture dépassé.")
        except httpx.WriteTimeout:
            raise HTTPException(status_code=504, detail="Délai d'attente d'écriture dépassé.")

        if response.status_code == 200:
            result = response.json()
            audio_data = result.get('google', {}).get('audio')
            if audio_data:
                audio_bytes = base64.b64decode(audio_data)
                # Renvoyer le contenu du fichier audio directement
                return Response(content=audio_bytes, media_type="audio/mpeg")
            else:
                raise HTTPException(status_code=400, detail="Aucune donnée audio disponible dans la réponse.")
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de la requête à l'API de conversion en parole.")
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de la requête à l'API de génération de texte.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
