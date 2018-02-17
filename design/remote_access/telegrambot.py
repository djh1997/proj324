# sudo pip install python-telegram-bot --upgrade

import logging
import os
import subprocess

from telegram.ext import CommandHandler, Updater
from shades import runningstateset, runningstateget, tintShadeset, sandd

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
    if update.message.from_user.id == myuserid:
        runningstateset(1)
        update.message.reply_text('started')
    else:
        update.message.reply_text('unavaliable for your user id.')


def stop(bot, update):
    if update.message.from_user.id == myuserid:
        runningstateset(0)
        update.message.reply_text('stoped')
    else:
        update.message.reply_text('unavaliable for your user id.')


def exit(bot, update):
    if update.message.from_user.id == myuserid:
        runningstateset(2)
        update.message.reply_text('exiting')
    else:
        update.message.reply_text('unavaliable for your user id.')


def help(bot, update):
    update.message.reply_text('Help me im stuck in a box!')


def up(bot, update):
    update.message.reply_text('shades {} is up.'.format(test_box))


def echo(bot, update):
    update.message.reply_text(update.message.text)


def uprecords(bot, update):
    p = subprocess.Popen(['uprecords', '-a'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    update.message.reply_text(out)


def temp(bot, update):
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000.0
    update.message.reply_text('CPU temperature is:{}' .format(temp))


def tint(bot, update):
    if update.message.from_user.id == myuserid:
        error = False
        input = update.message.text
        input = input.split('/tint ')
        tint = input[1].split(',')
        for i in range(len(tint)):
            tint[i] = int(tint[i])
            if tint[i] not in range(0, 256):
                error = True
                print(tint[i])
                update.message.reply_text(error)
        if error == False:
            tintShadeset(tint)
        else:
            update.message.reply_text(
                'valueError please enter rgb in this format /tint 0-255,0-255,0-255')
    else:
        update.message.reply_text('unavaliable for your user id.')


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


def telegramMain():
    global updater
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(test_box_api_key[test_box])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("exit", exit))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tint", tint))
    dp.add_handler(CommandHandler("rundmc", rundmc))
    dp.add_handler(CommandHandler("halt", halt))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("temp", temp))
    dp.add_handler(CommandHandler("uprecords", uprecords))
    dp.add_handler(CommandHandler("up", up))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    while runningstateget() != 2:
        if runningstateget() != 1:
            runningstateset(1)
            sandd()
    # updater.idle()
    updater.stop()


telegramMain()
