import discord
from discord.ext.commands import bot
import math

import update_data


async def use(client: bot, ctx, item, users, equipment, resources, skilltree, user_plot, icons):
    # User Variables
    user = ctx.message.author

    # Possible Reactions
    reaction_1 = "1⃣"
    reaction_2 = "2⃣"
    reaction_3 = "3⃣"
    reaction_4 = "4⃣"
    reaction_5 = "5⃣"
    reaction_6 = "6⃣"
    reaction_7 = "7⃣"
    reaction_8 = "8⃣"
    reaction_9 = "9⃣"
    timeout = 30

    # Workbench Stats & Cost
    ufibre = resources[user.id]["fibre"]
    fibre_per_rope = 15
    wood_per_plank = 5

    # Furnace Stats & Cost
    coal_per_copper = 1
    copper_per_bar = 3
    coal_per_iron = 3
    iron_per_bar = 5
    coal_per_gold = 5
    gold_per_bar = 10

    # Skill Level Variables
    base_xp = 30
    xp_per_smelting = 1

    # Embed Variables
    player_name = ctx.message.author.name
    player_avatar_url = ctx.message.author.avatar_url
    server_name = ctx.message.server.name
    bot_icon = "https://cdn.discordapp.com/attachments/538124566527213598/539066367375048737/NGB-Logo.png"

    # Possible Uses for Command
    if users[user.id]["nourishment"] >= 20:
        if item is None:
            workbench_built = user_plot[user.id]["workbench"]
            furnace_built = user_plot[user.id]["furnace"]
            cra = discord.Embed(
                title="Possible items for the .use command:",
                description="Workbench ({}) | Furnace ({})".format(workbench_built, furnace_built),
                colour=discord.Colour.darker_grey())
            cra.set_author(name="{}".format(player_name), icon_url=player_avatar_url)
            cra.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/538124566527213598/540471921721212946/crafting.png")
            cra.set_image(url=bot_icon)
            cra.set_footer(text=server_name)

            await client.say(embed=cra)

        # Workbench Menu
        elif item == "workbench" or item == "Workbench" or item == "wb":
            # Item Costs:
            stone_sword_stick_cost = 10
            stone_sword_stone_cost = 50
            stone_tool_stick_cost = 15
            stone_tool_stone_cost = 25
            cra = discord.Embed(
                title="Workbench Menu",
                description="{} **Stone Sword:** {}Sticks: {}/{} | {} Stones: {}/{}\n"
                            "{} **Stone Axe:** {}Sticks: {}/{} | {}Stones: {}/{}\n"
                            "{} **Stone Pickaxe:** {}Sticks: {}/{} | {}Stones: {}/{}\n"
                            "{} **Stone Shovel:** {}Sticks: {}/{} | {}Stones: {}/{}\n"
                            "{} **Stone Hammer:** {}Sticks: {}/{} | {}Stones: {}/{}\n"
                            "{} **Rope:** {} Fibre: {}/{}\n"
                            "{} **Planks:** {} Wood: {}/{}"
                    .format(reaction_1, icons["icon"]["stick"], resources[user.id]["stick"], stone_sword_stick_cost,
                            icons["icon"]["stone"], resources[user.id]["stone"], stone_sword_stone_cost,
                            reaction_2, icons["icon"]["stick"], resources[user.id]["stick"], stone_tool_stick_cost,
                            icons["icon"]["stone"], resources[user.id]["stone"], stone_tool_stone_cost,
                            reaction_3, icons["icon"]["stick"], resources[user.id]["stick"], stone_tool_stick_cost,
                            icons["icon"]["stone"], resources[user.id]["stone"], stone_tool_stone_cost,
                            reaction_4, icons["icon"]["stick"], resources[user.id]["stick"], stone_tool_stick_cost,
                            icons["icon"]["stone"], resources[user.id]["stone"], stone_tool_stone_cost,
                            reaction_5, icons["icon"]["stick"], resources[user.id]["stick"], stone_tool_stick_cost,
                            icons["icon"]["stone"], resources[user.id]["stone"], stone_tool_stone_cost,
                            reaction_6, icons["icon"]["fibre"], ufibre, fibre_per_rope,
                            reaction_7, icons["icon"]["wood"], resources[user.id]["wood"], wood_per_plank),
                colour=discord.Colour.darker_grey())
            cra.set_author(name="{}'s Workbench Menu".format(player_name), icon_url=player_avatar_url)
            cra.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/538124566527213598/540471921721212946/crafting.png")
            cra.set_image(url=bot_icon)
            cra.set_footer(text=server_name)

        # Furnace Menu
        elif item == "furnace" or item == "Furnace" or item == "furn":
            cra = discord.Embed(
                title="Chose ore:",
                description="{} **Copper Bar:** {}Coal: {} | {}Copper Ore: {}\n"
                            "{} **Iron Bar:** {}Coal: {} | {}Iron Ore: {}\n"
                            "{} **Gold Bar:** {}Coal: {} | {}Gold Ore: {}"
                    .format(reaction_1,
                            icons["icon"]["coal"], coal_per_copper, icons["icon"]["copper_ore"], copper_per_bar,
                            reaction_2,
                            icons["icon"]["coal"], coal_per_iron, icons["icon"]["iron_ore"], iron_per_bar,
                            reaction_3,
                            icons["icon"]["coal"], coal_per_gold, icons["icon"]["gold_ore"], gold_per_bar),
                colour=discord.Colour.darker_grey())
            cra.set_author(name="{}'s Furnace Menu".format(player_name), icon_url=player_avatar_url)
            cra.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/538124566527213598/540471921721212946/crafting.png")
            cra.set_image(url=bot_icon)
            cra.set_footer(text=server_name)

        else:
            await client.say("{}, you can't use '{}', check your spelling!".format(user.mention, item))

        # Workbench
        if users[user.id]["location"] == "Home":  # Check Location
            if item == "workbench" or item == "Workbench" or item == "wb":
                if user_plot[user.id]["workbench"]:  # Check Plot
                    hammer = equipment[user.id]["hammer"]  # Check Hammer
                    if hammer == "Wooden Hammer" or hammer == "Stone Hammer" or hammer == "Iron Hammer":

                        # Execute Embed
                        workbench_menu = await client.say(embed=cra)

                        # Add Reactions
                        await client.add_reaction(workbench_menu, reaction_1)
                        await client.add_reaction(workbench_menu, reaction_2)
                        await client.add_reaction(workbench_menu, reaction_3)
                        await client.add_reaction(workbench_menu, reaction_4)
                        await client.add_reaction(workbench_menu, reaction_5)
                        await client.add_reaction(workbench_menu, reaction_6)
                        await client.add_reaction(workbench_menu, reaction_7)

                        # Wait for User Reaction
                        user_reaction = await client.wait_for_reaction(user=user,
                                                                       emoji=['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣'],
                                                                       message=workbench_menu, timeout=10)
                        if user_reaction is None:
                            await client.say("{}, crafting canceled!".format(user.mention))

                        # Stone Sword
                        if user_reaction.reaction.emoji == "1⃣":
                            stick_cost = stone_sword_stick_cost
                            stone_cost = stone_sword_stone_cost
                            emo = "1⃣"
                            eqitem = "mainhand"
                            item_name = "Stone Sword"
                            item_attack = 5
                            item_defense = 0
                        # Stone Axe
                        elif user_reaction.reaction.emoji == "2⃣":
                            stick_cost = stone_tool_stick_cost
                            stone_cost = stone_tool_stone_cost
                            emo = "2⃣"
                            eqitem = "axe"
                            item_name = "Stone Axe"
                            item_durability = 60
                            item_durability_name = "axe_durability"
                            item_yield = 1
                            item_yield_name = "axe_yield"
                        # Stone Pickaxe
                        elif user_reaction.reaction.emoji == "3⃣":
                            stick_cost = stone_tool_stick_cost
                            stone_cost = stone_tool_stone_cost
                            emo = "3⃣"
                            eqitem = "pickaxe"
                            item_name = "Stone Pickaxe"
                            item_durability = 60
                            item_durability_name = "pickaxe_durability"
                            item_yield = 1
                            item_yield_name = "pickaxe_yield"
                        # Stone Shovel
                        elif user_reaction.reaction.emoji == "4⃣":
                            stick_cost = stone_tool_stick_cost
                            stone_cost = stone_tool_stone_cost
                            emo = "4⃣"
                            eqitem = "shovel"
                            item_name = "Stone Shovel"
                            item_durability = 60
                            item_durability_name = "shovel_durability"
                            item_yield = 1
                            item_yield_name = "shovel_yield"
                            # Stone Hammer
                        # Stone Hammer
                        elif user_reaction.reaction.emoji == "5⃣":
                            stick_cost = stone_tool_stick_cost
                            stone_cost = stone_tool_stone_cost
                            emo = "5⃣"
                            eqitem = "hammer"
                            item_name = "Stone Hammer"
                            item_durability = 60
                            item_durability_name = "hammer_durability"
                            item_yield = 1
                            item_yield_name = "hammer_yield"
                        # Rope
                        elif user_reaction.reaction.emoji == "6⃣":
                            emo = "6⃣"
                            amount_res = fibre_per_rope
                            type_res = ufibre
                            res_name = "fibre"
                            yield_name = "rope"
                            yield_emo = icons["icon"]["rope"]
                            res_emo = icons["icon"]["fibre"]
                        # Planks
                        elif user_reaction.reaction.emoji == "7⃣":
                            emo = "7⃣"
                            amount_res = wood_per_plank
                            type_res = resources[user.id]["wood"]
                            res_name = "wood"
                            yield_name = "plank"
                            yield_emo = icons["icon"]["plank"]
                            res_emo = icons["icon"]["wood"]

                        # Execute Craft
                        if user_reaction.reaction.emoji == emo:
                            if user_reaction.reaction.emoji != "6⃣" and user_reaction.reaction.emoji != "7⃣":
                                await client.delete_message(workbench_menu)
                                if resources[user.id]["stick"] >= stick_cost and resources[user.id]["stone"] >= stone_cost:
                                    equipped_item = equipment[user.id][eqitem]
                                    craft_check = True
                                    if equipped_item != "Empty Slot":
                                        await client.say("{}, you already have a {} equipped, do you want to replace it? "
                                                         "Type 'yes' to confirm or 'no' to cancel!"
                                                         .format(user.mention, equipped_item))
                                        msg = await client.wait_for_message(author=user, timeout=timeout)
                                        if msg.content == "yes":
                                            craft_check = True
                                        elif msg.content == "no":
                                            craft_check = False
                                        else:
                                            craft_check = False
                                    if craft_check:
                                        # Cost
                                        resources[user.id]["stick"] -= stick_cost
                                        resources[user.id]["stone"] -= stone_cost
                                        # Mainhand Update
                                        if item_name == "Stone Sword":
                                            equipment[user.id]["mainhand"] = item_name
                                            users[user.id]["attack"] -= equipment[user.id]["mainhand_attack"]
                                            equipment[user.id]["mainhand_attack"] = item_attack
                                            users[user.id]["attack"] += equipment[user.id]["mainhand_attack"]
                                            equipment[user.id]["mainhand_defense"] = item_defense
                                        # Stone Tool Update
                                        else:
                                            equipment[user.id][eqitem] = item_name
                                            equipment[user.id][item_durability_name] = item_durability
                                            equipment[user.id][item_yield_name] = item_yield
                                        # Hammer Durability
                                        equipment[user.id]["hammer_durability"] -= 2
                                        if equipment[user.id]["hammer_durability"] <= 0:
                                            equipment[user.id]["hammer_durability"] = 0
                                            equipment[user.id]["hammer"] = "Empty Slot"
                                            await client.say("{}, your Hammer broke!".format(user.mention))
                                        # Crafting Message
                                        await client.say("{}, you crafted a {}!".format(user.mention, item_name))

                                        # Craft Experience
                                        base_xp = 30
                                        xp_per_craft = 10
                                        # Skill Level
                                        skilltree[user.id]["smith_exp"] += xp_per_craft
                                        if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                                            skilltree[user.id]["smith"] += 1
                                            skilltree[user.id]["smith_exp"] = 0
                                            skilltree[user.id]["smith_exp_need"] = int(base_xp + (
                                                    xp_per_craft / 2 * skilltree[user.id]["smith"]))
                                            await client.say("{} has leveled up the SMITH skill to {}"
                                                             .format(user.mention, skilltree[user.id]["smith"]))
                                        # Character Level
                                        actions = 10
                                        user_level = users[user.id]["level"]
                                        await update_data.level_up(client, user, users, actions)
                                        if user_level < users[user.id]["level"]:
                                            await client.say("{} has leveled up to level {}\n"
                                                             "Rewards: ${}"
                                                             .format(user.mention, users[user.id]["level"],
                                                                     icons["icon"]["cash"]))
                                    # Canceling Message
                                    else:
                                        await client.say("{}, crafting canceled.".format(user.mention))
                                # No Resources Message
                                else:
                                    await client.say("{}, you don't have enough resources!".format(user.mention))
                            # Rope & Planks
                            elif user_reaction.reaction.emoji == "6⃣" or user_reaction.reaction.emoji == "7⃣":
                                # Workbench Embed Submenu
                                cra = discord.Embed(
                                    title="{}'s Workbench Menu".format(user.name),
                                    description="{} **Craft 1:**\n"
                                                "{} **Craft 5:**\n"
                                                "{} **Craft All:**".format(reaction_1, reaction_2, reaction_3),
                                    colour=discord.Colour.darker_grey())
                                cra.set_author(name="{}'s Workbench Menu".format(player_name), icon_url=player_avatar_url)
                                cra.set_thumbnail(
                                    url="https://cdn.discordapp.com/attachments/538124566527213598/540471921721212946/crafting.png")
                                cra.set_image(url=bot_icon)
                                cra.set_footer(text=server_name)

                                # Add Reactions
                                await client.delete_message(workbench_menu)
                                workbench_menu = await client.say(embed=cra)
                                await client.add_reaction(workbench_menu, reaction_1)
                                await client.add_reaction(workbench_menu, reaction_2)
                                await client.add_reaction(workbench_menu, reaction_3)
                                user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣'],
                                                                               message=workbench_menu, timeout=10)
                                if user_reaction is None:
                                    await client.say("{}, crafting canceled!".format(user.mention))

                                if user_reaction.reaction.emoji == "1⃣":
                                    amount_res = 1 * amount_res
                                    possible_crafts = 1
                                elif user_reaction.reaction.emoji == "2⃣":
                                    amount_res = 5 * amount_res
                                    possible_crafts = 5
                                elif user_reaction.reaction.emoji == "3⃣":
                                    possible_crafts = type_res // amount_res
                                    amount_res = possible_crafts * amount_res

                                # Delete Embed
                                await client.delete_message(workbench_menu)

                                # Convert to Int
                                amount_res = int(amount_res)
                                possible_crafts = int(possible_crafts)

                                # Add Experience & Resources
                                if amount_res <= type_res > 0:
                                    # Add Stuff
                                    resources[user.id][res_name] -= amount_res
                                    resources[user.id][yield_name] += possible_crafts
                                    await client.say("{}, you crafted {} {} {} "
                                                     "using {}{} {}."
                                                     .format(user.mention, yield_emo, possible_crafts, yield_name,
                                                             res_emo, amount_res, res_name))
                                    # Add Experience
                                    amount_countdown = possible_crafts
                                    xp_per_craft = 2
                                    user_level = users[user.id]["level"]
                                    skill_level = skilltree[user.id]["smith"]
                                    while amount_countdown > 0:
                                        amount_countdown -= 1
                                        # Skill Level
                                        skilltree[user.id]["smith_exp"] += xp_per_craft
                                        skilltree[user.id]["smith_exp"] = int(skilltree[user.id]["smith_exp"])
                                        if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                                            skilltree[user.id]["smith"] += 1
                                            skilltree[user.id]["smith_exp"] = 0
                                            skilltree[user.id]["smith_exp_need"] = int(base_xp + (
                                                    xp_per_craft * 5 * skilltree[user.id]["smith"]))
                                        # Character Level
                                        actions = 2
                                        await update_data.level_up(client, user, users, actions)

                                    # Skill Level Up Message
                                    if skill_level < skilltree[user.id]["smith"]:
                                        await client.say("{} has leveled up the SMITH skill to {}"
                                                         .format(user.mention, skilltree[user.id]["smith"]))
                                    # Player Level Up Message
                                    if user_level < users[user.id]["level"]:
                                        await client.say("{} has leveled up to level {}\n"
                                                         "Rewards: ${}"
                                                         .format(user.mention, users[user.id]["level"],
                                                                 icons["icon"]["cash"]))
                                else:
                                    await client.say("{}, you don't have enough resources!".format(user.mention))
                # No Workbench Message
                else:
                    await client.say("{}, you don't own a workbench!".format(user.mention))


            # Furnace
            elif item == "furnace" or item == "Furnace" or item == "furn":
                if user_plot[user.id]["furnace"]:

                    # Execute Embed
                    furnace_menu = await client.say(embed=cra)

                    # Add Reactions
                    await client.add_reaction(furnace_menu, reaction_1)
                    await client.add_reaction(furnace_menu, reaction_2)
                    await client.add_reaction(furnace_menu, reaction_3)

                    # Wait for User Reaction
                    user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣'],
                                                                   message=furnace_menu,
                                                                   timeout=10)
                    if user_reaction is None:
                        await client.say("{}, crafting canceled!".format(user.mention))

                    # Furnace Embed Submenu
                    cra = discord.Embed(
                        title="{}'s Furnace Menu".format(user.name),
                        description="{} **Craft 1:**\n"
                                    "{} **Craft 5:**\n"
                                    "{} **Craft All:**".format(reaction_1, reaction_2, reaction_3),
                        colour=discord.Colour.darker_grey())
                    cra.set_author(name="{}'s Furnace Menu".format(player_name), icon_url=player_avatar_url)
                    cra.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/538124566527213598/540471921721212946/crafting.png")
                    cra.set_image(url=bot_icon)
                    cra.set_footer(text=server_name)

                    # 1: Copper
                    if user_reaction.reaction.emoji == "1⃣":
                        coal_per_bar = coal_per_copper
                        ore_per_bar = copper_per_bar
                        uore = resources[user.id]["copper_ore"]
                        ore = "copper_ore"
                        bar = "copper_bar"
                        emo_ore = icons["icon"]["copper_ore"],
                        name_ore = "Copper Ore"
                        emo_bar = icons["icon"]["copper_bar"],
                        name_bar = "Copper Bar"

                    # 2: Iron
                    elif user_reaction.reaction.emoji == "2⃣":
                        coal_per_bar = coal_per_iron
                        ore_per_bar = iron_per_bar
                        uore = resources[user.id]["iron_ore"]
                        ore = "iron_ore"
                        bar = "iron_bar"
                        emo_ore = icons["icon"]["iron_ore"],
                        name_ore = "Iron Ore"
                        emo_bar = icons["icon"]["iron_bar"],
                        name_bar = "Iron Ore"

                    # 3: Gold
                    elif user_reaction.reaction.emoji == "3⃣":
                        coal_per_bar = coal_per_gold
                        ore_per_bar = gold_per_bar
                        uore = resources[user.id]["gold_ore"]
                        ore = "gold_ore"
                        bar = "gold_bar"
                        emo_ore = icons["icon"]["gold_ore"],
                        name_ore = "Gold Ore"
                        emo_bar = icons["icon"]["gold_bar"],
                        name_bar = "Gold Bar"

                    # Add Reactions
                    await client.delete_message(furnace_menu)
                    furnace_menu = await client.say(embed=cra)
                    await client.add_reaction(furnace_menu, reaction_1)
                    await client.add_reaction(furnace_menu, reaction_2)
                    await client.add_reaction(furnace_menu, reaction_3)
                    user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣'],
                                                                   message=furnace_menu,
                                                                   timeout=10)
                    if user_reaction is None:
                        await client.say("{}, crafting canceled!".format(user.mention))

                    # Smelting
                    if user_reaction.reaction.emoji == "1⃣":
                        amount_coal = 1 * coal_per_bar
                        amount_ore = 1 * ore_per_bar
                        possible_crafts = 1
                    elif user_reaction.reaction.emoji == "2⃣":
                        amount_coal = 5 * coal_per_bar
                        amount_ore = 5 * ore_per_bar
                        possible_crafts = 5
                    elif user_reaction.reaction.emoji == "3⃣":
                        possible_ore_crafts = uore // ore_per_bar
                        possible_coal_crafts = resources[user.id]["coal"] // coal_per_bar
                        if possible_coal_crafts >= possible_ore_crafts:
                            possible_crafts = possible_ore_crafts
                        else:
                            possible_crafts = possible_coal_crafts
                        amount_coal = possible_crafts * coal_per_bar
                        amount_ore = possible_crafts * ore_per_bar

                    # Delete Embed
                    await client.delete_message(furnace_menu)

                    # Convert to Int
                    amount_coal = int(amount_coal)
                    amount_ore = int(amount_ore)
                    possible_crafts = int(possible_crafts)

                    # Add Experience & Resources
                    if amount_coal <= resources[user.id]["coal"] and amount_ore <= uore:
                        skill_level = skilltree[user.id]["smith"]
                        user_level = users[user.id]["level"]
                        amount_countdown = possible_crafts
                        while amount_countdown > 0:
                            amount_countdown -= 1
                            # Level Up Character
                            actions = 1
                            await update_data.level_up(client, user, users, actions)
                            # Level Up Skill
                            skilltree[user.id]["smith_exp"] += ore_per_bar
                            if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                                skilltree[user.id]["smith"] += 1
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = base_xp + (
                                            xp_per_smelting * skilltree[user.id]["smith"])
                        # Level Cap
                        if skilltree[user.id]["smith"] >= 100:
                            skilltree[user.id]["smith"] = 100
                            skilltree[user.id]["smith_exp"] = 0
                            skilltree[user.id]["smith_exp_need"] = 0
                        # Level Up Message
                        elif skill_level < skilltree[user.id]["smith"]:
                            await client.say("{} has leveled up the SMITH skill to {}!".format(user.mention,
                                                                                               skilltree[user.id]["smith"]))
                        # Player Level Up Message
                        if user_level < users[user.id]["level"]:
                            await client.say("{} has leveled up to level {}\n"
                                             "Rewards: ${}"
                                             .format(user.mention, users[user.id]["level"], icons["icon"]["cash"]))
                        # Add Stuff
                        resources[user.id]["coal"] -= amount_coal
                        resources[user.id][ore] -= amount_ore
                        end_yield = math.ceil(possible_crafts * (0.5 + (0.015 * skilltree[user.id]["smith"])))
                        end_yield = int(end_yield)
                        resources[user.id][bar] += end_yield
                        await client.say("{}, you smelted down {}{} {} using {}{} Coal and {}{} {}."
                                         .format(user.mention, emo_bar, end_yield, name_bar,
                                                 icons["icon"]["coal"], amount_coal, emo_ore, amount_ore, name_ore))
                    else:
                        await client.say("{}, you don't have enough resources!".format(user.mention))

                else:
                    await client.say("{}, you don't own a furnace!".format(user.mention))
        # Location
        else:
            await client.say("{}, you must be at your base to use a machine!".format(user.mention))

    # Too Hungry Message
    else:
        await client.say("{}, you're too hungry to do that!".format(user.mention))
