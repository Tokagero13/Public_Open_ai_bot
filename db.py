import os, psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

db_config = {
    'dbname': 'telegram_bot',
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'port': DB_PORT
}

def ensure_table_exists():
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_messages (
            update_id BIGINT PRIMARY KEY,
            message_id BIGINT,
            from_id BIGINT,
            is_bot BOOLEAN,
            first_name VARCHAR(255),
            username VARCHAR(255),
            language_code VARCHAR(10),
            chat_id BIGINT,
            chat_first_name VARCHAR(255),
            chat_username VARCHAR(255),
            chat_type VARCHAR(50),
            date TIMESTAMP,
            text TEXT
        );
        """
        cur.execute(create_table_query)
    conn.commit()
    conn.close()

def insert_message_to_db(conn, message):
    with conn.cursor() as cur:
        insert_query = sql.SQL("""
            INSERT INTO telegram_messages (
                update_id, message_id, from_id, is_bot, first_name, username,
                language_code, chat_id, chat_first_name, chat_username, chat_type,
                date, text
            ) VALUES (
                %(update_id)s, %(message_id)s, %(from_id)s, %(is_bot)s, %(first_name)s, %(username)s,
                %(language_code)s, %(chat_id)s, %(chat_first_name)s, %(chat_username)s, %(chat_type)s,
                to_timestamp(%(date)s), %(text)s
            )
            ON CONFLICT (update_id) DO NOTHING;
        """)
        
        cur.execute(insert_query, {
            'update_id': message['update_id'],
            'message_id': message['message']['message_id'],
            'from_id': message['message']['from']['id'],
            'is_bot': message['message']['from']['is_bot'],
            'first_name': message['message']['from']['first_name'],
            'username': message['message']['from'].get('username'),
            'language_code': message['message']['from'].get('language_code'),
            'chat_id': message['message']['chat']['id'],
            'chat_first_name': message['message']['chat'].get('first_name'),
            'chat_username': message['message']['chat'].get('username'),
            'chat_type': message['message']['chat']['type'],
            'date': message['message']['date'],
            'text': message['message'].get('text')
        })
        
    conn.commit()