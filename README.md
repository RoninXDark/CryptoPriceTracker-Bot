# Crypto Price Tracker Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-2CA5E0)](https://docs.aiogram.dev/)
[![Tests](https://github.com/RoninXDark/CryptoPriceTracker-Bot/actions/workflows/tests.yml/badge.svg)](https://github.com/RoninXDark/CryptoPriceTracker-Bot/actions/workflows/tests.yml)

An asynchronous Telegram bot for checking live cryptocurrency prices and
24-hour market movement through the CoinGecko API.

## Why This Project

The project demonstrates a practical API automation workflow: Telegram handles
the user interface, CoinGecko supplies market data, and the application layer
validates user input, handles rate limits, and formats the result for chat.

## Features

- Live USD prices and 24-hour percentage changes
- Inline buttons for Bitcoin, Ethereum, Solana, and Tether
- Manual lookup using full names or common tickers
- Asynchronous HTTP requests with explicit timeouts
- Friendly handling for unknown assets, rate limits, and network failures
- Environment-based secret management
- Unit tests and GitHub Actions CI

## Architecture

```text
main.py
crypto_tracker/
|-- bot.py          Telegram handlers and application lifecycle
|-- coingecko.py    Market-data client and input normalization
|-- config.py       Environment configuration
`-- keyboards.py    Inline keyboard builders
tests/
`-- test_coingecko.py
```

## Local Setup

```bash
git clone https://github.com/RoninXDark/CryptoPriceTracker-Bot.git
cd CryptoPriceTracker-Bot
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Add the token created with Telegram's `@BotFather`:

```dotenv
TELEGRAM_BOT_TOKEN=your_token_here
```

Run the bot:

```bash
python main.py
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Security

The Telegram token is loaded from `TELEGRAM_BOT_TOKEN`. The `.env` file is
ignored by Git and must never be committed.

## Tech Stack

Python, Aiogram, aiohttp, CoinGecko REST API, python-dotenv, pytest, GitHub Actions
