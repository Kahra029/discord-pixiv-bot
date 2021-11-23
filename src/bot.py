import os
import re
import json
import discord
from pixivwork import PixivWork

with open('config.json', 'r') as f:
    config = json.load(f)
discordToken = config['discord_token']
artworkUrl = config['artwork_url']

client = discord.Client(ws = int(os.environ.get('PORT', 5000)))

@client.event
async def on_ready():
    print('READY')

@client.event
async def on_message(message):
    content = message.content
    if re.search(artworkUrl, content):
        if re.search('#manga', content):
            content = content.replace('#manga', '')
        
        if re.search('!all ', content):
            content = content.replace('!all ', '')
            artworkId = content[len(artworkUrl):]
            work = PixivWork(artworkId)

            result = work.getArtworks()
            embed=discord.Embed(title=result["user"], description=result["title"])
            for i in range(result["pageCount"]):
                artworkPath = f'{i}_{result["fileName"]}'
                file = discord.File(artworkPath)
                embed.set_image(url=f'attachment://{artworkPath}')
                if i == 0 :
                    await message.channel.send(file=file, embed=embed)
                else:
                    await message.channel.send(file=file)
                os.remove(artworkPath)
        else:
            artworkId = content[len(artworkUrl):]
            work = PixivWork(artworkId)
            result = work.getArtwork()
            file = discord.File(fp=result["fileName"],filename=result["fileName"])
            embed=discord.Embed(title=result["user"], description=result["title"])
            embed.set_image(url=f'attachment://{result["fileName"]}')
            await message.channel.send(file=file, embed=embed)
            os.remove(result["fileName"])

client.run(discordToken)