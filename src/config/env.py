import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")

WHATSAPP_USER = os.getenv("WHATSAPP_USER")
WORD_SEARCH = os.getenv("WORD_SEARCH")
NUMBER_HOURS_THREAD = os.getenv("NUMBER_HOURS_THREAD")
