"""Telegram control file."""
import os
import subprocess
from functools import wraps
from random import choice, randint
from time import strftime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from shades import (debugset, getiso, modeset, runningstateget,
                    runningstateset, sandd, tintBackset, tintShadeset)

# program variables
test_box_api_key = []
test_box = 0
user = False
admins = []
allowAll = True

jokelist = [
    'I cannot think of an ample joke currently',
    'My friend told me how electricity is measured and I was like Watt! ',
    'Two antennas get married. The wedding was boring,' +
    ' but the reception was great.',
    'Why was the robot mad? People kept pushing its buttons.',
    'Why did Mr Ohm marry Mrs. Ohm? \n\r Because he couldnt resistor!',
    'What kind of car does an electrician drive?\n\r A Volts-wagon',
    'What is a robots favourite kind of music? \n\r Heavy Metal.',
    'If only DEAD people understand hexadecimal,' +
    ' how many dead people are there?\n\r57,005.',
    'What is FACE value in decimal?\n\r64206',
    'I turned on the radio this morning all I heard was FFFFFF' +
    '\n\r it turns out it was White Noise!'
]

# retrive telegram keys
f = open('telegramkeys.txt', 'r')
test_box_api_key.append(f.readline().split('\n')[0])
admins.append(int(f.readline().split('\n')[0]))
f.close()
print test_box_api_key
print admins

# Create the EventHandler and  it your bot's token.
updater = Updater(test_box_api_key[test_box])
jbq = updater.job_queue


def restricted1(func):
    """Add re-stricter for access."""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id  # get user id
        if allowAll or user_id in admins:  # if in open mode or admin id
            return func(bot, update, *args, **kwargs)  # run function
        update.message.reply_text(
            "Access denied for {}.Ask [Jo](tg://user?id={}) for access.".
            format(user_id, admins[0]),
            parse_mode=ParseMode.MARKDOWN
        )  # else echo access denied back to user
        return 'error'

    return wrapped


def restricted2(func):
    """Add re-stricter for admin only access."""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id  # get user id
        if user_id in admins:  # if  admin id
            return func(bot, update, *args, **kwargs)  # run function
        update.message.reply_text(
            "Access denied for {}.Ask [Jo](tg://user?id={}) for access.".
            format(user_id, admins[0]),
            parse_mode=ParseMode.MARKDOWN
        )  # else echo access denied back to user
        return 'error'

    return wrapped


def time():
    """Return time in formated string."""
    return str(strftime('%d/%m/%Y %H:%M:%S'))


@restricted2
def spam(bot, update, args):
    """Repetitive messages for debug."""
    if int(args[0]) == 0:  # if interval = 0
        jbq.run_once(
            sendMessage, 0, context=[int(args[1]),
                                     args[2]])  # initiate job to reply
    else:  # for reppetive jobs
        jbq.run_repeating(
            sendMessage,
            interval=int(args[0]),
            first=0,
            context=[int(args[1]), args[2]])  # initiate job to repeat


@restricted2
def halt(bot, update):
    """Turn off glasses."""
    update.message.reply_text(
        'Halting at {}'
        .format(time()))  # echo that command was received
    os.system('sudo halt')  # send shutdown command


@restricted2
def reboot(bot, update):
    """Reboot glasses."""
    update.message.reply_text(
        'Rebooting at {}'
        .format(time()))  # echo that command was received
    os.system('sudo reboot')  # send reboot command


@restricted2
def allowallids(bot, update):
    """Toggle restriction level."""
    global allowAll  # pull allowAll in so function can edit

    if allowAll:  # toggle
        allowAll = False
        update.message.reply_text('allowing restricted ids.')
    else:
        allowAll = True
        update.message.reply_text('allowing all ids.')


@restricted2
def exit(bot, update, args):
    """Exit the program cleanly."""
    if len(args) >= 1:
        f = open('run.txt', 'w+')  # open file
        f.write('no')
        f.close()  # close file
    runningstateset(2)  # set sate to exit
    update.message.reply_text('Exiting at {}'
                              .format(time()))  # echo exiting back to user


