import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.owner_id = owner_id

    # async def is_owner(self, ctx):
    #     return ctx.author.id == self.client.owner_ids

    @commands.command(hidden=True)
    @commands.is_owner()
    async def osay(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def st(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(
            title="SumBot status",
            description=arg,
            timestamp=ctx.message.created_at
        )
        embed.set_author(name="SumBot status", icon_url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Owner(client))


