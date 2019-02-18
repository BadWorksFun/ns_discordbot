# Module Imports
import discord
from discord.ext import commands
import random
import json
from operator import itemgetter
import pandas as pd

# Scripts
import update_data
import labouring
import crafting
import char_inventory
import sleeping
import char_skilltree
import traveling
import eating
import char_stash
import building_menu
import using
import battling
import marketing

TOKEN = "NTM4MTEwMDM1NDQ0NjI5NTE2.DyvBzg.m9bifO4jlqDkSJ5oXMtm1yIBjco"
client = commands.Bot(command_prefix=".")
client.remove_command('help')


# On Ready
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Nathan's Server Game"))
    await client.send_message(discord.Object(id='541395172622073869'),
                              "Nathan's Game Bot is online!")
    print("Bot is online!")

    # Reset Stuff
    with open("users.json", "r") as f:
        users = json.load(f)

    # Reset in_combat Flag
    for user_ in users:
        users[user_]["in_combat"] = False


    with open("users.json", "w") as f:
        json.dump(users, f)


# Member Join
@client.event
async def on_member_join(member):
    # Rookie role for new members
    role = discord.utils.get(member.server.roles, name="Rookie")
    await client.add_roles(member, role)


# On Message & Auto Delete
@client.event
async def on_message(message):
    print(message.author.name)

    # Delete Nathan's GameBot Command Messages
    # if message.content.startswith("."):
    # async for log in client.logs_from(message.channel, limit=1):
    # if log.author == message.author:
    # await client.delete_message(log)

    # Message Experience
    with open("users.json", "r") as f:
        users = json.load(f)

    user = message.author
    if user.id in users:
        actions = 0.5
        await update_data.level_up(client, message.author, users, actions)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)

    # Process Commands
    await client.process_commands(message)


# Error Messages
@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.send_message(ctx.message.channel, content="This command is on a %.2fs cooldown."
                                                               % error.retry_after)

    elif isinstance(error, commands.CommandNotFound):
        user = ctx.message.author
        await client.send_message(ctx.message.channel, content="{}, this is no a valid command. Check your spelling!"
                                  .format(user.mention))

    raise error


# Account Check Fail
async def account_check(user):
    await client.say("{}, you don't have an account. Create one using the .create command to start playing!"
                     .format(user.mention))


# Channel Check
async def channel_check(user, channel_allowed):
    await client.say("{}, this is the wrong channel!\n"
                     "This command can be done primarily in #{}".format(user.mention, channel_allowed))


# Combat Check
async def combat_check(user):
    await client.say("{}, you are in combat, use .battle to start or .escape to attempt to flee!"
                     .format(user.mention))


