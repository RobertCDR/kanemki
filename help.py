import discord
import datetime
import random
from discord.ext import commands
from cogs.errors import CustomChecks

class Help(commands.HelpCommand):

    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Totally not a Rickroll",
            url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            description=f"Use `{self.clean_prefix}help [command]` for details",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        emotes = [":sparkles: ", ":smile: ", ":video_game: ", ":camera: ", ":performing_arts: ", ":rosette: ", ":cop: ", ":mobile_phone: ", ":bulb: "]
        categories = [f"`{self.clean_prefix}help actions`", f"`{self.clean_prefix}help fun`", f"`{self.clean_prefix}help games`",
            f"`{self.clean_prefix}help images`", f"`{self.clean_prefix}help memes`", f"`{self.clean_prefix}help misc`",
            f"`{self.clean_prefix}help mod`", f"`{self.clean_prefix}help social`", f"`{self.clean_prefix}help utils`"
        ]
        k = 0
        embed.set_author(name='Kanemki Command List', icon_url='https://cdn.discordapp.com/avatars/723864146965168168/38c2c8f8d4d7f0b0b279a140686d8bd0.webp?size=1024')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/726569752906170408/kanemki.png')
        embed.set_footer(icon_url='https://cdn.discordapp.com/avatars/465138950223167499/737c78651dbf2205aedc5ea3097ad4d5.webp?size=1024', text='Developed by RobertCDR#2573')
        for cog, cmds in mapping.items():
            command_signatures = [self.get_command_signature(c) for c in cmds]
            if command_signatures:
                cog_name = getattr(cog, "alias", "No Category")
                if str(cog_name) != 'No Category':
                    embed.add_field(name=f"{emotes[k] + cog_name}", value=categories[k], inline=True)
                    k += 1
                else:
                    pass
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(color=random.randint(0, 0xffffff),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=str(self.get_command_signature(command).split(" ", 1)[0].replace(self.clean_prefix, "")),
            icon_url='https://cdn.discordapp.com/avatars/723864146965168168/38c2c8f8d4d7f0b0b279a140686d8bd0.webp?size=1024'
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/740546485560803450/question.png')
        embed.add_field(name="Description", value=command.help)
        values = str(command.usage).split("###", 2)
        embed.add_field(name="Usage", value=f"{self.clean_prefix}{values[0]}", inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        else:
            embed.add_field(name="Aliases", value="`None`", inline=False)
        embed.add_field(name="Cooldown", value=values[1])
        embed.add_field(name="NSFW", value=values[2])
        embed.set_footer(icon_url=self.context.author.avatar_url, text=f"Requested by {self.context.author}")
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        commands = cog.get_commands()
        filtered = await self.filter_commands(commands, sort=True)
        channel = self.get_destination()
        emotes = {
            "Actions": ":sparkles: ", "Fun": ":smile: ", "Games": "video_game: ", "Images": ":camera: ", "Memes": ":performing_arts: ",
            "Misc": ":rosette: ", "Mod": ":cop: ", "Social": ":mobile_phone: ", "Utils": ":bulb: "
        }
        embed = discord.Embed(title=f"{emotes[cog.qualified_name]}{cog.qualified_name}", color=random.randint(0, 0xffffff))
        embed.set_footer(icon_url=self.context.author.avatar_url, text=f"Requested by {self.context.author}")
        embed.description = f"{', '.join(list(map(lambda x: f'`{x.qualified_name}`', filtered)))}"
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(color=0xbf1932, description=':exclamation: Command not found')
        channel = self.get_destination()
        await channel.send(embed=embed)

attributes = {
    "cooldown": commands.Cooldown(1, 1, commands.BucketType.user),
    "check": CustomChecks.blacklist_check(),
}

help_object = Help(command_attrs=attributes)
