from discord.ext import commands
from discord import Game
from dotenv import load_dotenv
from random import choice, randint, shuffle
from os import getenv
from time import sleep
from asyncio import TimeoutError
from funcs import *
from obtainables import *
import math

bot = commands.Bot(command_prefix=('jh!', 'Jh!', 'jH!', 'JH!'), owner_id=344645840381411329, case_insensitive=True, help_command=None)
load_dotenv()
TOKEN = getenv("BOT_TOKEN")


@bot.command(name="help", description="Returns all commands available.")
async def help(ctx, cmd=None):
    if cmd == None:
        columnheight = 10
        helptext = "```"
        commandlist = bot.commands
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
                appendcolumn.append(str(command))
                newcommandlist.remove(command)
                if len(str(command)) > columnwidth:
                    columnwidth = len(str(command))
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
            for coli in range(len(appendcols)):
                try:
                    cmdname = appendcols[coli][i]
                    helptext += cmdname+(" "*(colwidths[coli]-len(cmdname)+1))
                except:
                    pass
            helptext += "\n"
            if breaking:
                break
        helptext += "\nTry jh!help <command> to get more information on a command."
        helptext += "```"
        await ctx.send(helptext)
    else:
        found = False
        commandlist = bot.commands
        for command in commandlist:
            if cmd == command.name or cmd in command.aliases:
                foundcmd = command
                found = True
                break
        if found:
            outputdata = "```"+foundcmd.description+"\n\nUsage: jh!"
            outputdata += foundcmd.name
            for alias in foundcmd.aliases:
                outputdata += "|"+alias
            outputdata += " "+foundcmd.signature
            outputdata += "```"
            await ctx.send(outputdata)
        else:
            await ctx.send(":x: That command could not be found.")


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(name="jh!help, jh!rollspirit"))
    print(f'{bot.user} has connected to Discord!')


async def spiritduel(ctx, fighter1, fighter2, duelType):
    await ctx.send(":crossed_swords: **" + duelType.upper() + "** :crossed_swords:")
    hpcounter = await ctx.send("Turn -\nHP1: - HP2: -")
    message = await ctx.send("> -\n> -")
    spirit1 = fighter1[1]
    spirit2 = fighter2[1]
    name1 = spiritEmoji[spirit1.lower()] + "**" + fighter1[4] + "**"
    name2 = spiritEmoji[spirit2.lower()] + "**" + fighter2[4] + "**"
    level1 = int(fighter1[2])
    level2 = int(fighter2[2])
    statArr1 = spiritStats[spirit1]
    statArr2 = spiritStats[spirit2]
    modifier1 = 1.0 + (0.02 * level1)
    modifier2 = 1.0 + (0.02 * level2)
    p_modifier1 = 1 + (int(fighter1[7]) * 0.1)
    p_modifier2 = 1 + (int(fighter2[7]) * 0.1)
    t_modifiers1 = talismanBoosts[fighter1[9]]
    t_modifiers2 = talismanBoosts[fighter2[9]]
    stats1 = []
    stats2 = []
    for i in range(3):
        stats1.append(round(statArr1[i] * t_modifiers1[i] * modifier1 * p_modifier1))
        stats2.append(round(statArr2[i] * t_modifiers2[i] * modifier2 * p_modifier2))
    stats1.append(round(statArr1[3] * t_modifiers1[3]))
    stats2.append(round(statArr2[3] * t_modifiers2[3]))
    turn = 0
    await hpcounter.edit(content="**Turn " + str(turn) + "**\n" + name1 + " HP: " + str(
        round(stats1[0])) + " | " + name2 + " HP: " + str(round(stats2[0])))
    file = open("enablesmite.txt", "r")
    smiting = file.read()
    file.close()
    while stats1[0] > 0 and stats2[0] > 0:
        if turn > 50:
            await ctx.send("Duel exceeded 50 turns, resulted in a stalemate.")
            return
        elif turn % 2 == 0:
            move = choice(spiritMoves[spirit1])
            if fighter1[0] == str(bot.owner_id) and smiting == "ON":
                move = "Developer's Smite"
            await message.edit(content="> " + name1 + " uses **" + move + "** on " + name2 + "!\n> -")
            sleep(0.25)
            calculation = stats2[3] - (level1 - level2)
            if randint(1, 100) <= calculation:
                await message.edit(
                    content="> " + name1 + " uses **" + move + "** on " + name2 + "!\n> " + name2 + " evades the attack!")
            else:
                damage = round(
                    randint(round(stats1[1] * 0.9 * moveDamage[move]), round(stats1[1] * 1.1 * moveDamage[move])) -
                    stats2[2])
                if damage < 1:
                    damage = 1
                await message.edit(content="> " + name1 + " uses **" + move + "** on " + name2 + "!\n> " + name2 + " takes " +
                                           str(damage) + " damage!")
                stats2[0] = round(stats2[0] - damage)
                if stats2[0] < 0:
                    stats2[0] = 0
        elif turn % 2 == 1:
            move = choice(spiritMoves[spirit2])
            if fighter2[0] == str(bot.owner_id) and smiting == "ON":
                move = "Developer's Smite"
            await message.edit(content="> " + name2 + " uses **" + move + "** on " + name1 + "!\n> -")
            sleep(0.25)
            calculation = stats1[3] - (level2 - level1)
            if randint(1, 100) <= calculation:
                await message.edit(
                    content="> " + name2 + " uses **" + move + "** on " + name1 + "!\n> " + name1 + " evades the attack!")
            else:
                damage = round(
                    randint(round(stats2[1] * 0.9 * moveDamage[move]), round(stats2[1] * 1.1 * moveDamage[move])) -
                    stats1[2])
                if damage < 1:
                    damage = 1
                await message.edit(content="> " + name2 + " uses **" + move + "** on " + name1 + "!\n> " + name1 + " takes " +
                                           str(damage) + " damage!")
                stats1[0] = round(stats1[0] - damage)
                if stats1[0] < 0:
                    stats1[0] = 0
        await hpcounter.edit(content="**Turn " + str(turn) + "**\n" + name1 + " HP: " + str(
            round(stats1[0])) + " | " + name2 + " HP: " + str(round(stats2[0])))
        #sleep(0.25)
        turn += 1
    if stats1[0] <= 0:
        winner = fighter2
        winnerid = int(fighter2[0])
    elif stats2[0] <= 0:
        winner = fighter1
        winnerid = int(fighter1[0])
    return winner, winnerid


