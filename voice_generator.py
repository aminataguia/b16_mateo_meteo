import json
import requests
import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from meteofrance_api import MeteoFranceClient
import base64

from villes import cities, meteo

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
url = "https://api.edenai.run/v2/text/chat"
provider = "meta"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWI0MDFiNTQtNDA3ZS00YjliLWE2ZjQtODdhYzE2M2U0YTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.E4p5OS5QLYy2Tj7GTm-t9sWVsDA8UXUyKbHX1dUHE7U"
}

url = "https://api.edenai.run/v2/text/generation"

# bulletin pour renvoyer la meteo en print a l'aide du client !!!
payload = {
    "providers": "openai,cohere",
    "text": f"fait moi un bulletin meteo sous forme de phrase  {get_forecast_for_city('Montpellier')}",
    "temperature": 0.2,
    "max_tokens": 250,
    "fallback_providers": ""
}
response = requests.post(url, json=payload, headers=headers)
result = json.loads(response.text)
print(result['openai']['generated_text'])

# Code pour generer un audio
resultat = result['openai']['generated_text']
url_speech = "https://api.edenai.run/v2/audio/text_to_speech"
payload_speech = {
    "providers": "google,amazon", "language": "fr-FR",
    "option": "FEMALE",
    "text": resultat,
    "fallback_providers": ""
}
def text_to_speech():
    response = requests.post(url_speech, json=payload_speech, headers=headers)

    if response.status_code == 200:
        result = response.json()
        audio_data = result.get('google', {}).get('audio')
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            with open("audio.mp3", "wb") as audio_file:
                audio_file.write(audio_bytes)
            print("Fichier audio généré avec succès : audio.mp3")
        else:
            print("Aucune donnée audio disponible dans la réponse.")
    else:
        print(f"Erreur lors de la requête : {response.status_code} - {response.text}")

text_to_speech()

@app.get("/weather-bulletin/{city}")
async def weather_bulletin(city: str):
    url = "https://api.edenai.run/v2/text/generation"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWI0MDFiNTQtNDA3ZS00YjliLWE2ZjQtODdhYzE2M2U0YTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.E4p5OS5QLYy2Tj7GTm-t9sWVsDA8UXUyKbHX1dUHE7U"
    }
    payload = {
        "providers": "openai,cohere",
        "text": f"fait moi un bulletin météo sous forme de phrase {get_forecast_for_city(city)}",
        "temperature": 0.2,
        "max_tokens": 250,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    generated_text = result['openai']['generated_text']

    # Return the generated text
    return {"generated_text": generated_text}
@app.get("/bulletin_audio/{city}")
async def bulletin_audio(city: str):
    url_speech = "https://api.edenai.run/v2/audio/text_to_speech"
    payload_speech = {
        "providers": "google,amazon", "language": "fr-FR",
        "option": "FEMALE",
        "text": weather_bulletin(city),
        "fallback_providers": ""
          }
    weather_bulletin(city: str)
    response = requests.post(url_speech, json=payload_speech, headers=headers)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)



