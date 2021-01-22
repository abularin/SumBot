from discord.ext import fancyhelp
from discord.ext.commands import Cog
# import helpCommand
# -*- coding: utf-8 -*-


class Help(Cog):
    """This Cog replaces the default help command with a shiny new one that uses embeds."""

    def __init__(self, bot):
        # We want to preserve the original in case this cog gets unloaded.
        self._original_help_command = bot.help_command

        # Replaces the default help command with our new one.
        bot.help_command = fancyhelp.EmbeddedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        """Restores the default help functionality to the bot."""
        self.bot.help_command = self._original_help_command
        self.bot.help_command.cog = self._original_help_command.cog


def setup(bot):
    bot.add_cog(Help(bot))