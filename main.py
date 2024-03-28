# main.py
from db import get_db_connection
from fonctions import create_table, inserer_donnes, get_forecast_for_city
from villes import cities

def main():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        create_table(cursor)
        conn.commit()

    for city_name in cities:
        forecast = get_forecast_for_city(city_name)
        if forecast:
            print(forecast)
            for day in forecast: # Ici, nous itérons directement sur la liste retournée
                # Extraire les valeurs de chaque jour de prévision
                # Supposons que chaque élément de la liste est un dictionnaire contenant les informations de prévision pour un jour
                dt = day[0]
                min_temp = day[1]
                max_temp = day[2]
                min_humidity = day[3]
                max_humidity = day[4]
                precipitation = day[5]
                uv = day[6]
                weather_icon = day[7] 
                weather_desc = day[8]
                sunrise = day[9]
                sunset = day[10]

                # Insérer les données dans la base de données
                inserer_donnes(conn, city_name, dt, min_temp, max_temp, min_humidity, max_humidity, precipitation, uv, weather_icon, weather_desc, sunrise, sunset)

    conn.close()
    print("Fin de la connexion")

if __name__ == "__main__":
    main()


