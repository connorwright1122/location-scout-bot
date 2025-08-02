#!/bin/bash

#sleep 30

echo "===== Starting bot at $(date) =====" >> /home/connorwright/Downloads/location-scout-bot/bot.log

cd /home/connorwright/Downloads/location-scout-bot || exit

# Pull updates and log result
echo "Running git pull..." >> bot.log
/usr/bin/git pull >> bot.log 2>&1

# Activate venv and start bot
echo "Launching bot.py..." >> bot.log
/home/connorwright/Downloads/location-scout-bot/venv/bin/python bot.py >> /home/connorwright/Downloads/location-scout-bot/bot.log 2>&1

echo "===== Bot stopped at $(date) =====" >> bot.log
