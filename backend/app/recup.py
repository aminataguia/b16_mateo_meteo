from villes import cities
from fonctions import get_db_connection, inserer_donnes, get_forecast_for_city, create_table

def main():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        create_table(cursor)
        conn.commit()

    for city_name in cities:
        forecast = get_forecast_for_city(city_name)
        if forecast:
            for day in forecast.daily_forecast:
                # Extraire les valeurs de chaque jour de prévision
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

    conn.close()
    print("Fin de la connexion")

if __name__ == "__main__":
    main()






        
# je souhaite connecter la dt contenue dans le client meteo france pour la mettre dans mon serveur sql  ok
# j'aimerais bien convertir le language sql en python non  
# je souhaite separer mon code on plusieur fichier qui sapelle entre eux . ok 
# mettre a jour toute les 4-6 heure condition qui verifie que les taches planifier sont deja crée les chrone en fonctions de l'environnement ou il est 
# ajout de la voix  
