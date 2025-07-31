# location-scout-bot
Code for the Buzz Studios location scout Discord bot, hosted on a Raspberry Pi Zero W. Users can DM the bot with commands to perform actions related to location scouting. 

## Commands:
- !help == Lists all commands and instructions
- !search [keyword] == Provides links to location embeddings containing the keyword
- !submit [details] == 

For submitting, send a DM to the bot in this format with at least one image attached. It will send a message to the channel specified with LOCATION_SCOUT_CHANNEL_ID in the .env file.
!submit
Location Name: Skiles Classroom Building, Room 205
Address: 686 Cherry St NW, Atlanta, GA 30332
Google Maps Link: https://maps.app.goo.gl/ujoZeo7qVoQNPYZU6
Past Shoots: Twochyon Deliverance
Tags: classroom, large, stinky
Notes: Loud A/C.

## .env file format:
BOT_TOKEN = DISCORD_TOKEN_HERE ## You can find this in the Discord Developer Console: go to Bot tab and click Reset Token

LOCATION_SCOUT_CHANNEL_ID = DISCORD_CHANNEL_ID_HERE ## Find this by enabling Developer Mode in your settings, then right clicking a channel