@bot.command(name="set", description="Sets someone's data. <recipient> should be a mention. <value> is case sensitive."+
                                     "<datatype> needs to be one in this list: "+
                                     "[spirit, nickname, level, tokens, prestige, talisman] [ADMINISTRATOR ONLY]")
async def set(ctx, datatype, value, recipient="self"):
    if ctx.author.id != bot.owner_id and ctx.message.channel.id != 791393875800621068:
        await ctx.send(":x: You are not an administrator.")
        return
    if recipient == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    info = getinfo("info.txt", recipient)
    if info == -1:
        await ctx.send(":x: User **" + str(await bot.fetch_user(recipient)) + "** could not be found in the data files.")
        return
    validDTypes = ("spirit", "nickname", "level", "tokens", "prestige", "talisman")
    dtypeDict = {
        "spirit": 1,
        "nickname": 4,
        "level": 2,
        "tokens": 8,
        "prestige": 7,
        "talisman": 9,
    }
    if datatype.lower() not in validDTypes:
        await ctx.send(":x: Invalid data type. Refer to `jh!help set`.")
    info[dtypeDict[datatype.lower()]] = value
    updateinfo("info.txt", recipient, info)
    await ctx.send(":thumbsup: Successfully set **" + str(await bot.fetch_user(recipient)) + "**'s **"+datatype.lower()+"** to **"+value+"**.")


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
        original = "<@!"+str(ctx.author.id)+"> You rolled an " + spiritEmoji[spirit.lower()] + "**" + spirit + "**!"
    else:
        original = "<@!"+str(ctx.author.id)+"> You rolled a " + spiritEmoji[spirit.lower()] + "**" + spirit + "**!"
    message = await ctx.send(original)
    if getinfo("info.txt", ctx.author.id) == -1:
        adduser("info.txt", ctx.author.id, spirit)
    else:
        def check(reaction, user):
            return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message.id == message.id
        try:
            await message.edit(content=original+"\nDo you want to keep this spirit? React to this message to confirm.")
            await message.add_reaction("✅")
            reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
        except TimeoutError:
            await message.edit(content=original+"\n:x: Timed out.")
            return
        yourinfo = getinfo("info.txt", ctx.author.id)
        yourinfo[1] = spirit
        yourinfo[4] = spirit
        updateinfo("info.txt", ctx.author.id, yourinfo)
        await ctx.send(":thumbsup: You kept the spirit animal.")


