from discord.ext.commands import bot


async def travel(client: bot, ctx, location, level, users, icons):

    # User
    user = ctx.message.author
    users[user.id]["experience"] -= 1
    ulocation = users[user.id]["location"]
    ulocation_level = users[user.id]["location_lvl"]
    unourishment = users[user.id]["nourishment"]
    utravelpower = users[user.id]["travelpower"]

    # Current Location Variables
    if level is not None:
        try:
            level = int(level)
        except ValueError:
            level = 1
        level = int(level)

    if location is None:
        level = users[user.id]["location_lvl"]
    elif location == "Home" or location == "home" or location == "ho" or location == "h" or \
            location == "Market" or location == "market" or location == "mar" or location == "m":
            level = 0
    elif location == "Forest" or location == "forest" or location == "for" or location == "f":
        if level is None or level > users[user.id]["forest_lvl"] or level < 1:
            level = users[user.id]["forest_lvl"]
    elif location == "Mine" or location == "mine" or location == "mi" or location == "m":
        if level is None or level > users[user.id]["mine_lvl"] or level < 1:
            level = users[user.id]["mine_lvl"]
    elif location == "Treasure" or location == "treasure" or location == "tr" or location == "t":
        if level is None or level > users[user.id]["treasure_lvl"] or level < 1:
            level = users[user.id]["treasure_lvl"]
    elif location == "Dungeon" or location == "dungeon" or location == "dun" or location == "d":
        if level is None or level > users[user.id]["dungeon_lvl"] or level < 1:
            level = users[user.id]["dungeon_lvl"]


    # Check Input
    cost_travel_power = ""
    cost_food = ""
    location = str(location)
    ulocation = str(ulocation)

    if location.lower() == ulocation.lower() and level == users[user.id]["location_lvl"]:
        await client.say("{}, you're already here!".format(user.mention))
    elif location == "None":
        await client.say("{} You need to specify a location: ({}--{})\n"
                         "Home: 1--10)\n"
                         "Market: 1--20)\n"
                         "Forest: 2--30\n"
                         "Mine: 3--40\n"
                         "Treasure Island: 4--60\n"
                         "Dungeon: 5--80\n"
                         "**Your Location: {} (lvl {})**\n"
                         "**Your Travel Power: {}{}, Your Nourishment: {}{}**"
                         .format(user.mention, icons["icon"]["travelpower"], icons["icon"]["nourishment"],
                                 ulocation, ulocation_level, icons["icon"]["travelpower"], utravelpower,
                                 icons["icon"]["nourishment"], unourishment))

    # Future Location Variables
    elif location == "Home" or location == "home" or location == "ho" or location == "h":
        cost_travel_power = "1"
        cost_food = "10"
        location = "Home"
    elif location == "Market" or location == "market" or location == "mar" or location == "m":
        cost_travel_power = "1"
        cost_food = "20"
        location = "Market"
    elif location == "Forest" or location == "forest" or location == "for" or location == "f":
        cost_travel_power = "2"
        cost_food = "30"
        location = "Forest"
    elif location == "Mine" or location == "mine" or location == "mi" or location == "m":
        cost_travel_power = "3"
        cost_food = "40"
        location = "Mine"
    elif location == "Treasure" or location == "treasure" or location == "tr" or location == "t":
        cost_travel_power = "4"
        cost_food = "60"
        location = "Treasure"
    elif location == "Dungeon" or location == "dungeon" or location == "dun" or location == "d":
        cost_travel_power = "5"
        cost_food = "80"
        location = "dungeon"
    else:
        await client.say("{}, there's no location called {}".format(user.mention, location))

    # Execute Traveling
    if cost_travel_power != "":
        cost_travel_power = int(cost_travel_power)
        cost_food = int(cost_food)
        # Stamina Check
        if users[user.id]["stamina"] > 0:
            if cost_travel_power <= utravelpower and cost_food <= unourishment:
                users[user.id]["location"] = location
                users[user.id]["location_lvl"] = level
                users[user.id]["travelpower"] -= cost_travel_power
                users[user.id]["nourishment"] -= cost_food
                await client.say("{}, you have traveled to {} ({}) "
                                 "at the cost of {}{} Travel Power "
                                 "and {}{} Nourishment"
                                 .format(user.mention, location, level, icons["icon"]["travelpower"], cost_travel_power,
                                         icons["icon"]["nourishment"], cost_food))
            else:
                await client.say("{}, you don't have enough {}Travel Power ({}/{}) "
                                 "or {}Nourishment ({}/{})!\n"
                                 .format(user.mention, icons["icon"]["travelpower"], utravelpower, cost_travel_power,
                                         icons["icon"]["nourishment"], unourishment, cost_food))
        # No Stamina Message
        else:
            await client.say("{}, you can't travel with no {}Stamina!".format(user.mention, icons["icon"]["stamina"]))

