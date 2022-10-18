import discord
from paramiko import SSHClient
import requests



bot = discord.Bot(intents = discord.Intents.all())
b_name = "testing_bot"
client = SSHClient()
is_online = False

@bot.slash_command()
async def hi(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")

@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{b_name} says hello to {ctx.author.mention}!")

# Get Role test command
@bot.slash_command()
async def getrole(ctx):
    member = ctx.author
    name = ctx.author.name
    role = discord.utils.get(ctx.guild.roles, name="test")
    print(role)
    await member.add_roles(role)
    await ctx.respond(f"You got the role {role}, {name}!")

# Establishing a connection to the server and ls command print as discord message
@bot.slash_command(description="Connect to Server")
async def connect(ctx, pwd: str):
    usr = "root"
    await ctx.respond(f"Connecting to {usr}...")
    client.load_system_host_keys()
    client.connect('play.dylanderechte.online', username=usr, password=pwd)
    await ctx.respond(f"Connected to {usr}!")
    stdin, stdout, stderr = client.exec_command('cd ~; ls')
    out = stdout.read().decode("utf8")
    await ctx.respond(f"Output: \n {out}")

@bot.slash_command(description="Starting Server")
async def startserver(ctx):
    await ctx.respond(f"Starting Server...")
    stdin, stdout, stderr = client.exec_command('cd ~; ./test.sh')
    out = stdout.read().decode("utf8")
    await ctx.respond(f"Output: \n {out}")


# Disconnect from server
@bot.slash_command(description="Disconnect from the server")
async def disconnect(ctx):
    await ctx.respond(f"Disconnected from server!")
    stdin, stdout, stderr = client.exec_command('exit')
    client.close()
    await ctx.respond(f"Disconnected!")


# Check if Online
@bot.slash_command(description="Check if server is online")
async def online(ctx):
    response = requests.get('https://api.mcsrvstat.us/2/play.dylanderechte.online')
    if response.json()['online'] == True:
        await ctx.respond(f"Server is online!")
        is_online = True
    else:
        await ctx.respond(f"Offline")
    

bot.run("MTAyNzI5OTAzNzI0Mzc3Mjk5OA.GWjZe7.ygoC7BU7vEt_omJWA8PJBZXAhGPMRWFUMTFeI4")
