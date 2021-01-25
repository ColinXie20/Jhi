from discord.ext import commands
from discord import Game, Embed, Color
from dotenv import load_dotenv
from random import choice, randint, shuffle
from os import getenv
from time import sleep
from asyncio import TimeoutError
from copy import deepcopy
import math, datetime

from funcs import *
from obtainables import *

bot = commands.Bot(command_prefix=('jh!', 'Jh!', 'jH!', 'JH!'), owner_id=344645840381411329, case_insensitive=True, help_command=None)
load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def errorsend(ctx, errMessage):
    errEmbed = Embed(color=Color.red())
    errEmbed.description = ":x: "+errMessage
    await ctx.send(embed=errEmbed)


@bot.command(name="testprogressbar", description="Not for gameplay usage.")
async def testprogressbar(ctx):
    bar = []
    for i in range(15):
        bar.append(":black_large_square:")
    embed = Embed(color=Color.green())
    embed.description = "Loading...\n"
    for i in bar:
        embed.description += i
    message = await ctx.send(embed=embed)
    for i in range(15):
        bar[i] = ":green_square:"
        embed.description = "Loading...\n"
        for i in bar:
            embed.description += i
        await message.edit(embed=embed)
        sleep(0.75)
    embed.description = "Finished!"
    await message.edit(embed=embed)


@bot.command(name="help", description="Returns all commands available. If [type] is 'short', it will show the shortest aliases of the commands.")
async def help(ctx, type="long", cmd=None):
    if type.lower() not in ("long", "short") and cmd == None:
        cmd = type
        type = "long"
    if cmd == None:
        columnheight = 20
        if type.lower() == "short":
            columnheight = 12
        helptext = "**COMMANDS LIST**```fix"
        unsortedCommandList = bot.commands
        commandlist = []
        for command in unsortedCommandList:
            chosenAlias = str(command)
            if type.lower() == "short":
                aliases = deepcopy(command.aliases)
                aliases.append(str(command))
                for alias in aliases:
                    if len(alias) < len(chosenAlias):
                        chosenAlias = alias
            commandlist.append(chosenAlias)
        commandlist.sort()
        appendcols = []
        colwidths = []
        while True:
            appendcolumn = []
            columnwidth = 0
            newcommandlist = []
            for command in commandlist:
                newcommandlist.append(command)
            broke = False
            for command in commandlist:
                appendcolumn.append(command)
                newcommandlist.remove(command)
                if len(command) > columnwidth:
                    columnwidth = len(command)
                if len(appendcolumn) >= columnheight:
                    broke = True
                    break
            commandlist = newcommandlist
            appendcols.append(appendcolumn)
            colwidths.append(columnwidth+2)
            if not broke:
                break
            broke = False
        for i in range(columnheight):
            breaking = False
            helptext += "\n"
            for coli in range(len(appendcols)):
                try:
                    cmdname = appendcols[coli][i]
                    helptext += cmdname+(" "*(colwidths[coli]-len(cmdname)+1))
                except:
                    pass
            if breaking:
                break
        helptext += "```Try `jh!help <command>` to get more information on a command."
        helpEmbed = Embed(color=Color.gold())
        helpEmbed.description = helptext
        await ctx.author.send(embed=helpEmbed)
        embed = Embed(color=Color.gold())
        embed.description = ":thumbsup: Successfully sent you the "+type.lower()+" version of the command list!"
        await ctx.send(embed=embed)
    else:
        cmd = cmd.lower()
        found = False
        commandlist = bot.commands
        for command in commandlist:
            if cmd == command.name or cmd in command.aliases:
                foundcmd = command
                found = True
                break
        if found:
            outputdata = "**"+cmd+"**\n"+foundcmd.description+"\n\n**Usage:** `jh!"
            outputdata += foundcmd.name
            for alias in foundcmd.aliases:
                outputdata += "|"+alias
            outputdata += " "+foundcmd.signature+"`"
            helpEmbed = Embed(color=Color.gold())
            helpEmbed.description = outputdata
            await ctx.send(embed=helpEmbed)
        else:
            await errorsend(ctx, "That command could not be found.")


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(name="jh!help, jh!rollspirit"))
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="set", description="Sets someone's data. <recipient> should be an ID. <value> is case sensitive."+
                                     "<datatype> needs to be one in this list: "+
                                     "[spirit, nickname, level, tokens, prestige, talisman, wins, modifier] [ADMINISTRATOR ONLY]")
async def set(ctx, datatype, value, recipient = "self"):
    if ctx.author.id != bot.owner_id and ctx.message.channel.id != 791393875800621068:
        await errorsend(ctx, "You are not an administrator.")
        return
    if recipient == "self":
        recipient = ctx.author.id
    else:
        recipient = int(recipient)
    info = getinfo("info.txt", recipient)
    if info == -1:
        await errorsend(ctx, "User **" + str(await bot.fetch_user(recipient)) + "** could not be found in the data files.")
        return
    validDTypes = ("spirit", "nickname", "level", "tokens", "prestige", "talisman", "wins", "modifier")
    dtypeDict = {
        "spirit": 1,
        "nickname": 4,
        "level": 2,
        "tokens": 8,
        "prestige": 7,
        "talisman": 9,
        "wins": 10,
        "modifier": 11,
    }
    if datatype.lower() not in validDTypes:
        await errorsend(ctx, "Invalid data type. Refer to `jh!help set`.")
    info[dtypeDict[datatype.lower()]] = value
    if datatype.lower() == "spirit":
        info[4] = value
    updateinfo("info.txt", recipient, info)
    embed = Embed(color=Color.gold())
    embed.description = ":thumbsup: Successfully set **" + str(await bot.fetch_user(recipient)) + "**'s **"+datatype.lower()+"** to **"+value+"**."
    await ctx.send(embed=embed)


@bot.command(name="rollspirit", aliases=["roll", "rspirit", "reroll"], description="Rolls a random spirit animal. Can be rerolled with a 30 minute cooldown.")
@commands.cooldown(1, 1800, commands.BucketType.user)
async def rollspirit(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo != -1:
        spirit = yourinfo[1]
        currentSpirit = yourinfo[1]
    else:
        spirit = ""
        currentSpirit = ""
    while spirit == currentSpirit:
        percentage = randint(1, 100)
        if percentage <= 60:
            spirit = choice(commonSpirits)
        elif percentage <= 94:
            spirit = choice(rareSpirits)
        else:
            spirit = choice(legendarySpirits)
    if spirit[0].lower() in ("a", "e", "i", "o", "u"):
        text = "<@!"+str(ctx.author.id)+"> You rolled an " + spiritEmoji[spirit.lower()] + "**" + spirit + "**!"
    else:
        text = "<@!"+str(ctx.author.id)+"> You rolled a " + spiritEmoji[spirit.lower()] + "**" + spirit + "**!"
    embed = Embed(color=Color.green())
    embed.description = text
    newuser = False
    if getinfo("info.txt", ctx.author.id) == -1:
        newuser = True
        adduser("info.txt", ctx.author.id, spirit)
    else:
        embed.description += "\nDo you want to keep this spirit? React to this message to confirm."
    message = await ctx.send(embed=embed)
    if newuser:
        return
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message.id == message.id
    try:
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except TimeoutError:
        embed.description = text+"\n:x: Timed out."
        await message.edit(embed=embed)
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[1] = spirit
    yourinfo[4] = spirit
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.green())
    embed.description = ":thumbsup: You kept the spirit animal."
    await ctx.send(embed=embed)


