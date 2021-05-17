import datetime
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix='-', description='This is a backup bot')


@bot.command(name='backup')
@has_permissions(administrator=True)
async def backup(ctx, args='backup'):
    try:
        if args == 'backup':
            await ctx.reply(
                'Please enter a backup name and save it somewhere safe as it is the only way to retrieve your server. EX: -backup servername')
            return

        data = {}
        categories = ctx.guild.categories

        for category in categories:
            Text_Channels = {}
            for channel in category.text_channels:
                Text_Channels[channel.name] = []
                Text_Channels[channel.name].append({
                    'NSFW': 'false'
                })

            Voice_Channels = {}
            for channel in category.voice_channels:
                Voice_Channels[channel.name] = []
                Voice_Channels[channel.name].append({
                    'NSFW': 'false'
                })

            data[category.name] = []
            data[category.name].append({
                'Text_Channels': Text_Channels,
                'Voice_Channels': Voice_Channels,
            })

        with open(args + '.json', 'w') as outfile:
            json.dump(data, outfile)
            await ctx.reply('Backup Completed!')
            print('Backup Finished for {}'.format(ctx.guild.name))
    except MissingPermissions:
        await ctx.reply('Get an admin to do that.')


@bot.command(name='build')
@has_permissions(administrator=True)
async def build(ctx, args="backup"):
    try:
        with open(args + '.json') as json_file:
            guild = ctx.guild
            data = json.load(json_file)
            for category_name in data.keys():
                category = await guild.create_category(category_name)
                for channels in data[category_name]:
                    text_channels = channels['Text_Channels']
                    for text_channel in text_channels:
                        for info in text_channels[text_channel]:
                            NSFW = info['NSFW']

                            if NSFW == 'false':
                                NSFW = ''

                            await guild.create_text_channel(name=text_channel, category=category, nsfw=bool(NSFW))

                    voice_channels = channels['Voice_Channels']
                    for voice_channel in voice_channels:
                        for info in voice_channels[voice_channel]:
                            NSFW = info['NSFW']

                            if NSFW == 'false':
                                NSFW = ''

                            await guild.create_voice_channel(name=voice_channel, category=category, nsfw=bool(NSFW))

        await ctx.reply('Server building has finished!')
        print('Build Finished for {}'.format(ctx.guild.name))
    except FileNotFoundError:
        await ctx.reply("I couldn't find a backup file with that name.")
    except MissingPermissions:
        await ctx.reply('Get an admin to do that.')


@bot.event
async def on_ready():
    print('Backup Bot is Online!')
    for guild in bot.guilds:
        print('Connected to server: {}'.format(guild.name))


@bot.event
async def on_guild_join(guild):
    print('Bot has connected to {} @ {}'.format(guild.name, datetime.now()))

load_dotenv('.env')
bot.run(os.getenv('TOKEN'))
