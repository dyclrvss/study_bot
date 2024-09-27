import psycopg2 
import os
from dotenv import find_dotenv, load_dotenv
import random

def db_connect():
    find_dotenv()
    load_dotenv()
    try:
        connection = psycopg2.connect(
            database=os.getenv('DATABASE'),
            user=os.getenv('USER'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT'),
            password=os.getenv("PASSWORD")
        )
        
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        print(f"Connection error: {e}")
        return None, None

class FileSelect:
    def file_select(filetype , id):
        cursor , connection = db_connect()
        try:
            cursor = connection.cursor()
            connection.commit()
            query = f"SELECT {filetype}link FROM {filetype}s WHERE {filetype}Id = %s"
            cursor.execute(query, (id,))
            records = (cursor.fetchall())[0][0]
            return records
        except Exception as e:
            print(e)

    def select_random_file(filetype):
        cursor , connection = db_connect()
        try:
            cursor = connection.cursor()
            connection.commit() 
            cursor.execute(f"""SELECT {filetype}s.{filetype}Id FROM {filetype}s ORDER BY {filetype}Id DESC LIMIT 1""")
            num = (cursor.fetchall())
            random_id = random.randint(1, num[0][0])
            cursor.execute(f"""SELECT {filetype}Link FROM {filetype}s WHERE {filetype}Id = %s""", (random_id,))            
            file_name = (cursor.fetchall())[0][0]
            return file_name
        except Exception as e:
            print(e)

    def select_max_id(filetype):
        cursor , connection = db_connect()
        try:
            cursor = connection.cursor()
            connection.commit() 
            cursor.execute(f"""SELECT {filetype}s.{filetype}Id FROM {filetype}s ORDER BY {filetype}Id DESC LIMIT 1""")
            num = (cursor.fetchall())[0][0]
            return num
        except Exception as e:
            print(e)

    
