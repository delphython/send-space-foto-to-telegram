import os
import requests
from urllib.parse import urlparse, unquote
from datetime import datetime
from dotenv import load_dotenv
import telegram
from os import listdir
import time

IMAGE_DIR = "./images"


def download_image(url, filename, params=None):
    is_params = (params is not None)
    responses = {
        True: requests.get(url, params),
        False: requests.get(url),
    }
    response = responses[is_params]
    response.raise_for_status()

    path_to_save_image = os.path.join(IMAGE_DIR, filename)

    with open(path_to_save_image, "wb") as file:
        file.write(response.content)


def fetch_spacex_launch(launch_number):
    url = f"https://api.spacexdata.com/v3/launches/{launch_number}"
    links_header = "links"
    images_header = "flickr_images"

    response = requests.get(url)
    response.raise_for_status()

    last_launch = response.json()

    spacex_images = last_launch[links_header][images_header]
    for number, image_url in enumerate(spacex_images, start=1):
        image_file_name = f"spacex{number}.jpg"

        download_image(image_url, image_file_name)


def fetch_nasa_space_photos(token):
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

        download_image(image_url, image_file_name)


def fetch_nasa_epic_photos(token):
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

        download_image(image_url, image_file_name, params)


def get_file_extension(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    *arg, file_full_name = os.path.split(path)
    *arg, file_extension = os.path.splitext(file_full_name)

    return file_extension


def send_images_to_telegram():
    telegram_api_key = os.environ["TELEGRAM_API_KEY"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    time_to_send_image = 86400

    bot = telegram.Bot(token=telegram_api_key)

    while True:
        for image in listdir(IMAGE_DIR):
            bot.send_document(chat_id=chat_id, document=open(
                f"{IMAGE_DIR}/{image}", "rb"))
            time.sleep(time_to_send_image)


def main():
    load_dotenv()

    nasa_api_key = os.environ["NASA_API_KEY"]
    spacex_launch_number = 67

    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    fetch_spacex_launch(spacex_launch_number)
    fetch_nasa_space_photos(nasa_api_key)
    fetch_nasa_epic_photos(nasa_api_key)

    send_images_to_telegram()


if __name__ == "__main__":
    main()