@bot.command(name="summon", aliases=["summ"], description="Summons a random spirit animal, guaranteed to be rare or higher. Costs 50 tokens, though.")
@commands.cooldown(1, 300, commands.BucketType.user)
async def summon(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You do not have a spirit animal, and consequently, no tokens either. Roll one with `jh!rollspirit`.")
        return
    elif int(yourinfo[8]) < 50:
        await ctx.send(":x: You need **50**:diamond_shape_with_a_dot_inside: to summon. You currently have **"+yourinfo[8]+"**"+
                       ":diamond_shape_with_a_dot_inside:.")
        return
    message = await ctx.send("Do you really want to summon a spirit? This will cost you **50**:diamond_shape_with_a_dot_inside:. React to confirm.")
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message.id == message.id
    try:
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except TimeoutError:
        await message.edit(content=original+"\n:x: Timed out.")
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
    message = await ctx.send(text)
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[8] = str(int(yourinfo[8]) - 50)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    try:
        await message.edit(content=text+"\nDo you want to keep this summon? React to this message to confirm.")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except TimeoutError:
        await message.edit(content=text+"\n:x: Timed out.")
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    yourinfo[1] = spirit
    yourinfo[4] = spirit
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send(":thumbsup: You kept the summon.")


@bot.command(name="spirit", aliases=["sp", "profile"], description="Shows <recipient>'s spirit animal and its statistics."+
                                                                   "If no <recipient> is specified, it will show your spirit animal.")
async def spirit(ctx, recipient="self"):
    if recipient.lower() == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    userinfo = getinfo("info.txt", recipient)
    if userinfo == -1 and recipient == ctx.author.id:
        await ctx.send(":x: You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    elif userinfo == -1:
        await ctx.send(":x: Invalid recipient. Either they don't have a spirit animal, or they're an invalid user.")
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
    await ctx.send(spiritEmoji[spirit.lower()] + "**"+nickname+"\n:shield:Guild: "+guild+"\n:label:Rank: "+
                   rank+"**\n>>> **Prestige:** "+userinfo[7]+"(+"+str(int(userinfo[7])*10)+"% boost)\n**Level:** "
                   +str(level)+"/"+str(100+(int(userinfo[7])*100))+"\n**EXP:** " +str(exp)+"/" +expgoal+"\n**HP:** "+
                   str(stats[0])+"\n**ATK:** "+str(stats[1])+"\n**DEF:** "+str(stats[2])+"\n**EVA:** "+str(stats[3]))


@bot.command(name="shop", description="Shop to show talismans that can be bought with your tokens.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def shop(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send("You need a spirit animal to access the shop. Roll one with `jh!rollspirit`.")
        return
    outputdata  =  "**"+str(await bot.fetch_user(ctx.author.id))+"'s Equipment**\n"+\
                   "> Equipped Talisman: **"+yourinfo[9]+"**\n"+\
                   "> Tokens: **"+yourinfo[8]+"**:diamond_shape_with_a_dot_inside:\n"+\
                   "**Talismans Available:**\n"
    for i in range(7):
        t = shopTalismans[i]
        outputdata += "> ("+str(i+1)+")"+t+" "+talismanInfo[t]+" Price: **"+str(talismanPrices[t])+"**:diamond_shape_with_a_dot_inside:\n"
    outputdata += "`jh!buy <talisman_number>` to buy a talisman."
    await ctx.send(outputdata)


@bot.command(name="buy", description="Buy a talisman. This will replace your current talisman.")
async def buy(ctx, talisman_number):
    talisman_number = int(talisman_number)
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal to purchase talismans. Roll one using the `jh!rollspirit` command.")
        return
    if talisman_number <= 7 and talisman_number >= 1 and talismanIDs[talisman_number] != yourinfo[9]:
        if int(yourinfo[8]) >= talismanPrices[talismanIDs[talisman_number]]:
            yourinfo[8] = str(int(yourinfo[8])-talismanPrices[talismanIDs[talisman_number]])
            yourinfo[9] = talismanIDs[talisman_number]
            updateinfo("info.txt", ctx.author.id, yourinfo)
            await ctx.send(":thumbsup: You bought the **"+talismanIDs[talisman_number]+"**.")
        else:
            await ctx.send(":x: You do not have enough to buy this talisman. You need **"+
                           str(talismanPrices[talismanIDs[talisman_number]])+"**:diamond_shape_with_a_dot_inside:.")
    elif talismanIDs[talisman_number] == yourinfo[9]:
        await ctx.send(":x: You can't buy a talisman that you already own.")
    else:
        await ctx.send(":x: That talisman is not available in the shop.")


@bot.command(name="inventory", aliases=["inv", "balance", "bal"], description="Shows your equipped talisman, tokens, and spirit.")
async def inventory(ctx, recipient="self"):
    if recipient == "self":
        recipient = ctx.author.id
    else:
        recipient = ctx.message.mentions[0].id
    info = getinfo("info.txt", recipient)
    if info == -1 and recipient == ctx.author.id:
        await ctx.send(":x: You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    elif info == -1:
        await ctx.send(":x: Invalid user. They do not have a spirit animal.")
        return
    await ctx.send("**"+str(await bot.fetch_user(recipient))+"'s Inventory/Equipment**\n>>> "+
                   "Spirit Animal: " + spiritEmoji[info[1].lower()] + "**"+info[4]+"**\n"+
                   "Equipped Talisman: **"+info[9]+"**"+talismanInfo[info[9]]+"\n"+
                   "Tokens: **"+info[8]+"**:diamond_shape_with_a_dot_inside:")


@bot.command(name="donate", aliases=["give", "pay"], description="Gives some of your tokens to someone else.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def donate(ctx, amount, recipient):
    recipient = ctx.message.mentions[0].id
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You do not have a spirit animal! Roll one using the `jh!rollspirit` command!")
        return
    theirinfo = getinfo("info.txt", recipient)
    if theirinfo == -1:
        await ctx.send(":x: You cannot donate to someone who does not have a spirit animal. Tell them to roll one using the `jh!rollspirit` command.")
        return
    elif int(yourinfo[8]) < int(amount):
        await ctx.send(":x: You do not have that many tokens!")
        return
    elif int(amount) < 0:
        await ctx.send(":x: nooo!! you can't just donate a negative number!")
        return
    elif recipient == ctx.author.id:
        await ctx.send(":x: You can't donate to yourself!")
        return
    yourinfo[8] = str(int(yourinfo[8])-int(amount))
    theirinfo[8] = str(int(theirinfo[8])+int(amount))
    updateinfo("info.txt", ctx.author.id, yourinfo)
    updateinfo("info.txt", recipient, theirinfo)
    await ctx.send(":thumbsup: Successfully gave **"+amount+"**:diamond_shape_with_a_dot_inside: to **"+str(await bot.fetch_user(recipient))+"**. "+
                   "You now have **"+yourinfo[8]+"**:diamond_shape_with_a_dot_inside:, they now have **"+theirinfo[8]+"**:diamond_shape_with_a_dot_inside:.")


@bot.command(name="trade", aliases=["spirittrade", "strade"], description="Trade your spirit animal to someone else. You will keep your level though.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def trade(ctx, recipient):
    recipient = ctx.message.mentions[0].id
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    if yourinfo == -1 or theirinfo == -1:
        await ctx.send(":x: Both of you need a spirit animal to trade. Roll one with `jh!rollspirit`.")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        message = await ctx.send(":arrow_forward:**SPIRIT TRADE**:arrow_backward:\n"+
                                 "<@"+str(recipient)+">, react to this message to accept the trade request. You will both keep your levels.")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send(":x: Trade request timed out, they didn't confirm.")
        return
    swapspirits("info.txt", ctx.author.id, recipient)
    await ctx.send(":thumbsup: The trade was successful.")


@bot.command(name="ttrade", aliases=["talismantrade", "talistrade"], description="Trade your talisman to someone else. You will keep your spirit though.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ttrade(ctx, recipient):
    recipient = ctx.message.mentions[0].id
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    if yourinfo == -1 or theirinfo == -1:
        await ctx.send(":x: Both of you need a talisman, and by extension, a spirit animal to trade. Roll one with `jh!rollspirit`.")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        message = await ctx.send(":arrow_forward:**TALISMAN TRADE**:arrow_backward:\n"+
                                 "<@"+str(recipient)+">, react to this message to accept the trade request. You will both keep your spirits.")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send(":x: Trade request timed out, they didn't confirm.")
        return
    swaptalismans("info.txt", ctx.author.id, recipient)
    await ctx.send(":thumbsup: The trade was successful.")


@bot.command(name="prestige", description="Sacrifice your current levels to increase your level cap by 100. Requires level 100.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def prestige(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal to prestige. Roll one with `jh!rollspirit`.")
        return
    elif int(yourinfo[2]) < 100+int(yourinfo[7])*100:
        await ctx.send(":x: You have to be at least level "+str(100+int(yourinfo[7])*100)+" to prestige.")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == ctx.author.id and reaction.message == message
    try:
        message = await ctx.send(":trident: **PRESTIGE** :trident:\n"
                                 "<@"+str(ctx.author.id)+">, react to this message to prestige. This will reset your level, but raise your level cap by **100**, "+
                                 "and grant you **50**:diamond_shape_with_a_dot_inside:.")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send(":x: Prestige request timed out, you didn't confirm.")
        return
    yourinfo[7] = str(int(yourinfo[7])+1)
    yourinfo[2] = str(0)
    yourinfo[3] = str(0)
    yourinfo[8] = str(int(yourinfo[8])+50)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send(":trident: **You have prestiged. You are now level 0, but your level cap has increased by 100.**")


@bot.command(name="train", description="Train your spirit animal against wild animals.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def train(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal to train! Roll one using the `jh!rollspirit` command!")
        return
    animal = choice(commonSpirits)
    enemyLevel = int(yourinfo[2]) - randint(10, 20)
    enemyInfo = ["-1", animal, str(enemyLevel), "0", animal, "None", "None", "0", "0", "None"]
    winner, winnerid = await spiritduel(ctx, yourinfo, enemyInfo, "train")
    spirit = yourinfo[1]
    nickname = yourinfo[4]
    if winner == enemyInfo:
        await ctx.send("Your " + spiritEmoji[spirit.lower()] + "**" + nickname + "** was defeated.")
        return
    oldexp = int(yourinfo[3])
    level = int(yourinfo[2])
    oldlevel = level
    exp = round(randint(1500+level*30, 3000+level*60)*expmultiplier)
    newexp = oldexp + exp
    await ctx.send("Your " + spiritEmoji[spirit.lower()] + "**" + nickname + "** beats up a wild " + spiritEmoji[animal.lower()] + "" + animal + " and gains **"
                   + str(exp) + " experience!**")
    tokengain = 0
    while newexp >= 1000+level*100 and level < 100+(int(yourinfo[7])*100):
        newexp -= 1000+level*100
        level += 1
        tokengain += 1
    if level != oldlevel:
        await ctx.send("Your " + spiritEmoji[spirit.lower()] + "**" + nickname + "** leveled up! It is now level **" + str(level) + "**. "+
                       "You also earned **"+str(tokengain)+"**:diamond_shape_with_a_dot_inside:.")
    yourinfo[2] = str(level)
    yourinfo[3] = str(newexp)
    yourinfo[8] = str(int(yourinfo[8])+tokengain)
    updateinfo("info.txt", ctx.author.id, yourinfo)


@bot.command(name="interactivetrain", aliases=["itrain"], description="Interactively train your spirit animal by focusing. Gives more experience. "+
                                                                      "Can only be used in DMs.")
@commands.cooldown(1, 120, commands.BucketType.user)
async def interactivetrain(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal to train! Roll one using the `jh!rollspirit` command!")
        return
    elif ctx.message.guild != None:
        await ctx.send(":x: This command can only be used in DMs to prevent the messages from colliding!")
        return
    await ctx.send(":watch: Focus. There is a time limit, and there will be three rounds. Choose the correct reaction each round, or you will fail.\n"+
                   "Do not react while the reactions are being added by the bot.")
    sleep(3)
    correctReaction = ""
    indicators = ["🇦", "🇧", "🇨", "🇩", "🇪"]
    def check(reaction, user):
        return str(reaction.emoji) == correctReaction and user.id == ctx.author.id and reaction.message == message
    for trainround in range(3):
        correctReaction = choice(indicators)
        try:
            message = await ctx.send("**ROUND " + str(trainround + 1) + ":** React to this message with a " + correctReaction + "!")
            shuffle(indicators)
            for e in indicators:
                await message.add_reaction(e)
            reaction, user = await bot.wait_for('reaction_add', timeout=3.5, check=check)
        except TimeoutError:
            await ctx.send(":x: You failed the training session.")
            return
    tokengain = 0
    level = int(yourinfo[2])
    oldlevel = level
    exp = round(randint(4500 + level * 90, 9000 + level * 180)*expmultiplier)
    newexp = int(yourinfo[3]) + exp
    while newexp >= 1000+level*100 and level < 100+(int(yourinfo[7])*100):
        newexp -= 1000+level*100
        level += 1
        tokengain += 1
    yourinfo[3] = str(newexp)
    yourinfo[2] = str(level)
    yourinfo[8] = str(int(yourinfo[8])+tokengain)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send("You completed the interactive training and earned **"+str(exp)+" experience!**")
    if level != oldlevel:
        await ctx.send("Your " + spiritEmoji[yourinfo[1].lower()] + "**" + yourinfo[4] + "** leveled up! It is now level **" + str(level) + "**. " +
                       "You also earned **" + str(tokengain) + "**:diamond_shape_with_a_dot_inside:.")


@bot.command(name="search", aliases=["scout"], description="Search the ruins for spirit-boosting artifacts. You might find something special...")
@commands.cooldown(1, 240, commands.BucketType.user)
async def search(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal to search! Roll one using the `jh!rollspirit` command!")
        return
    spirit = yourinfo[1]
    nickname = yourinfo[4]
    level = int(yourinfo[2])
    await ctx.send("Your " + spiritEmoji[spirit.lower()] + "**" + nickname + "** searches for artifacts in the ruins.")
    message = await ctx.send("Searching...")
    sleep(randint(2, 4))
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
    if artifact == "None":
        await message.edit(content=spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with nothing.")
        return
    term = "a"
    if artifact[0].lower() in ("a", "e", "i", "o", "u"):
        term = "an"
    if artifact not in commonSearchableTalismans and artifact not in rareSearchableTalismans and artifact != "Easter Egg":
        levelcap = 100+(int(yourinfo[7])*100)
        if level < levelcap:
            oldlevel = level
            level += round(randint(artifactLevels[artifact][0], artifactLevels[artifact][1])*expmultiplier)
            tokengain = level-oldlevel
            if level > levelcap:
                level = levelcap
            yourinfo[2] = str(level)
            yourinfo[8] = str(int(yourinfo[8])+tokengain)
            updateinfo("info.txt", ctx.author.id, yourinfo)
            await message.edit(content=spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with " + term + " " +
                                       artifactEmojis[artifact] + "**" + artifact + "**!\nThe " +
                                       artifactEmojis[artifact] + "**" + artifact + "** boosts your spirit's level to **"
                                       + str(level) + "**. You also earned **"+str(tokengain)+"**:diamond_shape_with_a_dot_inside:.")
        else:
            await message.edit(content=spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with a " +
                                       artifactEmojis[artifact] + "**" + artifact + "**!")
    else:
        await message.edit(content=spiritEmoji[spirit.lower()] + "**" + nickname + "** comes back with " + term + " **" +
                                   artifact+"**! Stats: "+talismanInfo[artifact]+"\nWould you like to keep this talisman? It will replace your current one. "+
                                   "You can also sell it for **"+str(tsellPrices[ttype])+"**:diamond_shape_with_a_dot_inside:.\n"+
                                   "React with ✅ to keep and 💠 to sell.")
        def check(reaction, user):
            return str(reaction.emoji) in ["✅", "💠"] and user.id == ctx.author.id and reaction.message == message
        try:
            await message.add_reaction("✅")
            await message.add_reaction("💠")
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                yourinfo = getinfo("info.txt", ctx.author.id)
                yourinfo[9] = artifact
                updateinfo("info.txt", ctx.author.id, yourinfo)
                await ctx.send(":thumbsup: You kept the **" + artifact + "**.")
            elif str(reaction.emoji) == "💠":
                yourinfo = getinfo("info.txt", ctx.author.id)
                yourinfo[8] = str(int(yourinfo[8]) + tsellPrices[ttype])
                updateinfo("info.txt", ctx.author.id, yourinfo)
                await ctx.send(":thumbsup: You sold the **" + artifact + "** for **" + str(
                    tsellPrices[ttype]) + "**:diamond_shape_with_a_dot_inside:.")
        except TimeoutError:
            await ctx.send(":x: You left the talisman.")
            return


@bot.command(name="nickname", aliases=["nick", "rename"], description="Nickname your spirit animal! You can rename it anytime.")
async def nickname(ctx, *, new_nick):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal! Roll one with the `jh!rollspirit` command!")
        return
    elif len(new_nick) <= 18:
        for c in new_nick:
            if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ":
                await ctx.send(":x: Your spirit animal's nickname can only contain letters and spaces!")
                return
    else:
        await ctx.send(":x: Your spirit animal's nickname cannot exceed 18 characters in length!")
        return
    yourinfo[4] = new_nick
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send(":thumbsup: Successfully renamed your spirit animal.")


@bot.command(name="leaderboard", aliases=["lb", "top"], description="Shows a leaderboard with the top users of the bot, by spirit level.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def leaderboard(ctx):
    file = open("info.txt", "r")
    lines = file.readlines()
    file.close()
    infodict = {}
    for line in lines:
        info = eval(line[:len(line) - 1])
        infodict.update({int(info[0]): int(info[2])})
    idarr = sorted(infodict, key=infodict.get)
    idarr = idarr[::-1]
    counter = 0
    outputdata = ""
    for userid in idarr:
        if counter >= 10:
            break
        outputdata += str(counter+1)+". :medal:"+str(await bot.fetch_user(userid))+" - **Level "+str(infodict[userid])+"**\n"
        counter += 1
    await ctx.send(outputdata)


@bot.command(name="pleaderboard", aliases=["plb", "ptop"], description="Shows a leaderboard with the top users of the bot, by prestige.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def pleaderboard(ctx):
    file = open("info.txt", "r")
    lines = file.readlines()
    file.close()
    infodict = {}
    for line in lines:
        info = eval(line[:len(line) - 1])
        infodict.update({int(info[0]): int(info[7])})
    idarr = sorted(infodict, key=infodict.get)
    idarr = idarr[::-1]
    counter = 0
    outputdata = ""
    for userid in idarr:
        if counter >= 10:
            break
        outputdata += str(counter+1)+". :medal:"+str(await bot.fetch_user(userid))+" - **Prestige "+str(infodict[userid])+"**\n"
        counter += 1
    await ctx.send(outputdata)


@bot.command(name="richest", aliases=["rich"], description="Shows a leaderboard with the top users of the bot, by amount of tokens.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def richest(ctx):
    file = open("info.txt", "r")
    lines = file.readlines()
    file.close()
    infodict = {}
    for line in lines:
        info = eval(line[:len(line) - 1])
        infodict.update({int(info[0]): int(info[8])})
    idarr = sorted(infodict, key=infodict.get)
    idarr = idarr[::-1]
    counter = 0
    outputdata = ""
    for userid in idarr:
        if counter >= 10:
            break
        outputdata += str(counter+1)+". :medal:"+str(await bot.fetch_user(userid))+" - **"+str(infodict[userid])+"**:diamond_shape_with_a_dot_inside:\n"
        counter += 1
    await ctx.send(outputdata)


@bot.command(name="duel", aliases=["battle"], description="Duel another player! Both players must have a spirit animal.")
@commands.cooldown(1, 45, commands.BucketType.user)
async def duel(ctx, recipient):
    recipient = ctx.message.mentions[0].id
    if getinfo("info.txt", ctx.author.id) == -1 or getinfo("info.txt", recipient) == -1:
        await ctx.send(":x: At least one of you does not have a spirit animal! One of you needs to roll one with `jh!rollspirit`.")
        return
    elif recipient == ctx.author.id:
        await ctx.send(":x: You cannot duel yourself!")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        message = await ctx.send(":crossed_swords:**DUEL**:crossed_swords:\n<@"+str(recipient)+">, react to this message to accept the duel invitation!")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send(":x: Duel request timed out, recipient did not accept.")
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    winner, winnerid = await spiritduel(ctx, yourinfo, theirinfo, "duel")
    await ctx.send("**" + str(await bot.fetch_user(winnerid)) + "'s** " + winner[4] + " is victorious! :trophy: "+
                   "**+1**:diamond_shape_with_a_dot_inside:")
    winner[8] = str(int(winner[8])+1)
    updateinfo("info.txt", winnerid, winner)


@bot.command(name="wagerduel", aliases=["wagerbattle", "wduel", "wbattle"], description="Duel another player! Both players must have a spirit animal "+
                                                                                        "and at least <betAmount> tokens.")
@commands.cooldown(1, 45, commands.BucketType.user)
async def wagerduel(ctx, recipient, betAmount):
    recipient = ctx.message.mentions[0].id
    betAmount = int(betAmount)
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    if getinfo("info.txt", ctx.author.id) == -1 or getinfo("info.txt", recipient) == -1:
        await ctx.send(":x: At least one of you does not have a spirit animal! One of you needs to roll one with `jh!rollspirit`.")
        return
    elif recipient == ctx.author.id:
        await ctx.send(":x: You cannot duel yourself!")
        return
    elif int(yourinfo[8]) < betAmount or int(theirinfo[8]) < betAmount:
        await ctx.send(":x: Both of you must have at least **" + str(betAmount) + "**:diamond_shape_with_a_dot_inside:!")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == recipient and reaction.message == message
    try:
        message = await ctx.send(":crossed_swords:**WAGER DUEL**:crossed_swords:\n" +
                                 "<@"+str(recipient)+">, react to this message to accept the duel invitation!\n"+
                                 "The winner will gain **" + str(betAmount) + "**:diamond_shape_with_a_dot_inside: from the loser.")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send(":x: Duel request timed out, recipient did not accept.")
        return
    yourinfo = getinfo("info.txt", ctx.author.id)
    theirinfo = getinfo("info.txt", recipient)
    winner, winnerid = await spiritduel(ctx, yourinfo, theirinfo, "wager duel")
    winner[8] = str(int(winner[8])+betAmount)
    if winnerid != recipient:
        loser = getinfo("info.txt", recipient)
        loser[8] = str(int(loser[8])-betAmount)
    else:
        loser = getinfo("info.txt", ctx.author.id)
        loser[8] = str(int(loser[8]) - betAmount)
    if int(loser[8]) < 0:
        difference = 0 - int(loser[8])
        loser[8] = "0"
        winner[8] = str(int(winner[8])-difference)
    await ctx.send("**" + str(await bot.fetch_user(winnerid)) + "'s** " + winner[4] + " is victorious! :trophy: " +
                   "**+" + str(betAmount) + "**:diamond_shape_with_a_dot_inside:")
    updateinfo("info.txt", winnerid, winner)
    updateinfo("info.txt", int(loser[0]), loser)


@bot.command(name="createguild", aliases=["cguild"], description="Create a guild!")
async def createguild(ctx, *, name):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal in order to create a guild! Roll one with `jh!rollspirit`!")
        return
    if name[0] == '"' and name[len(name)-1] == '"':
        name = name[1:-1]
    if yourinfo[5] != "None":
        await ctx.send(":x: You cannot create a guild if you already have one! You can disband it with `jh!disband`, or leave it with `jh!leave`.")
        return
    elif len(name) > 20:
        await ctx.send(":x: Your guild name cannot exceed 20 characters in length!")
        return
    elif len(name) < 3:
        await ctx.send(":x: Your guild name has to be at least 3 characters long!")
        return
    for c in name:
        if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ":
            await ctx.send(":x: Your guild name can only contain letters and spaces!")
            return
    samename = False
    file = open("guildnames.txt", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        if name == line[:-1]:
            samename = True
            break
    if samename:
        await ctx.send(":x: The name you chose is already taken!")
        return
    yourinfo[5] = name
    yourinfo[6] = "Leader"
    updateinfo("info.txt", ctx.author.id, yourinfo)
    file = open("guildnames.txt", "a")
    file.write(name + "\n")
    file.close()
    await ctx.send("Successfully created guild **" + name + "**.")


@bot.command(name="guild", description="View the statistics of your guild. Requires access to your DMs, or it won't work.")
async def guild(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You do not have a spirit animal, and by extension, do not have a guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await ctx.send(":x: You do not have a guild.")
        return
    guildname = yourinfo[5]
    totalLevel = 0
    memberCount = 0
    file = open("info.txt", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        info = eval(line[:len(line) - 1])
        if info[5] == guildname:
            totalLevel += int(info[2])
            memberCount += 1
    await ctx.send(":shield: **"+guildname+"** :shield:\n> **Total Level:** "+str(totalLevel)+"\n> **Members:** "+str(memberCount))

@bot.command(name="guild-list", aliases=["glist", "g-list"], description="Get a full list of the members of your guild. Requires access to your DMs.")
async def guildlist(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You do not have a spirit animal, and by extension, do not have a guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await ctx.send(":x: You do not have a guild.")
        return
    file = open("info.txt", "r")
    lines = file.readlines()
    file.close()
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
        await user.send(outputdata)
        await ctx.send("Successfully sent you a DM with member info!")
    except:
        await ctx.send(":x: DM could not be sent. Make sure the bot has permission to DM you.")


@bot.command(name="disband", description="Disband your guild.")
async def disband(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You do not have a spirit animal, and by extension, no guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await ctx.send(":x: You cannot disband a guild if you don't have one!")
        return
    elif yourinfo[6] != "Leader":
        await ctx.send(":x: Only the leader can disband a guild!")
        return
    guildname = yourinfo[5]
    file = open("info.txt", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        info = eval(line[:len(line) - 1])
        if info[5] == guildname:
            info[5] = "None"
            info[6] = "None"
        updateinfo("info.txt", int(info[0]), info)
    file = open("guildnames.txt", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        if line == guildname+"\n":
            lines.remove(line)
    file = open("guildnames.txt", "w")
    file.write("".join(lines))
    file.close()
    await ctx.send("**"+guildname+"** has been disbanded. Goodbye.")


@bot.command(name="invite", description="Invite another player to your guild! <playername> should be a mention.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx, playername):
    inviter = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    invitee = getinfo("info.txt", playerid)
    if inviter == -1 or invitee == -1:
        await ctx.send(":x: One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif inviter[5] == "None":
        await ctx.send(":x: You cannot invite a player to your guild if you don't have a guild!")
        return
    elif inviter[6] not in ["Leader", "Recruiter"]:
        await ctx.send(":x: You cannot invite a player to your guild if you aren't the leader or a recruiter!")
        return
    elif invitee[5] != "None":
        await ctx.send(":x: You cannot invite a player that is already in a guild!")
        return
    message = None
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user.id == playerid and reaction.message == message
    try:
        message = await ctx.send("<@"+str(playerid)+">, react to this message to accept the guild invitation!")
        await message.add_reaction("✅")
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send(":x: Invite request timed out, recipient did not accept.")
        return
    invitee[5] = inviter[5]
    invitee[6] = "Member"
    updateinfo("info.txt", playerid, invitee)
    await ctx.send("**"+str(await bot.fetch_user(playerid))+"** has joined **"+inviter[5]+"**!")


@bot.command(name="kick", description="Kick a player out of your guild. <playername> should be a mention.")
async def kick(ctx, playername):
    kicker = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    kickee = getinfo("info.txt", playerid)
    if kicker == -1 or kickee == -1:
        await ctx.send(":x: One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif kicker[5] == "None":
        await ctx.send(":x: You cannot kick a player if you don't have a guild!")
        return
    elif kicker[6] != "Leader":
        await ctx.send(":x: You cannot kick a member of your guild if you aren't the leader!")
        return
    elif kicker[5] != kickee[5]:
        await ctx.send(":x: You cannot kick a player that isn't in your guild!")
        return
    kickee[5] = "None"
    kickee[6] = "None"
    updateinfo("info.txt", playerid, kickee)
    await ctx.send("**"+str(await bot.fetch_user(playerid))+"** has been kicked from your guild.")


@bot.command(name="leave", description="Leave your guild.")
async def leave(ctx):
    yourinfo = getinfo("info.txt", ctx.author.id)
    if yourinfo == -1:
        await ctx.send(":x: You do not have a spirit animal, and by extension, no guild either. Roll one with `jh!rollspirit`.")
        return
    elif yourinfo[5] == "None":
        await ctx.send(":x: You cannot leave a guild if you don't have one!")
        return
    elif yourinfo[6] == "Leader":
        await disband.invoke(ctx)
        return
    guildname = yourinfo[5]
    yourinfo[5] = "None"
    yourinfo[6] = "None"
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send("You have left **"+guildname+"**.")


@bot.command(name="promote", description="Promote a player in your guild!")
async def promote(ctx, playername):
    promoter = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    promotee = getinfo("info.txt", playerid)
    if promoter == -1 or promotee == -1:
        await ctx.send(":x: One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif promoter[5] == "None":
        await ctx.send(":x: You cannot promote a player if you don't have a guild!")
        return
    elif promoter[6] != "Leader":
        await ctx.send(":x: You cannot promote a player in your guild if you aren't the leader!")
        return
    elif promoter[5] != promotee[5]:
        await ctx.send(":x: You cannot promote a player that isn't in your guild!")
        return
    elif promotee[6] not in ["Member", "Elite"]:
        await ctx.send(":x: You cannot promote this player!")
        return
    if promotee[6] == "Member":
        promotee[6] = "Elite"
    else:
        promotee[6] = "Recruiter"
    updateinfo("info.txt", playerid, promotee)
    await ctx.send("Successfully promoted **"+str(await bot.fetch_user(playerid))+"** to **" + promotee[6] + "**!")


@bot.command(name="demote", description="Demote a player in your guild.")
async def demote(ctx, playername):
    demoter = getinfo("info.txt", ctx.author.id)
    playerid = ctx.message.mentions[0].id
    demotee = getinfo("info.txt", playerid)
    if demoter == -1 or demotee == -1:
        await ctx.send(":x: One of you does not have a spirit animal. Roll one with `jh!rollspirit`.")
        return
    elif demoter[5] == "None":
        await ctx.send(":x: You cannot demote a player if you don't have a guild!")
        return
    elif demoter[6] != "Leader":
        await ctx.send(":x: You cannot demote a player in your guild if you aren't the leader!")
        return
    elif demoter[5] != demotee[5]:
        await ctx.send(":x: You cannot demote a player that isn't in your guild!")
        return
    elif demotee[6] not in ["Elite", "Recruiter"]:
        await ctx.send(":x: You cannot demote this player!")
        return
    if demotee[6] == "Recruiter":
        demotee[6] = "Elite"
    else:
        demotee[6] = "Member"
    updateinfo("info.txt", playerid, demotee)
    await ctx.send("Successfully demoted **"+str(await bot.fetch_user(playerid))+"** to **" + demotee[6] + "**.")


@bot.command(name="smite", description="Owner exclusive command. Sets Developer's Smite to ON or OFF.")
async def smite(ctx, setting):
    if ctx.author.id != bot.owner_id:
        await ctx.send(":x: Fool. Only the owner of this bot can use this command.")
        return
    elif setting not in ["ON", "OFF"]:
        await ctx.send(":x: ON and OFF only supported.")
        return
    file = open("enablesmite.txt", "w")
    file.write(setting)
    file.close()
    await ctx.send(":zap: **Developer's Smite** has been set to **"+setting+"** for **"+str(await bot.fetch_user(bot.owner_id))+"**.")


@bot.command(name="coinflip", aliases=["coin", "flip"], description="Flip a coin. Double or nothing.")
@commands.cooldown(1, 5, commands.BucketType.user)
async def coinflip(ctx, amount, prediction):
    yourinfo = getinfo("info.txt", ctx.author.id)
    amount = int(amount)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal in order to gamble. Roll one with `jh!rollspirit`.")
        return
    elif prediction.lower() not in ["heads", "tails"]:
        await ctx.send(":x: Your prediction needs to be heads or tails!")
        return
    elif amount > int(yourinfo[8]):
        await ctx.send(":x: You don't have that much!")
        return
    elif amount < 1:
        await ctx.send(":x: You have to bet at least **1**:diamond_shape_with_a_dot_inside:!")
        return
    flip = choice(["heads", "tails"])
    content = ":coin: The coin landed on **"+flip.upper()+"**!\n"
    if flip == prediction.lower():
        content += "You won **"+str(amount)+"**:diamond_shape_with_a_dot_inside:!"
        yourinfo[8] = str(int(yourinfo[8])+amount)
    else:
        content += "You lost **"+str(amount)+"**:diamond_shape_with_a_dot_inside:..."
        yourinfo[8] = str(int(yourinfo[8])-amount)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send(content)


@bot.command(name="bet", description="Bet your money on guessing a number. The number will be randomly chosen from 1 to <max>. "+
                                     "<max> has to be at least 3, and cannot exceed 64.")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bet(ctx, amount, max, prediction):
    yourinfo = getinfo("info.txt", ctx.author.id)
    amount = int(amount)
    prediction = int(prediction)
    max = int(max)
    if yourinfo == -1:
        await ctx.send(":x: You need a spirit animal in order to gamble. Roll one with `jh!rollspirit`.")
        return
    elif amount > int(yourinfo[8]):
        await ctx.send(":x: You don't have that much!")
        return
    elif amount < 1:
        await ctx.send(":x: You have to bet at least **1**:diamond_shape_with_a_dot_inside:!")
        return
    elif max < 3 or max > 64:
        await ctx.send(":x: <max> has to be at least 3, and cannot exceed 64.")
        return
    elif prediction > max or prediction < 1:
        await ctx.send(":x: Your prediction needs to be between 1 and "+str(max)+"!")
        return
    number = randint(1, max)
    content = ":game_die: The die landed on **"+str(number)+"**!\n"
    if number == prediction:
        winamount = amount*(max-1)
        content += "You won **" + str(winamount) + "**:diamond_shape_with_a_dot_inside:!"
        yourinfo[8] = str(int(yourinfo[8]) + winamount)
    else:
        content += "You lost **" + str(amount) + "**:diamond_shape_with_a_dot_inside:..."
        yourinfo[8] = str(int(yourinfo[8]) - amount)
    updateinfo("info.txt", ctx.author.id, yourinfo)
    await ctx.send(content)


@bot.command(name="credits", description="Shows the credits of the bot.")
@commands.cooldown(1, 10, commands.BucketType.channel)
async def credits(ctx):
    await ctx.send(":panda_face:**Jhi#4308**\nA small game bot centered around spirit animals.\n"+
                   ":fire:Created by ||TheDysfunctionalDragon||#6910:fire:\n"+
                   ":sparkles:With help from the following beta testers::sparkles:\n"+
                   ">>> LaurelWyvern, Ghostie\nWingy, Jeffrier\nG0ld3n1i0nfac3, Raystro\nDarkMaster, Marshyy\n--Nico--, Pickle75\nD4rk, Overlord")


@credits.error
async def credits_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: As much as I hate to put a cooldown on credits, it fills up the chat. Try again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@rollspirit.error
async def roll_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot roll your spirit animal again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@summon.error
async def summ_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot summon a spirit again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@shop.error
async def shop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: The shop can be opened in this channel again in {:.2f}s. This is to prevent flooding.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@donate.error
async def donate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You can donate tokens again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@prestige.error
async def prestige_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot prestige again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@invite.error
async def invite_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot invite again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@trade.error
async def trade_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot spirit trade again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@ttrade.error
async def ttrade_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot talisman trade again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@duel.error
async def duel_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You cannot duel again for {:.2f}s!".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@train.error
async def train_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: Your spirit animal has gotten tired. You can train it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@interactivetrain.error
async def itrain_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: Your spirit animal has gotten tired. You can interactively train it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: Your spirit animal has gotten tired. You can have it search again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@leaderboard.error
async def leaderboard_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: There is a cooldown on leaderboard to prevent filling the chat too quickly. You can use it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@pleaderboard.error
async def pleaderboard_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: There is a cooldown on pleaderboard to prevent filling the chat too quickly. You can use it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@richest.error
async def richest_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: There is a cooldown on richest to prevent filling the chat too quickly. You can use it again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@coinflip.error
async def coinflip_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You can flip a coin again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@bet.error
async def bet_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ":x: You can roll a die again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@bot.command(name="ping", description="Get the current latency of the bot.")
async def ping(ctx):
    await ctx.send(":ping_pong: Pong! Latency: **"+str(round(bot.latency*1000, 2))+" ms**")


bot.run(TOKEN, bot=True, reconnect=True)