# .help
@client.command(pass_context=True)
async def help(ctx, command=None):
    channel = ctx.message.channel
    help_menu = discord.Embed(colour=discord.Colour.orange())
    help_menu.set_author(name="Help")
    # Command Overview
    if command is None:
        help_menu.add_field(
            name="Command Overview (1)",
            value="**SETUP:**\n"
                  "**>** .allow: *Allows commands in channels (required for initial setup)*\n"
                  "**>** .create: *Creates a new account.*\n"
                  "**>** .reset: *Resets all your progress.*\n"
                  "**STATS:**\n"
                  "**>** .top: *Shows a list of players, sorted by name, level or cash.*\n"
                  "**>** .inventory: *Shows your inventory or stash.*\n"
                  "**>** .skilltree: *Shows your skills and progression.*\n"
                  "**BASE & CRAFT:**\n"
                  "**>** .stash: *Allows you to store stuff at and get stuff from your stash.*\n"
                  "**>** .build: *Used for building projects at base.*\n"
                  "**>** .craft: *Used to craft simple tools and armour.*\n"
                  "**>** .use: *Allows you to use items you've acquired at your base.*\n"
                  "**>** .market: *Used to buy and sell items.*\n",
            inline=False)
        help_menu.add_field(
            name="Command Overview (2)",
            value="**ON THE ROAD:**\n"
                  "**>** .labour: *Used to gather, lumber or mine for resources.*\n"
                  "**>** .eat: *Used to fill your nourishment meter.*\n"
                  "**>** .travel: *Used to travel to any location.*\n"
                  "**>** .sleep: *Used to regain Stamina & Travel Power.*\n"
                  "**BATTLES & DUNGEONS:**\n"
                  "**>** .battle: *Initiates a battle if you have enemies nearby.*\n"
                  "**>** .escape: *Attempts to escape if you have enemies nearby.*",
            inline=False)
    # Single Commands
    elif command == "help":
        help_menu.add_field(
            name="The 'Help' Command:",
            value="Seriously?!\n"
                  "Well, '.help' to see the help menu and '.help command' to see more info about a specific command... "
                  "Jeez...",
            inline=False)
    elif command == "Nathan" or command == "nathan":
        help_menu.add_field(
            name="The 'Nathan':",
            value="Your Lord and Saviour.",
            inline=False)
    elif command == "bug":
        help_menu.add_field(
            name="The 'Bug':",
            value="There are no bugs in this bot.",
            inline=False)
    elif command == "allow":
        help_menu.add_field(
            name="The 'Allow' Command:",
            value="*Allows all or certain commands in specific channels. Admins only!*\n"
                  "**>** __Usage__: .allow (.al) => Allows all commands in this channel. "
                  "This will assign all commands to this channel for slot 1!\n"
                  "**>** To allow a command in a specific channel: .allow command (inside the channel). "
                  "Only one channel per command using this method!\n"
                  "**>** To allow a command in multiple channels: .allow command 1-5 (choose a number). "
                  "Up to 5 channels per command using this method!",
            inline=False)
    elif command == "create":
        help_menu.add_field(
            name="The 'Create' Command:",
            value="*Creates a new account if don't have one yet.*\n"
                  "**>** __Usage__: .create (no aliases)\n"
                  "Confirm by typing 'yes' (no prefix, case sensitive)\n"
                  "Decline by typing 'no' to cancel (or wait long enough)",
            inline=False)
    elif command == "reset":
        help_menu.add_field(
            name="The 'Reset' Command:",
            value="*Resets all your progress. You'll start fresh.*\n"
                  "**>** __Usage__: .reset (no aliases)",
            inline=False)
    elif command == "top":
        help_menu.add_field(
            name="The 'Top' Command:",
            value="*Shows a list of players, sorted by name, level or cash.*\n"
                  "**>** __Usage__: .top (no aliases)\n"
                  "**>** Sort by Name: .top name page_number (opt: page number)\n"
                  "**>** Sort by level: .top level page_number (opt: page number)\n"
                  "**>** Sort by cash: .top cash page_number (opt: page number",
            inline=False)
    elif command == "inventory":
        help_menu.add_field(
            name="The 'Inventory' Command:",
            value="*Shows your inventory or stash.*\n"
                  "**>** __Usage__: .inventory (.inv / .i)\n"
                  "**>** To show your character inventory: .i\n"
                  "**>** To show your stash/base inventory: .i stash (or .i st / .i base / .i b)",
            inline=False)
    elif command == "skilltree":
        help_menu.add_field(
            name="The 'Skilltree' Command:",
            value="*Shows your skills and progression.*\n"
                  "**>** __Usage__: .skilltree (.skill / .sk)\n",
            inline=False)
    elif command == "stash":
        help_menu.add_field(
            name="The 'Stash' Command:",
            value="*Allows you to store stuff at and get stuff from your stash. "
                  "You can only stash stuff at your base!*\n"
                  "**>** __Usage__: .stash (.st)\n"
                  "**>** To store stuff at your base: .stash b (or base)\n"
                  "**>** To store stuff in your inventory: .stash i (or inv)\n"
                  "**>** To store specific resources: .stash i/b item_name amount (ex: .st b berries 100)",
            inline=False)
    elif command == "build":
        help_menu.add_field(
            name="The 'Build' Command:",
            value="*Used for building projects at base.*\n"
                  "You can only use this at your base!*\n"
                  "**>** __Usage__: .build (.b)\n"
                  "**>** To see a list of what you can build: .b\n"
                  "**>** To build an item from the list: .b item_name",
            inline=False)
    elif command == "craft":
        help_menu.add_field(
            name="The 'Craft' Command:",
            value="*Used to craft simple tools and armour.*\n"
                  "You can use this anywhere!*\n"
                  "**>** __Usage__: .craft (.cr/.c)\n",
            inline=False)
    elif command == "use":
        help_menu.add_field(
            name="The 'Use' Command:",
            value="*Allows you to use items you've acquired at your base.*\n"
                  "You can only use this at your base!*\n"
                  "**>** __Usage__: .use (.u)\n"
                  "**>** To see a list of things you can use: .u\n"
                  "**>** To use an item from the list: .u item_name",
            inline=False)
    elif command == "market":
        help_menu.add_field(
            name="The 'Market' Command:",
            value="*Used to buy and sell items.*\n"
                  "You can only use this at the market!*\n"
                  "**>** __Usage__: .market (.mar/.m)\n"
                  "**>** To see a list of things you can buy: .m b (or buy)\n"
                  "**>** To see a list of things you can sell: .m s (or sell)\n"
                  "**>** To buy/sell something: .m b/s item_name amount (ex: .m b diamond 5)",
            inline=False)
    elif command == "labour":
        help_menu.add_field(
            name="The 'Labour' Command:",
            value="*Used to gather, lumber or mine for resources.*\n"
                  "**>** __Usage__: .labour (.lab/.l)\n"
                  "**>** To gather in the Forest: .labour gather/g number (ex: .l g a)\n"
                  "**>** To lumber in the Forest: .labour lumber/l number (ex: .l l 5)\n"
                  "**>** To mine in the Mine: .labour mine/m number (ex: .l m 5)",
            inline=False)
    elif command == "eat":
        help_menu.add_field(
            name="The 'Eat' Command:",
            value="*Used to fill your nourishment meter.*\n"
                  "**>** __Usage__: .eat (.e)\n"
                  "**>** To eat something: .eat food_name amount (ex: .e berries a)",
            inline=False)
    elif command == "travel":
        help_menu.add_field(
            name="The 'Travel' Command:",
            value="*Used to travel to any location.*\n"
                  "**>** __Usage__: .travel (.tr)\n"
                  "**>** To see a list of places and travel cost: .travel\n"
                  "**>** To travel to a location: .tr location_name location_lvl (none for max lvl)",
            inline=False)
    elif command == "sleep":
        help_menu.add_field(
            name="The 'Sleep' Command:",
            value="*Used to regain Stamina & Travel Power.*\n"
                  "**>** __Usage__: .sleep (.sl/.slp)\n"
                  "**>** To sleep for a certain amount of turns: .sl number (ex: .sl a)\n",
            inline=False)
    elif command == "battle":
        help_menu.add_field(
            name="The 'Battle' Command:",
            value="*Initiates a battle if you have enemies nearby.*\n"
                  "**>** __Usage__: .battle (.bat)\n",
            inline=False)
    elif command == "escape":
        help_menu.add_field(
            name="The 'Escape' Command:",
            value="*Attempts to escape if you have enemies nearby.*\n"
                  "**>** __Usage__: .escape (.esc)\n",
            inline=False)
    await client.send_message(channel, embed=help_menu)


