import discord
from discord.ext import commands, tasks
from cogs.errors import CustomChecks
import json
import datetime
import random
from PIL import Image, ImageDraw, ImageFont
from discord import File
import io
import aiohttp

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.rep_points_reset.start()

    alias = "Social & Economy"

    @commands.command(aliases=["rep"], help="`command under development`", usage="-###-###No")
    @CustomChecks.blacklist_check()
    @CustomChecks.rep_points_check()
    async def reputation(self, ctx, user: discord.User=None):
        with open('./user data/reputation.json', 'r') as f:
            reputation = json.load(f)
        try:
            author_points = reputation[str(ctx.author.id)]['points']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(ctx.author.id)] = {}
                reputation[str(ctx.author.id)]['points'] = 1
                author_points = reputation[str(ctx.author.id)]['points']
            else:
                raise
        try:
            author_rep = reputation[str(ctx.author.id)]['reputation']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(ctx.author.id)]['reputation'] = 0
                author_rep = reputation[str(ctx.author.id)]['reputation']
            else:
                raise
        try:
            user_points = reputation[str(user.id)]['points']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(user.id)] = {}
                reputation[str(user.id)]['points'] = 1
                user_points = reputation[str(user.id)]['points']
            else:
                raise
        try:
            user_rep = reputation[str(user.id)]['reputation']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(user.id)]['reputation'] = 0
                user_rep = reputation[str(user.id)]['reputation']
            else:
                raise
        if author_points > 0:
            author_points -= 1
            user_rep += 1
            reputation[str(ctx.author.id)]['points'] = author_points
            reputation[str(user.id)]['reputation'] = user_rep
        reputation[str(ctx.author.id)]['reputation'] = author_rep
        reputation[str(user.id)]['points'] = user_points
        with open('./user data/reputation.json', 'w') as f:
            json.dump(reputation, f, indent=4)
        embed = discord.Embed(description=f":military_medal: {ctx.author.mention} **gave** {user.mention} **a reputation point!**", color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pf'])
    async def profile(self, ctx, member: discord.Member=None):
        async with ctx.channel.typing():
            member = member or ctx.message.author
            background_url = 'https://cdn.discordapp.com/attachments/725102631185547427/815870901701967932/profile-background.png'
            status_urls = {
                'online': 'https://cdn.discordapp.com/attachments/725102631185547427/815876526724874240/online.png',
                'offline': 'https://cdn.discordapp.com/attachments/725102631185547427/815876525202604042/offline.png',
                'dnd': 'https://cdn.discordapp.com/attachments/725102631185547427/815876521549758514/dnd.png',
                'idle': 'https://cdn.discordapp.com/attachments/725102631185547427/815876523269554196/idle.png'
            }
            status_url = status_urls[str(member.status)]
            if member.public_flags.hypesquad_balance:
                hypesquad_url = 'https://cdn.discordapp.com/attachments/725102631185547427/769659063759667280/balance.png'
                hypesquad = '    Balance'
            elif member.public_flags.hypesquad_bravery:
                hypesquad_url = 'https://cdn.discordapp.com/attachments/725102631185547427/769659066246365184/bravery.png'
                hypesquad = '    Bravery'
            elif member.public_flags.hypesquad_brilliance:
                hypesquad_url = 'https://cdn.discordapp.com/attachments/725102631185547427/769659069224189962/brilliance.png'
                hypesquad = '    Brilliance'
            else:
                hypesquad = None
            if member.premium_since:
                premium = 'Yes'
            else:
                premium = 'No'
            if member.public_flags.staff:
                staff = 'Yes'
            else:
                staff = 'No'
            if member.public_flags.hypesquad:
                events = 'Yes'
            else:
                events = 'No'
            if member.public_flags.partner:
                partner = 'Yes'
            else:
                partner = 'No'
            if member.public_flags.bug_hunter or member.public_flags.bug_hunter_level_2:
                bug_hunter = 'Yes'
            else:
                bug_hunter = 'No'
            if member.public_flags.early_supporter:
                early_supporter = 'Yes'
            else:
                early_supporter = 'No'
            if member.public_flags.verified_bot_developer:
                verified_bot_dev = 'Yes'
            else:
                verified_bot_dev = 'No'
            if member.bot:
                bot = 'Yes'
            else:
                bot = 'No'
            if member.public_flags.verified_bot:
                verified_bot = 'Yes'
            else:
                verified_bot = 'No'
            async with aiohttp.ClientSession() as session:
                async with session.get(background_url) as response:
                    background = await response.read()
            async with aiohttp.ClientSession() as session:
                async with session.get(status_url) as response:
                    status = await response.read()
            background = io.BytesIO(background)
            background = Image.open(background)
            avatar_buffer = io.BytesIO()
            member_avatar = member.avatar_url_as(format='png', size=256)
            await member_avatar.save(avatar_buffer)
            avatar_buffer.seek(0)
            avatar_image = Image.open(avatar_buffer)
            avatar_image = avatar_image.resize((256, 256))
            background.paste(avatar_image, (2200, 30))
            buffer_output = io.BytesIO()
            background.save(buffer_output, format='PNG')
            font = ImageFont.truetype("./fonts/CrimsonRoman.ttf", 45)
            now = datetime.datetime.now()
            reg = f"{member.created_at.__format__('%d %b %Y %H:%M')} ({str(now-member.created_at).split(',', 1)[0]})"
            join = f"{member.joined_at.__format__('%d %b %Y %H:%M')} ({str(now-member.joined_at).split(',', 1)[0]})"
            if member.activity:
                activity = ', '.join(list(map(lambda x: x.name, member.activities)))
            else:
                activity = None
            text_list = [
                f"The Watcher info on {member}", f"ID: {member.id}", f"Account created: {reg}", f"Joined server: {join}",
                f"Nickname: {member.nick}", f"Status:     {str(member.status).capitalize()}", f"Activity: {activity}", f"HypeSquad: {hypesquad}",
                f"Discord Nitro: {premium}", f"Early Supporter: {early_supporter}", f"Discord Partner: {partner}",
                f"HypeSquad Events: {events}", f"Discord Staff: {staff}", f"Bug Hunter: {bug_hunter}",
                f"Verified Bot Dev: {verified_bot_dev}", f"Bot: {bot}", f"Verified Bot: {verified_bot}"
            ]
            colors = {
                "online": "#44b383", "idle": "#faa61a", "dnd": "#f04747", "offline": "#747f8d", "activity": "#1db954",
                "    Balance": "#45ddc0", "    Bravery": "#9c84ef", "    Brilliance": "#f47b67",
                None: "#747f8d"
            }
            flag_colors = ["#fb68f8", "#fc964b", "#3e84e9", "#ffd56c", "#7289d9", "#fbb848", "#3e70dd", "#7289da", "#7289da"]
            coordinates = [
                (1100, 10), (1100, 100), (1100, 150), (1100, 200), (1100, 250), (1100, 300), (1100, 350), (1100, 400),
                (1100, 450), (1100, 500), (1100, 550), (1100, 600), (1100, 650), (1100, 700), (1100, 750), (1100, 800), (1100, 850)
            ]
            buffer = io.BytesIO()
            for x in range(0, len(text_list)):
                draw = ImageDraw.Draw(background)
                if x == 5:
                    draw.text(coordinates[x], text_list[x], fill=colors[str(member.status)], font=font)
                elif x == 6:
                    draw.text(coordinates[x], text_list[x], fill=colors["activity"], font=font)
                elif x == 7:
                    draw.text(coordinates[x], text_list[x], fill=colors[hypesquad], font=font)
                elif x > 7:
                    draw.text(coordinates[x], text_list[x], fill=flag_colors[x-8], font=font)
                else:
                    draw.text(coordinates[x], text_list[x], fill="#ff0000", font=font)
                background.save(buffer, format='PNG')
                buffer.seek(0)
            status = io.BytesIO(status)
            status_image = Image.open(status)
            status_image = status_image.resize((40, 40))
            background.paste(status_image, (1223, 299))
            if hypesquad is not None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(hypesquad_url) as response:
                        hypesquad_resp = await response.read()
                hypesquad_resp = io.BytesIO(hypesquad_resp)
                hypesquad_image = Image.open(hypesquad_resp)
                hypesquad_image = hypesquad_image.resize((40, 40))
                background.paste(hypesquad_image, (1319, 399))
            buffer_output = io.BytesIO()
            background.save(buffer_output, format='PNG')
            buffer_output.seek(0)
            await ctx.send(file=File(buffer_output, 'thewatcherinfo.png'))

    """@tasks.loop(seconds=10, reconnect=True)
    async def rep_points_reset(self):
        with open('./user data/reputation.json', 'r') as f:
            reputation = json.load(f)
        for user in reputation:
            user['points'] = 1"""

def setup(bot):
    bot.add_cog(Social(bot))
