
import psycopg2
from meteofrance_api import MeteoFranceClient
from connexion import host, port, password, user, dbname

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
def main():
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        cursor = connection.cursor()

        # Call the recup_serveur function to fetch and print all rows from the meteo_forecast table
        recup_serveur(cursor)

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("The PostgreSQL connection is closed")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
def recup_serveur(cursor):
    cursor.execute("""
    SELECT * FROM meteo_forecast;
    """)
    records = cursor.fetchall()
    for row in records:
        print(row)

def recup_serveur(cursor):
    cursor.execute("""
    SELECT * FROM meteo_forecast;
    """)
    records = cursor.fetchall()
    for row in records:
        print(row)

def get_forecast_for_city(city_name):
    client = MeteoFranceClient()
    list_places = client.search_places(city_name)
    if list_places:
        my_place = list_places[0]
        forecast = client.get_forecast_for_place(my_place)
        daily_forecast = forecast.daily_forecast
        print(daily_forecast)
        return forecast
    return None
def get_forecasts_for_cities(cities):
    # Initialiser un dictionnaire pour stocker les prévisions
    forecasts = {}
    
    # Créer une instance du client MeteoFrance
    client = MeteoFranceClient()
    
    # Itérer sur chaque ville dans la liste des villes
    for city_name in cities:
        # Rechercher les lieux correspondant au nom de la ville
        list_places = client.search_places(city_name)
        
        # Vérifier si au moins un lieu a été trouvé
        if list_places:
            # Prendre le premier lieu trouvé
            my_place = list_places[0]
            
            # Obtenir la prévision météorologique pour ce lieu
            forecast = client.get_forecast_for_place(my_place)
            
            # Ajouter la prévision au dictionnaire des prévisions
            forecasts[city_name] = forecast
    
    # Retourner le dictionnaire contenant les prévisions pour toutes les villes
    return forecasts

# Exemple d'utilisation
cities = ["Paris", "Lyon", "Marseille"]
forecasts = get_forecasts_for_cities(cities)

# Afficher les prévisions pour chaque ville
for city, forecast in forecasts.items():
    print(f"Prévision pour {city}: {forecast.daily_forecast}")





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
