import asyncio
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
        await ctx.respond(f"Server is offline!")
    
@bot.command()
async def test(ctx):
    button = discord.ui.Button(label="Connect to server", style=discord.ButtonStyle.primary, emoji="<:herr_goetter:945325132480643132>")
    button2 = discord.ui.Button(label="Start Server", style=discord.ButtonStyle.primary, emoji="<:GigaChad:882287966951723068>")
    button3 = discord.ui.Button(label="Disconnect from server", style=discord.ButtonStyle.primary, emoji="<a:peepoExit:662162946667053056>")
    button4 = discord.ui.Button(label="Check if online", style=discord.ButtonStyle.primary, emoji="<a:x_Loading:737676088339202086>")
    button5 = discord.ui.Button(label="Player Count", style=discord.ButtonStyle.primary, emoji="<:sgpeople:1003299502834319360>")
    # button6 = discord.ui.Button(label="Stop Server", style=discord.ButtonStyle.primary, emoji="<:stop:980007702698799115>")
    async def callback(interaction: discord.Interaction):
        await ctx.defer()
        await asyncio.sleep(1)
        await ctx.followup.send("Connecting to server!", ephemeral=False)
        await connecttoserver(ctx)


    async def callback2(interaction: discord.Interaction):
        await interaction.response.send_message("Starting Server!", ephemeral=False)
        startserver()


    async def callback3(interaction: discord.Interaction):
        await interaction.response.send_message("Disconnecting from server!", ephemeral=False)
        await disonnectfromserver(ctx)


    async def callback4(interaction: discord.Interaction):
        await interaction.response.send_message("Checking if online!", ephemeral=False)
        await checkonline(ctx)


    async def callback5(interaction: discord.Interaction):
        await interaction.response.send_message("Getting player count!", ephemeral=False)
        await playercount(ctx)


    # async def callback6(interaction: discord.Interaction):
    #     await interaction.response.send_message("Stopping Server!", ephemeral=False)
    #     await stopserver(ctx)


    button.callback = callback
    button2.callback = callback2
    button3.callback = callback3
    button4.callback = callback4
    button5.callback = callback5
    # button6.callback = callback6
    view = discord.ui.View()
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    await ctx.send("s" , view=view)

async def connecttoserver(ctx):
    client.load_system_host_keys()
    client.connect('play.dylanderechte.online', username="root", password="Dylan@Server")
    stdin, stdout, stderr = client.exec_command('cd ~; ls')
    out = stdout.read().decode("utf8")
    print(out)
    await ctx.respond(f"Connected to the Server!")
    #stdin, stdout, stderr = client.exec_command('tmux new -s server')

def startserver():
    #stdin, stdout, stderr = client.exec_command('tmux new -s server | neofetch')
    stdin, stdout, stderr = client.exec_command('cd ~')
    stdin, stdout, stderr = client.exec_command('./test.sh')
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
    res = response.json()['players']['online']
    await ctx.respond(f"There are {res} players online!")

# async def stopserver(ctx):
#     stdin, stdout, stderr = client.exec_command('screen -r')
#     stdin, stdout, stderr = client.exec_command('stop')
#     await ctx.respond(f"Server stopped!")




bot.run("MTAyNzI5OTAzNzI0Mzc3Mjk5OA.GWjZe7.ygoC7BU7vEt_omJWA8PJBZXAhGPMRWFUMTFeI4")
