
import psycopg2
from meteofrance_api import MeteoFranceClient
import datetime
from connexion import host, port, password, user, dbname
from villes import cities

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

def get_forecast_for_city(city_name):
    client = MeteoFranceClient()
    list_places = client.search_places(city_name)
    if list_places:
        my_place = list_places[0]
        forecast = client.get_forecast_for_place(my_place)
        return forecast
    return None

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

# Exemple d'utilisation de la fonction
if __name__ == "__main__":
    city_name = "Paris"
    forecast_data = get_forecast_for_city(city_name)
    if forecast_data:
        for row in forecast_data:
            print(row)
    else:
        print("Aucune donnée trouvée pour la ville spécifiée.")

def inserer_donnes(conn, city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset):
    with conn.cursor() as cursor:
        # Convertir le timestamp Unix en date
        dt_date = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d')
        sunrise_date = datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d')
        sunset_date = datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d')
        
        query = """
        INSERT INTO meteo_forecast (city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (city_name, dt_date, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise_date, sunset_date))
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'insertion des données pour {city_name}: {e}")

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
get_forecast_for_city("Montpellier")