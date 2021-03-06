import discord
from discord.ext import commands
import random
import asyncio
from discord.message import Message
import os
from keep_alive import keep_alive

client = commands.Bot(command_prefix="-")
client.remove_command('help')

@client.event
async def on_ready():
  print("im alive and working!!(logged in as {0.user})".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="For -help"))

@client.command()
async def test(message):
  await message.send("yes sir")

@client.command()
async def open(message,*,issue):
  await message.send("a private ticket channel has been created and you have been pinged! please check your pings")
  guild = message.guild
  overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      guild.me: discord.PermissionOverwrite(read_messages=True)
  }
  code = random.randrange(100 , 999)
  channel = await guild.create_text_channel(f'{message.author.name}{code}', overwrites=overwrites, topic=f"{code} | {issue}")
  await channel.set_permissions(message.author, read_messages=True,send_messages=True)                              
  await channel.send(f"created ticket for {message.author.mention}!")

@client.command()
async def close(message,*,code): 
  if message.channel.topic[0:3]==code:        
    await message.send("Thank you! This channel will be deleted in `5s`")
    await asyncio.sleep(5)
    await message.channel.delete()
  else :
    await message.send("You entered the wrong code (it is the number in the channel topic!)") 

@client.group(invoke_without_command=True)
async def help(message):
  embed=discord.Embed(title="Ticket bot", description="Prefix - `;` ・ Made for [Leafbots](https://dsc.gg/leafbots)", color=0x2ecc71)
  embed.add_field(name=";open [topic]", value="Create a ticket with a specific topic\n`;open Help with rules`", inline=False)
  embed.add_field(name=";close [code]", value="Close a ticket created, the code is generated by the bot and will be there in the channel topic.\n`;close 335`", inline=False)
  await message.send(embed=embed)

my_secret = os.environ['sec']

keep_alive()
client.run(my_secret)