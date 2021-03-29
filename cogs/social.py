import discord
from discord.ext import commands, tasks
from cogs.errors import CustomChecks
import datetime
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
from discord import File
import io
import aiohttp
import asyncio
from config import user_collection
from pymongo.errors import DuplicateKeyError

async def image_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image = await response.read()
    return image

async def return_social(_id):
    social = []
    try:
        result = user_collection.find_one({"_id": _id})
        social.append(result["reputation"])
    except Exception as error:
        if isinstance(error, KeyError):
            social.append(0)
        elif isinstance(error, TypeError):
            social.append(0)
        else:
            raise error
    try:
        result = user_collection.find_one({"_id": _id})
        social.append(result["about"])
    except Exception as error:
        if isinstance(error, KeyError):
            social.append("-")
        elif isinstance(error, TypeError):
            social.append("-")
        else:
            raise error
    try:
        result = user_collection.find_one({"_id": _id})
        social.append(result["marriedwith"])
    except Exception as error:
        if isinstance(error, KeyError):
            social.append("-")
        elif isinstance(error, TypeError):
            social.append("-")
        else:
            raise error
    return social

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rep_points_reset.start()

    @tasks.loop(hours=24, reconnect=True)
    async def rep_points_reset(self):
        user_collection.update_many({}, {"$set": {"rep_points": +1}})

    alias = "Social & Economy"

    @commands.command(aliases=["rep"], help="give a reputation point to someone", usage="reputation @user###24h/user###No")
    @CustomChecks.blacklist_check()
    @CustomChecks.rep_points_check()
    async def reputation(self, ctx, user: discord.User=None):
        if user == ctx.message.author:
            return await ctx.send("you can't rep yourself")
        elif user is None:
            return await ctx.send("you need to mention someone to rep")
        try:
            points_to_give = user_collection.find_one({"_id": ctx.author.id})
            points_to_give = points_to_give["rep_points"]
        except Exception as error:
            if isinstance(error, KeyError):
                user_collection.find_one_and_update({"_id": ctx.author.id}, {"$inc": {"rep_points": +1}})
            else:
                raise error
        try:
            user_collection.insert_one({"_id": user.id,"reputation": 1, "rep_points":1})
        except Exception as error:
            if isinstance(error, DuplicateKeyError):
                user_collection.update_one({"_id": user.id}, {"$inc": {"reputation": +1}})
        user_collection.update_one({"_id": ctx.author.id}, {"$inc": {"rep_points": -1}})
        embed = discord.Embed(description=f":military_medal: {ctx.author.mention} **gave** {user.mention} **a reputation point!**", color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(aliases=["setdescription", "setdescr"], help="set a description to display on your profile (limit: 200 characters)", usage="setabout <description>###5s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setabout(self, ctx, *, description: str=None):
        if description is None:
            return await ctx.send("you can set nothing as a description only literally")
        elif len(description) > 200:
            return await ctx.send("description too long")
        user_collection.update_one({"_id": ctx.author.id}, {"$set": {"about": description}})
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: Successfully set profile description')
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pf'], help="see your profile card or someone else's", usage="profile @user`[optional]`###5s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member=None):
        async with ctx.channel.typing():
            member = member or ctx.message.author
            background_url = 'https://cdn.discordapp.com/attachments/725102631185547427/818107019659575316/profile-asset.png'
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
            background.paste(avatar_image, (1000, 10))
            font = ImageFont.truetype("./fonts/CrimsonRoman.ttf", 45)
            now = datetime.datetime.now()
            reg = f"{member.created_at.__format__('%d %b %Y %H:%M')} ({str(now-member.created_at).split(',', 1)[0]})"
            join = f"{member.joined_at.__format__('%d %b %Y %H:%M')} ({str(now-member.joined_at).split(',', 1)[0]})"
            try:
                if member.activity:
                    activity = ', '.join(list(map(lambda x: x.name, member.activities)))
                else:
                    activity = None
            except TypeError:
                activity = None
            if member.nick:
                nick = member.nick
            else:
                nick = "-"
            rep = await return_social(member.id)
            about = textwrap.wrap(rep[1], width=30)
            about = '\n'.join(about)
            if rep[2] == "-":
                married = "-"
            else:
                married = str(await self.bot.fetch_user(rep[2]))
            text_list = [
                str(member), str(member.id), reg, join, nick, str(rep[0]), married, str(member.status).capitalize(), str(hypesquad),
                premium, early_supporter, partner, events, staff, bug_hunter, verified_bot_dev, bot, verified_bot, str(activity), about
            ]
            text_list2 = [
                "The Watcher info on", "ID:", "Account created:", "Joined server:", "Nickname:", "Reputation points:", "Married with:", "Status:",
                "HypeSquad:", "Discord Nitro:", "Early Supporter:", "Discord Partner:", "HypeSquad Events:",
                "Discord Staff:", "Bug Hunter:", "Verified Bot Dev:", "Bot:", "Verified Bot:", "Activity:", "About:"
            ]
            flag_colors = ["#fb68f8", "#fc964b", "#3e84e9", "#ffd56c", "#7289d9", "#fbb848", "#3e70dd", "#7289da", "#7289da"]
            colors = {
                "online": "#44b383", "idle": "#faa61a", "dnd": "#f04747", "offline": "#747f8d", "activity": "#1db954",
                "    Balance": "#45ddc0", "    Bravery": "#9c84ef", "    Brilliance": "#f47b67", "married": "#f88b86",
                None: "#747f8d"
            }
            coordinates = [
                (410, 10), (95, 100), (340, 150), (280, 200), (230, 250), (365, 300), (290, 350), (200, 400), (260, 450), (295, 500), (330, 550),
                (330, 600), (380, 650), (280, 700), (255, 750), (345, 800), (110, 850), (265, 900), (190, 950), (900, 350)
            ]
            coordinates2 = [
                (30, 10), (30, 100), (30, 150), (30, 200), (30, 250), (30, 300), (30, 350), (30, 400), (30, 450), (30, 500), (30, 550),
                (30, 600), (30, 650), (30, 700), (30, 750), (30, 800), (30, 850), (30, 900), (30, 950), (1064, 300)
            ]
            for x in range(0, len(text_list)):
                draw = ImageDraw.Draw(background)
                draw.text(coordinates2[x], text_list2[x], fill="#ff0000", font=font)
                if x == 6:
                    draw.text(coordinates[x], text_list[x], fill=colors["married"], font=font)
                elif x == 7:
                    draw.text(coordinates[x], text_list[x], fill=colors[str(member.status)], font=font)
                elif x == 18:
                    draw.text(coordinates[x], text_list[x], fill=colors["activity"], font=font)
                elif x == 8:
                    draw.text(coordinates[x], text_list[x], fill=colors[hypesquad], font=font)
                elif x >= 9 and x <= 17:
                    draw.text(coordinates[x], text_list[x], fill=flag_colors[x-9], font=font)
                else:
                    draw.text(coordinates[x], text_list[x], fill="#ffffff", font=font)
            status = io.BytesIO(status)
            status_image = Image.open(status)
            status_image = status_image.resize((40, 40))
            background.paste(status_image, (153, 399))
            if hypesquad is not None:
                hypesquad_resp = await image_request(hypesquad_url)
                hypesquad_resp = io.BytesIO(hypesquad_resp)
                hypesquad_image = Image.open(hypesquad_resp)
                hypesquad_image = hypesquad_image.resize((40, 40))
                background.paste(hypesquad_image, (249, 449))
            buffer_output = io.BytesIO()
            background.save(buffer_output, format='PNG')
            buffer_output.seek(0)
            await ctx.send(file=File(buffer_output, 'thewatcherinfo.png'))

    @commands.command(aliases=["propose"], help="ask someone to marry you (be romantic)\n(currently the ring is on the house)", usage="marry @user###10s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def marry(self, ctx, member: discord.Member=None):
        if member is None:
            return await ctx.send("404 pair not found. Who are you proposing to?")
        elif member is ctx.author:
            return await ctx.send("You should love yourself but... I mean... uh... not to this point tho...")
        try:
            already_married = user_collection.find_one({"_id": ctx.author.id})
            already_married = already_married["marriedwith"]
            if already_married is not None:
                already_married = await self.bot.fetch_user(already_married)
                embed = discord.Embed(color=random.randint(0, 0xffffff), description=f'You are already married with {already_married.mention}.')
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                def check(x):
                    return x.channel == ctx.message.channel and x.author == member
                embed = discord.Embed(color=random.randint(0, 0xffffff), description="Respond with yes/y/no/n.")
                embed.set_author(icon_url=member.avatar_url, name=member)
                await ctx.send(embed=embed)
                try:
                    response = await self.bot.wait_for('message', check=check, timeout=30)
                    _response = response.content.lower()
                except asyncio.TimeoutError:
                    embed = discord.Embed(color=random.randint(0, 0xffffff), description=f"It looks like {member.mention} needs some more time to think.")
                    return await ctx.send(embed=embed)
                if _response == 'yes' or _response == 'y':
                    user_collection.update_one({"_id": ctx.author.id}, {"$set": {"marriedwith": member.id}})
                    user_collection.update_one({"_id": member.id}, {"$set": {"marriedwith": ctx.author.id}})
                    embed = discord.Embed(color=random.randint(0, 0xffffff), title=f'**{str(ctx.message.author)}** :ring: **{str(member)}**')
                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/825995294788419634/husband-wife.jpg')
                    embed.description = f"***By the power invested in me by no valid or legal authority, I now pronounce {ctx.author.mention} & {member.mention} husband and wife*** :man_in_tuxedo::woman_with_veil:"
                    return await ctx.send(embed=embed)
                elif _response == 'no' or _response == 'n':
                    embed = discord.Embed(color=random.randint(0, 0xffffff), description="Oh... well... maybe give it some time...")
                    return await ctx.send(embed=embed)
                else:
                    return await ctx.send('Not a valid response')
            else:
                raise error

    @commands.command(help="divorce the person you married", usage="divorce###10s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def divorce(self, ctx):
        try:
            already_married = user_collection.find_one({"_id": ctx.author.id})
            if already_married is not None:
                user_collection.update_one({"_id": ctx.author.id}, {"$unset": {"marriedwith": 1}})
                user_collection.update_one({"_id": already_married["marriedwith"]}, {"$unset": {"marriedwith": 1}})
                already_married = await self.bot.fetch_user(already_married["marriedwith"])
                embed = discord.Embed(color=random.randint(0, 0xffffff), description=f'{ctx.author.mention} divorced {already_married.mention}.')
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            else:
                raise KeyError
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: You are not married.')
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            else:
                raise error

def setup(bot):
    bot.add_cog(Social(bot))