@bot.command(name="summon", aliases=["summ"], description="Summons a random spirit animal, guaranteed to be rare or higher. Costs 50 tokens, though.")
@commands.cooldown(1, 300, commands.BucketType.user)
async def summon(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal, and consequently, no tokens either. Roll one with `jh!rollspirit`.")
        return
    elif int(yourinfo[8]) < 100:
        await errorsend(ctx, "You need **100**:diamond_shape_with_a_dot_inside: to summon. You currently have **"+yourinfo[8]+"**"+
                       ":diamond_shape_with_a_dot_inside:.")
        return
    embed = Embed(color=Color.green())
    embed.description = "Do you really want to summon a spirit? This will cost you **100**:diamond_shape_with_a_dot_inside:. React to confirm."
    message = await ctx.send(embed=embed)
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message.id == message.id
    try:
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except TimeoutError:
        await message.edit(content=":x: Timed out.")
        return
    spirit = yourinfo[1]
    currentSpirit = yourinfo[1]
    while spirit == currentSpirit:
        percentage = randint(1, 100)
        if percentage <= 60:
            spirit = choice(rareSpirits)
        elif percentage <= 90:
            spirit = choice(legendarySpirits)
        else:
            spirit = choice(mythicalSpirits)
    text = ":six_pointed_star:**SUMMON**:om_symbol:\n<@!"+str(ctx.author.id)+"> "
    if spirit[0].lower() in ("a", "e", "i", "o", "u"):
        text += "You summoned an " + spiritEmoji[spirit.lower()] + "**" + spirit + "**!"
    else:
        text += "You summoned a " + spiritEmoji[spirit.lower()] + "**" + spirit + "**!"
    embed = Embed(color=Color.green())
    embed.description = text+"\nDo you want to keep this summon? React to this message to confirm."
    message = await ctx.send(embed=embed)
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[8] = str(int(yourinfo[8]) - 100)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    try:
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except TimeoutError:
        embed.description = text+"\n:x: Timed out."
        await message.edit(embed=embed)
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[1] = spirit
    yourinfo[4] = spirit
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.green())
    embed.description = ":thumbsup: You kept the summon."
    await ctx.send(embed=embed)


