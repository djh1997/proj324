# sudo pip install python-telegram-bot --upgrade

import logging
import os
import subprocess

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from shades import runningstateset, runningstateget, tintShadeset, tintBackset, modeset, sandd, getiso

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


def mode(bot, update):
    if update.message.from_user.id == myuserid:
        input = update.message.text.split('/mode ')
        modeset(int(input[1]))
        update.message.reply_text('mode set to {}'.format(input[1]))
    else:
        update.message.reply_text('unavaliable for your user id.')


def help(bot, update):
    update.message.reply_text(
        '/mode 0=manual 1=tint 2=points 3=full auto\n\r' +
        '/tint percentage\n\r' +
        '/colourset fore-back@0-255,0-255,0-255\n\r' +
        '/start starts shades\n\r' +
        '/stop stop shades\n\r' +
        '/exit exit shades\n\r' +
        '/reboot reboot shades\n\r' +
        '/halt shutsdown shades')


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


def colourset(bot, update):
    if update.message.from_user.id == myuserid:
        input = update.message.text.split('/colourset ')
        update.message.reply_text(colorSplit(input[1]))
    else:
        update.message.reply_text('unavaliable for your user id.')


def autoback(bot, update):
    if update.message.from_user.id == myuserid:
        input = getiso()
        input = 'back@{},{},{}'.format(
            int(input), int(input), int(input))
        update.message.reply_text(colorSplit(input))
    else:
        update.message.reply_text('unavaliable for your user id.')


def tint(bot, update):
    if update.message.from_user.id == myuserid:
        input = update.message.text
        input = input.split('/tint ')
        input = 100 - int(input[1])
        input = 'back@{},{},{}'.format(
            int(input * 2.55), int(input * 2.55), int(input * 2.55))
        update.message.reply_text(colorSplit(input))
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


def pickcolour(bot, update):
    keyboard = [[InlineKeyboardButton("10", callback_data=10)],
                [InlineKeyboardButton("50", callback_data=50)],
                [InlineKeyboardButton("80", callback_data=80)],
                [InlineKeyboardButton("90", callback_data=90)],
                [InlineKeyboardButton("100", callback_data=100)],
                [InlineKeyboardButton("red", callback_data=101)],
                [InlineKeyboardButton("green", callback_data=102)],
                [InlineKeyboardButton("blue", callback_data=103)],
                [InlineKeyboardButton("gold", callback_data=104)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    tint = int(query.data)
    if tint <= 100:
        tint = int(tint * 2.55)
        tint = '{},{},{}'.format(tint, tint, tint)
    elif tint == 101:
        tint = '255, 200, 200'
    elif tint == 102:
        tint = '200, 255, 200'
    elif tint == 103:
        tint = '200, 200, 255'
    elif tint == 104:
        tint = '255, 223, 0'
    bot.edit_message_text(text="Selected option: {}".format(colorSplit('back@{}'.format(tint))),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def colorSplit(input):
    error = False
    input = input.split('@')
    tint = input[1].split(',')
    for i in range(len(tint)):
        tint[i] = int(tint[i])
        if tint[i] not in range(0, 256):
            error = True
            return(error)
    if error == False:
        if input[0] == 'back':
            tintBackset(tint)
            return(tint)
        elif input[0] == 'fore':
            tintShadeset(tint)
            return(tint)
        else:
            return(
                'valueError please enter rgb in this format fore-back@0-255,0-255,0-255')
    else:
        return(
            'valueError please enter rgb in this format fore-back@0-255,0-255,0-255')


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
    dp.add_handler(CommandHandler("mode", mode))
    dp.add_handler(CommandHandler("autoback", autoback))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tint", tint))
    dp.add_handler(CommandHandler("colourset", colourset))
    #dp.add_handler(CommandHandler("rundmc", rundmc))
    dp.add_handler(CommandHandler("halt", halt))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("temp", temp))
    dp.add_handler(CommandHandler("uprecords", uprecords))
    dp.add_handler(CommandHandler("up", up))
    dp.add_handler(CommandHandler('pickcolour', pickcolour))
    dp.add_handler(CallbackQueryHandler(button))

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
