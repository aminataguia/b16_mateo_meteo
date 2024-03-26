
import psycopg2
from meteofrance_api import MeteoFranceClient
import datetime
import requests 
import base64

from connexion import host, port, password, user, dbname
from villes import cities

# je veux me conecter a ma base sql
def get_db_connection():
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connexion à la base de données PostgreSQL réussie !")
    return conn

# Je veux crée un table dans ma base sql
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

# Je veux inserer de la donner dans ma base sql en requetant l'api france meteo
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

# Je veux requeter ma base pour les information concernant une ville donnée  ( je veux prendre tout )
def get_forecast_for_city(city_name):
    # Obtenir la connexion à la base de données
    conn = get_db_connection()
    
    # Créer un curseur
    with conn.cursor() as cursor:
        # Requête SQL pour récupérer les données pour la ville spécifiée
        query = """
        SELECT * FROM meteo_forecast
        WHERE city_name = %s;
        """
        try:
            # Exécuter la requête avec le paramètre de la ville
            cursor.execute(query, (city_name,))
            # Récupérer les résultats
            rows = cursor.fetchall()
            # Fermer la connexion
            conn.close()
            # Renvoyer les résultats
            return rows
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {city_name}: {e}")
            return None
































