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
import asyncio
from discord.ext import commands
import sqlite3
from typing import Optional


class Mod(commands.Cog):
    """
    Moderator commands
    """
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("./app.db")
        self.cr = self.db.cursor()
        self.warn_count = {}

    @commands.command(name='setprefix', aliases=['set_prefix', "set-prefix", "prefix"])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str = ""):
        try:
            if len(prefix) > 5:
                await ctx.send(embed=discord.Embed(
                    description='The prefix cannot be more than 5 characters long.',
                    color=discord.Colour.red()
            ))
            elif prefix == "":
                self.cr.execute("UPDATE guilds SET prefix = '@' WHERE guild_id = ?", (ctx.guild.id,))
                self.db.commit()
                await ctx.send(embed=discord.Embed(
                    description=f"the prefix has been reset to `@`",
                    color=discord.Colour.green()))
            else:
                self.cr.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id))
                self.db.commit()
                prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                await ctx.send(embed=discord.Embed(
                    description=f"the prefix now is `{prefix.fetchone()[0]}`",
                    color=discord.Colour.green()))
        except Exception as e:
            print(e)
            # self.cr.execute(
            #     "INSERT OR IGNORE INTO guilds(guild_id, prefix) VALUES(?, ?)", (ctx.guild.id, "-"))
            # self.db.commit()

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass

    @commands.command(help='to re-send the your message')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.has_permissions(manage_messages=True)
    @say.error
    async def say_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{}say <messgae>`\n**Type:** Mod'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to re-send the your message in embed')
    @commands.guild_only()
    @commands.has_permissions(embed_links=True)
    async def embed(self, ctx, *, arg):
        embed = discord.Embed(
            description=arg,
            color=ctx.author.color,
            timestamp=ctx.message.created_at)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.has_permissions(embed_links=True)
    @embed.error
    async def embed_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{}embed <messgae>`\n**Type:** Mod'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='I do not have permissions `embed_links`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="You don't have permissions `embed_links`",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help="to remove the namber message")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        if amount > 200:
            await ctx.send(embed=discord.Embed(
                description='You cannot delete more than 200 messages.',
                color=discord.Colour.red()
            ))
        elif amount <= 0:
            await ctx.send(embed=discord.Embed(
                description='You cannot delete less than one message.',
                color=discord.Colour.red()
            ))
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
            await ctx.send(embed=discord.Embed(
                description="✅ Done",
                color=discord.Colour.green()
            ))
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)

    @commands.has_permissions(manage_messages=True)
    @clear.error
    async def clear_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{}clear <namber>`\n**Type:** Mod'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='🙄 I do not have permissions `manage messages`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions `manage messages`",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to hide the channel in everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.read_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(
                description='👤 | channel has been Hide {}'.format(channel.mention),
                color=discord.Colour.green()
            ))

    @commands.has_permissions(manage_channels=True)
    @hide.error
    async def hide_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='🙄 I do not have permissions `manage channels`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions `manage channels`",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help="to unhide the channel in everyone")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.read_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(
                description='👥 | channel has been unHide {}'.format(channel.mention),
                color=discord.Colour.green()
            ))

    @commands.has_permissions(manage_channels=True)
    @unhide.error
    async def unhide_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='🙄 I do not have permissions `manage channels`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions `manage channels`",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to lock the channel in everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(
                description='🔒 | channel locked {}'.format(channel.mention),
                color=discord.Colour.green()
            ))

    @commands.has_permissions(manage_messages=True)
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='🙄 I do not have permissions `manage messages`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions `manage messages`",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to unlock the channel in everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(
                description='🔓 | channel unlock {}'.format(channel.mention),
                color=discord.Colour.green()
            ))

    @commands.has_permissions(manage_messages=True)
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='🙄 I do not have permissions `manage messages`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions `manage messages`",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(invoke_without_command=True, help='to send the message in channel')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, channel: discord.TextChannel, *, arg):
        await channel.send(arg)
        await ctx.send(embed=discord.Embed(
                description='Message was sent in {}'.format(channel.mention),
                color=discord.Colour.green()
            ))

    @commands.has_permissions(manage_messages=True)
    @echo.error
    async def echo_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{0}echo(channel, message)`\n**Type:** Mod\n**description:** To add the bot to your server'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description='🙄 I could not find this channel',
                color=discord.Colour.red()
            ))
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description='🙄 You don\'t have permissions `manage messages`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 I don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to make the poll')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            description=arg,
            color=ctx.author.color)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        msg = await ctx.send("📢 poll 📢", embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.has_permissions(manage_messages=True)
    @poll.error
    async def poll_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{}poll <messgae>`\n**Type:** Mod'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description='🙄 You don\'t have permissions `manage messages`',
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(aliases=['nick', "rename"], help='add and remove nickname')
    @commands.has_guild_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, new: str = None):

        if new == None:
            await member.edit(nick="")
            await ctx.send(embed=discord.Embed(
                description=f'{member.name} has been reset nickname',
                color=discord.Colour.green()
            ))
        else:
            await member.edit(nick=f'{new}')
            await ctx.send(embed=discord.Embed(
                description=f'{member.name} has been changed to {new}',
                color=discord.Colour.green()
            ))

    @nickname.error
    async def nickname_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{}nick <member> <name>`\n**Type:** Mod'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description='🙄 You don\'t have permissions `manage nicknames`',
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=discord.Embed(
                description='🙄 I don\'t have permissions `manage nicknames`',
                color=discord.Colour.red()
            ))

    # @commands.command(name="warn")
    # @commands.has_guild_permissions(administrator=True)
    # async def warn(self, ctx, user: discord.User = None, *, reason=None):
    #
    #
    # @commands.command(name="clearwarn")
    # @commands.has_guild_permissions(administrator=True)
    # async def clearwarn(self, ctx, user: discord.User = None):
    #     """Clear warnings of every user, or just the set user"""
    #     if user is None:
    #         self.warn_count = {}
    #         await ctx.send("Clearing all warns.")
    #     else:
    #         self.warn_count[str(user)] = 0
    #         await ctx.send(f"Clearing warns for {user}.")
    #
    # @commands.command(name="warncount")
    # async def warncount(self, ctx, user: discord.User):
    #     """Get the amount of warnings that a user has"""
    #     if str(user) not in self.warn_count:
    #         self.warn_count[str(user)] = 0
    #
    #     count = self.warn_count[str(user)]
    #     await ctx.send(f"{user} has been warned {count} time(s)")


def setup(client):
    client.add_cog(Mod(client))
