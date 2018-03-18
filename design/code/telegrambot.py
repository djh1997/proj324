# sudo pip install python-telegram-bot --upgrade

import logging
import os
import subprocess
from random import choice, randint

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from shades import (debugset, getiso, modeset, runningstateget,
                    runningstateset, sandd, tintBackset, tintShadeset)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

test_box_api_key = ['514877936:AAH1p-_zloWkXoJC4j8dVYTf05NNBYOQ5e8']
test_box = 0
user = False
admins = [417245494]
allowAll = True

# Create the EventHandler and pass it your bot's token.
updater = Updater(test_box_api_key[test_box])


def start(bot, update):
    f = open('log.txt', 'a')
    f.write('{}\n\r'.format(update.message.from_user))
    f.close()
    if update.message.from_user.id in admins or allowAll:
        runningstateset(1)
        update.message.reply_text('started')
    else:
        update.message.reply_text('unavailable for your user id.')


def stop(bot, update):
    if update.message.from_user.id in admins or allowAll:
        runningstateset(0)
        update.message.reply_text('stopped')
    else:
        update.message.reply_text('unavailable for your user id.')


def exit(bot, update):
    if update.message.from_user.id in admins:
        runningstateset(2)
        update.message.reply_text('exiting')
    else:
        update.message.reply_text('unavailable for your user id.')


def mode(bot, update):
    if update.message.from_user.id in admins or allowAll:
        usrin = update.message.text.split('/mode ')
        modeset(int(usrin[1]))
        update.message.reply_text('mode set to {}'.format(usrin[1]))
    else:
        update.message.reply_text('unavailable for your user id.')


def help(bot, update):
    update.message.reply_text(
        'help im stuck in a box \n\r' +
        '/mode 0=manual 1=tint 2=points 3=full auto\n\r' +
        '/tint percentage\n\r' + '/colourset fore-back@0-255,0-255,0-255\n\r' +
        '/start starts shades\n\r' + '/stop stop shades\n\r' +
        '/exit exit shades\n\r' + '/reboot reboot shades\n\r' +
        '/halt shutsdown shades')


def up(bot, update):
    update.message.reply_text('shades {} is up.'.format(test_box))


def echo(bot, update):
    update.message.reply_text('command {} not recognised.'.format(
        update.message.text))
    f = open('log.txt', 'a')
    f.write('{} : '.format(update.message.text))
    f.write('{}\n\r'.format(update.message.from_user))
    f.close()


