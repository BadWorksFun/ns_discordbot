import discord
from discord.ext.commands import bot

import update_data


async def craft(client: bot, ctx, users, resources, equipment, skilltree, icons):
    # User
    user = ctx.message.author
    # Craft Quality
    if skilltree[user.id]["smith"] < 20:
        eq_quality = 0.5
        eq_quality_alias = "Poor"
    elif skilltree[user.id]["smith"] < 40:
        eq_quality = 0.75
        eq_quality_alias = "Handy"
    elif skilltree[user.id]["smith"] < 60:
        eq_quality = 1
        eq_quality_alias = "Balanced"
    elif skilltree[user.id]["smith"] < 80:
        eq_quality = 1.25
        eq_quality_alias = "Masterpiece"
    elif skilltree[user.id]["smith"] <= 100:
        eq_quality = 1.5
        eq_quality_alias = "Perfect"

    if users[user.id]["nourishment"] >= 20:
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

        # Craft Variables
        base_xp = 30
        xp_per_craft = 10  # 5 as a base for level calculation / 2 for fibre

        # Description Title, Description Text, Side Colour
        cra = discord.Embed(
            title="Crafting Menu",
            description="{} Tools\n"
                        "{} Weapons\n"
                        "{} Armour\n"
                        "{} Miscellaneous".format(reaction_1, reaction_2, reaction_3, reaction_4),
            colour=discord.Colour.darker_grey()
        )

        # Embed Variables
        player_name = ctx.message.author.name
        player_avatar_url = ctx.message.author.avatar_url
        server_name = ctx.message.server.name
        bot_icon = "https://cdn.discordapp.com/attachments/538124566527213598/539066367375048737/NGB-Logo.png"
        cra.set_thumbnail(url="https://cdn.discordapp.com/attachments/538124566527213598/540471921721212946/crafting.png")
        cra.set_image(url=bot_icon)
        cra.set_footer(text=server_name)
        cra.set_author(name="{}'s Crafting Menu".format(player_name), icon_url=player_avatar_url)

        # Execute Embed
        crafting_menu = await client.say(embed=cra)

        # Add Reactions
        await client.add_reaction(crafting_menu, reaction_1)
        await client.add_reaction(crafting_menu, reaction_2)
        await client.add_reaction(crafting_menu, reaction_3)
        await client.add_reaction(crafting_menu, reaction_4)

        # Wait for User Reaction
        user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣', '4⃣'], message=crafting_menu,
                                                       timeout=timeout)
        if user_reaction is None:
            await client.say("{}, crafting canceled!".format(user.mention))
        # 1: Tools
        elif user_reaction.reaction.emoji == "1⃣":
            await client.delete_message(crafting_menu)

            # Tools Stats & Cost
            wooden_durability = 30
            wooden_yield_boost = 0.5
            stick_cost = 5
            wood_cost = 10
            ustick = resources[user.id]["stick"]
            uwood = resources[user.id]["wood"]

            # Update Embed
            cra = discord.Embed(title="{}'s Tools Crafting Menu".format(user.name),
                                description="=> **Cost:** {}Sticks: {}/{} | {}Wood: {}/{}\n"
                                            "{} **Wooden Axe:** Durability: {}, Yield Boost: {}\n"
                                            "{} **Wooden Pick:** Durability: {}, Yield Boost: {}\n"
                                            "{} **Wooden Shovel:** Durability: {}, Yield Boost: {}\n"
                                            "{} **Wooden Hammer:** Durability: {}, Yield Boost: {}"
                                .format(icons["icon"]["stick"], ustick, stick_cost,
                                        icons["icon"]["wood"], uwood, wood_cost,
                                        reaction_1, wooden_durability, wooden_yield_boost,
                                        reaction_2, wooden_durability, wooden_yield_boost,
                                        reaction_3, wooden_durability, wooden_yield_boost,
                                        reaction_4, wooden_durability, wooden_yield_boost),
                                colour=discord.Colour.darker_grey())
            # Execute Embed
            tools_crafting_menu = await client.say(embed=cra)

            # Add Reactions
            await client.add_reaction(tools_crafting_menu, reaction_1)
            await client.add_reaction(tools_crafting_menu, reaction_2)
            await client.add_reaction(tools_crafting_menu, reaction_3)
            await client.add_reaction(tools_crafting_menu, reaction_4)

            # Wait for User Reaction
            user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣', '4⃣'],
                                                           message=tools_crafting_menu, timeout=timeout)
            if user_reaction is None:
                await client.say("{}, crafting canceled!".format(user.mention))

            # Tools Variables
            if user_reaction.reaction.emoji == "1⃣":
                emo = "1⃣"
                eq_tool = "axe"
                tool_name = "Wooden Axe"
                tool_dur_name = "axe_durability"
                tool_yield_name = "axe_yield_boost"
                eq_quality_name = "axe_quality"
            elif user_reaction.reaction.emoji == "2⃣":
                emo = "2⃣"
                eq_tool = "pickaxe"
                tool_name = "Wooden Pickaxe"
                tool_dur_name = "pickaxe_durability"
                tool_yield_name = "pickaxe_yield_boost"
                eq_quality_name = "pickaxe_quality"
            elif user_reaction.reaction.emoji == "3⃣":
                emo = "3⃣"
                eq_tool = "shovel"
                tool_name = "Wooden Shovel"
                tool_dur_name = "shovel_durability"
                tool_yield_name = "shovel_yield_boost"
                eq_quality_name = "shovel_quality"
            elif user_reaction.reaction.emoji == "4⃣":
                emo = "4⃣"
                eq_tool = "hammer"
                tool_name = "Wooden Hammer"
                tool_dur_name = "hammer_durability"
                tool_yield_name = "hammer_yield_boost"
                eq_quality_name = "hammer_quality"
            # Execute Craft
            if user_reaction.reaction.emoji == emo:
                if ustick >= stick_cost and uwood >= wood_cost:
                    equipped_item = equipment[user.id][eq_tool]
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
                        # Craft Item
                        equipment[user.id][eq_tool] = tool_name
                        equipment[user.id][tool_dur_name] = wooden_durability * eq_quality
                        equipment[user.id][tool_yield_name] = wooden_yield_boost * eq_quality
                        equipment[user.id][eq_quality_name] = eq_quality_alias
                        resources[user.id]["stick"] -= stick_cost
                        resources[user.id]["wood"] -= wood_cost
                        await client.say("{}, you crafted a {} ({})!".format(user.mention, tool_name, eq_quality_alias))
                        # Skill Level
                        skilltree[user.id]["smith_exp"] += xp_per_craft
                        if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                            if skilltree[user.id]["smith"] < 100:
                                skilltree[user.id]["smith"] += 1
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = int(base_xp + (
                                            xp_per_craft / 2 * skilltree[user.id]["smith"]))
                                await client.say("{} has leveled up the SMITH skill to {}"
                                                 .format(user.mention, skilltree[user.id]["smith"]))
                            else:
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = 0
                        # Character Level
                        actions = 10
                        user_level = users[user.id]["level"]
                        await update_data.level_up(client, user, users, actions)
                        if user_level < users[user.id]["level"]:
                            await client.say("{} has leveled up to level {}\n"
                                             "Rewards: ${}\n"
                                             "Increased: {}HP, {}Stamina, {}Travel Power"
                                             .format(user.mention, users[user.id]["level"],
                                                     icons["icon"]["cash"],
                                                     icons["icon"]["hp"], icons["icon"]["stamina"], icons["icon"]["travelpower"]))
                    else:
                        await client.say("{}, crafting canceled.".format(user.mention))
                else:
                    await client.say("{}, you don't have enough materials!\n".format(user.mention))
            # Delete Embed
            await client.delete_message(tools_crafting_menu)

        # 2: Weapons
        elif user_reaction.reaction.emoji == "2⃣":
            await client.delete_message(crafting_menu)

            # Weapons Cost
            ustick = resources[user.id]["stick"]
            stick_cost_sword = 10
            stick_cost_shield = 5
            uwood = resources[user.id]["wood"]
            wood_cost_sword = 5
            wood_cost_shield = 20

            # Weapons Stats
            wooden_sword_attack = 3
            wooden_sword_defense = 0
            wooden_shield_attack = 0
            wooden_shield_defense = 5

            # Weapons Crafting Menu
            cra = discord.Embed(
                title="{}'s Weapons Crafting Menu".format(user.name),
                description="{} **Wooden Sword:** {}{}/{} | {}{}/{} "
                            ":arrow_right: Attack: {}\n"
                            "{} **Wooden Shield:** {}{}/{} | {}{}/{} "
                            ":arrow_right: Defense: {}"
                    .format(reaction_1, icons["icon"]["stick"], ustick, stick_cost_sword,
                            icons["icon"]["wood"], uwood, wood_cost_sword, wooden_sword_attack,
                            reaction_2, icons["icon"]["stick"], ustick, stick_cost_shield,
                            icons["icon"]["wood"], uwood, wood_cost_shield, wooden_shield_defense
                            ), colour=discord.Colour.darker_grey())

            # Execute Embed
            weapons_crafting_menu = await client.say(embed=cra)

            # Add Reactions
            await client.add_reaction(weapons_crafting_menu, reaction_1)
            await client.add_reaction(weapons_crafting_menu, reaction_2)

            # Wait for User Reaction
            user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣'],
                                                           message=weapons_crafting_menu, timeout=timeout)
            if user_reaction is None:
                await client.say("{}, crafting canceled!".format(user.mention))

            # Sword Variables
            if user_reaction.reaction.emoji == "1⃣":
                emo = "1⃣"
                stick_cost = stick_cost_sword
                wood_cost = wood_cost_sword
                eq_item = "mainhand"
                item_name = "Wooden Sword"
                item_attack = wooden_sword_attack
                item_attack_name = "mainhand_attack"
                item_defense = wooden_sword_defense
                item_defense_name = "mainhand_defense"
                eq_quality_name = "mainhand_quality"
            # Shield Variables
            elif user_reaction.reaction.emoji == "2⃣":
                emo = "2⃣"
                stick_cost = stick_cost_shield
                wood_cost = wood_cost_shield
                eq_item = "offhand"
                item_name = "Wooden Shield"
                item_attack = wooden_shield_attack
                item_attack_name = "offhand_attack"
                item_defense = wooden_shield_defense
                item_defense_name = "offhand_defense"
                eq_quality_name = "offhand_quality"
            # Execute Craft
            if user_reaction.reaction.emoji == emo:
                if ustick >= stick_cost and uwood >= wood_cost:
                    equipped_item = equipment[user.id][eq_item]
                    craft_check = True
                    if equipped_item != "Empty Slot":
                        await client.say("{}, you already have a {} equipped, do you want to replace it? "
                                         "Type 'yes' to confirm!"
                                         .format(user.mention, equipped_item))
                        msg = await client.wait_for_message(author=user, timeout=timeout)
                        if msg.content == "yes":
                            craft_check = True
                        elif msg.content == "no":
                            craft_check = False
                        else:
                            craft_check = False
                    if craft_check:
                        equipment[user.id][eq_item] = item_name
                        equipment[user.id][eq_quality_name] = eq_quality_alias
                        # Attack
                        users[user.id]["attack"] -= equipment[user.id][item_attack_name]
                        equipment[user.id][item_attack_name] = item_attack
                        users[user.id]["attack"] += int(equipment[user.id][item_attack_name] * eq_quality)
                        # Defense
                        users[user.id]["defense"] -= equipment[user.id][item_defense_name]
                        equipment[user.id][item_defense_name] = item_defense
                        users[user.id]["defense"] += int(equipment[user.id][item_defense_name] * eq_quality)
                        # Cost
                        resources[user.id]["stick"] -= stick_cost
                        resources[user.id]["wood"] -= wood_cost
                        await client.say("{}, you crafted a {} ({})!".format(user.mention, item_name, eq_quality_alias))

                        # Skill Level
                        skilltree[user.id]["smith_exp"] += xp_per_craft
                        if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                            if skilltree[user.id]["smith"] < 100:
                                skilltree[user.id]["smith"] += 1
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = int(base_xp + (
                                        xp_per_craft / 2 * skilltree[user.id]["smith"]))
                                await client.say("{} has leveled up the SMITH skill to {}"
                                                 .format(user.mention, skilltree[user.id]["smith"]))
                            else:
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = 0
                        # Character Level
                        actions = 10
                        user_level = users[user.id]["level"]
                        await update_data.level_up(client, user, users, actions)
                        if user_level < users[user.id]["level"]:
                            await client.say("{} has leveled up to level {}\n"
                                             "Rewards: ${}\n"
                                             "Increased: {}HP, {}Stamina, {}Travel Power"
                                             .format(user.mention, users[user.id]["level"],
                                                     icons["icon"]["cash"],
                                                     icons["icon"]["hp"], icons["icon"]["stamina"], icons["icon"]["travelpower"]))
                    else:
                        await client.say("{}, crafting canceled.".format(user.mention))
                else:
                    await client.say("{}, you don't have enough materials!\n".format(user.mention,))
            # Delete Embed
            await client.delete_message(weapons_crafting_menu)

        # 3: Armour
        elif user_reaction.reaction.emoji == "3⃣":
            await client.delete_message(crafting_menu)

            # Armour Cost
            wood_head_cost = 10
            wood_chest_cost = 50
            wood_feet_cost = 8
            fibre_head_cost = 10
            fibre_chest_cost = 10
            fibre_feet_cost = 10
            uwood = resources[user.id]["wood"]
            ufibre = resources[user.id]["fibre"]

            # Armour Stats
            chest_defense = 2
            head_defense = 1
            feet_defense = 1

            # Armour Crafting Menu
            cra = discord.Embed(
                title="{}'s Armour Crafting Menu".format(user.name),
                description="{} Wooden Helmet: {}{}/{} | {}{}/{}\n"
                            "{} Wooden Breastplate: {}{}/{} | {}{}/{}\n"
                            "{} Wooden Boots: {}{}/{} | {}{}/{}\n"
                    .format(reaction_1, icons["icon"]["wood"], uwood, wood_head_cost,
                            icons["icon"]["fibre"], ufibre, fibre_head_cost,
                            reaction_2, icons["icon"]["wood"], uwood, wood_chest_cost,
                            icons["icon"]["fibre"], ufibre, fibre_chest_cost,
                            reaction_3, icons["icon"]["wood"], uwood, wood_feet_cost,
                            icons["icon"]["fibre"], ufibre, fibre_feet_cost),
                colour=discord.Colour.darker_grey())

            # Execute Embed
            armour_crafting_menu = await client.say(embed=cra)

            # Add Reactions
            await client.add_reaction(armour_crafting_menu, reaction_1)
            await client.add_reaction(armour_crafting_menu, reaction_2)
            await client.add_reaction(armour_crafting_menu, reaction_3)

            # Wait for User Reaction
            user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣'],
                                                           message=armour_crafting_menu, timeout=timeout)
            if user_reaction is None:
                await client.say("{}, crafting canceled!".format(user.mention))

            # Option Variables
            if user_reaction.reaction.emoji == "1⃣":
                fibre_cost = fibre_head_cost
                wood_cost = wood_head_cost
                emo = "1⃣"
                eq_armour = "head"
                armour_name = "Wooden Helmet"
                armour_def = "head_defense"
                def_stat = head_defense
                eq_quality_name = "head_quality"
            elif user_reaction.reaction.emoji == "2⃣":
                fibre_cost = fibre_chest_cost
                wood_cost = wood_chest_cost
                emo = "2⃣"
                eq_armour = "chest"
                armour_name = "Wooden Breastplate"
                armour_def = "chest_defense"
                def_stat = chest_defense
                eq_quality_name = "chest_quality"
            elif user_reaction.reaction.emoji == "3⃣":
                fibre_cost = fibre_feet_cost
                wood_cost = wood_feet_cost
                emo = "3⃣"
                eq_armour = "feet"
                armour_name = "Wooden Boots"
                armour_def = "feet_defense"
                def_stat = feet_defense
                eq_quality_name = "feet_quality"

            # Armour
            if user_reaction.reaction.emoji == emo:
                if ufibre >= fibre_cost and uwood >= wood_cost:
                    equipped_armour = equipment[user.id][eq_armour]
                    craft_check = True
                    if equipped_armour != "Empty Slot":
                        await client.say("{}, you already have a {} equipped, do you want to replace it? "
                                         "Type 'yes' to confirm or 'no' to cancel!"
                                         .format(user.mention, equipped_armour))
                        msg = await client.wait_for_message(author=user, timeout=timeout)
                        if msg.content == "yes":
                            craft_check = True
                        elif msg.content == "no":
                            craft_check = False
                        else:
                            craft_check = False
                    if craft_check:
                        equipment[user.id][eq_armour] = armour_name
                        equipment[user.id][eq_quality_name] = eq_quality_alias
                        # Defense
                        users[user.id]["defense"] -= equipment[user.id][armour_def]
                        equipment[user.id][armour_def] = def_stat
                        users[user.id]["defense"] += int(equipment[user.id][armour_def]) * eq_quality
                        # Cost
                        resources[user.id]["wood"] -= wood_cost
                        resources[user.id]["fibre"] -= fibre_cost
                        await client.say("{}, you crafted a {}!".format(user.mention, armour_name))

                        # Skill Level
                        skilltree[user.id]["smith_exp"] += xp_per_craft
                        if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                            if skilltree[user.id]["smith"] < 100:
                                skilltree[user.id]["smith"] += 1
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = int(base_xp + (
                                        xp_per_craft / 2 * skilltree[user.id]["smith"]))
                                await client.say("{} has leveled up the SMITH skill to {}"
                                                 .format(user.mention, skilltree[user.id]["smith"]))
                            else:
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = 0
                        # Character Level
                        actions = 10
                        user_level = users[user.id]["level"]
                        await update_data.level_up(client, user, users, actions)
                        if user_level < users[user.id]["level"]:
                            await client.say("{} has leveled up to level {}\n"
                                             "Rewards: ${}\n"
                                             "Increased: {}HP, {}Stamina, {}Travel Power"
                                             .format(user.mention, users[user.id]["level"], icons["icon"]["cash"],
                                                     icons["icon"]["hp"], icons["icon"]["stamina"], icons["icon"]["travelpower"]))
                    else:
                        await client.say("{}, crafting canceled.".format(user.mention))
                else:
                    await client.say("{}, you don't have enough materials!\n".format(user.mention))

            # Delete Embed
            await client.delete_message(armour_crafting_menu)

        # 4: Miscellaneous
        elif user_reaction.reaction.emoji == "4⃣":
            await client.delete_message(crafting_menu)

            # Miscellaneous Crafting Menu
            cra = discord.Embed(
                title="{}'s Miscellaneous Crafting Menu".format(user.name),
                description="{} Bandages: {}Fibre: {}/10)\n"
                            "{} Option 2\n"
                            "{} Option 3".format(reaction_1, icons["icon"]["fibre"], resources[user.id]["fibre"],
                                                 reaction_2, reaction_3),
                colour=discord.Colour.darker_grey()
            )

            # Execute Embed
            miscellaneous_crafting_menu = await client.say(embed=cra)

            # Add Reactions
            await client.add_reaction(miscellaneous_crafting_menu, reaction_1)
            await client.add_reaction(miscellaneous_crafting_menu, reaction_2)
            await client.add_reaction(miscellaneous_crafting_menu, reaction_3)

            # Wait for User Reaction
            user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣'],
                                                           message=miscellaneous_crafting_menu, timeout=timeout)
            if user_reaction is None:
                await client.say("{}, crafting canceled!".format(user.mention))

            # 1: Bandages
            if user_reaction.reaction.emoji == "1⃣":
                ubandage = users[user.id]["bandage"]
                ubandagemax = users[user.id]["bandagemax"]
                bandages_needed = ubandagemax - ubandage
                ufibre = resources[user.id]["fibre"]
                possible_crafts = (ufibre / 10)
                possible_crafts = int(possible_crafts)
                if possible_crafts >= bandages_needed:
                    users[user.id]["bandage"] += bandages_needed
                    final_amount = bandages_needed
                else:
                    users[user.id]["bandage"] += possible_crafts
                    final_amount = possible_crafts

                if final_amount > 0:
                    final_amount = int(final_amount)
                    cost_fibre = final_amount * 10
                    resources[user.id]["fibre"] -= cost_fibre
                    await client.say("{}, you were able to craft {}{} Bandage(s) using {}{} Fibre"
                                     .format(user.mention, icons["icon"]["bandage"], final_amount,
                                             icons["icon"]["fibre"], cost_fibre))
                    # Add Experience
                    amount_countdown = final_amount
                    user_level = users[user.id]["level"]
                    skill_level = skilltree[user.id]["smith"]
                    while amount_countdown > 0:
                        amount_countdown -= 1
                        # Skill Level
                        skilltree[user.id]["smith_exp"] += xp_per_craft/5
                        skilltree[user.id]["smith_exp"] = int(skilltree[user.id]["smith_exp"])
                        if skilltree[user.id]["smith_exp"] >= skilltree[user.id]["smith_exp_need"]:
                            if skilltree[user.id]["smith"] < 100:
                                skilltree[user.id]["smith"] += 1
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = int(base_xp + (
                                        xp_per_craft / 2 * skilltree[user.id]["smith"]))
                            else:
                                skilltree[user.id]["smith_exp"] = 0
                                skilltree[user.id]["smith_exp_need"] = 0
                        # Character Level
                        actions = 10
                        await update_data.level_up(client, user, users, actions)

                    # Skill Level Up Message
                    if skill_level < skilltree[user.id]["smith"]:
                        await client.say("{} has leveled up the SMITH skill to {}"
                                         .format(user.mention, skilltree[user.id]["smith"]))
                    # Player Level Up Message
                    if user_level < users[user.id]["level"]:
                        await client.say("{} has leveled up to level {}\n"
                                         "Rewards: ${}\n"
                                         "Increased: {}HP, {}Stamina, {}Travel Power"
                                         .format(user.mention, users[user.id]["level"], icons["icon"]["cash"],
                                                 icons["icon"]["hp"], icons["icon"]["stamina"], icons["icon"]["travelpower"]))

                else:
                    await client.say("{}, you don't have enough materials or you are full on {}Bandages."
                                     .format(user.mention, icons["icon"]["bandage"]))

            # 2: Option 2
            elif user_reaction.reaction.emoji == "2⃣":
                await client.send_message(ctx.message.channel,
                                          "{0.user} reacted with {0.reaction.emoji}".format(user_reaction))

            # 3: Option 3
            elif user_reaction.reaction.emoji == "3⃣":
                await client.send_message(ctx.message.channel,
                                          "{0.user} reacted with {0.reaction.emoji}".format(user_reaction))

            # Delete Embed
            await client.delete_message(miscellaneous_crafting_menu)

    # Too Hungry Message
    else:
        await client.say("{}, you're too hungry to do that!".format(user.mention))
