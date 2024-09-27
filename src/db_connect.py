import psycopg2 
import os
from dotenv import find_dotenv, load_dotenv

find_dotenv()
load_dotenv()

def db_connect():
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

def insert_images(cursor, connection):
    if cursor is None or connection is None:
        print("No valid cursor or connection.")
        return
    
    try:
        folder = os.getenv('IMAGE_DIR')
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):  
                try:
                    cursor.execute('INSERT INTO images(imageLink) VALUES(%s)', (file))
                except Exception as e:
                    print(f"Error inserting file {file}: {e}")

        connection.commit()
        cursor.execute('SELECT * FROM images')
        records = cursor.fetchall()
        for record in records:
            print(record)
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_audios(cursor, connection):
    if cursor is None or connection is None:
        print("No valid cursor or connection.")
        return
    
    try:
        folder = os.getenv('AUDIO_DIR')
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):  
                try:
                    cursor.execute('INSERT INTO audios(audioLink) VALUES(%s)', (file))
                except Exception as e:
                    print(f"Error inserting file {file}: {e}")

        connection.commit()
        cursor.execute('SELECT * FROM audios')
        records = cursor.fetchall()
        for record in records:
            print(record)
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Unpack the cursor and connection directly
cursor, connection = db_connect()
if cursor and connection:
    insert_images(cursor, connection)
    insert_audios(cursor, connection)
