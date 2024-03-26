import psycopg2
from meteofrance_api import MeteoFranceClient

from connexion import host, port, password, user, dbname
from villes import cities
import datetime

from fonctions import get_db_connection, inserer_donnes, get_forecast_for_city, create_table, inserer_donnes

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
print("Connexion à la base de données PostgreSQL réussie !")


# Exécution de la commande SQL pour créer la table
with conn.cursor() as cursor:
    create_table(cursor)
    conn.commit()

client = MeteoFranceClient()

for city_name in cities:
    list_places = client.search_places(city_name)
    if list_places:
        my_place = list_places[0]
        forecast = client.get_forecast_for_place(my_place)

        for day in forecast.daily_forecast:
            dt = day['dt']
            min_temp = day['T']['min']
            max_temp = day['T']['max']
            min_humidity = day['humidity']['min']
            max_humidity = day['humidity']['max']
            precipitation = day['precipitation']['24h']
            uv = day['uv']
            weather_icon = day['weather12H']['icon'] if day['weather12H'] else None
            weather_desc = day['weather12H']['desc'] if day['weather12H'] else None
            sunrise = day['sun']['rise']
            sunset = day['sun']['set']

            # Insérer les données dans la base de données
            inserer_donnes(conn, city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset)

# Fermeture de la connexion à la base de données
conn.close()
print("Fin de la connexion")

# je souhaite que mes requete soit faite dirrectement avec le client api et non en dur 