def uprecords(bot, update):
    p = subprocess.Popen(
        ['uprecords', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    update.message.reply_text(out[0])


def temp(bot, update):
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000.0
    update.message.reply_text('CPU temperature is:{}'.format(temp))


def colourset(bot, update):
    if update.message.from_user.id in admins or allowAll:
        usrin = update.message.text.split('/colourset ')
        update.message.reply_text(colorSplit(usrin[1]))
    else:
        update.message.reply_text('unavailable for your user id.')


def autoback(bot, update):
    if update.message.from_user.id in admins or allowAll:
        usrin = getiso()
        usrin = 'back@{},{},{}'.format(int(usrin), int(usrin), int(usrin))
        update.message.reply_text(colorSplit(usrin))
    else:
        update.message.reply_text('unavailable for your user id.')


def tint(bot, update):
    if update.message.from_user.id in admins or allowAll:
        usrin = update.message.text
        usrin = usrin.split('/tint ')
        usrin = 100 - int(usrin[1])
        usrin = 'back@{},{},{}'.format(
            int(usrin * 2.56), int(usrin * 2.56), int(usrin * 2.56))
        update.message.reply_text(colorSplit(usrin))
    else:
        update.message.reply_text('unavailable for your user id.')


def rundmc(bot, update):
    if update.message.from_user.id in admins or allowAll:
        usrin = update.message.text
        usrin = usrin.split('/rundmc ')
        os.system(usrin[1])
    else:
        update.message.reply_text('unavailable for your user id.')


def halt(bot, update):
    if update.message.from_user.id in admins:
        update.message.reply_text('goodbye.')
        os.system('sudo halt')
    else:
        update.message.reply_text('unavailable for your user id.')


def debug(bot, update):
    if update.message.from_user.id in admins or allowAll:
        debugset()
        update.message.reply_text('debug toggled')
    else:
        update.message.reply_text('unavailable for your user id.')


def allowallids(bot, update):
    global allowAll
    if update.message.from_user.id in admins:
        if allowAll:
            allowAll = False
            update.message.reply_text('allowing restricted ids.')
        else:
            allowAll = True
            update.message.reply_text('allowing all ids.')
    else:
        update.message.reply_text('unavailable for your user id.')


def joke(bot, update):
    jokelist = [
        'I cannot think of a joke currently',
        'My friend told me how electricity is measured and I was like Watt! ',
        'Two antennas get married. The wedding was boring, but the reception was great.',
        'Why was the robot mad? People kept pushing its buttons.',
        'Why did Mr Ohm marry Mrs. Ohm? \n\r Because he couldnt resistor!',
        'What kind of car does an electrician drive?\n\r A Volts-wagon',
        'What is a robots favourite kind of music? \n\r Heavy Metal.',
        'If only DEAD people understand hexadecimal, how many dead people are there?\n\r57,005.',
        'What is FACE value in decimal? 64206',
        'I turned on the radio this morning all I heard was FFFFFF it turns out it was White Noise!'
    ]
    joke = choice(jokelist)
    update.message.reply_text(joke)
    print joke


def meme(bot, update):
    chat_id = update.message.chat_id
    memeid = randint(1, 17)
    bot.send_photo(
        chat_id=chat_id, photo=open('memes/{}.jpg'.format(memeid), 'rb'))


def reboot(bot, update):
    if update.message.from_user.id in admins:
        update.message.reply_text('see you in a second.')
        os.system('sudo reboot')
    else:
        update.message.reply_text('unavailable for your user id.')


def image(bot, update):
    if update.message.from_user.id in admins:
        chat_id = update.message.chat_id
        bot.send_photo(chat_id=chat_id, photo=open('image1.jpg', 'rb'))
    else:
        update.message.reply_text('unavailable for your user id.')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def pickcolour(bot, update):
    keyboard = [[
        InlineKeyboardButton("50", callback_data=50),
        InlineKeyboardButton("80", callback_data=80),
        InlineKeyboardButton("90", callback_data=90),
        InlineKeyboardButton("100", callback_data=100)
    ], [
        InlineKeyboardButton("red", callback_data=101),
        InlineKeyboardButton("green", callback_data=102),
        InlineKeyboardButton("blue", callback_data=103),
        InlineKeyboardButton("gold", callback_data=104)
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def pickmode(bot, update):
    keyboard = [[
        InlineKeyboardButton("manual", callback_data=0),
        InlineKeyboardButton("tint", callback_data=1),
        InlineKeyboardButton("point", callback_data=2),
        InlineKeyboardButton("full auto", callback_data=3)
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    tint = int(query.data)
    if tint <= 3:
        modeset(tint)
        bot.edit_message_text(
            text="mode set to {}".format(tint),
            chat_id=query.message.chat_id,
            message_id=query.message.message_id)
    else:
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
        bot.edit_message_text(
            text="Selected option: {}".format(
                colorSplit('back@{}'.format(tint))),
            chat_id=query.message.chat_id,
            message_id=query.message.message_id)


def colorSplit(usrin):
    error = False
    usrin = usrin.split('@')
    tint = usrin[1].split(',')
    reply = ''
    for i in range(len(tint)):
        tint[i] = int(tint[i])
        if tint[i] not in range(0, 256):
            reply = 'tint out of spec'
    if error is False:
        if usrin[0] == 'back':
            tintBackset(tint)
            reply = tint
        elif usrin[0] == 'fore':
            tintShadeset(tint)
            reply = tint
        else:
            reply = 'valueError please enter rgb in this format fore-back@0-255,0-255,0-255'

    else:
        reply = 'valueError please enter rgb in this format fore-back@0-255,0-255,0-255'
    return reply


def telegramMain():
    global updater

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
    # dp.add_handler(CommandHandler("rundmc", rundmc))
    dp.add_handler(CommandHandler("halt", halt))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("temp", temp))
    dp.add_handler(CommandHandler("uprecords", uprecords))
    dp.add_handler(CommandHandler("up", up))
    dp.add_handler(CommandHandler('pickcolour', pickcolour))
    dp.add_handler(CommandHandler('pickmode', pickmode))
    dp.add_handler(CommandHandler('image', image))
    dp.add_handler(CommandHandler('debug', debug))
    dp.add_handler(CommandHandler('allowallids', allowallids))
    dp.add_handler(CommandHandler('joke', joke))
    dp.add_handler(CommandHandler('meme', meme))
    dp.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, echo))

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
