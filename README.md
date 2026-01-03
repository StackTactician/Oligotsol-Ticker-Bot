# Oligotsol Ticker Bot

A simple Telegram bot for checking live crypto prices from the Binance API, tailored for the Olisgotsol community.

## Overview

This bot provides real-time cryptocurrency price information directly within Telegram, using the public Binance API. It's designed to be lightweight and easily deployable, making it a convenient tool for staying updated on the crypto market.

## Features

*   **Real-time Price Data:** Fetches the latest prices directly from Binance.
*   **Simple Commands:** Easy-to-use Telegram commands for quick price checks.
*   **Lightweight:** Minimal resource usage, suitable for deployment on various platforms.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/StackTactician/Oligotsol-Ticker-Bot.git
    cd Oligotsol-Ticker-Bot
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**

    *   You'll need a Telegram Bot token.  You can get one by talking to BotFather on Telegram.
    *   Set the `TELEGRAM_BOT_TOKEN` environment variable.

    ```bash
    export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    ```

4.  **Run the bot:**

    ```bash
    python main.py
    ```

## Usage

Once the bot is running, you can use the following commands in Telegram:

*   `/price <symbol>`:  Get the current price of a cryptocurrency (e.g., `/price BTCUSDT`).

## Deployment

The bot is designed to be easily deployed.  The `Procfile` and `runtime.txt` files are included for platforms like Heroku.

1.  **Create a Heroku app:**

    ```bash
    heroku create
    ```

2.  **Set the `TELEGRAM_BOT_TOKEN` config var:**

    ```bash
    heroku config:set TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    ```

3.  **Deploy the app:**

    ```bash
    git push heroku main
    ```

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, descriptive messages.
4.  Submit a pull request.

## License

This project is open source.  (Consider adding a LICENSE file to specify the exact license).

## Acknowledgements

*   Uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.
*   Utilizes the Binance API for cryptocurrency data.
