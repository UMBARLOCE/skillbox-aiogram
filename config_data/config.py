import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    # exit("Переменные окружения не загружены т.к отсутствует файл .env")
    BOT_TOKEN = input("Введите TOKEN телеграм-бота:\n")
    RAPID_API_KEY = input("Введите API_KEY сервиса hotels4.p.rapidapi.com:\n")
    with open(".env", "w", encoding="utf-8") as file:
        file.write(f"BOT_TOKEN = {BOT_TOKEN}\n")
        file.write(f"RAPID_API_KEY = {RAPID_API_KEY}\n")

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
base_url = "https://hotels4.p.rapidapi.com/"
