#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
sudo pip install python-telegram-bot --upgrade
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import subprocess

from telegram.ext import CommandHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

test_box_api_key = ['514877936:AAH1p-_zloWkXoJC4j8dVYTf05NNBYOQ5e8']
test_box = 0
user = False
myuserid = 417245494
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help me im stuck in a box!')


def up(bot, update):
    update.message.reply_text('shades {} is up.'.format(test_box))


def echo(bot, update):
    update.message.reply_text(update.message.text)


def uprecords(bot, update):
    p = subprocess.Popen(['uprecords', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    update.message.reply_text(out)


def temp(bot, update):
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000.0
    update.message.reply_text('CPU temperature is:{}' .format(temp))

def rundmc(bot, update):
    if update.message.from_user.id == myuserid:
        input = update.message.text
        input = input.split('/rundmc ')
        os.system(input[1])
    else:
        update.message.reply_text('unavaliable for your user id.')

def halt(bot, update):
    if update.message.from_user.id == myuserid:
        update.message.reply_text('goodbye.')
        os.system('sudo halt')
    else:
        update.message.reply_text('unavaliable for your user id.')


def reboot(bot, update):
            if update.message.from_user.id == myuserid:
                update.message.reply_text('see you in a second.')
                os.system('sudo reboot')
            else:
                update.message.reply_text('unavaliable for your user id.')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(test_box_api_key[test_box])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rundmc", rundmc))
    dp.add_handler(CommandHandler("halt", halt))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("temp", temp))
    dp.add_handler(CommandHandler("uprecords", uprecords))
    dp.add_handler(CommandHandler("up", up))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
