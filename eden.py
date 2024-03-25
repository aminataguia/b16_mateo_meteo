import json
import requests
import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from meteofrance_api import MeteoFranceClient
import base64

from fonctions import get_weather_data
from villes import cities, meteo

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
payload = {
    "providers": provider,
    "text": "",
    "chatbot_global_action": f"Act like an assistant with this :{provider}",
    "previous_history": [],
    "temperature": 0.5,
    "max_tokens": 50,
    "fallback_providers": "",
}
url = "https://api.edenai.run/v2/text/generation"

# bulletin pour renvoyer la meteo en print 
payload = {
    "providers": "openai,cohere",
    "text": f"fait moi un bulletin meteo sous forme de phrase  {json.dumps(meteo)}",
    "temperature": 0.2,
    "max_tokens": 250,
    "fallback_providers": ""
}
response = requests.post(url, json=payload, headers=headers)
result = json.loads(response.text)
print(result['openai']['generated_text'])



# URL de l'API
url = "https://api.edenai.run/v2/audio/text_to_speech"
payload = {
    "providers": "google,amazon", "language": "en-US",
    "option": "MALE",
    "text": "this is a test",
    "fallback_providers": ""
}
response = requests.post(url, json=payload, headers=headers)

result = json.loads(response.text)
encoded = base64.b64encode(result)
print(encoded)
encoded
print(result['google']['audio'])


# Configuration du logging
logging.basicConfig(level=logging.DEBUG)

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'application Chatbot FastAPI"}

@app.post("/chatbot/{prompt}")
async def chatbot(prompt: str):
    if "weather" in prompt.lower():
        city_name = prompt.split("weather")[1].strip()
        weather_data = get_weather_data(city_name)
        if weather_data:
            weather_response = f"La météo à {city_name} est actuellement {weather_data[10]} avec une température minimale de {weather_data[3]}°C et maximale de {weather_data[4]}°C."
            payload["text"] = weather_response
        else:
            payload["text"] = f"Je n'ai pas pu trouver les données météorologiques pour {city_name}."
    else:
        payload["text"] = prompt

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    rp = result['meta']
    return (rp['generated_text'])

# @app.on_event("startup")
# async def startup_event():
#     client = MeteoFranceClient()
#     list_places = client.search_places("Montpellier")
#     if list_places:
#         my_place = list_places[0]
#         my_place_weather_forecast = client.get_forecast_for_place(my_place)
#         my_place_daily_forecast = my_place_weather_forecast.daily_forecast
#         print(my_place_daily_forecast)
#     else:
#         print("Aucun lieu trouvé pour la recherche.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
