import os
import re
import json
import discord
import pixivwork

with open('config.json', 'r') as f:
    config = json.load(f)
discordToken = config['discord_token']
pixivUrl = config['artwork_url']

client = discord.Client(ws = int(os.environ.get('PORT', 5000)))

@client.event
async def on_ready():
    print('READY')

@client.event
async def on_message(message):
    content = message.content
    if re.search(pixivUrl, content):
        if re.search('#manga', content):
            content = content.replace('#manga', '')
        
        if re.search('!all ', content):
            content = content.replace('!all ', '')
            artworkId = content[len(pixivUrl):]
            work = pixivwork.Pixivwork(artworkId = artworkId)

            title, user, fileName, pageCount = work.getArtworks()
            embed=discord.Embed(title=user, description=title)
            for i in range(pageCount):
                artworkPath = f'{i}_{fileName}'
                file = discord.File(artworkPath)
                embed.set_image(url=f'attachment://{artworkPath}')
                if i == 0 :
                    await message.channel.send(file=file, embed=embed)
                else:
                    await message.channel.send(file=file)
                os.remove(artworkPath)
        else:
            artworkId = content[len(pixivUrl):]
            work = pixivwork.Pixivwork(artworkId = artworkId)

            title, user, artworkPath = work.getArtwork()
            file = discord.File(fp=artworkPath,filename=artworkPath)
            embed=discord.Embed(title=user, description=title)
            embed.set_image(url=f'attachment://{artworkPath}')
            await message.channel.send(file=file, embed=embed)
            os.remove(artworkPath)

client.run(discordToken)