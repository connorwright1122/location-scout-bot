import discord
import re
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LOCATION_SCOUT_CHANNEL_ID = int(os.getenv('LOCATION_SCOUT_CHANNEL_ID'))
print(LOCATION_SCOUT_CHANNEL_ID)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.dm_messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # only respond to user messages
    if message.guild is not None or message.author.bot:
        return 
    if message.author == client.user:
        return
    
    content = message.content.strip()

    # Extract info 
    name_match = re.search(r"Location Name:\s*(.+)", content, re.IGNORECASE)
    address_match = re.search(r"Address:\s*(.+)", content, re.IGNORECASE)
    maps_match = re.search(r"Google Maps Link:\s*(.+)", content, re.IGNORECASE)
    tags_match = re.search(r"Tags:\s*(.+)", content, re.IGNORECASE)
    notes_match = re.search(r"Notes:\s*([\s\S]*?)(?=\n\S|$)", content, re.IGNORECASE)
    past_shoots_match = re.search(r"Past Shoots:\s*(.+)", content, re.IGNORECASE)

    if not name_match:
        await message.channel.send("⚠️ Please attach at least 1 image and format your message like: \
                                   ``` \
                                   \nLocation Name: Skiles Classroom Building, Room 205 \
                                   \nAddress: 686 Cherry St NW, Atlanta, GA 30332 \
                                   \nGoogle Maps Link: https://maps.app.goo.gl/ujoZeo7qVoQNPYZU6 \
                                   \nPast Shoots: Twochyon Deliverance \
                                   \nTags: classroom, large, stinky \
                                   \nNotes: Loud A/C. \
                                   \n```")
        return

    location_name = name_match.group(1).strip()
    address = address_match.group(1).strip()
    maps_link = maps_match.group(1).strip()
    tags = tags_match.group(1).strip() if tags_match else "N/A"
    notes = notes_match.group(1).strip() if notes_match else "N/A"
    past_shoots = past_shoots_match.group(1).strip() if past_shoots_match else "N/A"

    embed = discord.Embed(
        title=f"📍 {location_name}",
        description=f"**Submitted by:** {message.author.display_name}",
        color=discord.Color.blue()
    )
    if address and maps_link: 
        embed.add_field(name="🗺️ Address", value=f"[{address}]({maps_link})", inline=False)
    else:
        embed.add_field(name="🗺️ Address", value=address, inline=False)
    embed.add_field(name="🎬 Past Shoots", value=past_shoots, inline=False)
    embed.add_field(name="🏷️ Tags", value=tags, inline=False)
    embed.add_field(name="📝 Notes", value=notes, inline=False)

    image_urls = []
    for attachment in message.attachments:
        if attachment.content_type and "image" in attachment.content_type:
            image_urls.append(attachment.url)

    if len(image_urls) == 0:
        await message.channel.send("⚠️ Error: Please attach at least one image.")
        return

    if image_urls:
        embed.set_image(url=image_urls[0])  # Only the first is shown in the embed
        if len(image_urls) > 1:
            embed.add_field(name="🖼️ Additional Images", value="\n".join(image_urls[1:]), inline=False)

    location_channel = client.get_channel(LOCATION_SCOUT_CHANNEL_ID)
    if location_channel:
        await location_channel.send(embed=embed)
        await message.channel.send("✅ Your location has been submitted!")
    else:
        await message.channel.send("⚠️ Error: Could not find the #location-scout channel.")


client.run(BOT_TOKEN)