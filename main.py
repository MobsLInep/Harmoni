#The version of harmoni beta 1.0
#Adding cogs in Beta 2.0
#More working on waifu features
import discord
from datetime import datetime
import json
import os
import random
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
import requests
from youtube_dl import YoutubeDL
import asyncio
from discord.ext import commands

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]
Token=os.environ.get("token")
intents= discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, help_command=None, intents=intents)

@client.event
async def on_ready():
    activity = discord.Game(name=f'-help in {len(client.guilds)} servers.', type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)

#help
@client.command()
async def help(ctx, argument='', member: discord.Member=None):
    member=ctx.author
    if argument.lower()=='utility':
        embed=discord.Embed(title="Utility Commands", description='''`-changeprefix [new prefix]`
Changes the prefix of Harmoni for the server

`-whois [member mention/id]`
Gives information about the user

`-avatar (optional:Member)`
Get the avatar of yourself or another user.

`-serverinfo`
Gives information about the guild
''', color=0x109319)
        await ctx.send(embed=embed)
    elif argument.lower()=='moderator':
        embed=discord.Embed(title="Moderator Commands", description='''`-ban [member] (optional:reason)`
Bans a member from the server

`-unban [member]`
Unbans a pre-banned member from the server

`-kick [member] (optional reason)`
Kicks a member from the server

`-mute [member] (optional:reason)`
Temporarily mutes a member in the server


''', color=0x109319)
        await ctx.send(embed=embed)
    elif argument.lower()=='music':
        embed=discord.Embed(title="Music Commands", description='''`-join`
Joins the voice channel.(Required before -play)

`-play [youtube url]`
Plays the song.

`-pause`
Pause the current song

`-resume`
Resumes the current song.

`-stop`
Stops the current song playing.

`-leave`
Leaves the voice channel.(Required)
''', color=0x109319)
        await ctx.send(embed=embed)
    elif argument.lower()=='aboutdev':
        embed=discord.Embed(title="About Commands", description='''`-aboutdev`
Gives a general info about the developer of Harmoni Bot.

`-ping`
Tells you the current latency of Hormoni bot.

`-invite`
Gives a invite link for Harmoni Bot.
''', color=0x109319)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Harmoni Bot", description='''**All Harmoni Commands Categories:**
You could type .help <command_category> for more info.''', color=0x109319)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/865876260748132353/17cc0e8ff24cbcdf4c2ea1a0f8456206.png?size=128")
        embed.add_field(name="1. :gear:Utility:", value='''`changeprefix`, `whois`, `avatar`, `serverinfo`

Type "-help utility" will give more info about all the bot commands.''', inline=False)
        embed.add_field(name="2. :hammer:Moderator:", value='''`ban`, `tempban` , `kick`, `mute`, `purge`

Type "-help moderator" to get more info about all the moderator commands.''', inline=False)
        embed.add_field(name="3. :musical_note:Music(Very unstable):", value='''`join`, `play`, `pause`, `resume`, `stop`, `leave`

Type "-help music" to get more info about all the music commands.''', inline=False)
		
        embed.add_field(name="4. :robot:About Bot and Dev(Just for fun)", value='''`aboutdev`, `ping`, `invite`

