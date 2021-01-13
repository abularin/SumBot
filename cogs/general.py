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
import time
import arabic_reshaper
from PIL import Image
from io import BytesIO
from PIL import ImageFont, ImageDraw
import arabic_reshaper
import asyncio
from discord_webhook import DiscordWebhook, DiscordEmbed


class General(commands.Cog):
    """
    General commands
    """
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['inv'], help='invite bot', description='To invite the bot in your server')
    @commands.guild_only()
    async def invite(self, ctx):
        """
        To invite the bot in your server
        """
        embed = discord.Embed(
            description='''
**Invite bot => [Click here](https://discord.com/oauth2/authorize?client_id={}&scope=bot&permissions=8)**
**Support bot => [Click here]({})**'''.format(self.client.user.id, 'https://discord.gg/MJmzZ62qv2'),
            color=ctx.author.color,
            timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @invite.error
    async def inv_error(self, ctx, error):       
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions `embed_links`")

    @commands.command(invoke_without_command=True, help='To know the connection speed of the bot on the server')
    @commands.guild_only()
    async def ping(self, ctx):

        before = time.monotonic()

        embed = discord.Embed(
            description='!pong',
            timestamp=ctx.message.created_at,
            color=ctx.author.color)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        msg = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(
            description='''Time taken: `{} ms`
Discord API: `{} ms`
            '''.format(int(ping), round(self.client.latency * 1000)),
            timestamp=ctx.message.created_at,
            color=ctx.author.color)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await msg.edit(content="pong!", embed=embed)

    @ping.error
    async def ping_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.group(invoke_without_command=True, help='To know the personal avatar')
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member if member else ctx.author
        embed = discord.Embed(
            title='avatar',
            description='**[png]({}) | [jpg]({}) | [jpeg]({}) **'.format(
                member.avatar_url_as(format="png"),
                member.avatar_url_as(format="jpg"),
                member.avatar_url_as(format="jpeg")), timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar_url_as(size=1024))
        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('🙄 I could not find this member')        
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions `embed_links`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        if isinstance(ctx.channel, commands.errors.CommandOnCooldown):
            await ctx.send(error)
    
    @avatar.command()
    @commands.guild_only()
    async def server(self, ctx):
        """Shows the server icon."""
        embed = discord.Embed(
            title="Server icon",
            description="[Server Icon]({}).".format(ctx.guild.icon_url),
            colour=0X008CFF)
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @server.error
    async def icon_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @avatar.command()
    @commands.guild_only()
    async def bot(self, ctx):
        """Shows the avatar bot."""
        embed = discord.Embed(
            title="Bot avatar",
            description="[Bot avatar]({}).".format(self.client.user.avatar_url),
            colour=0X008CFF)
        embed.set_image(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @bot.error
    async def bot_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(name='len', help='length your arg')
    async def length(self, ctx, *, arg):
        await ctx.send('Your message is `{}` characters long.'.format(str(len(arg))))

    @length.error
    async def length_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("error")
    
    @commands.command(name='bag')
    async def report(self, ctx):
        # channel = self.client.get_channel(797576932249960498)
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/797588095780257802/l7rC9owUuIGQU2t-cJk5hxw-tj6aE3jc_aAcsVkrwBLFHzJT-v3K2pYg290NObwz9ARF',
            username="bag")
        questions = [
            "Entr your name?",
            "What is the problem that you suffer from?",
            "When the problem occurred?"]
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
        embed = DiscordEmbed(
            title='Bug',
            description="`Description bug`: \n {}.\nTime bag:\n{}".format(answers[1], answers[2]),
            url=f"https://discord.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=8",
            # timestamp=ctx.message.created_at
        )
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        webhook.add_embed(embed)
        response = webhook.execute()
        # await channel.send(embed=embed)

    @commands.command(aliases=['bot'], help='show bot info')
    @commands.guild_only()
    async def botinfo(self, ctx):
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            color=ctx.author.color,
            description=f"""
**[invite](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=8) | [Vote](https://top.gg/bot/738120633430573176) | [github](https://github.com/SumBot/SumBot) | [website](http://sumbot.tk/) | [support](https://discord.com/invite/BZKJfqZ)**
""")
        img = Image.open("./img/info_bot.jpg")  # import img
        draw = ImageDraw.Draw(img)  # draw img
        font = ImageFont.truetype("./fonts/Nawar_Font.otf", size=60)  # font all text

        draw.text(
            [300, 140],
            F"{len(self.client.guilds)}",
            font=font,
            fill="#d9d9d9")

        draw.text(
            [380, 225],
            "Python",
            font=font,
            fill="#d9d9d9")

        draw.text(
            [290, 320],
            "discord.py",
            font=font,
            fill="#d9d9d9")

        img.save(f'./img/bot.png')  # save img
        file = discord.File(f"./img/bot.png", filename="botinfo.png")
        embed.set_image(url="attachment://botinfo.png")
        # embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(file=file, embed=embed)

    @botinfo.error
    async def botinfo_error(self, ctx, error):
        await ctx.send(error)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(aliases=['s'], pass_context=True, help='show server info')
    @commands.guild_only()
    async def server(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title='server info',
            timestamp=ctx.message.created_at)
        embed.add_field(name='📛 | Name', value=guild.name)
        embed.add_field(name='🆔 | guild id', value=guild.id)
        embed.add_field(name='👑 | Owner', value='<@' + str(guild.owner_id) + ">")
        embed.add_field(name='👥 | Members', value=guild.member_count)
        embed.add_field(
            name=f'channels({len(guild.channels)})',
            value=f'''
📣 Categories: {len(guild.categories)}
💬 text: {len(ctx.guild.text_channels)} 
🔊 voice: {len(ctx.guild.voice_channels)}''')
        embed.add_field(name='🕍 | created at', value=guild.created_at.strftime("%m/%d/%Y, %H:%M:%S %p"))
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text='Requested by {}'.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(aliases=["id", "userinfo"], help='show user info')
    async def user(self, ctx, member: discord.Member = None):

        member = ctx.author if not member else member

        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            color=ctx.author.color
        )

        embed.set_author(
            name=self.client.user,
            url="https://discord.com/oauth2/authorize?client_id=738120633430573176&permissions=8&scope=bot",
            icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.avatar_url)
        embed.add_field(name="{} ╎ Member:".format(self.client.get_emoji(795052145635622942)), value=member.mention)
        embed.add_field(name="🆔 ╎ ID:", value=member.id)
        embed.add_field(name="{} ╎ Join At:".format(self.client.get_emoji(795053266111168562)), value=member.created_at.strftime("%Y/%m/%d"))
        embed.add_field(name="{} ╎ Join Server At:".format(self.client.get_emoji(795053825395654666)), value=member.joined_at.strftime("%Y/%m/%d"))
        badges = ""
        for i in list(iter(member.public_flags)):
            if i[1] and i[0] == "staff":
                badges += (str(self.client.get_emoji(795021566375231508)))
            if i[1] and i[0] == "partner":
                badges += (str(self.client.get_emoji(795021566668701706)))
            if i[1] and i[0] == "early_supporter":
                badges += (str(self.client.get_emoji(795021566387814420)))
            if i[1] and i[0] == "bug_hunter":
                badges += (str(self.client.get_emoji(762364793361006603)))
            if i[1] and i[0] == "bug_hunter_level_2":
                badges += (str(self.client.get_emoji(795021566253596702)))
            if i[1] and i[0] == "early_verified_bot_developer":
                badges += (str(self.client.get_emoji(795021566177968148)))
            if i[1] and i[0] == "verified_bot":
                badges += (str(self.client.get_emoji(795021566072717332)))
            if i[1] and i[0] == "hypesquad":
                badges += (str(self.client.get_emoji(795021566076780564)))
            if i[1] and i[0] == "hypesquad_bravery":
                badges += (str(self.client.get_emoji(795021565975986181)))
            if i[1] and i[0] == "hypesquad_brilliance":
                badges += (str(self.client.get_emoji(795021565800480789)))
            if i[1] and i[0] == "hypesquad_balance":
                badges += (str(self.client.get_emoji(795021565901144084)))
            if i[1] and i[0] == "nitro":
                badges += (str(self.client.get_emoji(795021565901144084)))
            if i[1] and i[0] == "bot":
                badges += (str(self.client.get_emoji(795047209111388190)))
            else:
                badges += ""
        if badges == "":
            badges = "None"
        embed.add_field(name="{} ╎ Badges:".format(self.client.get_emoji(795054399944130620)), value=badges)
        status = ""
        if member.status == discord.Status.online:
            status += str(self.client.get_emoji(795225784637587488))
        elif member.status == discord.Status.offline:
            status += str(self.client.get_emoji(795225784850579456))
        elif member.status == discord.Status.idle:
            status += str(self.client.get_emoji(795225784649383947))
        elif member.status == discord.Status.dnd:
            status += str(self.client.get_emoji(795225784758697985))
        else:
            status += str(self.client.get_emoji(795225784947048478))

        embed.add_field(name="⁉ ╎ Status:", value=status)
        roles = " ".join([role.mention for role in member.roles if role != ctx.guild.default_role])
        roles = "Nothing" if not roles else roles
        embed.add_field(name="{} ╎ Roles ({}):".format(self.client.get_emoji(795054968700403712), len(member.roles) - 1), value=roles, inline=False)

        await ctx.send(embed=embed)

    @commands.command(help='show the profile')
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):

        if user == None:
            user = ctx.author
        img = Image.open("./img/profile_sorce.png")  # import img

        ava = user.avatar_url_as(size=128)  # save avatar user
        data = BytesIO(await ava.read())  # None

        pfp = Image.open(data)  # open img

        pfp = pfp.resize((345, 352))  # resize avatar url
        img.paste(pfp, (905, 30))  # None

        draw = ImageDraw.Draw(img)  # draw img
        font = ImageFont.truetype("./fonts/Sukar_Black.ttf", size=60)  # font all text
        shadow_color = "yellow"  # shadow color all text
        stroke_width = 2  # stroke width
        color_stroke = "black"  # color stroke

        username = user.name  # get user name
        user_tag = "#" + user.discriminator  # get user tag
        join_at = user.created_at.strftime("%Y/%m/%d")  # get join at
        user_id = user.id  # get user id

        # fonts and size name
        draw.text(
            [270, 100],
            arabic_reshaper.reshape(username),  # add arabic
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # fonts and size tag
        draw.text(
            [190, 260],
            user_tag,
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # fonts and size join at
        draw.text(
            [278, 405],
            join_at,
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # fonts and size user id
        draw.text(
            [190, 572],
            str(user_id),
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # # copy rights SumBot
        # draw.text(
        #     [580, 375],
        #     "© SumBot",
        #     font=font,
        #     fill="black",
        #     stroke_width=2,
        #     stroke_fill="white")

        img.save(f'./img/profile.png')  # save img

        await ctx.send(file=discord.File(f"./img/profile.png"))  # send profile img

    @profile.error
    async def profile_error(self, ctx, error):

        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('🙄 I could not find this member')

        elif isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(General(client))
