from dis import disco
from multiprocessing import AuthenticationError
from sys import stdin
import this
import discord
from paramiko import SSHClient


bot = discord.Bot(intents = discord.Intents.all())
b_name = "@testing_bot"

@bot.slash_command()
async def hi(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")

@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{b_name} says hello to {ctx.author.mention}!")
@bot.slash_command()
async def getrole(ctx):
    member = ctx.author
    name = ctx.author.name
    role = discord.utils.get(ctx.guild.roles, name="test")
    print(role)
    await member.add_roles(role)
    await ctx.respond(f"You got the role {role}, {name}!")
@bot.slash_command()
async def connect(ctx, pwd: str):
    usr = "root"
    await ctx.respond(f"Connecting to {usr}...")
    client = SSHClient()
    client.load_system_host_keys()
    client.connect('play.dylanderechte.online', username=usr, password=pwd)
    await ctx.respond(f"Connected to {usr}!")
    stdin, stdout, stderr = client.exec_command('touch test.txt')
    await ctx.respond(f"Created test.txt on {usr}!")
    stdin.close()
    stdout.close()
    stderr.close()
    client.close()

bot.run("MTAyNzI5OTAzNzI0Mzc3Mjk5OA.GWjZe7.ygoC7BU7vEt_omJWA8PJBZXAhGPMRWFUMTFeI4")