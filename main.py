from operator import inv
from turtle import title
from unicodedata import name
import discord
import DiscordUtils
import aiosqlite
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tracker = DiscordUtils.InviteTracker(bot)

@bot.event
async def on_ready():
    global invDB
    invDB = await aiosqlite.connect("invites.db")
    await invDB.execute("CREATE TABLE IF NOT EXISTS invites (member_id ,regular, left, bonus, PRIMARY KEY(member_id))")
    print(f"{bot.user} is online!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Latency: `{round(bot.latency * 1000)}`ms")

@bot.event
async def on_member_join(member):
    inviter = await tracker.fetch_inviter(member)
    await invDB.execute(f"INSERT INTO invites VALUES ({inviter.id}, 1, 0, 0) ON CONFLICT(member_id) DO UPDATE SET regular = regular + 1 WHERE member_id = {inviter.id}")
    await invDB.commit()
    print(inviter)

@bot.command()
async def credits(ctx):
    embed = discord.Embed(
        title="PGamerX Development",
        url="https://development.pgamerx.com/",
        colour=discord.Color.red())

    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/690557545965813770/a_fc0875596ba95c84f0b8356570fc7472.gif?size=1024")
    embed.add_field(name="Founder", value="PGamerX#2809", inline=True)
    embed.add_field(name="Bot Developer", value="Developer X#0001", inline=True)
    embed.add_field(name="Coding Language", value="Python", inline=True)
    embed.add_field(name="Coding Library", value="Discord.py", inline=True)
    embed.add_field(name="Who we are?", value="We are an organization that creates **free** custom **Discord Bots for everyone**, we aim to create **thousands of discord bots** for everyone. Everyone deserves to get a custom discord bot to enable them to do whatever they want in their **Discord Server**.\n\nGet a **free custom** Discord bot **for your server** Today!\n\nHead over to <https://development.pgamerx.com> for more information!\n\nWe are also **committed** to **Open Source <3**, All the **bots** developed will be Open Sourced, and their **source code **shall be available on our Github.\n\n❣️ PGamerX Development Team", inline=False)
    embed.set_footer(text="This watermark is not removable!")

    await ctx.send(embed=embed)

@bot.command()
async def invites(ctx, member:discord.Member=None):
    if member is None:
        async with invDB.execute(f"SELECT regular, left, bonus FROM invites WHERE member_id = {member.id}") as cursor:
            data = await cursor.fetchone()
            if data is None:
                embed = discord.Embed(title=f"**{member}**", description=f"You currently have **0** invites. (**0** regular, **0** left, **0** bonus)", color=discord.Color.random())
                await ctx.send(embed=embed)    
            else:
                regular = data[0]
                left = data[1]
                bonus = data[2]
                total = regular + bonus - left
                print(regular, left, bonus, total)
                embed = discord.Embed(title=f"**{member}**", description=f"You currently have **{total}** invites. (**{regular}** regular, **{left}** left, **{bonus}** bonus)", color=discord.Color.random())
                embed.set_footer("Bot Developer: Developer X#0001 by PGamerX Development")
                await ctx.send(embed=embed)

    if member is not None:
        async with invDB.execute(f"SELECT regular, left, bonus FROM invites WHERE member_id = {member.id}") as cursor:
            data = await cursor.fetchone()
            if data is None:
                embed = discord.Embed(title=f"**{member}**", description=f"{member} currently have **0** invites. (**0** regular, **0** left, **0** bonus)", color=discord.Color.random())
                await ctx.send(embed=embed)    
            else:
                regular = data[0]
                left = data[1]
                bonus = data[2]
                total = regular + bonus - left
                print(regular, left, bonus, total)
                embed = discord.Embed(title=f"**{member}**", description=f"{member} currently have **{total}** invites. (**{regular}** regular, **{left}** left, **{bonus}** bonus)", color=discord.Color.random())
                embed.set_footer("Bot Developer: Developer X#0001 by PGamerX Development")
                await ctx.send(embed=embed)

bot.run("OTM3NDAwMDMyMTQ2MTI4OTI2.YfbLzw.wpu4ysWyOwoRWMHqzUYw3mikhE0")