import discord
import tok
from paramiko import SSHClient
import requests
import asyncio
import json
# from discord.ext import commands


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
async def startbot(ctx):
    await startup(ctx)

@bot.slash_command(description="Connect to Server")
async def connect(ctx,usr: str , pwd: str, server_ip: discord.Option(str, "Select server to connect to", choices=['play.dylanderechte.online'])):
    # usr = "root"
    await ctx.respond(f"Connecting to {usr}...")
    client.load_system_host_keys()
    client.connect('play.dylanderechte.online', username=usr, password=pwd)
    await ctx.respond(f"Connected to {usr}!")
    stdin, stdout, stderr = client.exec_command('cd ~; ls')
#    out = stdout.read().decode("utf8")
#    await ctx.respond(f"Output: \n {out}")

@bot.slash_command(description="Starting Server")
# @commands.has_role("server")
async def startserver(ctx):
    await startserver(ctx)

# Disconnect from server
@bot.slash_command(description="Disconnect from the server")
# @commands.has_role("server")
async def disconnect(ctx):
    await disonnectfromserver(ctx)

# Check if Online
@bot.slash_command(description="Check if server is online")
async def online(ctx, server_ip: discord.Option(str, "Select server to check", choices=['play.dylanderechte.online', '178.254.38.26'])):
    await checkonline(ctx, server_ip)

# Check player count
@bot.slash_command(description="Check player count")
async def playercount(ctx, server_ip: discord.Option(str, "Select Server to check Playercount", choices=['play.dylanderechte.online', '178.254.38.26'])):
    await playercount(ctx, server_ip)

# Stop server
@bot.slash_command(description="Stop the server")
# @commands.has_role("server")
async def stopserver(ctx):
    await stopserver(ctx)

# Get Player Names
@bot.slash_command(description="Display all Players currently online")
async def getplayer(ctx, serverip:str):
    await get_player(ctx, serverip)

# Get Mod List
@bot.slash_command(description="Display all Mods currently installed")
async def getmods(ctx, serverip:str):
    await get_mods(ctx, serverip)

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

async def checkonline(ctx, serv: str):
    response = requests.get(f"https://api.mcsrvstat.us/2/{serv}")
    if response.json()['online'] == True:
       print(response)
       await ctx.respond(f"Server {serv} is online!")
       is_online = True
    else:
        print(response)
        await ctx.respond(f"Server is offline!")

async def playercount(ctx, server:str):
    response = requests.get(f'https://api.mcsrvstat.us/2/{server}')
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
    status = response.json()['motd']['clean'][0]
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.respond(f"Type /help to see all commands!")

#Get Playernames
async def get_player(ctx, ServerIP:str):
    await ctx.respond("Checking for online players")
    check = requests.get(f"https://api.mcsrvstat.us/2/{ServerIP}")
    if check.json()['players']['online'] == 0:
        await ctx.respond("No players online")
        return
    await ctx.respond("Getting Player Names")
    response = requests.get(f"https://api.mcsrvstat.us/2/{ServerIP}")
    playerlist = response.json()['players']['list']
    print(playerlist)
    json.dumps(playerlist)
    print(type(playerlist))
    playerlist.sort()
    playerlist = json.dumps(playerlist)
    playerlist = playerlist.replace('"', '')
    playerlist = playerlist.replace('[', '')
    playerlist = playerlist.replace(']', '')
    await ctx.respond(f"Players online: {playerlist}")

#Get mod list
async def get_mods(ctx, ServerIP:str):
    await ctx.respond("Checking for mods")
    check = requests.get(f"https://api.mcsrvstat.us/2/{ServerIP}")
    
    with open('file.json', 'wb') as f:
        f.write(check.content)
    with open('file.json', 'r') as f:
        data = json.load(f)
    if 'mods' not in data:
        await ctx.respond("This server has no mods installed")
        await ctx.respond("If you think this is a mistake, please contact the server owner")
        return
    await ctx.respond("Getting mod list")
    response = requests.get(f"https://api.mcsrvstat.us/2/play.dylanderechte.online")
    modlist = response.json()['mods']['names']
    modlist.sort()
    modlist = json.dumps(modlist)
    modlist = modlist.replace('"', '')
    modlist = modlist.replace('[', '')
    modlist = modlist.replace(']', '')
    print(modlist)
    with open('modlist.json', 'w') as f:
        json.dump(modlist, f)
    js = json.load(open('modlist.json'))
    await ctx.send("Mods installed on this server: \n", file=discord.File('modlist.json'))
bot.run(tok.token)