@bot.command(name="upgrademodifier", aliases=["upgrademod", "upmod"], description="Upgrade your spirit's experience modifier.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def upgrademodifier(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal to upgrade experience gain for. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[11] == "1.5":
        await errorsend(ctx, "You have maxed your experience modifier already.")
        return
    price = int(100 + 0.5 + (float(yourinfo[11]) - 1.0) * 1000)
    if int(yourinfo[8]) < price:
        await errorsend(ctx, "You need **" + str(price) + "**:diamond_shape_with_a_dot_inside: to upgrade your modifier."+
                       "You currently have **" + yourinfo[8] + "**:diamond_shape_with_a_dot_inside:.")
        return
    text = "Do you really want to upgrade your modifier? This will cost you **" + str(price) + "**:diamond_shape_with_a_dot_inside:. React to confirm."
    embed = Embed(color=Color.gold())
    embed.description = text
    message = await ctx.send(embed=embed)
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message.id == message.id
    try:
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
    except TimeoutError:
        await message.edit(content=text + "\n:x: Timed out.")
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[8] = str(int(yourinfo[8]) - price)
    yourinfo[11] = str(round(float(yourinfo[11]) + 0.1, 1))
    updateinfo("info.txt", ctx.author.id, yourinfo)
    newEmbed = embed
    newEmbed.description = ":thumbsup: You upgraded your experience modifier to **" + yourinfo[11] + "** for "+\
                           "**" + str(price) + "**:diamond_shape_with_a_dot_inside:."
    await message.edit(embed=newEmbed)


@bot.command(name="spirit", aliases=["sp", "profile"], description="Shows <recipient>'s spirit animal and its statistics. "+
                                                                   "If no <recipient> is specified, it will show your spirit animal.")
async def spirit(ctx, recipient = "self"):
    if recipient.lower() == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    userinfo = getinfo("info.txt", recipient)
    if userinfo == -1 and recipient == ctx.author.id:
        await errorsend(ctx, "You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    elif userinfo == -1:
        await errorsend(ctx, "Invalid recipient. Either they don't have a spirit animal, or they're an invalid user.")
        return
    spirit = userinfo[1]
    nickname = userinfo[4]
    level = int(userinfo[2])
    exp = int(userinfo[3])
    expgoal = str(1000+level*150)
    if level >= 100+(int(userinfo[7])*100):
        expgoal = ":infinity:"
    modifier = 1+(0.02*level)
    p_modifier = 1+(int(userinfo[7])*0.1)
    t_modifiers = talismanBoosts[userinfo[9]]
    statArr = spiritStats[spirit]
    stats = []
    for i in range(3):
        stats.append(round(statArr[i] * t_modifiers[i] * modifier * p_modifier))
    stats.append(round(statArr[3] * t_modifiers[3]))
    guild = userinfo[5]
    rank = userinfo[6]
    embed = Embed(color=Color.green())
    embed.description = spiritEmoji[spirit.lower()] + "**"+nickname+"\n:shield:Guild: "+guild+"\n:label:Rank: "+rank+\
                        "**\n>>> **Prestige:** "+userinfo[7]+"(+"+str(int(userinfo[7])*10)+"% boost)" + \
                        "\n**Level:** "+str(level)+"/"+str(100+(int(userinfo[7])*100))+\
                        "\n**EXP:** " +str(exp)+"/" +expgoal+\
                        "\n**HP:** "+str(stats[0])+\
                        "\n**ATK:** "+str(stats[1])+\
                        "\n**DEF:** "+str(stats[2])+\
                        "\n**EVA:** "+str(stats[3])
    await ctx.send(embed=embed)


@bot.command(name="stats", description="Shows <recipient>'s spirit animal's base stats. If no <recipient is specified, " +
                                       "it will show the sender's stats.")
async def stats(ctx, recipient = "self"):
    if recipient.lower() == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    userinfo = getinfo("info.txt", recipient)
    if userinfo == -1 and recipient == ctx.author.id:
        await errorsend(ctx, "You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    elif userinfo == -1:
        await errorsend(ctx, "Invalid recipient. Either they don't have a spirit animal, or they're an invalid user.")
        return
    spirit = userinfo[1]
    statArr = spiritStats[spirit]
    emoji = spiritEmoji[spirit.lower()]
    rarity = ""
    if spirit in commonSpirits:
        rarity = "common"
    elif spirit in rareSpirits:
        rarity = "rare"
    elif spirit in legendarySpirits:
        rarity = "legendary"
    elif spirit in mythicalSpirits:
        rarity = "mythical"
    else:
        rarity = "admin"
    # stats are: (HP, ATK, DEF, EVA)
    embed = Embed(color=Color.green())
    embed.description = emoji + "**" + spirit + \
                        "**\n:sparkles:**Rarity:** " + rarity.upper() + ":sparkles:" + \
                        "\n>>> **HP:** " + str(statArr[0]) + \
                        "\n**ATK:** " + str(statArr[1]) + \
                        "\n**DEF:** " + str(statArr[2]) + \
                        "\n**EVA:** " + str(statArr[3])
    await ctx.send(embed=embed)


@bot.command(name="shop", description="Shop to show talismans that can be bought with your tokens.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def shop(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to access the shop. Roll one with `jh!rollspirit`.")
        return
    outputdata  =  "**"+str(await bot.fetch_user(ctx.author.id))+"'s Equipment**\n"+\
                   "> Equipped Talisman: **"+yourinfo[9]+"**"+talismanInfo[yourinfo[9]]+"\n"+\
                   "> Tokens: **"+yourinfo[8]+"**:diamond_shape_with_a_dot_inside:\n"+\
                   "**Talismans Available:**\n"
    for i in range(7):
        t = shopTalismans[i]
        outputdata += "> ("+str(i+1)+")"+t+" "+talismanInfo[t]+" Price: **"+str(talismanPrices[t])+"**:diamond_shape_with_a_dot_inside:\n"
    outputdata += "`jh!buy <talisman_number>` to buy a talisman."
    embed = Embed(color=Color.orange())
    embed.description = outputdata
    await ctx.send(embed=embed)


@bot.command(name="travellingmerchant", aliases=["merchant", "merch"], description="Merchant's shop. Items rotate out every day.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def travellingmerchant(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to access the merchant. Roll one with `jh!rollspirit`.")
        return
    greeting = choice(("Howdy", "Oi, you", "Hey", "You there", "Hey you. Yeah, you", "Yo"))
    outputdata  =  "Merchant: "+greeting+". Want some sweet sweet talismans I found? Come get some before they sell out.\n"+\
                   "**"+str(await bot.fetch_user(ctx.author.id))+"'s Equipment**\n"+\
                   "> Equipped Talisman: **"+yourinfo[9]+"**"+talismanInfo[yourinfo[9]]+"\n"+\
                   "> Tokens: **"+yourinfo[8]+"**:diamond_shape_with_a_dot_inside:\n"+\
                   "**Talismans Available: (rotates every day)**\n"
    day = datetime.datetime.today().weekday()
    for i in range(3):
        t = MerchantTLists[day][i]
        outputdata += "> ("+str(i+1)+")"+t+" "+talismanInfo[t]+" Price: **"+str(talismanPrices[t])+"**:diamond_shape_with_a_dot_inside:\n"
    outputdata += "`jh!merchbuy <talisman_number>` to buy a talisman."
    embed = Embed(color=Color.orange())
    embed.description = outputdata
    await ctx.send(embed=embed)


@bot.command(name="buy", description="Buy a talisman from the shop. This will replace your current talisman.")
async def buy(ctx, talisman_number):
    talisman_number = int(talisman_number)
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to purchase talismans. Roll one using the `jh!rollspirit` command.")
        return
    talisman = talismanIDs[talisman_number]
    if talisman_number <= 7 and talisman_number >= 1 and talisman != yourinfo[9]:
        if int(yourinfo[8]) >= talismanPrices[talisman]:
            yourinfo[8] = str(int(yourinfo[8])-talismanPrices[talisman])
            yourinfo[9] = talisman
            updateinfo("info.txt", ctx.author.id, yourinfo)
            embed = Embed(color=Color.orange())
            embed.description = ":thumbsup: You bought the **"+talisman+"**."
            await ctx.send(embed=embed)
        else:
            await errorsend(ctx, "You do not have enough to buy this talisman. You need **"+
                           str(talismanPrices[talisman])+"**:diamond_shape_with_a_dot_inside:.")
    elif talisman == yourinfo[9]:
        await errorsend(ctx, "You can't buy a talisman that you already own.")
    else:
        await errorsend(ctx, "That talisman is not available in the shop.")


@bot.command(name="merchbuy", aliases=["mbuy"], description="Buy a talisman from the merchant. This will replace your current talisman.")
async def merchbuy(ctx, talisman_number):
    talisman_number = int(talisman_number)
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to purchase talismans. Roll one using the `jh!rollspirit` command.")
        return
    talisman = MerchantTLists[datetime.datetime.today().weekday()][talisman_number-1]
    if talisman_number <= 7 and talisman_number >= 1 and talisman != yourinfo[9]:
        if int(yourinfo[8]) >= talismanPrices[talisman]:
            yourinfo[8] = str(int(yourinfo[8])-talismanPrices[talisman])
            yourinfo[9] = talisman
            updateinfo("info.txt", ctx.author.id, yourinfo)
            embed = Embed(color=Color.orange())
            embed.description = ":thumbsup: You bought the **" + talisman + "**."
            await ctx.send(embed=embed)
        else:
            await errorsend(ctx, "You do not have enough to buy this talisman. You need **"+
                           str(talismanPrices[talisman])+"**:diamond_shape_with_a_dot_inside:.")
    elif talisman == yourinfo[9]:
        await errorsend(ctx, "You can't buy a talisman that you already own.")
    else:
        await errorsend(ctx, "That talisman is not available in the shop.")


@bot.command(name="selltalisman", aliases=["sell", "tsell"], description="Sells your equipped talisman.")
async def sell(ctx, recipient = "self"):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[9] == "None":
        await errorsend(ctx, "You do not have a talisman.")
        return
    if yourinfo[9] in commonTalismans:
        ttype = "common"
    elif yourinfo[9] in uncommonTalismans:
        ttype = "uncommon"
    elif yourinfo[9] in rareTalismans:
        ttype = "rare"
    elif yourinfo[9] == "Easter Egg":
        ttype = "easter_egg"
    sellPrice = tsellPrices[ttype]
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message == message
    try:
        embed = Embed(color=Color.orange())
        embed.description = "Are you sure you would like to sell your **" + yourinfo[9] + "** for " + \
                            "**" + str(sellPrice) + "**:diamond_shape_with_a_dot_inside:?"
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await errorsend(ctx, "Sell request timed out, you didn't confirm.")
        return
    yourinfo[9] = "None"
    yourinfo[8] = str(int(yourinfo[8]) + sellPrice)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.orange())
    embed.description = ":thumbsup: You sold your **" + yourinfo[9] + "** for **" + str(sellPrice) + "**:diamond_shape_with_a_dot_inside:."
    await ctx.send(embed=embed)


@bot.command(name="inventory", aliases=["inv"], description="Shows your equipped talisman, inventory, experience modifier, and spirit.")
async def inventory(ctx, recipient = "self"):
    if recipient == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    info = getinfo("info.txt", recipient)
    if info == -1 and recipient == ctx.author.id:
        await errorsend(ctx, "You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    elif info == -1:
        await errorsend(ctx, "Invalid user. They do not have a spirit animal.")
        return
    embed = Embed(color=Color.green())
    embed.description = "**"+str(await bot.fetch_user(recipient))+"'s Inventory/Equipment**\n>>> "+\
                        "Spirit Animal: " + spiritEmoji[info[1].lower()] + "**"+info[4]+"**\n"+\
                        "Equipped Talisman: **"+info[9]+"**"+talismanInfo[info[9]]+"\n"+\
                        "Experience Modifier: **"+info[11]+"**"
    await ctx.send(embed=embed)


@bot.command(name="balance", aliases=["bal"], description="Tells you how many tokens someone has. Defaults to show your balance.")
async def balance(ctx, recipient = "self"):
    if recipient == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    info = getinfo("info.txt", recipient)
    if info == -1 and recipient == ctx.author.id:
        await errorsend(ctx, "You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    elif info == -1:
        await errorsend(ctx, "That person does not have any money.")
        return
    embed = Embed(color=Color.green())
    if recipient == ctx.author.id:
        embed.description = ":moneybag: You currently have **"+info[8]+"**:diamond_shape_with_a_dot_inside:, <@!"+str(recipient)+">!"
    else:
        embed.description = ":moneybag: <@!"+str(recipient)+"> has **"+info[8]+"**:diamond_shape_with_a_dot_inside:."
    await ctx.send(embed=embed)


@bot.command(name="donate", aliases=["give", "pay"], description="Gives some of your tokens to someone else.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def donate(ctx, amount, recipient):
    recipient = ctx.message.mentions[0].id
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    theirinfo = getinfo("info.txt", recipient)
    if theirinfo == -1:
        await errorsend(ctx, "You cannot donate to someone who does not have a spirit animal. Tell them to roll one using the `jh!rollspirit` command.")
        return
    elif int(yourinfo[8]) < int(amount):
        await errorsend(ctx, "You do not have that many tokens!")
        return
    elif int(amount) < 0:
        await errorsend(ctx, "nooo!! you can't just donate a negative number!")
        return
    elif recipient == ctx.author.id:
        await errorsend(ctx, "You can't donate to yourself!")
        return
    yourinfo[8] = str(int(yourinfo[8])-int(amount))
    theirinfo[8] = str(int(theirinfo[8])+int(amount))
    updateinfo("info.txt", ctx.author.id, yourinfo)
    updateinfo("info.txt", recipient, theirinfo)
    embed = Embed(color=Color.orange())
    embed.description = ":thumbsup: Successfully gave **"+amount+"**:diamond_shape_with_a_dot_inside: to **"+str(await bot.fetch_user(recipient))+"**. "+\
                        "You now have **"+yourinfo[8]+"**:diamond_shape_with_a_dot_inside:, they now have **"+theirinfo[8]+"**:diamond_shape_with_a_dot_inside:."
    await ctx.send(embed=embed)


@bot.command(name="trade", aliases=["spirittrade", "strade"], description="Trade your spirit animal to someone else. You will keep your level though.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def trade(ctx, recipient):
    recipient = ctx.message.mentions[0].id
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    if yourinfo == -1 or theirinfo == -1:
        await errorsend(ctx, "Both of you need a spirit animal to trade. Roll one with `jh!rollspirit`.")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        embed = Embed(color=Color.orange())
        embed.description = ":arrow_forward:**SPIRIT TRADE**:arrow_backward:\n" + \
                            "<@" + str(recipient) + ">, react to this message to accept the trade request. You will both keep your levels."
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await errorsend(ctx, "Trade request timed out, they didn't confirm.")
        return
    swapspirits("info.txt", ctx.author.id, recipient)
    embed = Embed(color=Color.orange())
    embed.description = ":thumbsup: The trade was successful."
    await ctx.send(embed=embed)


@bot.command(name="ttrade", aliases=["talismantrade", "talistrade"], description="Trade your talisman to someone else. You will keep your spirit though.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ttrade(ctx, recipient):
    recipient = ctx.message.mentions[0].id
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    if yourinfo == -1 or theirinfo == -1:
        await errorsend(ctx, "Both of you need a talisman, and by extension, a spirit animal to trade. Roll one with `jh!rollspirit`.")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        embed = Embed(color=Color.orange())
        embed.description = ":arrow_forward:**TALISMAN TRADE**:arrow_backward:\n"+\
                            "<@"+str(recipient)+">, react to this message to accept the trade request. You will both keep your spirits."
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await errorsend(ctx, "Trade request timed out, they didn't confirm.")
        return
    swaptalismans("info.txt", ctx.author.id, recipient)
    embed = Embed(color=Color.orange())
    embed.description = ":thumbsup: The trade was successful."
    await ctx.send(embed=embed)


@bot.command(name="prestige", description="Sacrifice your current levels to increase your level cap by 100. Requires level 100.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def prestige(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to prestige. Roll one with `jh!rollspirit`.")
        return
    elif int(yourinfo[2]) < 100+int(yourinfo[7])*100:
        await errorsend(ctx, "You have to be at least level **"+str(100+int(yourinfo[7])*100)+"** to prestige.")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message == message
    try:
        embed = Embed(color=Color.gold())
        embed.description = ":trident: **PRESTIGE** :trident:\n<@"+str(ctx.author.id)+">, react to this message to prestige."+\
                            "This will reset your level, but raise your level cap by **100**, and grant you **50**:diamond_shape_with_a_dot_inside:."
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await errorsend(ctx, "Prestige request timed out, you didn't confirm.")
        return
    yourinfo[7] = str(int(yourinfo[7])+1)
    yourinfo[2] = str(0)
    yourinfo[3] = str(0)
    yourinfo[8] = str(int(yourinfo[8])+50)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.gold())
    embed.description = ":trident: **You have prestiged. You are now level 0, but your level cap has increased by 100.**"
    await ctx.send(embed=embed)


@bot.command(name="train", description="Train your spirit animal against wild animals.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def train(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to train! Roll one using the `jh!rollspirit` command!")
        return
    spirit = yourinfo[1]
    animal = choice(commonSpirits)
    nickname = yourinfo[4]
    oldexp = int(yourinfo[3])
    level = int(yourinfo[2])
    oldlevel = level
    selfModifier = float(yourinfo[11])
    exp = round(randint(1500+level*30, 3000+level*60)*expmultiplier*selfModifier)
    newexp = oldexp + exp
    tokengain = 0
    while newexp >= 1000+level*100 and level < 100+(int(yourinfo[7])*100):
        newexp -= 1000+level*100
        level += 1
        tokengain += 1
    content = "Your " + spiritEmoji[spirit.lower()] + "**" + nickname + "** beats up a wild " + spiritEmoji[animal.lower()] + animal + \
              " and gains **" + str(exp) + " experience!**"
    if level != oldlevel:
        content += "\nYour " + spiritEmoji[spirit.lower()] + "**" + nickname + "** leveled up! It is now level **" + str(level) + "**. "+\
                   "You also earned **"+str(tokengain)+"**:diamond_shape_with_a_dot_inside:."
    embed = Embed(color=Color.green())
    embed.description = content
    await ctx.send(embed=embed)
    yourinfo[2] = str(level)
    yourinfo[3] = str(newexp)
    yourinfo[8] = str(int(yourinfo[8])+tokengain)
    updateinfo("info.txt", ctx.author.id, yourinfo)


@bot.command(name="interactivetrain", aliases=["itrain"], description="Interactively train your spirit animal by focusing. Gives more experience. "+
                                                                      "Can only be used in DMs.")
@commands.cooldown(1, 180, commands.BucketType.user)
async def interactivetrain(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to train! Roll one using the `jh!rollspirit` command!")
        return
    startEmbed = Embed(color=Color.green())
    startEmbed.description = ":watch: Focus. There is a time limit, and there will be three rounds. Choose the correct reaction each round, or you will fail.\n"+\
                             "Do not react while the reactions are being added by the bot."
    await ctx.send(embed=startEmbed)
    sleep(3)
    correctReaction = ""
    indicators = ["🇦", "🇧", "🇨", "🇩", "🇪"]
    def check(reaction, user):
        return str(reaction.emoji) == correctReaction and user.id == ctx.author.id and reaction.message == message
    for trainround in range(3):
        correctReaction = choice(indicators)
        try:
            roundEmbed = Embed(color=Color.green())
            roundEmbed.description = "<@!" + str(ctx.author.id) + "> **ROUND " + str(trainround + 1) + ":**" +\
                                     " React to this message with a " + correctReaction + "!"
            message = await ctx.send(embed=roundEmbed)
            shuffle(indicators)
            for e in indicators:
                await message.add_reaction(e)
            reaction, user = await bot.wait_for('reaction_add', timeout=3.5, check=check)
        except TimeoutError:
            await errorsend(ctx, "You failed the training session.")
            return
    tokengain = 0
    yourinfo = getinfo("info.txt", ctx.author.id)
    level = int(yourinfo[2])
    oldlevel = level
    selfModifier = float(yourinfo[11])
    exp = round(randint(4500 + level * 90, 9000 + level * 180)*expmultiplier*selfModifier)
    newexp = int(yourinfo[3]) + exp
    while newexp >= 1000+level*100 and level < 100+(int(yourinfo[7])*100):
        newexp -= 1000+level*100
        level += 1
        tokengain += 1
    yourinfo[3] = str(newexp)
    yourinfo[2] = str(level)
    yourinfo[8] = str(int(yourinfo[8])+tokengain)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    content = "You completed the interactive training and earned **"+str(exp)+" experience!**"
    if level != oldlevel:
        content += "\nYour " + spiritEmoji[yourinfo[1].lower()] + "**" + yourinfo[4] + "** leveled up! It is now level **" + str(level) + "**. " + \
                   "You also earned **" + str(tokengain) + "**:diamond_shape_with_a_dot_inside:."
    embed = Embed(color=Color.green())
    embed.description = content
    await ctx.send(embed=embed)


@bot.command(name="shellgame", aliases=["shell"], description="Guess which shell the coin lies under. If you are correct, you earn some tokens.")
@commands.cooldown(1, 300, commands.BucketType.user)
async def shellgame(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to use this command! Roll one using the `jh!rollspirit` command!")
        return
    header = ":coin:**SHELL GAME**:coin:\nGuess which shell the coin lies under!\nReact to this message to guess.\n"
    shells = [":chestnut:", ":chestnut:", ":chestnut:"]
    coinLocation = randint(0, 2)
    embed = Embed(color=Color.green())
    embed.description = header + "> " + shells[0] + " " + shells[1] + " " + shells[2]
    message = await ctx.send(embed=embed)
    reactDict = {0: "1️⃣", 1: "2️⃣", 2: "3️⃣"}
    correctReaction = reactDict[coinLocation]
    shells[coinLocation] = ":coin:"
    newEmbed = embed
    def check(reaction, user):
        if str(reaction.emoji) != correctReaction and user.id == ctx.author.id and reaction.message == message:
            raise
        return user.id == ctx.author.id and reaction.message == message
    for i in range(3):
        await message.add_reaction(reactDict[i])
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
    except:
        newEmbed.description = header + "> " + shells[0] + " " + shells[1] + " " + shells[2] + "\n" + ":x: You chose incorrectly/timed out."
        await message.edit(embed=newEmbed)
        return
    newEmbed.description = header + "> " + shells[0] + " " + shells[1] + " " + shells[2] + "\n" + \
                           ":thumbsup: You guessed correctly and earned **20**:diamond_shape_with_a_dot_inside:."
    await message.edit(embed=newEmbed)
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[8] = str(int(yourinfo[8]) + 20)
    updateinfo("info.txt", ctx.author.id, yourinfo)


@bot.command(name="search", aliases=["scout"], description="Search the ruins for spirit-boosting artifacts. You might find something special...")
@commands.cooldown(1, 180, commands.BucketType.user)
async def search(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to search! Roll one using the `jh!rollspirit` command!")
        return
    spirit = yourinfo[1]
    nickname = yourinfo[4]
    level = int(yourinfo[2])
    embed1 = Embed(color=Color.green())
    embed1.description = "Your " + spiritEmoji[spirit.lower()] + "**" + nickname + "** searches for artifacts in the ruins.\nSearching..."
    message = await ctx.send(embed=embed1)
    percentage = randint(1, 155)
    if percentage <= 70:
        artifact = choice(commonArtifacts)
    elif percentage <= 85:
        artifact = choice(rareArtifacts)
    elif percentage <= 90:
        artifact = choice(superRareArtifacts)
    elif percentage <= 98:
        artifact = choice(commonSearchableTalismans)
        ttype = "common"
    elif percentage <= 100:
        artifact = choice(rareSearchableTalismans)
        ttype = "rare"
    elif percentage == 101:
        artifact = "Easter Egg"
        ttype = "easter_egg"
    else:
        artifact = "None"
    embed2 = embed1
    if artifact == "None":
        sleep(randint(2, 4))
        embed2.description = spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with nothing."
        await message.edit(embed=embed2)
        return
    term = "a"
    if artifact[0].lower() in ("a", "e", "i", "o", "u"):
        term = "an"
    if artifact not in commonSearchableTalismans and artifact not in rareSearchableTalismans and artifact != "Easter Egg":
        levelcap = 100+(int(yourinfo[7])*100)
        selfModifier = float(yourinfo[11])
        levelUpAmount = round(randint(artifactLevels[artifact][0], artifactLevels[artifact][1]) * expmultiplier * selfModifier)
        if level < levelcap:
            level += levelUpAmount
            if level > levelcap:
                level = levelcap
            yourinfo[2] = str(level)
            yourinfo[8] = str(int(yourinfo[8])+levelUpAmount)
            updateinfo("info.txt", ctx.author.id, yourinfo)
            sleep(randint(2, 4))
            embed2.description = spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with " + term + " " +\
                                 artifactEmojis[artifact] + "**" + artifact + "**!\nThe " +artifactEmojis[artifact] + "**" + artifact + \
                                 "** boosts your spirit's level to **"+ str(level) + "**. You also earned **"+str(levelUpAmount)+\
                                 "**:diamond_shape_with_a_dot_inside:."

        else:
            yourinfo[8] = str(int(yourinfo[8]) + levelUpAmount)
            updateinfo("info.txt", ctx.author.id, yourinfo)
            sleep(randint(2, 4))
            embed2.description = spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with a " + artifactEmojis[artifact] + "**" + artifact + "**!\n"+\
                                 "You also earned **"+str(levelUpAmount)+"**:diamond_shape_with_a_dot_inside:."
        await message.edit(embed=embed2)
    else:
        sleep(randint(2, 4))
        embed2.description = spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with " + \
                             term + " **" +artifact+"**! Stats: "+talismanInfo[artifact]+\
                             "\nWould you like to keep this talisman? It will replace your current one. "+\
                             "You can also sell it for **"+str(tsellPrices[ttype])+"**:diamond_shape_with_a_dot_inside:.\n"+\
                             "React with ✅ to keep and 💠 to sell. If you choose to keep it, it will sell your current talisman."
        await message.edit(embed=embed2)
        def check(reaction, user):
            return str(reaction.emoji) in ["✅", "💠"] and user.id == ctx.author.id and reaction.message == message
        try:
            await message.add_reaction("✅")
            await message.add_reaction("💠")
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                yourinfo = getinfo("info.txt", ctx.author.id)
                oldTalisman = yourinfo[9]
                if oldTalisman in commonTalismans:
                    sellPrice = tsellPrices["common"]
                elif oldTalisman in uncommonTalismans:
                    sellPrice = tsellPrices["uncommon"]
                elif oldTalisman in rareTalismans:
                    sellPrice = tsellPrices["rare"]
                elif oldTalisman == "Easter Egg":
                    sellPrice = tsellPrices["easter_egg"]
                else:
                    sellPrice = 0
                yourinfo[9] = artifact
                yourinfo[8] = str(int(yourinfo[8])+sellPrice)
                updateinfo("info.txt", ctx.author.id, yourinfo)
                embed = Embed(color=Color.green())
                if oldTalisman != "None":
                    embed.description = ":thumbsup: You kept the **" + artifact + "** "+\
                                        "and sold your **" + oldTalisman + "** for **" + str(sellPrice) + "**:diamond_shape_with_a_dot_inside:."
                else:
                    embed.description = ":thumbsup: You kept the **" + artifact + "**."
                await ctx.send(embed=embed)
            elif str(reaction.emoji) == "💠":
                yourinfo = getinfo("info.txt", ctx.author.id)
                yourinfo[8] = str(int(yourinfo[8]) + tsellPrices[ttype])
                updateinfo("info.txt", ctx.author.id, yourinfo)
                embed = Embed(color=Color.green())
                embed.description = ":thumbsup: You sold the **" + artifact + "** for **" + str(tsellPrices[ttype]) + "**:diamond_shape_with_a_dot_inside:."
                await ctx.send(embed=embed)
        except TimeoutError:
            await errorsend(ctx, "You left the talisman.")
            return


@bot.command(name="ritual", description="Conduct a ritual to strengthen your spirit. There is a chance to fail...")
@commands.cooldown(1, 3600, commands.BucketType.user)
async def ritual(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal to use this command! Roll one using the `jh!rollspirit` command!")
        return
    elif int(yourinfo[2]) < 50:
        await errorsend(ctx, "Your spirit is not powerful enough to conduct a ritual. Get to level **50** first.")
        return
    embed = Embed(color=Color.green())
    embed.description = ":star_and_crescent:**RITUAL**:six_pointed_star:\n"+\
                        "Do you want to conduct a ritual? If it is successful, your spirit will gain a random number of levels. "+\
                        "If it fails, your spirit will lose a random number of levels.\n"+\
                        "You will not gain or lose :diamond_shape_with_a_dot_inside: from this command.\n"+\
                        "React to this message to confirm."
    message = await ctx.send(embed=embed)
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message == message
    try:
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        embed.description = text + "\n:x: Timed out."
        await message.edit(embed=embed)
        return
    spirit = yourinfo[1]
    nickname = yourinfo[4]
    level = int(yourinfo[2])
    levelCap = (int(yourinfo[7])+1)*100
    success = choice((True, False))
    levelAmount = randint(10, 50)
    if success:
        level += levelAmount
        if level > levelCap:
            level = levelCap
        embed = Embed(color=Color.green())
        embed.description = ":star_and_crescent:**RITUAL**:six_pointed_star:\n:white_check_mark:The ritual went successfully.\n"+\
                            "Your "+spiritEmoji[spirit.lower()]+"**"+nickname+"** levels up to level **"+str(level)+"**."
    else:
        level -= levelAmount
        embed = Embed(color=Color.red())
        embed.description = ":star_and_crescent:**RITUAL**:six_pointed_star:\n:x:The ritual ends in a catastrophic failure.\n"+\
                            "Your "+spiritEmoji[spirit.lower()]+"**"+nickname+"** is hurt in the process and loses **"+str(levelAmount)+"** levels."
    yourinfo[2] = str(level)
    yourinfo[3] = '0'
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await message.edit(embed=embed)


@bot.command(name="nickname", aliases=["nick", "rename"], description="Nickname your spirit animal! You can rename it anytime.")
async def nickname(ctx, *, new_nick):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal! Roll one with the `jh!rollspirit` command!")
        return
    elif len(new_nick) <= 18:
        for c in new_nick:
            if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ":
                await errorsend(ctx, "Your spirit animal's nickname can only contain letters and spaces!")
                return
    else:
        await errorsend(ctx, "Your spirit animal's nickname cannot exceed 18 characters in length!")
        return
    yourinfo[4] = new_nick
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.green())
    embed.description = ":thumbsup: Successfully renamed your spirit animal."
    await ctx.send(embed=embed)


@bot.command(name="leaderboard", aliases=["lb", "top"], description="Shows a leaderboard with the top users of the bot, by a user-specified measure. "+
                                                                    "[measure] should be either level, prestige, tokens, or wins.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def leaderboard(ctx, measure = "level"):
    index = {"level": 2, "prestige": 7, "tokens": 8, "wins": 10}[measure.lower()]
    unit = {"level": " Levels", "prestige": " Prestige", "tokens": ":diamond_shape_with_a_dot_inside:", "wins": " Battle(s) Won"}[measure.lower()]
    lines = getallplayers("info.txt")
    infodict = {}
    for line in lines:
        info = eval(line[:len(line) - 1])
        infodict.update({int(info[0]): int(info[index])})
    idarr = sorted(infodict, key=infodict.get)
    idarr = idarr[::-1]
    counter = 0
    outputdata = ""
    for userid in idarr:
        if counter >= 10:
            break
        outputdata += str(counter+1)+". :medal:"+str(await bot.fetch_user(userid))+" - **"+str(infodict[userid])+unit+"**\n"
        counter += 1
    embed = Embed(color=Color.gold())
    embed.description = outputdata
    await ctx.send(embed=embed)


@bot.command(name="duel", aliases=["battle", "kill"], description="Duel another player! Both players must have a spirit animal."+
                                                                  "The winner receives one token.")
@commands.cooldown(1, 45, commands.BucketType.user)
async def duel(ctx, recipient):
    recipient = ctx.message.mentions[0].id
    if getinfo("info.txt", ctx.author.id) == -1 or getinfo("info.txt", recipient) == -1:
        await errorsend(ctx, "At least one of you does not have a spirit animal! One of you needs to roll one with `jh!rollspirit`.")
        return
    elif recipient == ctx.author.id:
        await errorsend(ctx, "You cannot duel yourself!")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        embed = Embed(color=Color.red())
        embed.description = ":crossed_swords:**DUEL**:crossed_swords:\n<@"+str(recipient)+">, react to this message to accept the duel invitation!"
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await errorsend(ctx, "Duel request timed out, recipient did not accept.")
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    duelmessage = ":crossed_swords: **DUEL** :crossed_swords:"
    hpcounter = "Turn -\nHP1: - HP2: -"
    movelog = "> -\n> -"
    duelEmbed = Embed(color=Color.red())
    duelEmbed.description = duelmessage + "\n" + hpcounter + "\n" + movelog
    message = await ctx.send(embed=duelEmbed)
    spirit1 = yourinfo[1]
    spirit2 = theirinfo[1]
    name1 = spiritEmoji[spirit1.lower()] + "**" + yourinfo[4] + "**"
    name2 = spiritEmoji[spirit2.lower()] + "**" + theirinfo[4] + "**"
    level1 = int(yourinfo[2])
    level2 = int(theirinfo[2])
    statArr1 = spiritStats[spirit1]
    statArr2 = spiritStats[spirit2]
    modifier1 = 1.0 + (0.02 * level1)
    modifier2 = 1.0 + (0.02 * level2)
    p_modifier1 = 1 + (int(yourinfo[7]) * 0.1)
    p_modifier2 = 1 + (int(theirinfo[7]) * 0.1)
    t_modifiers1 = talismanBoosts[yourinfo[9]]
    t_modifiers2 = talismanBoosts[theirinfo[9]]
    stats1 = []
    stats2 = []
    for i in range(3):
        stats1.append(round(statArr1[i] * t_modifiers1[i] * modifier1 * p_modifier1))
        stats2.append(round(statArr2[i] * t_modifiers2[i] * modifier2 * p_modifier2))
    stats1.append(round(statArr1[3] * t_modifiers1[3]))
    stats2.append(round(statArr2[3] * t_modifiers2[3]))
    turn = 0
    hpcounter = "**Turn " + str(turn) + "**\n" + name1 + " HP: " + str(round(stats1[0])) + " | " + name2 + " HP: " + str(round(stats2[0]))
    file = open("enablesmite.txt", "r")
    smiting = file.read()
    file.close()
    await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
    while stats1[0] > 0 and stats2[0] > 0:
        if turn > 50:
            await errorsend(ctx, "Duel exceeded 50 turns, resulted in a stalemate.")
            return
        elif turn % 2 == 0:
            move = choice(spiritMoves[spirit1])
            if yourinfo[0] == str(bot.owner_id) and smiting == "ON":
                move = "Developer's Smite"
            movelog = "> " + name1 + " uses **" + move + "** on " + name2 + "!\n> -"
            await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
            sleep(0.25)
            if move == "Developer's Smite":
                calculation = 0
            if randint(1, 100) <= stats2[3]:
                movelog = "> " + name1 + " uses **" + move + "** on " + name2 + "!\n> " + name2 + " evades the attack!"
                await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
            else:
                damage = round(
                    randint(round(stats1[1] * 0.9 * moveDamage[move]), round(stats1[1] * 1.1 * moveDamage[move])) -
                    stats2[2])
                if damage < 1:
                    damage = 1
                movelog = "> " + name1 + " uses **" + move + "** on " + name2 + "!\n> " + name2 + " takes " + str(damage) + " damage!"
                await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
                stats2[0] = round(stats2[0] - damage)
                if stats2[0] < 0:
                    stats2[0] = 0
        elif turn % 2 == 1:
            move = choice(spiritMoves[spirit2])
            if theirinfo[0] == str(bot.owner_id) and smiting == "ON":
                move = "Developer's Smite"
            movelog = "> " + name2 + " uses **" + move + "** on " + name1 + "!\n> -"
            await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
            sleep(0.25)
            if move == "Developer's Smite":
                calculation = 0
            if randint(1, 100) <= stats1[3]:
                movelog = "> " + name2 + " uses **" + move + "** on " + name1 + "!\n> " + name1 + " evades the attack!"
                await message.edit( embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
            else:
                damage = round(
                    randint(round(stats2[1] * 0.9 * moveDamage[move]), round(stats2[1] * 1.1 * moveDamage[move])) -
                    stats1[2])
                if damage < 1:
                    damage = 1
                movelog = "> " + name2 + " uses **" + move + "** on " + name1 + "!\n> " + name1 + " takes " + str(damage) + " damage!"
                await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
                stats1[0] = round(stats1[0] - damage)
                if stats1[0] < 0:
                    stats1[0] = 0
        hpcounter = "**Turn " + str(turn) + "**\n" + name1 + " HP: " + str(round(stats1[0])) + " | " + name2 + " HP: " + str(round(stats2[0]))
        await message.edit(embed=Embed(color=Color.red(), description=duelmessage + "\n" + hpcounter + "\n" + movelog))
        sleep(0.25)
        turn += 1
    if stats1[0] <= 0:
        winner = theirinfo
        winnerid = int(theirinfo[0])
    elif stats2[0] <= 0:
        winner = yourinfo
        winnerid = int(yourinfo[0])
    embed.description = "**" + str(await bot.fetch_user(winnerid)) + "'s** " + spiritEmoji[winner[1].lower()] + "**" + winner[4] + "** is victorious!"+\
                        ":trophy: **+1**:diamond_shape_with_a_dot_inside:"
    await ctx.send(embed=embed)
    winner[8] = str(int(winner[8])+1)
    winner[10] = str(int(winner[10])+1)
    updateinfo("info.txt", winnerid, winner)


@bot.command(name="createguild", aliases=["cguild"], description="Create a guild!")
async def createguild(ctx, *, name):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal in order to create a guild! Roll one with `jh!rollspirit`!")
        return
    if name[0] == '"' and name[len(name)-1] == '"':
        name = name[1:-1]
    if yourinfo[5] != "None":
        await errorsend(ctx, "You cannot create a guild if you already have one! You can disband it with `jh!disband`, or leave it with `jh!leave`.")
        return
    elif len(name) > 20:
        await errorsend(ctx, "Your guild name cannot exceed 20 characters in length!")
        return
    elif len(name) < 3:
        await errorsend(ctx, "Your guild name has to be at least 3 characters long!")
        return
    for c in name:
        if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ":
            await errorsend(ctx, "Your guild name can only contain letters and spaces!")
            return
    samename = False
    lines = getallguilds("guildnames.txt")
    for line in lines:
        if name == line[:-1]:
            samename = True
            break
    if samename:
        await errorsend(ctx, "The name you chose is already taken!")
        return
    yourinfo[5] = name
    yourinfo[6] = "Leader"
    updateinfo("info.txt", ctx.author.id, yourinfo)
    addguild("guildnames.txt", name)
    embed = Embed(color=Color.blue())
    embed.description = ":thumbsup: Successfully created guild **" + name + "**."
    await ctx.send(embed=embed)


@bot.command(name="guild", description="View the statistics of your guild.")
async def guild(ctx, recipient = "self"):
    if recipient == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    info = getinfo("info.txt", recipient)
    if info == -1 and recipient == ctx.author.id:
        await errorsend(ctx, "You do not have a spirit animal, and by extension, do not have a guild either. Roll one with `jh!rollspirit`.")
        return
    elif info[5] == "None" and recipient == ctx.author.id:
        await errorsend(ctx, "You do not have a guild.")
        return
    elif info == -1:
        await errorsend(ctx, "They do not have a spirit animal, and by extension, do not have a guild either.")
        return
    elif info[5] == "None":
        await errorsend(ctx, "They do not have a guild.")
        return
    guildname = info[5]
    totalLevel = 0
    memberCount = 0
    lines = getallplayers("info.txt")
    for line in lines:
        info = eval(line[:len(line) - 1])
        if info[5] == guildname:
            totalLevel += int(info[2])
            memberCount += 1
    embed = Embed(color=Color.blue())
    embed.description = ":shield: **"+guildname+"** :shield:\n> **Total Level:** "+str(totalLevel)+"\n> **Members:** "+str(memberCount)
    await ctx.send(embed=embed)


@bot.command(name="guild-list", aliases=["glist", "g-list", "members"], description="Get a list of the members of your guild. DMs must be enabled.")
async def guildlist(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal, and by extension, do not have a guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await errorsend(ctx, "You do not have a guild.")
        return
    lines = getallplayers("info.txt")
    guildname = yourinfo[5]
    outputdata = "**:shield: Members of "+guildname+" :shield:**\n>>> "
    for line in lines:
        info = eval(line[:len(line) - 1])
        if info[5] == guildname:
            level = int(info[2])
            name = str(await bot.fetch_user(int(info[0])))
            rank = info[6]
            outputdata += "**"+rank+"** - "+name+" - **Level "+str(level)+"**\n"
    user = await bot.fetch_user(ctx.author.id)
    try:
        embed = Embed(color=Color.blue())
        embed.description = outputdata
        await user.send(embed=embed)
        content = ":thumbsup: Successfully sent you a DM with member info!"
    except:
        content = ":x: DM could not be sent. Make sure the bot has permission to DM you."
    embed = Embed(color=Color.blue())
    embed.description = content
    await ctx.send(embed=embed)


@bot.command(name="disband", description="Disband your guild. Will automatically kick all members out.")
async def disband(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal, and by extension, no guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await errorsend(ctx, "You cannot disband a guild if you don't have one!")
        return
    elif yourinfo[6] != "Leader":
        await errorsend(ctx, "Only the leader can disband a guild!")
        return
    guildname = yourinfo[5]
    lines = getallplayers("info.txt")
    for line in lines:
        info = eval(line[:len(line) - 1])
        if info[5] == guildname:
            info[5] = "None"
            info[6] = "None"
        updateinfo("info.txt", int(info[0]), info)
    lines = getallguilds("guildnames.txt")
    for line in lines:
        if line == guildname+"\n":
            lines.remove(line)
    file = open("guildnames.txt", "w")
    file.write("".join(lines))
    file.close()
    embed = Embed(color=Color.blue())
    embed.description = ":wave:**"+guildname+"** has been disbanded. Goodbye."
    await ctx.send(embed=embed)


@bot.command(name="invite", description="Invite another player to your guild! <playername> should be a mention.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx, playername):
    inviter = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    invitee = getinfo("info.txt", playerid)
    if inviter == -1 or invitee == -1:
        await errorsend(ctx, "One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif inviter[5] == "None":
        await errorsend(ctx, "You cannot invite a player to your guild if you don't have a guild!")
        return
    elif inviter[6] not in ["Leader", "Recruiter"]:
        await errorsend(ctx, "You cannot invite a player to your guild if you aren't the leader or a recruiter!")
        return
    elif invitee[5] != "None":
        await errorsend(ctx, "You cannot invite a player that is already in a guild!")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == playerid and reaction.message == message
    try:
        embed = Embed(color=Color.blue())
        embed.description = "<@"+str(playerid)+">, react to this message to accept the guild invitation!"
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await errorsend(ctx, "Invite request timed out, recipient did not accept.")
        return
    invitee[5] = inviter[5]
    invitee[6] = "Member"
    updateinfo("info.txt", playerid, invitee)
    embed = Embed(color=Color.blue())
    embed.description = ":wave:**"+str(await bot.fetch_user(playerid))+"** has joined **"+inviter[5]+"**!"
    await ctx.send(embed=embed)


@bot.command(name="leave", description="Leave your guild.")
async def leave(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You do not have a spirit animal, and by extension, no guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await errorsend(ctx, "You cannot leave a guild if you don't have one!")
        return
    elif yourinfo[6] == "Leader":
        await disband.invoke(ctx)
        return
    guildname = yourinfo[5]
    yourinfo[5] = "None"
    yourinfo[6] = "None"
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.blue())
    embed.description = "You have left **"+guildname+"**."
    await ctx.send(embed=embed)


@bot.command(name="kick", description="Kick a player out of your guild. <playername> should be a mention.")
async def kick(ctx, playername):
    kicker = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    kickee = getinfo("info.txt", playerid)
    if kicker == -1 or kickee == -1:
        await errorsend(ctx, "One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif kicker[5] == "None":
        await errorsend(ctx, "You cannot kick a player if you don't have a guild!")
        return
    elif kicker[6] != "Leader":
        await errorsend(ctx, "You cannot kick a member of your guild if you aren't the leader!")
        return
    elif kicker[5] != kickee[5]:
        await errorsend(ctx, "You cannot kick a player that isn't in your guild!")
        return
    elif kicker == kickee:
        await leave.invoke(ctx)
        return
    kickee[5] = "None"
    kickee[6] = "None"
    updateinfo("info.txt", playerid, kickee)
    embed = Embed(color=Color.blue())
    embed.description = "**"+str(await bot.fetch_user(playerid))+"** has been kicked from your guild."
    await ctx.send(embed=embed)


@bot.command(name="promote", description="Promote a player in your guild!")
async def promote(ctx, playername):
    promoter = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    promotee = getinfo("info.txt", playerid)
    if promoter == -1 or promotee == -1:
        await errorsend(ctx, "One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif promoter[5] == "None":
        await errorsend(ctx, "You cannot promote a player if you don't have a guild!")
        return
    elif promoter[6] != "Leader":
        await errorsend(ctx, "You cannot promote a player in your guild if you aren't the leader!")
        return
    elif promoter[5] != promotee[5]:
        await errorsend(ctx, "You cannot promote a player that isn't in your guild!")
        return
    elif promotee[6] not in ["Member", "Elite"]:
        await errorsend(ctx, "You cannot promote this player!")
        return
    if promotee[6] == "Member":
        promotee[6] = "Elite"
    else:
        promotee[6] = "Recruiter"
    updateinfo("info.txt", playerid, promotee)
    embed = Embed(color=Color.blue())
    embed.description = "Successfully promoted **"+str(await bot.fetch_user(playerid))+"** to **" + promotee[6] + "**!"
    await ctx.send(embed=embed)


@bot.command(name="demote", description="Demote a player in your guild.")
async def demote(ctx, playername):
    demoter = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    demotee = getinfo("info.txt", playerid)
    if demoter == -1 or demotee == -1:
        await errorsend(ctx, "One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif demoter[5] == "None":
        await errorsend(ctx, "You cannot demote a player if you don't have a guild!")
        return
    elif demoter[6] != "Leader":
        await errorsend(ctx, "You cannot demote a player in your guild if you aren't the leader!")
        return
    elif demoter[5] != demotee[5]:
        await errorsend(ctx, "You cannot demote a player that isn't in your guild!")
        return
    elif demotee[6] not in ["Elite", "Recruiter"]:
        await errorsend(ctx, "You cannot demote this player!")
        return
    if demotee[6] == "Recruiter":
        demotee[6] = "Elite"
    else:
        demotee[6] = "Member"
    updateinfo("info.txt", playerid, demotee)
    embed = Embed(color=Color.blue())
    embed.description = "Successfully demoted **" + str(await bot.fetch_user(playerid)) + "** to **" + demotee[6] + "**."
    await ctx.send(embed=embed)


@bot.command(name="smite", description="Owner exclusive command. Sets Developer's Smite to ON or OFF.")
async def smite(ctx, setting):
    if ctx.author.id != bot.owner_id:
        await errorsend(ctx, "Fool. Only the owner of this bot can use this command.")
        return
    elif setting not in ["ON", "OFF"]:
        await errorsend(ctx, "ON and OFF only supported.")
        return
    file = open("enablesmite.txt", "w")
    file.write(setting)
    file.close()
    embed = Embed(color=Color.gold())
    embed.description = ":zap: **Developer's Smite** has been set to **"+setting+"** for **"+str(await bot.fetch_user(bot.owner_id))+"**."
    await ctx.send(embed=embed)


@bot.command(name="coinflip", aliases=["coin", "flip"], description="Flip a coin. Double or nothing. Default prediction is heads.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def coinflip(ctx, amount, prediction="heads"):
    yourinfo = getinfo("info.txt", ctx.author.id)
    amount = int(amount)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal in order to gamble. Roll one with `jh!rollspirit`.")
        return
    elif prediction.lower() not in ["heads", "tails"]:
        await errorsend(ctx, "Your prediction needs to be heads or tails!")
        return
    elif amount > int(yourinfo[8]):
        await errorsend(ctx, "You don't have that much!")
        return
    elif amount < 1:
        await errorsend(ctx, "You have to bet at least **1**:diamond_shape_with_a_dot_inside:!")
        return
    elif amount > 100:
        await errorsend(ctx, "You cannot bet more than **100**:diamond_shape_with_a_dot_inside: at a time!")
        return
    flip = choice(["heads", "tails"])
    content = ":coin: The coin landed on **"+flip.upper()+"**!\n"
    if flip == prediction.lower():
        content += "You won **"+str(amount)+"**:diamond_shape_with_a_dot_inside:!"
        color = Color.green()
        yourinfo[8] = str(int(yourinfo[8])+amount)
    else:
        content += "You lost **"+str(amount)+"**:diamond_shape_with_a_dot_inside:..."
        color = Color.red()
        yourinfo[8] = str(int(yourinfo[8])-amount)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=color)
    embed.description = content
    await ctx.send(embed=embed)


@bot.command(name="bet", description="Bet your money on guessing a number. The number will be randomly chosen from 1 to <max>. "+
                                     "<max> has to be at least 3, and cannot exceed 64.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def bet(ctx, amount, max, prediction):
    yourinfo = getinfo("info.txt", ctx.author.id)
    amount = int(amount)
    prediction = int(prediction)
    max = int(max)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal in order to gamble. Roll one with `jh!rollspirit`.")
        return
    elif amount > int(yourinfo[8]):
        await errorsend(ctx, "You don't have that much!")
        return
    elif amount < 1:
        await errorsend(ctx, "You have to bet at least **1**:diamond_shape_with_a_dot_inside:!")
        return
    elif amount > 100:
        await errorsend(ctx, "You cannot bet more than **100**:diamond_shape_with_a_dot_inside: at a time!")
        return
    elif max < 3 or max > 64:
        await errorsend(ctx, "`<max>` has to be at least 3, and cannot exceed 64.")
        return
    elif prediction > max or prediction < 1:
        await errorsend(ctx, "Your prediction needs to be between 1 and "+str(max)+"!")
        return
    number = randint(1, max)
    content = ":game_die: The die landed on **"+str(number)+"**!\n"
    if number == prediction:
        winamount = amount*(max-1)
        content += "You won **" + str(winamount) + "**:diamond_shape_with_a_dot_inside:!"
        color = Color.green()
        yourinfo[8] = str(int(yourinfo[8]) + winamount)
    else:
        content += "You lost **" + str(amount) + "**:diamond_shape_with_a_dot_inside:..."
        color = Color.red()
        yourinfo[8] = str(int(yourinfo[8]) - amount)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=color)
    embed.description = content
    await ctx.send(embed=embed)


@bot.command(name="daily", description="Claim your daily reward.")
@commands.cooldown(1, 43200, commands.BucketType.user)
async def daily(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await errorsend(ctx, "You need a spirit animal in order to claim your daily reward. Roll one with `jh!rollspirit`.")
        return
    yourinfo[8] = str(int(yourinfo[8]) + 40)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    embed = Embed(color=Color.gold())
    embed.description = ":moneybag: You claimed your daily reward of **40**:diamond_shape_with_a_dot_inside:."
    await ctx.send(embed=embed)


@bot.command(name="credits", description="Shows the credits of the bot.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def credits(ctx):
    embed = Embed(color=Color.gold())
    embed.description = ":panda_face:**Jhi#4308**\nA small game bot centered around spirit animals.\n"+\
                        ":fire:Created by ||TheDysfunctionalDragon||#6910:fire:\n"+\
                        ":sparkles:With help from the following beta testers::sparkles:\n"+\
                        ">>> LaurelWyvern, Ghostie\nWingy, Jeffrier\nG01d3n1i0nfac3, Raystro\nDarkMaster, Marshyy\n--Nico--, Pickle75\nD4rk, Overlord"
    await ctx.send(embed=embed)


@bot.command(name="botstats", aliases=["botinfo"], description="Shows the statistics of the bot.")
async def botstats(ctx):
    servers = list(bot.guilds)
    players = getallplayers("info.txt")
    embed = Embed(color=Color.gold())
    embed.description = ":panda_face:**Jhi#4308**\n"+\
                        ":shield:**"+str(len(servers))+"** servers.:shield:\n"+\
                        ":sparkles:**"+str(len(players))+"** players.:sparkles:\n"+\
                        ":zap:Invite me with [this link.](https://discord.com/api/oauth2/authorize?client_id=576874975307497533&permissions=355392&scope=bot)\n"+\
                        ":page_facing_up:[Link to source code.](https://github.com/ColinXie20/Jhi)"
    await ctx.send(embed=embed)


@bot.command(name="support", aliases=["supportserver", "server"], description="Gives a link to the support server.")
async def support(ctx):
    embed = Embed(color=Color.gold())
    embed.description = "**Jhi Support Server**\n"+\
                        "[Click here to join.](https://discord.gg/kspXEAbqKG)"
    await ctx.send(embed=embed)


@credits.error
async def credits_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: As much as I hate to put a cooldown on credits, it fills up the chat. Try again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot claim your daily reward again for {:.2f} minutes.".format(round(error.retry_after/60))
        await ctx.send(embed=embed)
    else:
        raise error


@rollspirit.error
async def roll_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot roll your spirit animal again for {:.2f} minutes!".format(round(error.retry_after/60))
        await ctx.send(embed=embed)
    else:
        raise error


@summon.error
async def summ_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot summon a spirit again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@upgrademodifier.error
async def upmod_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot upgrade your experience modifier again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@shop.error
async def shop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: The shop can be opened in this channel again in {:.2f}s. This is to prevent flooding.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@travellingmerchant.error
async def merch_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: The merchant's shop can be opened in this channel again in {:.2f}s. This is to prevent flooding.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@donate.error
async def donate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You can donate tokens again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@prestige.error
async def prestige_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot prestige again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error

@invite.error
async def invite_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot invite again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@trade.error
async def trade_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot spirit trade again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@ttrade.error
async def ttrade_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot talisman trade again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@duel.error
async def duel_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot duel again for {:.2f}s!".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@train.error
async def train_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: Your spirit animal has gotten tired. You can train it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@interactivetrain.error
async def itrain_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: Your spirit animal has gotten tired. You can interactively train it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@shellgame.error
async def shellgame_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: This command is on cooldown. Try again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: Your spirit animal has gotten tired. You can have it search again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@ritual.error
async def ritual_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You cannot conduct a ritual again for {:.2f} minutes!".format(round(error.retry_after/60))
        await ctx.send(embed=embed)
    else:
        raise error


@leaderboard.error
async def leaderboard_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: There is a cooldown on leaderboard to prevent filling the chat too quickly. "+\
                            "You can use it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@coinflip.error
async def coinflip_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You can flip a coin again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@bet.error
async def bet_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(color=Color.red())
        embed.description = ":x: You can roll a die again in {:.2f}s.".format(error.retry_after)
        await ctx.send(embed=embed)
    else:
        raise error


@bot.command(name="ping", description="Get the current latency of the bot.")
async def ping(ctx):
    latency = round(bot.latency*1000, 2)
    if latency < 70:
        color = Color.green()
        append_message = ":white_check_mark: The bot is running in good condition."
    elif latency < 100:
        color = Color.gold()
        append_message = ":thumbsup: The bot is doing fine."
    elif latency < 160:
        color = Color.orange()
        append_message = ":x: The bot is currently experiencing difficulties."
    else:
        color = Color.red()
        append_message = ":skull: The bot is running very slowly and data issues may occur."
    embed = Embed(color=color)
    embed.description = ":ping_pong: Pong! Latency: **"+str(latency)+" ms**\n"+append_message
    await ctx.send(embed=embed)


bot.run(TOKEN, bot=True, reconnect=True)
