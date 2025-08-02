#!/bin/bash

## make sure that the bot has access to write to bot.log with sudo chmod 666 /home/connorwright/Downloads/location-scout-bot/bot.log

echo "===== Starting bot at $(date) =====" >> /home/connorwright/Downloads/location-scout-bot/bot.log

cd /home/connorwright/Downloads/location-scout-bot || exit

# Stash local changes before pulling
echo "Stashing local changes..." >> "$LOGFILE"
/usr/bin/git stash --include-untracked >> "$LOGFILE" 2>&1

# Pull updates and log result
echo "Running git pull..." >> bot.log
/usr/bin/git pull >> bot.log 2>&1

sleep 10

# Activate venv and start bot
echo "Launching bot.py..." >> bot.log
/home/connorwright/Downloads/location-scout-bot/venv/bin/python bot.py >> /home/connorwright/Downloads/location-scout-bot/bot.log 2>&1

echo "===== Bot stopped at $(date) =====" >> bot.log
