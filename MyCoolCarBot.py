#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Location
from time import sleep

# Bot token receieved from BotFather
TOKEN = '{bot-token}'

# Global parameters
is_locked = False
is_lights_on = False

################################################### GPIO pins setup #############################################################
GPIO.setmode(GPIO.BOARD)

#Servo
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)
#LEDs
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)


# Change the angle of the Servo motor
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)


##################################################### Command Handlers ##########################################################
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!'
                              'Im the cool car bot'
                              'What would you like to do ?')


def lock(update, context):
    set_angle(90)
    global is_locked
    is_locked = True
    update.message.reply_text('The car is locked!')


def unlock(update, context):
    set_angle(0)
    global is_locked
    is_locked = False
    update.message.reply_text('The car is unlocked!')


def turn_on_lights(update, context):
    GPIO.output(5, True)
    GPIO.output(7, True)
    GPIO.output(29, True)
    GPIO.output(31, True)
    global is_lights_on
    is_lights_on = True
    update.message.reply_text('Lights are ON!')


def turn_off_lights(update, context):
    GPIO.output(5, False)
    GPIO.output(7, False)
    GPIO.output(29, False)
    GPIO.output(31, False)
    global is_lights_on
    is_lights_on = False
    update.message.reply_text('Lights are OFF!')


def is_locked(update, context):
    global is_locked
    if is_locked:
        update.message.reply_text("I'm locked!")
    else:
        update.message.reply_text("I'm not locked")


def is_lights_on(update, context):
    global is_lights_on
    if is_lights_on:
        update.message.reply_text('Lights ON!')
    else:
        update.message.reply_text('Lights OFF!')


def where_are_you(update, context):
    context.bot.send_location(chat_id=update.message.chat_id, latitude=31.794934, longitude=35.230327)


#################################################################################################################################


def main():
    print("got inside")

	# Set up the bot updater with the bot Token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
	
	# Set up a commnad handler for each command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("lock", lock))
    dp.add_handler(CommandHandler("unlock", unlock))
    dp.add_handler(CommandHandler("islocked", is_locked))
    dp.add_handler(CommandHandler("turnonlights", turn_on_lights))
    dp.add_handler(CommandHandler("turnofflights", turn_off_lights))
    dp.add_handler(CommandHandler("islightson", is_lights_on))
    dp.add_handler(CommandHandler("whereareyou", where_are_you))

	# Start listen for incoming messages
    updater.start_polling()
    updater.idle()
    print("exit")

if __name__ == '__main__':
    main()