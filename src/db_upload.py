import psycopg2 
import os
from dotenv import find_dotenv, load_dotenv

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

class FileUpload:
    def uploadFile(filetype , filelink):
        cursor , connection = db_connect()
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {filetype}s({filetype}Link) VALUES('{filelink}')")
            connection.commit()
            cursor.execute(f"SELECT {filetype}Id FROM {filetype}s WHERE {filetype}Link = '{filelink}'")
            records = cursor.fetchall()[0][0]
            return records
        except Exception as e:
            print(e)