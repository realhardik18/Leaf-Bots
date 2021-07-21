import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
#from discord import Embed
#from discord import MissingPermissions
client = commands.Bot(command_prefix=":")
client.remove_command('help')


@client.event
async def on_ready():
  print("im alive and working!!(logged in as {0.user})".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="For :help"))

@client.command()
async def test(ctx):
  await ctx.send("```yaml\nI am Alive and Working!```")


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, why=f"No Reason Provided"):
    await member.kick(reason=why)
    #await ctx.channel.send(f"**{member} has been kicked from this server by {ctx.author}**")
    em = discord.Embed(title=f"{member.name}#{member.discriminator}is kicked", description = f"Name : `{member.name}`\nKicked by : `{ctx.author}`\nReason : `{why}`")
    em.set_footer(text = 'this bot was made for FREE by leaf bots, https://dsc.gg/leafbots')
    
    await ctx.send(embed = em)

@kick.error
async def kick_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(":redTick: You don't have permission to kick members.")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    em = discord.Embed(title = 'Banned!' , description = f'Name : {member}\nMod : {ctx.author}\nReason : {reason}')
    em.set_footer(text = 'this bot was made for FREE by leaf bots, https://dsc.gg/leafbots')
    await ctx.send(embed = em)

#The below code unbans player.
@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'```yaml\nUnbanned {user.mention}```')
            return

@client.command()
@commands.has_permissions(administrator = True)
async def warn(ctx,mem:discord.Member , * , tex):
  em = discord.Embed(title = f'Warning from {ctx.author.guild}' , description = f'Moderator : {ctx.author}\nReason : {tex}')
  await mem.send(embed = em)
  await ctx.send('```yaml\n-Warning sent to user```')

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f"```yaml\n- you have unmuted from: - {ctx.guild.name}```")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f"```diff\n- you have been muted from: {guild.name} reason: {reason}```")


@client.command()
async def help(ctx):
  em = discord.Embed(title = 'Help Menu!' , description = '```𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 - 𝘼𝙙𝙢𝙞𝙣 𝙤𝙣𝙡𝙮\nPrefix - :\n\nban <member> <reason>\nunban <member>\nkick <member> <reason>\nwarn <member> <reason>\nmute <member> <reason>\nunmute <member> <reason>\ntest\n\nExample - :ban @member#1234```')
  em.set_footer(text='Made by LeafBots : dsc.gg/leafbots')
  await ctx.send(embed = em)




keep_alive()

my_secret = os.environ['code']

client.run(my_secret)