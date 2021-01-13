#########################################################################################
# MIT License                                                                           #
#                                                                                       #
# Copyright (c) 2021 SumBot team                                                        #
#                                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining a copy          #
# of this software and associated documentation files (the "Software"), to deal         #
# in the Software without restriction, including without limitation the rights          #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell             #
# copies of the Software, and to permit persons to whom the Software is                 #
# furnished to do so, subject to the following conditions:                              #
#                                                                                       #
# The above copyright notice and this permission notice shall be included in all        #
# copies or substantial portions of the Software.                                       #
#                                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR            #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,              #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE           #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,         #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE         #
# SOFTWARE.                                                                             #
# © 2021 GitHub, Inc.                                                                   #
#########################################################################################

import discord
from discord.ext import commands
import random
import asyncio


class Giveaway(commands.Cog):
    """
    Giveaway commands
    """
    def __init__(self, client):
        self.client = client

    @commands.command(name='gcreate', help='to made giveaway advanced settings')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def giveaway_create(self, ctx):
        questions = [
            "Which channel should it be hosted in?",
            "What should be the duration of the giveaway? (s|m|h|d|mo)",
            "What is the prize of the giveaway?"]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel 
        for i in questions:
            await ctx.send(i)
            try:
                msg = await self.client.wait_for('message', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)
        try:

            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return
        channel = self.client.get_channel(c_id)

        def convert(timer):

            pos = ["s", "m", "h", "d", "mo"]
            time_dict = {"s": 1, "m": 60, "h": 60*60, "d": 3600*24, "mo": 86400*30}
            unit = timer[-1]
            if unit not in pos:
                return -1
            try:
                val = int(timer[:-1])

            except:
                return -2

            return val * time_dict[unit]

        time = convert(answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d|mo) next time!")
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return            
        prize = answers[2]

        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")

        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description='**prize:** {}\n**Ends At:** {}\n**Host By:** {}'.format(prize, answers[1], ctx.author.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        my_msg = await channel.send('🎉 Giveaway! 🎉', embed=embed)
        await my_msg.add_reaction("🎉")
        await asyncio.sleep(time)
        new_msg = await channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)

        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description="**prize:** {}\n**Host By:** {}\n**winner:** {}".format(
                prize,
                ctx.author.mention,
                winner.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await my_msg.edit(embed=embed)
        await channel.send(f"the winner is {winner.mention} Won in **{prize}**!")

    @commands.has_permissions(administrator=True)
    @giveaway_create.error
    async def giveaway_error(self, ctx, error):    
        print(error)  
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to re-winner in giveaway')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx, channel: discord.TextChannel, message_id: int):
        try:
            new_msg = await channel.fetch_message(message_id)

        except:
            await ctx.send("The id was entered incorrectly.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)
        await channel.send(f"the winner is {winner.mention}.!")

    @commands.has_permissions(administrator=True)
    @reroll.error
    async def roll_winner_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Used: `{}reroll <#channel> id_message`'.format(self.client.command_prefix))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(name='gstart', help='to made giveaway quick')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def giveaway_start(self, ctx, time, *, prize: str):
        await ctx.message.delete()

        def convert(time):
            """
            @type time: object
            """
            pos = ["s", "m", "h", "d", "mo"]
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24, "mo": 86400*30}
            unit = time[-1]
            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2
            return val * time_dict[unit]

        time1 = convert(time)
        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description='**prize:** {}\n**Ends At:** {}\n**Host By:** {}'.format(prize, time, ctx.author.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        my_msg = await ctx.send('🎉 Giveaway! 🎉', embed=embed)
        await my_msg.add_reaction("🎉")

        await asyncio.sleep(time1)

        new_msg = await ctx.channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)
        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description='**prize:** {}\n**Host By:** {}\n**winner:** {}'.format(
                prize,
                ctx.author.mention,
                winner.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await my_msg.edit(embed=embed)
        await ctx.send(f"the winner is {winner.mention} won in **{prize}**!")

    @commands.has_permissions(administrator=True)
    @giveaway_start.error
    async def giveaway_start_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='**Used:** `{}gstart Time prize`\n**Type:** giveaway'.format(self.client.command_prefix),
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_image(url='http://g.recordit.co/ziWu7QMEEU.gif')
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        
               
def setup(client):
    client.add_cog(Giveaway(client))
