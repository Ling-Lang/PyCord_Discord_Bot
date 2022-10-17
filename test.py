import discord

bot = discord.Bot()
b_name = "@testing_bot"
@bot.slash_command()
async def hi(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")

@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{b_name} says hello to {ctx.author.mention}!")

bot.run("MTAyNzI5OTAzNzI0Mzc3Mjk5OA.GWjZe7.ygoC7BU7vEt_omJWA8PJBZXAhGPMRWFUMTFeI4")