# .allow
@client.command(aliases=["al"], pass_context=True)
@commands.has_role("Admin")
async def allow(ctx, command=None, index=1):
    # Open Json
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # All Commands
    channel_name = ctx.message.channel
    channel_name = str(channel_name)
    channel_id = ctx.message.channel.id
    if command is None:
        for indexes in (1, 2, 3, 4, 5):
            # Channel Names
            allowed_channels[indexes] = {}
            for names in (
                    "battle_name", "build_name", "craft_name", "create_name", "eat_name", "escape_name", "furnace_id",
                    "labour_name", "market_name", "inventory_name", "reset_name", "sleep_name", "skilltree_name", "stash_name",
                    "store_name", "travel_name", "use_name", "workbench_name"):
                allowed_channels[indexes][names] = channel_name
            # Channel IDs
            for ids in (
                    "battle_id", "build_id", "craft_id", "create_id", "eat_id", "escape_id", "furnace_id",
                    "labour_id", "market_id", "inventory_id", "reset_id", "sleep_id", "skilltree_id",
                    "stash_id", "store_id", "travel_id", "use_id", "workbench_id"):
                allowed_channels[indexes][ids] = channel_id
    # Specific Commands
    else:
        if 0 < index < 5:
            allowed_channels[index][command + "_name"] = channel_name
            allowed_channels[index][command + "_id"] = channel_id

    # Update Json
    with open("allowed_channels.json", "w") as f:
        json.dump(allowed_channels, f)


