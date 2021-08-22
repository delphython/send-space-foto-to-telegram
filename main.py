import os
import requests
from urllib.parse import urlparse, unquote
from datetime import datetime
from dotenv import load_dotenv
import telegram
from os import listdir
import time


def download_image(url, filename, image_dir, params=None):
    is_params = (params is not None)
    responses = {
        True: requests.get(url, params),
        False: requests.get(url),
    }
    response = responses[is_params]
    response.raise_for_status()

    path_to_save_image = os.path.join(image_dir, filename)

    with open(path_to_save_image, "wb") as file:
        file.write(response.content)


def fetch_spacex_launch(launch_number, image_dir):
    url = f"https://api.spacexdata.com/v3/launches/{launch_number}"
    links_header = "links"
    images_header = "flickr_images"

    response = requests.get(url)
    response.raise_for_status()

    last_launch = response.json()

    spacex_images = last_launch[links_header][images_header]
    for number, image_url in enumerate(spacex_images, start=1):
        image_file_name = f"spacex{number}.jpg"

        download_image(image_url, image_file_name, image_dir)


def fetch_nasa_space_photos(token, image_dir):
    images_count = 2
    url_header = "url"

    nasa_url = "https://api.nasa.gov/planetary/apod"
    params = {
      "api_key": token,
      "count": images_count,
    }

    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    nasa_images = response.json()

    for number, nasa_image in enumerate(nasa_images, start=1):
        image_url = nasa_image[url_header]
        file_extension = get_file_extension(image_url)
        image_file_name = f"nasa{number}{file_extension}"

        download_image(image_url, image_file_name, image_dir)


def fetch_nasa_epic_photos(token, image_dir):
    image_header = "image"

    epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {
      "api_key": token,
    }

    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    epic_images = response.json()

    for number, epic_image in enumerate(epic_images, start=1):
        image_name = epic_image[image_header]
        image_dt = datetime.strptime(epic_image["date"], "%Y-%m-%d %H:%M:%S")
        image_date = datetime.strftime(image_dt, "%Y/%m/%d")
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png"
        image_file_name = f"epic{number}.png"

        download_image(image_url, image_file_name, image_dir, params)


def get_file_extension(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    *arg, file_full_name = os.path.split(path)
    *arg, file_extension = os.path.splitext(file_full_name)

    return file_extension


def send_images_to_telegram(token, chat_id, image_dir):
    send_image_time = 86400

    bot = telegram.Bot(token=token)

    while True:
        for image in listdir(image_dir):
            with open(f"{image_dir}/{image}", "rb") as document:
                bot.send_document(chat_id=chat_id, document=document)
            time.sleep(send_image_time)


def main():
    load_dotenv()

    nasa_api_key = os.environ["NASA_API_KEY"]
    telegram_api_key = os.environ["TELEGRAM_API_KEY"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    spacex_launch_number = 67
    image_dir = "./images"

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    fetch_spacex_launch(spacex_launch_number, image_dir)
    fetch_nasa_space_photos(nasa_api_key, image_dir)
    fetch_nasa_epic_photos(nasa_api_key, image_dir)

    send_images_to_telegram(telegram_api_key, chat_id, image_dir)


if __name__ == "__main__":
    main()
