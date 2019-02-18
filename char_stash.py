from discord.ext.commands import bot


async def stash(client: bot, ctx, users, resources, stash_base, location, res_item, amount):
    # User
    user = ctx.message.author
    if res_item is None:
        if users[user.id]["location"] == "Home":
            if location is None:
                await client.say("{}, please specify where you want to store your stuff. (base, inv)\n"
                                 "You can also store specific items using .stash location item amount => e.g. "
                                 "'.stash base berries 100'".format(user.mention))
            elif location == "base" or location == "Base" or location == "b":
                await client.say(
                    "{}, you took everything from your inventory and stored it in your stash!".format(user.mention))
                for res_item in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore",
                                 "plank", "rope", "copper_bar", "iron_bar", "gold_bar",
                                 "meat", "milk", "eggs", "leather", "wool", "feathers",
                                 "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
                    # Stash Resources
                    stash_base[user.id][res_item] += resources[user.id][res_item]
                    resources[user.id][res_item] -= resources[user.id][res_item]

            elif location == "inventory" or location == "Inventory" or location == "inv":
                await client.say(
                    "{}, you took everything from your stash and stored it in your inventory!".format(user.mention))
                for res_item in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore",
                                 "plank", "rope", "copper_bar", "iron_bar", "gold_bar",
                                 "meat", "milk", "eggs", "leather", "wool", "feathers",
                                 "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
                    # Stash Resources
                    resources[user.id][res_item] += stash_base[user.id][res_item]
                    stash_base[user.id][res_item] -= stash_base[user.id][res_item]
            # Spelling Message
            else:
                await client.say("{}, you can't store your stuff in '{}'".format(user.mention, location))
        # Location Message
        else:
            await client.say("{}, you can only stash stuff at your base!".format(user.mention))
    # Store Single Items
    elif res_item is not None:
        if users[user.id]["location"] == "Home":
            if res_item in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore",
                            "plank", "rope", "copper_bar", "iron_bar", "gold_bar",
                            "meat", "milk", "eggs", "leather", "wool", "feathers",
                            "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
                # Location Check
                if location == "base" or location == "b":
                    json_source = resources
                    json_target = stash_base
                    stash_type = "stash"
                elif location == "inventory" or location == "inv" or location == "i":
                    json_source = stash_base
                    json_target = resources
                    stash_type = "inventory"
                else:
                    await client.say("{}, you can't store your stuff in '{}'!".format(user.mention, location))
                # Execute Transaction

                if amount is None:
                    amount = json_source[user.id][res_item]
                try:
                    amount = int(amount)
                except ValueError:
                    amount = json_source[user.id][res_item]
                amount = int(amount)
                if amount > json_source[user.id][res_item]:
                    amount = json_source[user.id][res_item]
                elif amount < 1:
                    amount = 0
                json_source[user.id][res_item] -= amount
                json_target[user.id][res_item] += amount
                # Confirmation Message
                await client.say("{}, you stored {} {} in your {}!".format(user.mention, amount, res_item, stash_type))
            # Spelling Message
            else:
                await client.say("{}, check your spelling => wood, stone, coal, iron_ore, copper_ore, gold_ore, "
                                 "plank, rope, copper_bar, iron_bar, gold_bar, "
                                 "meat, milk, eggs, leather, wool, feathers, "
                                 "wheat, potatoes, apples, fibre, stick, berries".format(user.mention))
        # Location Message
        else:
            await client.say("{}, you can only stash stuff at your base!".format(user.mention))
