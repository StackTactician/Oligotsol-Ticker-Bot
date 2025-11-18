"""
Production-ready Telegram bot for cryptocurrency price lookups.

SETUP INSTRUCTIONS:
1. Install dependencies:
   pip install python-telegram-bot requests

2. Set environment variable:
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   
   Or on Windows:
   set TELEGRAM_BOT_TOKEN=your_bot_token_here

3. Run the bot:
   python main.py

USAGE:
- Send /price BTC to get Bitcoin price
- Send /price eth to get Ethereum price
- Ticker symbol is case-insensitive
"""

import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def fetch_price(ticker: str) -> dict:
    """
    Fetch cryptocurrency price from Binance API.
    
    Args:
        ticker: Cryptocurrency ticker symbol (e.g., 'BTC', 'ETH')
    
    Returns:
        dict with 'success' (bool), 'price' (str), and 'error' (str) keys
    """
    try:
        symbol = f"{ticker.upper()}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 400:
            return {
                'success': False,
                'price': None,
                'error': 'Ticker not found.'
            }
        
        response.raise_for_status()
        data = response.json()
        
        if 'price' not in data:
            return {
                'success': False,
                'price': None,
                'error': 'Ticker not found.'
            }
        
        return {
            'success': True,
            'price': data['price'],
            'error': None
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'price': None,
            'error': 'Request timed out. Please try again.'
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'price': None,
            'error': 'Network error. Please check your connection.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'price': None,
            'error': f'API error: {str(e)}'
        }
    except (KeyError, ValueError) as e:
        return {
            'success': False,
            'price': None,
            'error': f'Error parsing response: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'price': None,
            'error': f'Unexpected error: {str(e)}'
        }


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /price command.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    if not context.args:
        await update.message.reply_text(
            "Please provide a ticker symbol.\n"
            "Usage: /price BTC"
        )
        return
    
    ticker = context.args[0]
    
    await update.message.reply_text("Fetching price...")
    
    result = fetch_price(ticker)
    
    if result['success']:
        price = float(result['price'])
        await update.message.reply_text(
            f"💰 {ticker.upper()}/USDT: ${price:,.2f}"
        )
    else:
        await update.message.reply_text(f"❌ {result['error']}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "Welcome to Crypto Price Bot! 🚀\n\n"
        "Use /price {ticker} to get cryptocurrency prices.\n"
        "Example: /price BTC"
    )


def main() -> None:
    """Start the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN environment variable is not set.\n"
            "Please set it with your bot token from @BotFather"
        )
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("price", price_command))
    
    logger.info("Bot started. Polling for updates...")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