@restricted2
def addwifi(bot, update, args):
    """Add WiFi network."""
    ssid = args[0]
    psk = args[1]
    f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a')  # open file
    f.write('\nnetwork={\n        ssid="')  # format and store network
    f.write(ssid)
    f.write('"\n        psk="')
    f.write(psk)
    f.write('"\n}\n')
    f.close()  # close file
    update.message.reply_text(
        'added {} to wifi'.format(ssid))  # echo added WiFi back to user


@restricted1
def image(bot, update):
    """Send most recent image from camera."""
    bot.send_photo(
        chat_id=update.message.chat_id, photo=open('image1.jpg',
                                                   'rb'))  # send image


@restricted1
def start(bot, update):
    """Start the glasses cleanly."""
    f = open('users.txt', 'a')  # currently debugging by logging new users
    f.write('{}\n\r'.format(update.message.from_user))
    f.close()
    runningstateset(1)  # set state to running
    update.message.reply_text('started')  # echo started back to user


@restricted1
def stop(bot, update):
    """Stop/pause glasses."""
    runningstateset(0)  # set running state to stopped
    update.message.reply_text('stopped')  # echo stopped back to user


@restricted1
def mode(bot, update, args):
    """Manually change the mode."""
    modeset(int(args[0]))  # set mode
    update.message.reply_text('mode set to {}'.format(
        args[0]))  # echo mode back to user


@restricted1
def colourset(bot, update, args):
    """Set the colour of the lenses."""
    update.message.reply_text(colorSplit(
        args[0]))  # colour information to handler


@restricted1
def autoback(bot, update):
    """Calculate the background tint in manual mode."""
    usrin = getiso()  # get ambient light level
    usrin = 'back@{},{},{}'.format(
        int(usrin), int(usrin),
        int(usrin))  # format string to be passed to handler
    update.message.reply_text(colorSplit(usrin))  # string to handler


@restricted1
def tint(bot, update, args):
    """Set background tint percentage."""
    usrin = 100 - int(args[0])  # invert percentage
    usrin = 'back@{},{},{}'.format(
        int(usrin * 2.56), int(usrin * 2.56),
        int(usrin * 2.56))  # format string to be passed to handler
    update.message.reply_text(colorSplit(usrin))  # string to handler


@restricted1
def debug(bot, update):
    """Toggle command line debug."""
    debugset()  # toggle command line debug
    update.message.reply_text(
        'debug toggled')  # echo that the debug has been toggled back to user


def uprecords(bot, update):
    """Run the uprecords command and echo results."""
    p = subprocess.Popen(
        ['uprecords', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )  # open subprocess in thread and pipe back results
    out = p.communicate()  # collect results
    update.message.reply_text(out[0])  # echo results


def temp(bot, update):
    """Get cpu temperature."""
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000.0
    update.message.reply_text('CPU temperature is:{}'.format(temp))


def joke(bot, update):
    """Send a joke."""
    update.message.reply_text(choice(jokelist))  # pick random joke and send


def meme(bot, update):
    """Send a meme."""
    memeid = randint(1, 17)  # pick random image
    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=open('memes/{}.jpg'.format(memeid), 'rb'))  # send image


def help(bot, update):
    """Display help menu."""
    update.message.reply_text(
        'help im stuck in a box \n\r' +
        '/pickcolour - pick from list of tints\n\r' +
        '/pickmode- manual,tint,points or full auto\n\r' +
        '/tint percentage\n\r' + '/colourset fore-back@0-255,0-255,0-255\n\r' +
        '/start starts shades\n\r' + '/stop stop shades\n\r' +
        'for more info check the [site](git.djh1997.uk)',
        parse_mode=ParseMode.MARKDOWN)


def up(bot, update):
    """Check if glasses are online."""
    update.message.reply_text('shades {} is online.'.format(test_box))


def echo(bot, update):
    """Catch all for unrecognised commands."""
    update.message.reply_text('command {} not recognised.'.format(
        update.message.text))  # echo that the command was unrecognised
    f = open('log.txt', 'a')  # log the user id and message
    f.write('{} : '.format(update.message.text))
    f.write('{}\n\r'.format(update.message.from_user))
    f.close()


def pickcolour(bot, update):
    """Inline keyboard to pick a preset colour."""
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
    ]]  # setup layout

    reply_markup = InlineKeyboardMarkup(keyboard)  # create keyboard

    update.message.reply_text(
        'Please choose:', reply_markup=reply_markup)  # send keyboard


