import psycopg2
from meteofrance_api import MeteoFranceClient

from connexion import host, port, password, user, dbname
from villes import cities
<<<<<<< Updated upstream
<<<<<<< Updated upstream:recup.py
=======
from fonctions import get_db_connection, inserer_donnes, get_forecast_for_city, create_table, get_weather_data
>>>>>>> Stashed changes:main.py
=======

from fonctions import get_db_connection, inserer_donnes, get_forecast_for_city, create_table #get_weather_data
>>>>>>> Stashed changes

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
print("Connexion à la base de données PostgreSQL réussie !")

# Commande SQL pour créer la tabledef create_table(cursor):
def create_table(cursor):
    cursor.execute("""
CREATE TABLE IF NOT EXISTS meteo_forecast (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(255),
    dt BIGINT,
    min_temp DOUBLE PRECISION,
    max_temp DOUBLE PRECISION,
    min_humidity INTEGER,
    max_humidity INTEGER,
    precipitation DOUBLE PRECISION,
    uv INTEGER,
    weather_icon VARCHAR(255),
    weather_desc VARCHAR(255),
    sunrise BIGINT,
    sunset BIGINT
);
""")


# Exécution de la commande SQL pour créer la table
with conn.cursor() as cursor:
    create_table(cursor)
    conn.commit()

# Fonction pour insérer les données
def inserer_donnes(conn, city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset):
    with conn.cursor() as cursor:
        query = """
        INSERT INTO meteo_forecast (city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset))
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'insertion des données pour {city_name}: {e}")

# Liste des villes de France (à remplacer par une source externe ou une liste complète)

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


        
# je souhaite connecter la dt contenue dans le client meteo france pour la mettre dans mon serveur sql  ok
# j'aimerais bien convertir le language sql en python 
<<<<<<< Updated upstream
# je souhaite separer mon code on plusieur fichier qui sapelle 
<<<<<<< Updated upstream
# mettre a jour toute les 4-6 heure condition qui verifie que les taches planifier sont deja crée les chrone en fonctions de l'environnement ou il est 
<<<<<<< Updated upstream:recup.py
        
=======
# ajout du bulletin meteo
# ajout de la voix  
>>>>>>> Stashed changes:main.py
=======
# je souhaite separer mon code on plusieur fichier qui sapelle  ok 
# mettre a jour toute les 4-6 heure condition qui verifie que les taches planifier sont deja crée les chrone en fonctions de l'environnement ou il est 
# ajout du bulletin meteo
# ajout de la voix  
>>>>>>> Stashed changes
=======
# mettre a jour toute les 1 jours et condition qui verifie que les taches planifier sont deja crée les chrone en fonctions de l'environnement ou il est ok
# ajout du bulletin meteo ok 
# ajout de la voix  ok
# je veux que le bulletin meteo se base sur la data a jours et que l'on ai juste a donner la ville pour obtenir le bulletin 
>>>>>>> Stashed changes
