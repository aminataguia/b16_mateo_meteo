import os
import base64
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from meteofrance_api import MeteoFranceClient
from fonctions import get_forecast_for_city

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration de l'API externe
API_KEY = os.getenv("API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}"
}
print(headers)
# Endpoint to generate weather bulletin
@app.post("/weather-bulletin/{city}")
async def weather_bulletin(city: str):



    url = "https://api.edenai.run/v2/text/generation"
    payload = {
        "providers": "openai,cohere",
        "text": f"fait moi un bulletin météo sous forme de phrase {get_forecast_for_city(city)}, noublie pas d'indiquer la température et de rappeler le nom de la ville et le jours de la prediction",
        "temperature": 0.2,
        "max_tokens": 250,
        "fallback_providers": ""
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        generated_text = result['openai']['generated_text']
        return {"generated_text": generated_text}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de la requête à l'API de génération de texte.")

# Endpoint to generate audio from weather bulletin
@app.post("/bulletin_audio/{city}")
async def bulletin_audio(city: str):
    bulletin_text = get_forecast_for_city(city)
    url_speech = "https://api.edenai.run/v2/audio/text_to_speech"
    payload_speech = {
        "providers": "google,amazon",
        "language": "fr-FR",
        "option": "FEMALE",
        "text": bulletin_text,
        "fallback_providers": ""
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url_speech, json=payload_speech, headers=headers)
    if response.status_code == 200:
        result = response.json()
        audio_data = result.get('google', {}).get('audio')
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            # Save the audio file
            with open("audio.mp3", "wb") as audio_file:
                audio_file.write(audio_bytes)
            return {"message": "Fichier audio généré avec succès : audio.mp3"}
        else:
            raise HTTPException(status_code=400, detail="Aucune donnée audio disponible dans la réponse.")
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de la requête à l'API de conversion en parole.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)



