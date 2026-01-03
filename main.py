"""
Telegram bot for cryptocurrency price lookups.

SETUP:
1. Install deps:
   pip install python-telegram-bot requests

2. Set token:
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   (Windows: set TELEGRAM_BOT_TOKEN=your_bot_token_here)

3. Run:
   python main.py

USAGE:
- /price BTC
- /price eth
"""

import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def fetch_price(ticker: str) -> dict:
    """Fetch price from Binance."""
    try:
        symbol = f"{ticker.upper()}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

        response = requests.get(url, timeout=10)

        if response.status_code == 400:
            return {'success': False, 'price': None, 'error': 'Ticker not found.'}

        response.raise_for_status()
        data = response.json()

        if 'price' not in data:
            return {'success': False, 'price': None, 'error': 'Ticker not found.'}

        return {'success': True, 'price': data['price'], 'error': None}

    except requests.exceptions.Timeout:
        return {'success': False, 'price': None, 'error': 'Request timed out.'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'price': None, 'error': 'Network error.'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'price': None, 'error': f'API error: {e}'}
    except (KeyError, ValueError) as e:
        return {'success': False, 'price': None, 'error': f'Parse error: {e}'}
    except Exception as e:
        return {'success': False, 'price': None, 'error': f'Unexpected error: {e}'}


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "Provide a ticker symbol.\nUsage: /price BTC"
        )
        return

    ticker = context.args[0]
    await update.message.reply_text("Fetching price...")

    result = fetch_price(ticker)

    if result['success']:
        price = float(result['price'])
        await update.message.reply_text(
            f"{ticker.upper()}/USDT: ${price:,.2f}"
        )
    else:
        await update.message.reply_text(result['error'])


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Crypto Price Bot\n\n"
        "Use /price <ticker>\n"
        "Example: /price BTC"
    )


def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("price", price_command))

    logger.info("Bot started.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