# .create
@client.command(pass_context=True)
async def create(ctx):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("stash_base.json", "r") as f:
        stash_base = json.load(f)
    with open("user_plot.json", "r") as f:
        user_plot = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check (Unique)
    check_account = False
    user = ctx.message.author
    if not user.id in users:
        check_account = True
    else:
        await client.say("{}, you already have an account!".format(user.mention))
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "create_name"
    channel_id = "create_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message

    # Execute Use
    if check_account and check_channel:
        await update_data.update_data_users(client, ctx, users, equipment, resources, skilltree, stash_base, user_plot)

    # Dump Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("equipment.json", "w") as f:
        json.dump(equipment, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)
    with open("stash_base.json", "w") as f:
        json.dump(stash_base, f)
    with open("user_plot.json", "w") as f:
        json.dump(user_plot, f)
    with open("allowed_channels.json", "w") as f:
        json.dump(allowed_channels, f)


# .reset
@client.command(pass_context=True)
async def reset(ctx):
    # Open Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("stash_base.json", "r") as f:
        stash_base = json.load(f)
    with open("user_plot.json", "r") as f:
        user_plot = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "reset_name"
    channel_id = "reset_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message

    # Execute Use
    if check_account and check_channel:
        await client.say("{}, do you really want to reset all your progress? Confirm by typing 'delete'."
                         .format(user.mention))
        msg = await client.wait_for_message(author=user, timeout=30)
        if msg.content == "delete":
            reset_check = True
        else:
            reset_check = False
        if reset_check:
            await client.say("{}, resetting your data...".format(user.mention))
            await update_data.update_data_users(client, ctx, users, equipment, resources, skilltree, stash_base,
                                                user_plot)
        else:
            await client.say("{}, resetting canceled!".format(user.mention))

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("equipment.json", "w") as f:
        json.dump(equipment, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)
    with open("stash_base.json", "w") as f:
        json.dump(stash_base, f)
    with open("user_plot.json", "w") as f:
        json.dump(user_plot, f)
    with open("allowed_channels.json", "w") as f:
        json.dump(allowed_channels, f)


# .top
@client.command(pass_context=True)
async def top(ctx, atr=None, page=1):
    with open("users.json", "r") as f:
        users = json.load(f)

    class Member:
        def __init__(self, name, level, cash):
            self.name = name
            self.level = level
            self.cash = cash

        def __repr__(self):
            return "\n> {} | Level: {} | Cash: {}".format(self.name, self.level, self.cash)

    # Lists
    list_final = []
    for user_ in users:
        list_member = Member(users[user_]["name"], users[user_]["level"], users[user_]["cash"])
        list_final.append(list_member)

    def m_sort(mem):
        if atr == "level":
            return mem.level
        elif atr == "cash":
            return mem.cash

    # List Sorting
    page = page * 10
    if atr is None or atr == "name":
        s_members = sorted(list_final, key=lambda m: m.name.lower())
        s_members = s_members[page-10:page]
    elif atr == "level" or atr == "cash":
        s_members = sorted(list_final, key=m_sort, reverse=True)
        s_members = s_members[page-10:page]

    # Message
    await client.say(s_members)


