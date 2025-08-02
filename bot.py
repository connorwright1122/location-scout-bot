import discord
import re
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LOCATION_SCOUT_CHANNEL_ID = int(os.getenv('LOCATION_SCOUT_CHANNEL_ID'))
#print(LOCATION_SCOUT_CHANNEL_ID)

prefix_search = "!search"
prefix_submit = "!submit"
prefix_help = "!help"
prefix_adminmsg = "!adminmsg"
prefix_stats = "!stats"

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

    if content.startswith(prefix_submit):
        await submit_location(message=message, content=content)
    
    elif content.startswith(prefix_search):
        await search_location(message=message, content=content)
    
    elif content.startswith(prefix_adminmsg):
        await admin_msg(message=message, content=content)
    
    elif content.startswith(prefix_stats):
        await get_stats(message=message, content=content)

    else:
        await help(message=message)

async def submit_location(message, content):
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

async def search_location(message, content):
    search_term = content.split(prefix_search, 1)[1].strip()
    found_messages = []
    location_channel = client.get_channel(LOCATION_SCOUT_CHANNEL_ID)

    if not location_channel:
        await message.channel.send("⚠️ Could not access the location channel.")
        return

    messages = [msg async for msg in location_channel.history(limit=1000)]

    for msg in messages:
        # check raw text
        #if search_term.lower() in msg.content.lower():
            #found_messages.append(msg)
        
        # check embedding text
        if (len(msg.embeds) > 0):
            for embed in msg.embeds: 
                #print("Embed Title:", embed.title)
                #print("Embed Description:", embed.description)

                if search_term.lower() in embed.title.lower():
                    found_messages.append({"location": embed.title, "url": msg.jump_url})
                    continue

                elif (embed.fields):
                    for field in embed.fields:
                        #print(f"Field Name: {field.name}, Field Value: {field.value}")
                        if search_term.lower() in field.value.lower():
                            found_messages.append({"location": embed.title, "url": msg.jump_url})
                            continue

                #elif (embed.footer):
                    #print("Footer Text:", embed.footer.text)
    
    if found_messages:
        response = f"Found {len(found_messages)} locations containing '{search_term}':\n"
        for msg in found_messages:
            #response += f"- {msg.author.display_name}: {msg.content} ({msg.jump_url})\n"
            response += f"{msg['location']} - ({msg['url']})\n"
        await message.channel.send(response)
    else:
        await message.channel.send(f"No locations found containing '{search_term}' in this channel.")

async def admin_msg(message, content):
    msg = content.split(prefix_adminmsg, 1)[1].strip()
    found_messages = []
    location_channel = client.get_channel(LOCATION_SCOUT_CHANNEL_ID)

    if not location_channel:
        await message.channel.send("⚠️ Could not access the location channel.")
        return
    
    await location_channel.send(msg)

async def get_stats(message, content):
    leaderboard = {}
    author = message.author.display_name
    location_channel = client.get_channel(LOCATION_SCOUT_CHANNEL_ID)

    if not location_channel:
        await message.channel.send("⚠️ Could not access the location channel.")
        return

    messages = [msg async for msg in location_channel.history(limit=1000)]

    for msg in messages:
        # check raw text
        #if search_term.lower() in msg.content.lower():
            #found_messages.append(msg)
        
        # check embedding text
        if (len(msg.embeds) > 0):
            for embed in msg.embeds: 
                #extracted_author = # from embed.description which is f"**Submitted by:** {message.author.display_name}",
                match = re.search(r"\*\*Submitted by:\*\*\s*(.+)", embed.description)
                extracted_author = match.group(1) if match else "Unknown"

                if extracted_author not in leaderboard:
                    leaderboard[extracted_author] = 0

                #if extracted_author in leaderboard:
                leaderboard[extracted_author] += 1

                continue
    
    if leaderboard:
        your_val = leaderboard[author] if leaderboard[author] else 0
        response = f"You have submitted {your_val} locations.\nStats:\n"
        for key, value in leaderboard.items():
            response += f"{key} - {value}\n"
        await message.channel.send(response)
    else:
        await message.channel.send(f"Error fetching stats.")


async def help(message):
    response = "Commands: \
    \n- !help \
    \n- !stats \
    \n- !search [keyword] \
    \n- !submit  \
        \nLocation Name: Skiles Classroom Building, Room 205 \
        \nAddress: 686 Cherry St NW, Atlanta, GA 30332 \
        \nGoogle Maps Link: https://maps.app.goo.gl/ujoZeo7qVoQNPYZU6 \
        \nPast Shoots: Twochyon Deliverance \
        \nTags: classroom, large, stinky \
        \nNotes: Loud A/C. \
        \n\
    "
    await message.channel.send(response)

client.run(BOT_TOKEN)