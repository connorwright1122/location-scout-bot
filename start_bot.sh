#!/bin/bash

# Wait for internet and user services to be ready
sleep 30

# Move to project directory
cd /home/connorwright/Downloads/location-scout-bot || exit

# Pull latest changes
/usr/bin/git pull

# Load environment and run bot
/home/connorwright/Downloads/location-scout-bot/venv/bin/python bot.py >> /home/connorwright/Downloads/location-scout-bot/bot.log 2>&1