# .test
@client.command(pass_context=True)
async def test(ctx, atr=None, page=1):
    with open("users.json", "r") as f:
        users = json.load(f)

    # User Variables
    user = ctx.message.author

    # List Sorting
    page = page * 10
    p_list = []
    p_list_sorted = []
    for user_ in users:
        players = ({"name": users[user_]["name"], "level": users[user_]["level"], "cash": users[user_]["cash"]})
        p_list.append(players)

    # Sort
    for x in sorted(p_list, key=itemgetter("level", "name"), reverse=True):
        p_list_sorted.append(x)


    p_list_sorted = p_list_sorted[page-10:page]

    final_list = pd.DataFrame(p_list_sorted).reindex(columns=["name", "level", "cash"])

    await client.say(final_list)


    #await client.say("\n".join("{}: {} | {}: {} | {}: {}".format(*k) for k in enumerate(p_list_sorted)))


# .inventory
@client.command(aliases=["i", "inv"], pass_context=True)
async def inventory(ctx, stash=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("stash_base.json", "r") as f:
        stash_base = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)
    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "inventory_name"
    channel_id = "inventory_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Inventory
    if check_account and check_channel and check_combat:
        await char_inventory.inventory(client, ctx, stash, users, resources, stash_base, equipment, skilltree, icons)


# .skilltree
@client.command(aliases=["sk", "skill"], pass_context=True)
async def skilltree(ctx):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "skilltree_name"
    channel_id = "skilltree_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Skilltree
    if check_account and check_channel and check_combat:
        await char_skilltree.skilltree(client, ctx, users, skilltree, icons)


