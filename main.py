
import os
import time
from datetime import datetime
from os import listdir
from urllib.parse import urlparse, unquote

import requests
import telegram
from dotenv import load_dotenv


def download_image(url, filename, image_dir, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    image_path = os.path.join(image_dir, filename)

    with open(image_path, "wb") as file:
        file.write(response.content)


def fetch_spacex_launch(launch_number, image_dir):
    url = f"https://api.spacexdata.com/v3/launches/{launch_number}"

    response = requests.get(url)
    response.raise_for_status()

    specific_launch = response.json()

    spacex_images = specific_launch["links"]["flickr_images"]
    for number, image_url in enumerate(spacex_images, start=1):
        image_file_name = f"spacex{number}.jpg"

        download_image(image_url, image_file_name, image_dir)


def fetch_nasa_space_photos(token, image_dir):
    images_count = 2

    nasa_url = "https://api.nasa.gov/planetary/apod"
    params = {
      "api_key": token,
      "count": images_count,
    }

    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    nasa_images = response.json()

    for number, nasa_image in enumerate(nasa_images, start=1):
        image_url = nasa_image["url"]
        file_extension = get_file_extension(image_url)
        image_file_name = f"nasa{number}{file_extension}"

        download_image(image_url, image_file_name, image_dir)


def fetch_nasa_epic_photos(token, image_dir):
    epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {
      "api_key": token,
    }

    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    epic_images = response.json()

    for number, epic_image in enumerate(epic_images, start=1):
        image_name = epic_image["image"]
        image_dt = datetime.strptime(epic_image["date"], "%Y-%m-%d %H:%M:%S")
        image_date = datetime.strftime(image_dt, "%Y/%m/%d")
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png"
        image_file_name = f"epic{number}.png"

        download_image(image_url, image_file_name, image_dir, params)


def get_file_extension(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    *arg, file_extension = os.path.splitext(path)

    return file_extension


def send_images_to_telegram(token, chat_id, image_dir):
    image_sending_time = 86400

    bot = telegram.Bot(token=token)

    while True:
        for image in listdir(image_dir):
            with open(f"{image_dir}/{image}", "rb") as document:
                bot.send_document(chat_id=chat_id, document=document)
            time.sleep(image_sending_time)


def main():
    load_dotenv()

    nasa_api_key = os.environ["NASA_API_KEY"]
    telegram_api_key = os.environ["TELEGRAM_API_KEY"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    spacex_launch_number = 67
    image_dir = "./images"

    os.makedirs(image_dir, exist_ok=True)

    fetch_spacex_launch(spacex_launch_number, image_dir)
    fetch_nasa_space_photos(nasa_api_key, image_dir)
    fetch_nasa_epic_photos(nasa_api_key, image_dir)

    send_images_to_telegram(telegram_api_key, chat_id, image_dir)


if __name__ == "__main__":
    main()
