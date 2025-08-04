#!/bin/bash

LOGFILE="/home/connorwright/Downloads/location-scout-bot/bot.log"
REPO_DIR="/home/connorwright/Downloads/location-scout-bot"

# Make sure log file is writable
sudo chmod 666 "$LOGFILE"

echo "===== Starting bot at $(date) =====" >> "$LOGFILE"

cd "$REPO_DIR" || exit

# Stash only tracked changes (keep untracked files like venv/ and bot.log)
echo "Stashing tracked changes (keeping untracked files)..." >> "$LOGFILE"
/usr/bin/git stash push --keep-index >> "$LOGFILE" 2>&1

# Pull updates and log result
echo "Running git pull..." >> "$LOGFILE"
/usr/bin/git pull >> "$LOGFILE" 2>&1

# Optional: small delay to ensure environment settles
sleep 5

# Launch the bot
echo "Launching bot.py..." >> "$LOGFILE"
"$REPO_DIR/venv/bin/python" "$REPO_DIR/bot.py" >> "$LOGFILE" 2>&1

echo "===== Bot stopped at $(date) =====" >> "$LOGFILE"