# .stash
@client.command(aliases=["st"], pass_context=True)
async def stash(ctx, location=None, res_item=None, amount=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("stash_base.json", "r") as f:
        stash_base = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "stash_name"
    channel_id = "stash_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Stash
    if check_account and check_channel and check_combat:
        await char_stash.stash(client, ctx, users, resources, stash_base, location, res_item, amount)

    # Update Json
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("stash_base.json", "w") as f:
        json.dump(stash_base, f)


# .build
@client.command(aliases=["b"], pass_context=True)
async def build(ctx, item=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("user_plot.json", "r") as f:
        user_plot = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "build_name"
    channel_id = "build_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Build
    if check_account and check_channel and check_combat:
        await building_menu.build(client, ctx, item, users, equipment, resources, user_plot, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("user_plot.json", "w") as f:
        json.dump(user_plot, f)


# .craft
@client.command(aliases=["c", "cr"], pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def craft(ctx):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "skilltree_name"
    channel_id = "skilltree_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Craft
    if check_account and check_channel and check_combat:
        await crafting.craft(client, ctx, users, resources, equipment, skilltree, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)
    with open("equipment.json", "w") as f:
        json.dump(equipment, f)


# .use
@client.command(aliases=["u"], pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def use(ctx, item=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("user_plot.json", "r") as f:
        user_plot = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "use_name"
    channel_id = "use_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Use
    if check_account and check_channel and check_combat:
        await using.use(client, ctx, item, users, equipment, resources, skilltree, user_plot, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("equipment.json", "w") as f:
        json.dump(equipment, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)
    with open("user_plot.json", "w") as f:
        json.dump(user_plot, f)


# .market
@client.command(aliases=["mar", "m"], pass_context=True)
async def market(ctx, trans=None, item=None, amount=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "market_name"
    channel_id = "market_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Use
    if check_account and check_channel and check_combat:
        await marketing.market(client, ctx, users, user, trans, item, amount, equipment, resources, skilltree)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("equipment.json", "w") as f:
        json.dump(equipment, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)


# .labour
@client.command(aliases=["lab",  "l"], pass_context=True)
async def labour(ctx, l_type=None, amount=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("equipment.json", "r") as f:
        equipment = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("stash_base.json", "r") as f:
        stash_base = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "labour_name"
    channel_id = "labour_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Craft
    if check_account and check_channel and check_combat:
        await labouring.labour(client, ctx, l_type, amount, users, equipment, resources, skilltree, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("equipment.json", "w") as f:
        json.dump(equipment, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)


# .eat
@client.command(aliases=["e"], pass_context=True)
async def eat(ctx, food_type=None, amount=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "eat_name"
    channel_id = "eat_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Eat
    if check_account and check_channel and check_combat:
        await eating.eat(client, ctx, users, resources, food_type, amount, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)


# .travel
@client.command(aliases=["tr", "trav"], pass_context=True)
async def travel(ctx, location=None, level=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "travel_name"
    channel_id = "travel_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Travel
    if check_account and check_channel and check_combat:
        await traveling.travel(client, ctx, location, level, users, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)


# .sleep
@client.command(aliases=["sl", "slp"], pass_context=True)
async def sleep(ctx, amount=None):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("icons.json", "r") as f:
        icons = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "sleep_name"
    channel_id = "sleep_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check
    check_combat = False
    if users[user.id]["combat"] == 0:
        check_combat = True
    else:
        await combat_check(user)  # In Combat Message

    # Execute Sleep
    if check_account and check_channel and check_combat:
        await sleeping.sleep(client, ctx, amount, users, resources, icons)

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)


# .battle
@client.command(aliases=["bat"], pass_context=True)
async def battle(ctx):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)
    with open("skilltree.json", "r") as f:
        skilltree = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "battle_name"
    channel_id = "battle_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check (Special)
    if not users[user.id]["in_combat"]:
        check_combat = True
    else:
        check_combat = False
        await client.say("{}, you are already fighting something!".format(user.mention))

    # Execute Battle
    if check_account and check_channel and check_combat:
        if users[user.id]["combat"] > 0:
            users[user.id]["in_combat"] = True
            with open("users.json", "w") as f:
                json.dump(users, f)
            await battling.battle(client, ctx, users, resources, skilltree)
        else:
            await client.say("{}, you don't have any enemies nearby!".format(user.mention))

    # Update Json Files
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)
    with open("skilltree.json", "w") as f:
        json.dump(skilltree, f)


# .escape
@client.command(aliases=["esc"], pass_context=True)
async def escape(ctx):
    # Load Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("allowed_channels.json", "r") as f:
        allowed_channels = json.load(f)

    # Account Check
    check_account = False
    user = ctx.message.author
    if user.id in users:
        check_account = True
    else:
        await account_check(user)  # No Account Message
    # Channel Check
    check_channel = False
    channel = ctx.message.channel.id
    channel_name = "escape_name"
    channel_id = "escape_id"
    for indexes in ("1", "2", "3", "4", "5"):
        channel_allowed = allowed_channels[indexes][channel_name]
        if allowed_channels[indexes][channel_id] == channel:
            check_channel = True
    if not check_channel:
        await channel_check(user, channel_allowed)  # Wrong Channel Message
    # Combat Check (Special)
    if not users[user.id]["in_combat"]:
        check_combat = True
    else:
        check_combat = False
        await client.say("{}, you are currently fighting something!".format(user.mention))

    # Execute Escape
    if check_account and check_channel and check_combat:
        # Combat Check
        if users[user.id]["combat"] > 0:
            if users[user.id]["escaped"]:
                enemies = users[user.id]["combat"]
                success = 0
                while enemies > 0:
                    enemies -= 1
                    temp_chance = random.randint(1, 3)
                    if temp_chance == 1:
                        success += 1

                if success == users[user.id]["combat"]:
                    await client.say("{}, you managed to escape!".format(user.mention))
                    users[user.id]["combat"] = 0
                    users[user.id]["escaped"] = True
                else:
                    enemies = users[user.id]["combat"] - success
                    await client.say(
                        "{}, you only escaped {} enemies and still have to fight {} of them!".format(user.mention, success, enemies))
                    users[user.id]["escaped"] = False
            else:
                await client.say("{}, you have already attempted to escape or engaged with enemies!".format(user.mention))
        else:
            await client.say("{}, you are not in combat!".format(user.mention))

    # Update Json Files
    with open("users.json", "w") as f:
        json.dump(users, f)


# .give
@client.command()
async def give(item=None, atr=None, user: discord.Member = None):
    # Open Json
    with open("resources.json", "r") as f:
        resources = json.load(f)

    # Give Stuff
    user = user.id
    atr = int(atr)
    resources[user][item] += atr

    # Update Json
    with open("resources.json", "w") as f:
        json.dump(resources, f)


# .god
@client.command(pass_context=True)
async def god(ctx, amount=1):
    # Open Json
    with open("users.json", "r") as f:
        users = json.load(f)
    with open("resources.json", "r") as f:
        resources = json.load(f)

    user = ctx.message.author

    # Too Many Resources
    if resources[user.id]["stick"] < 1000000 and amount < 1000000:
        # User
        await client.say("{}, Do you also want to level up? Type 'yes' to confirm or 'no' to only receive resources."
                         .format(user.mention))
        msg = await client.wait_for_message(author=user, timeout=15)
        if msg.content == "yes":
            level_up = True
        elif msg.content == "no":
            level_up = False
        else:
            level_up = False
        if level_up:
            users[user.id]["level"] += 10
            users[user.id]["experience"] += 100

        # Money
        users[user.id]["cash"] += 1000000

        # Raw Resources
        resources[user.id]["wood"] += 100 * amount
        resources[user.id]["stone"] += 100 * amount
        resources[user.id]["coal"] += 100 * amount
        resources[user.id]["iron_ore"] += 100 * amount
        resources[user.id]["copper_ore"] += 100 * amount
        resources[user.id]["gold_ore"] += 100 * amount

        # Refined Resources
        resources[user.id]["plank"] += 100 * amount
        resources[user.id]["rope"] += 100 * amount
        resources[user.id]["copper_bar"] += 100 * amount
        resources[user.id]["iron_bar"] += 100 * amount
        resources[user.id]["gold_bar"] += 100 * amount

        # Animal Produce
        resources[user.id]["meat"] += 100 * amount
        resources[user.id]["milk"] += 100 * amount
        resources[user.id]["eggs"] += 100 * amount
        resources[user.id]["leather"] += 100 * amount
        resources[user.id]["wool"] += 100 * amount
        resources[user.id]["feathers"] += 100 * amount

        # Animals
        resources[user.id]["cows"] += 100 * amount
        resources[user.id]["sheep"] += 100 * amount
        resources[user.id]["chickens"] += 100 * amount

        # Farm Produce
        resources[user.id]["wheat"] += 100 * amount
        resources[user.id]["potatoes"] += 100 * amount
        resources[user.id]["apples"] += 100 * amount

        # Gathering
        resources[user.id]["fibre"] += 100 * amount
        resources[user.id]["stick"] += 100 * amount
        resources[user.id]["berries"] += 100 * amount

        # Message
        await client.say("{}, you received {} resources!".format(user.mention, 100 * amount))
    else:
        await client.say("{}, you have too many resources!".format(user.mention))

    # Update Json
    with open("users.json", "w") as f:
        json.dump(users, f)
    with open("resources.json", "w") as f:
        json.dump(resources, f)


# .clear
@client.command(aliases=["cl"], pass_context=True)
@commands.has_role("Moderator")
async def clear(ctx, amount=100):
    user = ctx.message.author
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say("{} messages deleted by {}".format(amount, user.name))


# Token
client.run(TOKEN)
