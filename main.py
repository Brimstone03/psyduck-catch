import asyncio, random, string, json 
from discord.ext import commands, tasks
import re

TOKEN = "MTE3MTY2NTgyNDc4MDY2MDgwNw.GEaSy9.XYsAidc0KnnfCYRH29ZmJFo82GPUXywTyNuuf4"

CAPTCHA_CHANNEL_id = 1175086658320859268 #put here captcha alert channel id 

with open('pokemon', 'r', encoding='utf8') as file: 
    pokemon_list = file.read()

client = commands.Bot(command_prefix='$')
client.remove_command('help')
captcha = True

def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    solution = re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)
    return solution

@client.event
async def on_ready():
    print(f'Logged into account: {client.user.name}')
    channel = client.get_channel(CAPTCHA_CHANNEL_id)
    await channel.send("I'm Ready Catch")

@client.event
async def on_message(message):
    global captcha

    if message.author.id == 854233015475109888:
        match = re.search(r'^(.+)\s?:', message.content)
        if match:
            text_before_colon = match.group(1)
            await asyncio.sleep(random.randint(1, 3))
            await message.channel.send(f'<@716390085896962058> c {text_before_colon}')

    if message.author.id == 716390085896962058:
        content = message.content
        if 'The pokémon is ' in content:
            if not len(solve(content)):
                print('Pokemon not found.')
            else:
                for i in solve(content):
                    if captcha == True:
                        await asyncio.sleep(random.randint(1, 3))
                        await message.channel.send(f'<@716390085896962058> c {i}')

        if 'That is the wrong pokémon!' in content:
            if captcha == True:
                await asyncio.sleep(random.randint(1, 3))
                await message.channel.send(f'<@716390085896962058> h')

        elif 'human' in content:
            captcha = False
            channel = client.get_channel(CAPTCHA_CHANNEL_id)
            await channel.send(f"@everyone Please verify the Poketwo captcha asap! \nafter captcha solve type `$start` https://verify.poketwo.net/captcha/{client.user.id}")

    await client.process_commands(message)

@client.command()
async def start(ctx):
    global captcha
    captcha = True
    await ctx.send("Successfully started")

@client.command()
async def say(ctx, *, text):
    await ctx.send(text)


client.run(TOKEN)