def pickmode(bot, update):
    """Inline keyboard to pick mode."""
    keyboard = [[
        InlineKeyboardButton("manual", callback_data=0),
        InlineKeyboardButton("tint", callback_data=1),
        InlineKeyboardButton("point", callback_data=2),
        InlineKeyboardButton("full auto", callback_data=3)
    ]]  # setup layout

    reply_markup = InlineKeyboardMarkup(keyboard)  # create keyboard

    update.message.reply_text(
        'Please choose:', reply_markup=reply_markup)  # send keyboard


def button(bot, update):
    """Create handler for inline keyboard."""
    query = update.callback_query
    tint = int(query.data)  # convert button id to int
    if tint <= 3:  # if mode button
        modeset(tint)  # set mode
        bot.edit_message_text(
            text="mode set to {}".format(tint),
            chat_id=query.message.chat_id,
            message_id=query.message.message_id)  # echo new mode
    else:  # if tint setting
        if tint <= 100:  # if standard tint
            tint = int(tint * 2.55)  # format tint
            tint = '{},{},{}'.format(tint, tint, tint)  # format tint
        elif tint == 101:  # if colour tint
            tint = '255, 200, 200'  # red
        elif tint == 102:
            tint = '200, 255, 200'  # green
        elif tint == 103:
            tint = '200, 200, 255'  # blue
        elif tint == 104:
            tint = '255, 223, 0'  # gold
        bot.edit_message_text(
            text="Selected option: {}".format(
                colorSplit('back@{}'.format(tint))),
            chat_id=query.message.chat_id,
            message_id=query.message.message_id)  # set tint and echo result


def colorSplit(usrin):
    """Colour handler."""
    error = False
    usrin = usrin.split('@')  # split colour and location
    tint = usrin[1].split(',')  # split colours
    reply = ''
    for i in range(len(tint)):  # iterate over rgb values
        tint[i] = int(tint[i])  # convert to int
        if tint[i] not in range(0, 257):  # check value is in valid range
            reply = 'rgb out of range'  # warn user of error
            error = True  # trigger error
    if error is False:  # if all values in spec
        if usrin[0] == 'back':  # set background tint
            tintBackset(tint)  # data to handler
            reply = tint  # echo back the rgb values
        elif usrin[0] == 'fore':  # set foreground tint
            tintShadeset(tint)  # data to handler
            reply = tint  # echo back the rgb values
        else:  # if not fore or back warn user and show formatting
            reply = 'valueError format like this fore-back@0-255,0-255,0-255'
    return reply


def sendMessage(bot, job):
    """Send message handler for job_queue."""
    bot.send_message(chat_id=job.context[0], text=job.context[1])


def telegramMain():
    """Telegram main function."""
    global updater

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # all
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("uprecords", uprecords))
    dp.add_handler(CommandHandler("up", up))
    dp.add_handler(CommandHandler("temp", temp))
    dp.add_handler(CommandHandler('joke', joke))
    dp.add_handler(CommandHandler('meme', meme))

    # togglable
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("mode", mode, pass_args=True))
    dp.add_handler(CommandHandler("autoback", autoback))
    dp.add_handler(CommandHandler("tint", tint, pass_args=True))
    dp.add_handler(CommandHandler("colourset", colourset, pass_args=True))
    dp.add_handler(CommandHandler('pickcolour', pickcolour))
    dp.add_handler(CommandHandler('pickmode', pickmode))
    dp.add_handler(CommandHandler('image', image))
    dp.add_handler(CommandHandler('debug', debug))

    # admins only
    dp.add_handler(CommandHandler("exit", exit, pass_args=True))
    dp.add_handler(CommandHandler('spam', spam, pass_args=True))
    dp.add_handler(CommandHandler('allowallids', allowallids))
    dp.add_handler(CommandHandler("halt", halt))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("addwifi", addwifi, pass_args=True))

    # keyboard handler
    dp.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    jbq.run_once(sendMessage, 0, context=[
                 admins[0], 'Shades booting at {}'.format(time())])
    while runningstateget() != 2:
        if runningstateget() != 1:
            runningstateset(1)
            sandd()
    # updater.idle()
    updater.stop()


telegramMain()
