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

async def reset(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            await reset(value)
        else:
            dictionary['points'] = 1

async def image_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image = await response.read()
    return image

async def return_rep(id):
    try:
        with open('./user data/reputation.json', 'r') as f:
            reps = json.load(f)
        return dict(reps[str(id)])['reputation']
    except Exception as error:
        if isinstance(error, KeyError):
            with open('./user data/reputation.json', 'r') as f:
                reps = json.load(f)
            reps[str(id)] = {}
            reps[str(id)]['points'] = 1
            reps[str(id)]['reputation'] = 0
            with open('./user data/reputation.json', 'w') as f:
                json.dump(reps, f, indent=4)
            return reps[str(id)]['reputation']

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rep_points_reset.start()

    @tasks.loop(hours=24, reconnect=True)
    async def rep_points_reset(self):
        try:
            with open('./user data/reputation.json', 'r') as f:
                reputation = dict(json.load(f))
            await reset(reputation)
            with open('./user data/reputation.json', 'w') as f:
                json.dump(reputation, f, indent=4)
        except:
            pass

    alias = "Social & Economy"

    @commands.command(aliases=["rep"], help="give a reputation point to someone", usage="reputation @user###24h/user###No")
    @CustomChecks.blacklist_check()
    @CustomChecks.rep_points_check()
    async def reputation(self, ctx, user: discord.User=None):
        if user == ctx.message.author:
            return await ctx.send("you can't rep yourself")
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

    @commands.command(aliases=['pf'], help="see your profile card or someone else's", usage="profile @user`[optional]`###5s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
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
            background = await image_request(background_url)
            status = await image_request(status_url)
            background = io.BytesIO(background)
            background = Image.open(background)
            avatar_buffer = io.BytesIO()
            member_avatar = member.avatar_url_as(format='png', size=256)
            await member_avatar.save(avatar_buffer)
            avatar_buffer.seek(0)
            avatar_image = Image.open(avatar_buffer)
            avatar_image = avatar_image.resize((256, 256))
            background.paste(avatar_image, (2200, 30))
            font = ImageFont.truetype("./fonts/CrimsonRoman.ttf", 45)
            now = datetime.datetime.now()
            reg = f"{member.created_at.__format__('%d %b %Y %H:%M')} ({str(now-member.created_at).split(',', 1)[0]})"
            join = f"{member.joined_at.__format__('%d %b %Y %H:%M')} ({str(now-member.joined_at).split(',', 1)[0]})"
            if member.activity:
                activity = ', '.join(list(map(lambda x: x.name, member.activities)))
            else:
                activity = None
            rep = await return_rep(member.id)
            text_list = [
                str(member), str(member.id), reg, join, member.nick, str(rep), str(member.status).capitalize(), str(activity),
                str(hypesquad), premium, early_supporter, partner, events, staff, bug_hunter, verified_bot_dev, bot, verified_bot
            ]
            text_list2 = [
                "The Watcher info on", "ID:", "Account created:", "Joined server:", "Nickname:", "Reputation points:", "Status:",
                "Activity:", "HypeSquad:", "Discord Nitro:", "Early Supporter:", "Discord Partner:", "HypeSquad Events:",
                "Discord Staff:", "Bug Hunter:", "Verified Bot Dev:", "Bot:", "Verified Bot:"
            ]
            flag_colors = ["#fb68f8", "#fc964b", "#3e84e9", "#ffd56c", "#7289d9", "#fbb848", "#3e70dd", "#7289da", "#7289da"]
            colors = {
                "online": "#44b383", "idle": "#faa61a", "dnd": "#f04747", "offline": "#747f8d", "activity": "#1db954",
                "    Balance": "#45ddc0", "    Bravery": "#9c84ef", "    Brilliance": "#f47b67",
                None: "#747f8d"
            }
            coordinates = [
                (1480, 10), (1165, 100), (1410, 150), (1350, 200), (1300, 250), (1435, 300), (1270, 350), (1260, 400), (1330, 450),
                (1365, 500), (1400, 550), (1400, 600), (1450, 650), (1350, 700), (1325, 750), (1415, 800), (1180, 850), (1335, 900)
            ]
            coordinates2 = [
                (1100, 10), (1100, 100), (1100, 150), (1100, 200), (1100, 250), (1100, 300), (1100, 350), (1100, 400), (1100, 450),
                (1100, 500), (1100, 550), (1100, 600), (1100, 650), (1100, 700), (1100, 750), (1100, 800), (1100, 850), (1100, 900)
            ]
            for x in range(0, len(text_list)):
                draw = ImageDraw.Draw(background)
                draw.text(coordinates2[x], text_list2[x], fill="#ff0000", font=font)
                if x == 6:
                    draw.text(coordinates[x], text_list[x], fill=colors[str(member.status)], font=font)
                elif x == 7:
                    draw.text(coordinates[x], text_list[x], fill=colors["activity"], font=font)
                elif x == 8:
                    draw.text(coordinates[x], text_list[x], fill=colors[hypesquad], font=font)
                elif x > 8:
                    draw.text(coordinates[x], text_list[x], fill=flag_colors[x-9], font=font)
                else:
                    draw.text(coordinates[x], text_list[x], fill="#ff0000", font=font)
            status = io.BytesIO(status)
            status_image = Image.open(status)
            status_image = status_image.resize((40, 40))
            background.paste(status_image, (1223, 349))
            if hypesquad is not None:
                hypesquad_resp = await image_request(hypesquad_url)
                hypesquad_resp = io.BytesIO(hypesquad_resp)
                hypesquad_image = Image.open(hypesquad_resp)
                hypesquad_image = hypesquad_image.resize((40, 40))
                background.paste(hypesquad_image, (1319, 449))
            buffer_output = io.BytesIO()
            background.save(buffer_output, format='PNG')
            buffer_output.seek(0)
            await ctx.send(file=File(buffer_output, 'thewatcherinfo.png'))

def setup(bot):
    bot.add_cog(Social(bot))
