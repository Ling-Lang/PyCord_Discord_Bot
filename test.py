from dis import disco
from multiprocessing import AuthenticationError
import this
import discord

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
async def getrole(ctx, name: str = None):
    member = ctx.author
    name = name or ctx.author.name
    role =discord.guild.get_role(1031829317530955857)
    member.add_roles(role)

bot.run("MTAyNzI5OTAzNzI0Mzc3Mjk5OA.GWjZe7.ygoC7BU7vEt_omJWA8PJBZXAhGPMRWFUMTFeI4")