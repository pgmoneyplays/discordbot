from discord.ext import commands
import asyncio
import discord


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_guild_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)
        await ctx.channel.send(f"**{member} has been kicked from this server by {ctx.author}**")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} you don´t have the Permissions")



    @commands.command()
    @commands.bot_has_guild_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def clear(self, ctx, amount=1000):
        amount = amount if not amount else amount
        deleted = await ctx.channel.purge(limit=amount + 1)
        mes = await ctx.send(f"Purged **{len(deleted) - 1}** messages.")
        await asyncio.sleep(2)
        await mes.delete()

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} you don´t have the Permissions")

    @commands.bot_has_guild_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def ban(ctx, member: discord.Member):

            if member == None:
                await ctx.send("Spieler nicht angegeben")
            else:
                await member.ban()
                await ctx.sen(f"{member} has been banned from this server by {ctx.author}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} you don´t have the Permissions")


def setup(bot):
    bot.add_cog(Moderation(bot))
