import discord
from paramiko import SSHClient
import requests
import asyncio
from discord.ext import commands


bot = discord.Bot(intents = discord.Intents.all())
b_name = "Dylan's Server Manager"
client = SSHClient()
is_online = False

#@bot.slash_command()
#@commands.has_role("test")
#async def getrole(ctx):
#    member = ctx.author
#    name = ctx.author.name
#    role = discord.utils.get(ctx.guild.roles, name="test")
#    print(role)
#    await member.add_roles(role)
#    await ctx.respond(f"You got the role {role}, {name}!")

@bot.slash_command(description="Updates the bot")
async def startup(ctx):
    await startup(ctx)

@bot.slash_command(description="Connect to Server")
@commands.has_role("server")
async def connect(ctx, pwd: str):
    usr = "root"
    await ctx.respond(f"Connecting to {usr}...")
    client.load_system_host_keys()
    client.connect('play.dylanderechte.online', username=usr, password=pwd)
    await ctx.respond(f"Connected to {usr}!")
    stdin, stdout, stderr = client.exec_command('cd ~; ls')
#    out = stdout.read().decode("utf8")
#    await ctx.respond(f"Output: \n {out}")

@bot.slash_command(description="Starting Server")
@commands.has_role("server")
async def startserver(ctx):
    await startserver(ctx)

# Disconnect from server
@bot.slash_command(description="Disconnect from the server")
@commands.has_role("server")
async def disconnect(ctx):
    await disonnectfromserver(ctx)

# Check if Online
@bot.slash_command(description="Check if server is online")
async def online(ctx):
    await checkonline(ctx)

# Check player count
@bot.slash_command(description="Check player count")
async def playercount(ctx):
    await playercount(ctx)

# Stop server
@bot.slash_command(description="Stop the server")
@commands.has_role("server")
async def stopserver(ctx):
    await stopserver(ctx)


async def connecttoserver(ctx):
    client.load_system_host_keys()
    client.connect('play.dylanderechte.online', username="root", password="Dylan@Server")
    stdin, stdout, stderr = client.exec_command('cd ~; ls')
    out = stdout.read().decode("utf8")
    print(out)
    await ctx.respond(f"Connected to the Server!")
    #stdin, stdout, stderr = client.exec_command('tmux new -s server')

async def startserver(ctx):
    #stdin, stdout, stderr = client.exec_command('tmux new -s server | neofetch')
    stdin, stdout, stderr = client.exec_command('cd ~')
    stdin, stdout, stderr = client.exec_command('./test.sh')
    await ctx.respond(f"Server starting!")
    out = stdout.read().decode("utf8")
    print(out)

async def disonnectfromserver(ctx):
    stdin, stdout, stderr = client.exec_command('tmux detach')
    stdin, stdout, stderr = client.exec_command('exit')
    await ctx.respond(f"Disconnected from Server!")
    client.close()

async def checkonline(ctx):
    response = requests.get('https://api.mcsrvstat.us/2/play.dylanderechte.online')
    if response.json()['online'] == True:
       await ctx.respond(f"Server is online!")
       is_online = True
    else:
        await ctx.respond(f"Server is offline!")

async def playercount(ctx):
    response = requests.get('https://api.mcsrvstat.us/2/play.dylanderechte.online')
    res1 = response.json()['players']['online']
    res2 = response.json()['players']['max']
    await ctx.respond(f"There are {res1} out of {res2} players online!")

async def stopserver(ctx):
     stdin, stdout, stderr = client.exec_command('screen -R')
     out = stdout.read().decode("utf8")
     await ctx.respond(f"Output: \n {out}")
     stdin, stdout, stderr = client.exec_command('stop')
     await ctx.respond(f"Server stopped!")
     client.send(chr(3))

async def startup(ctx):
    await ctx.respond(f"Bot is online!")
    response = requests.get('https://api.mcsrvstat.us/2/play.dylanderechte.online')
    status = response.json()['motd']['clean']
    await bot.change_presence(activity=discord.Game(name= status))
    await ctx.respond(f"Type /help to see all commands!")



bot.run("MTAyNzI5OTAzNzI0Mzc3Mjk5OA.GWjZe7.ygoC7BU7vEt_omJWA8PJBZXAhGPMRWFUMTFeI4")
