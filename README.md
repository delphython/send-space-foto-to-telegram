# Space Instagram

Space Instagram is a console utility that download photos from the last SpaceX launch, NASA's Astronomy Picture of the Day site and NASA's Earth Polychromatic Imaging Camera site. And send it to Telegram channel.

## Prerequisites

Python3 should be already installed. Use `pip` to install dependences:
```bash
pip install -r requirements.txt
```

## Installation
You have to set NASA_API_KEY, TELEGRAM_API_KEY and TELEGRAM_CHAT_ID enviroment variables before use script.

1. Create .env file in project directory.
2. Visit [NASA API portal](https://api.nasa.gov/) and sing up to generate API Key. Copy your NASA API key to .env file:
```
export NASA_API_KEY="9b7934f7d7f422a6sddf11df0663197ff0409ed82"
```
3. Create Telegram channel or use your own. How to create bot and get a token from Telegram see [this tutorial](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) for instructions. How to add a Telegram bot to Telegram channel see [this tutorial](https://www.alphr.com/add-bot-telegram/) for instructions. Copy your Telegram API token to .env file:
```
export TELEGRAM_API_KEY="1998822660:AAGOTlPYBKJHpLzQORy8tYIkxO7KMUpcBNo"
```
4. TELEGRAM_CHAT_ID is a link to Telegrem channel, for example: @dvmn_flood. Copy it to .env file:
```
export TELEGRAM_CHAT_ID = "@dvmn_flood"
```

## Usage

Run python script:
```sh
python main.py
```
Use Ctrl+C to interrupt script.

## Meta

Vitaly Klyukin – [@delphython](https://t.me/delphython) – [delphython@gmail.com](mailto:delphython@gmail.com)

[https://github.com/delphython](https://github.com/delphython/)