Type "-help aboutdev" to get more info about all the About commands.
[**Invite Link**](https://discord.com/api/oauth2/authorize?client_id=865876260748132353&permissions=8&scope=bot)  ||   [**Support Server**](https://discord.gg/ReTdc9dFuP)''', inline=False)
        embed.set_footer(text=f'''Harmoni Bot version-Beta 1.0. More features will be added in the upcoming version.
Requested by:{member}''', icon_url=member.avatar_url)
        await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    embed = discord.Embed(
                description=f'Ping of Bot is:{round(client.latency * 1000)}ms',
                color=0x42F56C)
    await ctx.send(embed=embed)

@client.command(aliases=['av'])
async def avatar(ctx, *,  member : discord.Member=None):
    if member==None:
      member=ctx.author
    userAvatarUrl = member.avatar_url
    embed=discord.Embed(title=f"{member.name}'s Avatar")
    embed.set_image(url=userAvatarUrl)
    await ctx.send(embed=embed)

#json.prefixes
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "-"

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
@commands.has_permissions(manage_guild=True)
async def changeprefix(ctx, prefix=''):
    try:
        if len(prefix)==0 or prefix==" " or len(prefix)>1:
            embed=discord.Embed(title="**Command triggered Insufficient/Wrong Data**", description='''Please give a appropriate single charcter
**Example**: <prefix>changeprefix *''', colour=0x3498db)
            mymessage = await ctx.send(embed=embed)
            await asyncio.sleep(4)
            await mymessage.delete()

        else:
            if prefix.isdigit()==True:

                embed=discord.Embed(title="**Command triggered Insufficient/Wrong Data**", description='''Please give a appropriate single charcter
**Example**: <prefix>changeprefix *''', colour=0x3498db)
                mymessage = await ctx.send(embed=embed)
                await asyncio.sleep(4)
                await mymessage.delete()

            else:
                with open('prefixes.json', 'r') as f:
                    prefixes = json.load(f)

                prefixes[str(ctx.guild.id)] = prefix

                with open('prefixes.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                embed=discord.Embed(title=f'**Prefix is changed to **{prefix}', colour=0xe91e63)
                await ctx.send(embed=embed)

    except:
        embed=discord.Embed(title="**Command triggered Insufficient/Wrong Data**", description='''Please give a appropriate single charcter
**Example**: <prefix>changeprefix *''', colour=0x3498db)
        mymessage = await ctx.send(embed=embed)
        await asyncio.sleep(4)
        await mymessage.delete()

#whois
@client.command()
async def whois(ctx, target: discord.Member=None):
    if target==None:
      target=ctx.author
    if target.bot==True: 
      temp='Bot' 
    else: 
      temp='Human'
    embed=discord.Embed(title='User Information',colour=target.colour,timestamp=datetime.utcnow())
    embed.set_thumbnail(url=target.avatar_url)
    role_names = [role.name for role in target.roles]
    role_names.remove('@everyone')
    if len(role_names)==0: 
      temp2=None
    else:
      temp2=role_names
    fields = [("Name", str(target), True),
				  ("ID", target.id, True),
				  ("Human/Bot?", temp, True),
				  (f"Roles[{len(role_names)}]", temp2,False),
				  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True)]


    for name,value,inline in fields:
        embed.add_field(name=name, value=value,inline=inline)

    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
		embed = discord.Embed(title="Server information",
					  colour=0x3498db,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=ctx.guild.icon_url)

		fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

@client.command()
async def verify(ctx):
    print(ctx.message.channel.id)
    print(ctx.message.author)
    mymessage = await ctx.send('Done! Welcome!')
    await asyncio.sleep(3)
    await mymessage.delete()
    await ctx.message.delete()


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=0):
    if amount<=0:
        embed=discord.Embed(title="**Command triggered Insufficient/Wrong Data**", description='''Please specify the number of messages to be purged
**Example**: .purge 10''', colour=0x3498db)
        mymessage = await ctx.send(embed=embed)
        await asyncio.sleep(4)
        await mymessage.delete()
    elif amount>0:
        await ctx.channel.purge(limit=amount+1)
        await asyncio.sleep(0.2)
        temp=str(amount)
        temp2='Purged '+temp+' Messages'
        embed=discord.Embed(title=temp2, colour=0xe74c3c)
        mymessage = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await mymessage.delete()


@client.command(aliases=['toss'])
async def random8balltest(ctx):
    responses=['Heads','Tails']
    col=[0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5]
    embed = discord.Embed(
                description=f'Tossing a coin \n Result: {random.choice(responses)}',
                color=random.choice(col))
    mym= await ctx.send(embed=embed)
    await asyncio.sleep(100)
    await mym.delete()

@client.command(name="msg", pass_context=True)
async def msg(context, userid, *, message):
    user = client.get_user(userid)
    await user.send(message)

#ban,unban,kick,mute
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=''):
  if member==None or member==ctx.author:
    await ctx.send('Mention a user')
  else:
    message = discord.Embed(description=f"You have been banned from {ctx.guild.name} \nReason: {reason}")
    await member.send(embed=message)
    await ctx.guild.ban(member, reason=reason)
    embed=discord.Embed(description=f"{member.mention} has been banned! \nReason: {reason}")
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None, *, reason='Not Specified'):
  if member==None or member==ctx.author:
    await ctx.send('Mention a user')
  else:
    message = discord.Embed(description=f"You have been kicked from {ctx.guild.name} \nReason: {reason}")
    await member.send(embed=message)
    await ctx.guild.kick(member, reason=reason)
    embed=discord.Embed(description=f"{member.mention} has been kicked! \nReason: {reason}")
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason='Not Specified'):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    message = discord.Embed(description=f"You have been muted in {ctx.guild.name} \nReason: {reason}")
    await member.send(embed=message)
  
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, userId: discord.User):
  await ctx.guild.unban(userId)
  await ctx.send(f"{userId.mention} have been unbanned sucessfully")


@client.command(aliases=['fakeban'])
async def fakebanfunctioncallment(ctx,member : discord.Member, *, reason=''):
    await ctx.send(f'Trying to Ban **{member.name}** and... its Done!')

@client.command()
async def invite(ctx):
  embed=discord.Embed(title='**Invite Link**', colour=0x3498db)
  embed.add_field(name='If you wish to add me in your server:' ,value='[Click here to add](https://discord.com/api/oauth2/authorize?client_id=865876260748132353&permissions=8&scope=bot)', inline=False)
  embed.add_field(name='Support Server for Harmoni:' ,value='[Discord Server](https://discord.gg/ReTdc9dFuP)', inline=False)
  await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    embed=discord.Embed(title="**Wrong Command Triggered**", description='''Type .help to get more info about Harmoni Bot''', colour=0xe74c3c)
    mymessage = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await mymessage.delete()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')

#command for bot to leave
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


def nekoGET(endpoint):
    r = requests.get("https://neko-love.xyz/api/v1/" + endpoint)
    if r.status_code != 200:
        return "An error has occurred"
    else:
        return r.json()["url"]
@client.command()
async def waifu(ctx):
	msg=f'{nekoGET("neko")}'
	embed=discord.Embed(title='Harmoni Waifu',colour=0xe91e63)
	embed.set_image(url=msg)
	await ctx.send(embed=embed)




keep_alive.keep_alive()
client.run(Token)
