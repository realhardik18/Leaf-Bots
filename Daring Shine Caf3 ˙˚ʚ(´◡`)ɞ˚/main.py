import discord
from discord.ext import commands
import random
import asyncio

client = commands.Bot(command_prefix=";")
client.remove_command('help')

@client.event
async def on_ready():
  print("im alive and working!!(logged in as {0.user})".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="For *help"))

@client.command()
async def test(message):
  await message.send("yes chef")

@client.command()
async def open(message,*,issue):
    await message.send("a private ticket channel has been created and you have been pinged! please check your pings")
    guild = message.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    code = random.randrange(10 , 100000)
    channel = await guild.create_text_channel(f'{message.author.name}{code}', overwrites=overwrites, topic=f"{code} | {issue}")
    
    await channel.send("test123")

@client.command()
async def ticket_close(message,*,code): 
    if message.channel.topic==code:
        
        await message.send("Thank you! This channel will be deleted in `5s`")
        await asyncio.sleep(5)
        await message.channel.delete()
    
    else :
        await message.send("**You entered the wrong code (it is the number in the channel topic!)**") 

client.run("ODY3MzcwMDI1MzI4MzEyMzUw.YPgHSA.rEpvSueGp0ezqTS39a2_anyeZKY")

