#!/usr/bin/env python
# pylint: disable=C0116,W0613


import logging
import requests
from telegram import Update, ForceReply
from bs4 import BeautifulSoup
from informer import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import urllib3
import bs4

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

URL = "https://www.mediapark.uz/products/view/12623"





def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'URL tashla'
    )


def getP(url):
    Url = requests.get(url)
    soup = BeautifulSoup(Url.content, 'html.parser')

    priceContent = soup.find(
        "a",  class_="Catalog-information-right-block-right-main-top")
    if priceContent:
            price = float(priceContent["content"])
    else:
        price = None
    return price




def url(update: Update, context: CallbackContext) -> None:
    
   
    for item,details in Items.items():
       
        priceMax = details.get('priceMax',0)    
        url = details.get('url',0)              

        price = getP(url)                   

        
        if price == None:
            update.message.reply_text('Narx urlda topilmadi')

        
        elif price < priceMax:            
            update.message.reply_text('Buyumning narxi ' + item +
                                      str(price) + ' va ko`rsatilgan narxidan past ' + str(priceMax))


    
    

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5522269859:AAHYiP4qDKtVndALtubKKDa1tAg1XZ272Pc")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
