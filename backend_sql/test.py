import psycopg2

from connexion import host, port, password, user, dbname
from recup import create_table

def test_create_table():
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    with conn.cursor() as cursor:
        create_table(cursor)
        cursor.execute("SELECT to_regclass('meteo_forecast');")
        result = cursor.fetchone()
        assert result[0] == 'meteo_forecast'
    conn.close()
