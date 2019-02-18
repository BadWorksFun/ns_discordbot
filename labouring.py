from discord.ext.commands import bot
import random
import update_data


async def labour(client: bot, ctx, l_type, amount, users, equipment, resources, skilltree, icons):
    # User
    user = ctx.message.author
    users[user.id]["experience"] -= 1

    # Check Input
    if amount == "all":
        amount = users[user.id]["stamina"]
    elif amount == "a":
        amount = users[user.id]["stamina"]
    elif amount is None:
        amount = 1
    try:
        amount = int(amount)
    except ValueError:
        amount = 1
    amount = int(amount)

    # Labour Variables
    if l_type is None:
        await client.say("{}, please specify a labour (gather/lumber/mine)!".format(user.mention))
    else:
        command_spelling = True
        if l_type == "gather" or l_type == "ga" or l_type == "g":
            l_type = "gather"
            req_loc = "Forest"
            req_eq = "nothing"
            req_skill = "gathering"
            req_skill_exp = "gathering_exp"
            req_skill_exp_need = "gathering_exp_need"
            eq_yield_boost = 1
            mat_1 = "fibre"
            min_mat_1 = (1 + 0.25 * skilltree[user.id]["gathering"]) * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_1 = 3 + 0.5 * skilltree[user.id]["gathering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_2 = "stick"
            min_mat_2 = 1 + 0.25 * skilltree[user.id]["gathering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_2 = 3 + 0.5 * skilltree[user.id]["gathering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_3 = "berries"
            min_mat_3 = 2 + 0.25 * skilltree[user.id]["gathering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_3 = 5 + 0.5 * skilltree[user.id]["gathering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_4 = "nothing"
            min_mat_4 = 0
            max_mat_4 = 0
            mat_5 = "nothing"
            min_mat_5 = 0
            max_mat_5 = 0
        elif l_type == "lumber" or l_type == "lu" or l_type == "l":
            l_type = "lumber"
            req_loc = "Forest"
            req_eq = "axe"
            req_eq_dur = "axe_durability"
            eq_emo = icons["icon"]["axe"]
            req_skill = "lumbering"
            req_skill_exp = "lumbering_exp"
            req_skill_exp_need = "lumbering_exp_need"
            eq_yield_boost = equipment[user.id]["axe_yield_boost"]
            mat_1 = "stick"
            min_mat_1 = 1 + 0.25 * skilltree[user.id]["lumbering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_1 = 2 + 0.5 * skilltree[user.id]["lumbering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_2 = "wood"
            min_mat_2 = 2 + 0.25 * skilltree[user.id]["lumbering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_2 = 3 + 0.5 * skilltree[user.id]["lumbering"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_3 = "nothing"
            min_mat_3 = 0
            max_mat_3 = 0
            mat_4 = "nothing"
            min_mat_4 = 0
            max_mat_4 = 0
            mat_5 = "nothing"
            min_mat_5 = 0
            max_mat_5 = 0
        elif l_type == "mine" or l_type == "mi" or l_type == "m":
            l_type = "mine"
            req_loc = "Mine"
            req_eq = "pickaxe"
            req_eq_dur = "pickaxe_durability"
            eq_emo = icons["icon"]["pickaxe"]
            req_skill = "mining"
            req_skill_exp = "mining_exp"
            req_skill_exp_need = "mining_exp_need"
            eq_yield_boost = equipment[user.id]["pickaxe_yield_boost"]
            mat_1 = "stone"
            min_mat_1 = 2 + 0.25 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_1 = 5 + 0.5 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_2 = "coal"
            min_mat_2 = 1 + 0.25 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_2 = 4 + 0.5 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_3 = "copper_ore"
            min_mat_3 = 1 + 0.25 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_3 = 3 + 0.5 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_4 = "iron_ore"
            min_mat_4 = 0 + 0.25 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_4 = 2 + 0.5 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            mat_5 = "gold_ore"
            min_mat_5 = 0 + 0.25 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
            max_mat_5 = 1 + 0.5 * skilltree[user.id]["mining"] * (0.5 + 0.2 * (users[user.id]["location_lvl"] - 1))
        else:
            await client.say("{}, '{}' is not a valid labour, check your spelling!".format(user.mention, l_type))
            command_spelling = False

        if command_spelling:
            check_location = True
            check_equipment = True
            check_stamina = True
            check_nourishment = True

            # Location check
            if users[user.id]["location"] != req_loc:
                check_location = False
                await client.say("{}, you need to be in the {} for {}, use '.travel {}' to go there!"
                                 .format(user.mention, req_loc, req_skill, req_loc))

            # Equipment Check
            if req_eq != "nothing":
                if equipment[user.id][req_eq] == "Empty Slot":
                    check_equipment = False
                    await client.say("{}, you have no {}! Use .craft to fix that!".format(user.mention, req_eq))

            # Stamina Check
            if users[user.id]["stamina"] < amount or amount <= 0:
                check_stamina = False
                await client.say("{}, check your Stamina! ({}{}/{})"
                                 .format(user.mention, icons["icon"]["stamina"],
                                         users[user.id]["stamina"], users[user.id]["staminamax"]))

            # Nourishment Check
            if users[user.id]["nourishment"] < 20:
                check_nourishment = False
                await client.say("{}, you're too hungry to do that. Use .eat to fix that!".format(user.mention))

            # Calculations
            if check_location and check_equipment and check_stamina and check_nourishment:
                # Stamina Usage
                if users[user.id]["stamina"] >= amount > 0:
                    users[user.id]["stamina"] -= amount
                    # Tool Durability
                    if req_eq != "nothing":
                        equipment[user.id][req_eq_dur] -= amount
                        if equipment[user.id][req_eq_dur] <= 0:
                            equipment[user.id][req_eq] = "Empty Slot"
                            await client.say("{}, your {}{} just broke!".format(user.mention, eq_emo, req_eq))

                    # Reward
                    min_mat_1 = int(min_mat_1)
                    max_mat_1 = int(max_mat_1)
                    min_mat_2 = int(min_mat_2)
                    max_mat_2 = int(max_mat_2)
                    min_mat_3 = int(min_mat_3)
                    max_mat_3 = int(max_mat_3)
                    min_mat_4 = int(min_mat_4)
                    max_mat_4 = int(max_mat_4)
                    min_mat_5 = int(min_mat_5)
                    max_mat_5 = int(max_mat_5)
                    ran_mat_1 = ran_mat_2 = ran_mat_3 = ran_mat_4 = ran_mat_5 = 0
                    amount_countdown = amount
                    # Check User and Skill Level
                    user_level = users[user.id]["level"]
                    skill_level = skilltree[user.id][req_skill]
                    while amount_countdown > 0:
                        amount_countdown -= 1
                        ran_mat_1_temp = round(random.randint(min_mat_1, max_mat_1) * eq_yield_boost)
                        ran_mat_2_temp = round(random.randint(min_mat_2, max_mat_2) * eq_yield_boost)
                        ran_mat_3_temp = round(random.randint(min_mat_3, max_mat_3) * eq_yield_boost)
                        ran_mat_4_temp = round(random.randint(min_mat_4, max_mat_4) * eq_yield_boost)
                        ran_mat_5_temp = round(random.randint(min_mat_5, max_mat_5) * eq_yield_boost)

                        ran_mat_1 += ran_mat_1_temp
                        ran_mat_2 += ran_mat_2_temp
                        ran_mat_3 += ran_mat_3_temp
                        ran_mat_4 += ran_mat_4_temp
                        ran_mat_5 += ran_mat_5_temp

                        # Character Level
                        actions = 5
                        await update_data.level_up(client, user, users, actions)

                        # Skill Level
                        base_xp = 25
                        xp_per_action = 5
                        final_level = skilltree[user.id][req_skill] + 1
                        skilltree[user.id][req_skill_exp] += xp_per_action
                        if skilltree[user.id][req_skill_exp] >= skilltree[user.id][req_skill_exp_need]:
                            skilltree[user.id][req_skill] += 1
                            skilltree[user.id][req_skill_exp] = 0
                            skilltree[user.id][req_skill_exp_need] = base_xp + (xp_per_action * final_level)

                    # Skill Level Up Message
                    if skill_level < skilltree[user.id][req_skill]:
                        await client.say("{}, has leveled up the {} skill to {}!".format(user.mention, req_skill,
                                                                                         skilltree[user.id][req_skill]))

                    # Player Level Up Message
                    if user_level < users[user.id]["level"]:
                        await client.say("{} has leveled up to level {}\n"
                                         "Rewards: ${}\n"
                                         "Increased: {}HP, {}Stamina, {}Travel Power"
                                         .format(user.mention, users[user.id]["level"], icons["icon"]["cash"],
                                                 icons["icon"]["hp"], icons["icon"]["stamina"], icons["icon"]["travelpower"]))

                    # Receive Materials
                    if l_type == "gather":
                        resources[user.id][mat_1] += ran_mat_1
                        resources[user.id][mat_2] += ran_mat_2
                        resources[user.id][mat_3] += ran_mat_3
                        await client.say("{} gathered {} time(s) and collected {}{} Fibre, "
                                         "{}{} Sticks and {}{} Berries, using {}{} Stamina."
                                         .format(user.mention, amount, icons["icon"]["fibre"], ran_mat_1,
                                                 icons["icon"]["stick"], ran_mat_2,
                                                 icons["icon"]["berries"], ran_mat_3,
                                                 icons["icon"]["stamina"], amount))
                    elif l_type == "lumber":
                        resources[user.id][mat_1] += ran_mat_1
                        resources[user.id][mat_2] += ran_mat_2
                        await client.say("{} lumbered {} time(s) and collected {}{} Sticks and "
                                         "{}{} Wood, using {}{} Stamina."
                                         .format(user.mention, amount, icons["icon"]["stick"], ran_mat_1,
                                                 icons["icon"]["wood"], ran_mat_2,
                                                 icons["icon"]["stamina"], amount))
                    elif l_type == "mine":
                        resources[user.id][mat_1] += ran_mat_1
                        resources[user.id][mat_2] += ran_mat_2
                        resources[user.id][mat_3] += ran_mat_3
                        resources[user.id][mat_4] += ran_mat_4
                        resources[user.id][mat_5] += ran_mat_5
                        await client.say("{} mined {} time(s) and collected {}{} Stone, {}{} Coal, {}{} Copper Ore, "
                                         "{}{} Iron Ore, {}{} Gold Ore, using {}{} Stamina."
                                         .format(user.mention, amount, icons["icon"]["stone"], ran_mat_1,
                                                 icons["icon"]["coal"], ran_mat_2,
                                                 icons["icon"]["copper_ore"], ran_mat_3,
                                                 icons["icon"]["iron_ore"], ran_mat_4,
                                                 icons["icon"]["gold_ore"], ran_mat_5,
                                                 icons["icon"]["stamina"], amount))
