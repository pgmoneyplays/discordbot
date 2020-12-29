import asyncio
import json
import os
import random
import datetime
from discord import Member, guild, Colour
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import re

PREFIX = ("$")
bot = commands.Bot(command_prefix=PREFIX, description='Hi', intents=discord.Intents.all())



async def on_ready(self):
    print(f"Bot is online!")


if __name__ == '__main__':
    for file in os.listdir("cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"{file[:-3]} loaded!")



@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)


@bot.command(name='avatar')
async def avatar(ctx, *, avamember: discord.Member = None):
    userAvatarUrl = ctx.author.avatar_url
    await ctx.send(userAvatarUrl)


@bot.event
async def on_ready():
    activity = discord.Game(name=f"im on {len(bot.guilds)} Server", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")


class BetterUserconverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            user = await commands.UserConverter().convert(ctx, argument)
        except commands.UserNotFound:
            user = None
        if not user and ctx.guild:
            user = ctx.bot.get_member_named(argument)
        if user == None:
            match = re.compile(r'([0-9]{15,21})$').match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
            if match:
                argument = match.group(1)

            # if not match:
            # match2 = re.match(r'<@&([0-9]+)>$',argument)
            # if match2:
            # argument2=match2.group(1)
            # role=ctx.bot.get_role(int(argument2))
            # going to be around when 1.16 comes around lol
            if argument.isdigit():
                user = bot.get_user(int(argument))
                if user == None:
                    try:
                        user = await bot.fetch_user(int(argument))
                    except:
                        user = None
        if user == None:
            tag = re.match(r"#?(\d{4})", argument)
            if tag:
                test = discord.utils.get(bot.users, discriminator=tag.group(1))
                if test:
                    user = test
                if not test:
                    user = ctx.author
        return user


@bot.command(help="a command that gives information on users",
             brief="this can work with mentions, ids, usernames, and even full names.")
async def userinfo(ctx, *, user: BetterUserconverter = None):
    if user is None:
        user = ctx.author

    if user.bot:
        user_type = "Bot"
    if not user.bot:
        user_type = "User"

    if ctx.guild:
        member_version = ctx.guild.get_member(user.id)
        if member_version:
            nickname = str(member_version.nick)
            joined_guild = member_version.joined_at.strftime('%m/%d/%Y %H:%M:%S')
            status = str(member_version.status).upper()
            highest_role = member_version.roles[-1]
        if not member_version:
            nickname = str(member_version)
            joined_guild = "N/A"
            status = "Unknown"
            for guild in bot.guilds:
                member = guild.get_member(user.id)
                if member:
                    status = str(member.status).upper()
                    break
            highest_role = "None Found"
    if not ctx.guild:
        nickname = "None"
        joined_guild = "N/A"
        status = "Unknown"
        for guild in bot.guilds:
            member = guild.get_member(user.id)
            if member:
                status = str(member.status).upper()
                break
        highest_role = "None Found"

    guilds_list = [guild for guild in bot.guilds if guild.get_member(user.id)]
    if not guilds_list:
        guild_list = "None"

    x = 0
    for g in guilds_list:
        if x < 1:
            guild_list = g.name
        if x > 0:
            guild_list = guild_list + f", {g.name}"
        x = x + 1

    embed = discord.Embed(title=f"{user}", description=f"Type: {user_type}", color=random.randint(0, 16777215),
                          timestamp=ctx.message.created_at)
    embed.add_field(name="Username: ", value=user.name)
    embed.add_field(name="Discriminator:", value=user.discriminator)
    embed.add_field(name="Nickname: ", value=nickname)
    embed.add_field(name="Joined Discord: ", value=(user.created_at.strftime('%m/%d/%Y %H:%M:%S')))
    embed.add_field(name="Joined Guild: ", value=joined_guild)
    embed.add_field(name="Part of Guilds:", value=guild_list)
    embed.add_field(name="ID:", value=user.id)
    embed.add_field(name="Status:", value=status)
    embed.add_field(name="Highest Role:", value=highest_role)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)


bot.run('NzkwMDM5MTMzOTg3OTMwMTcz.X96zRw.nOI-yhBhapOu_OnNElFJk_qWSFc')