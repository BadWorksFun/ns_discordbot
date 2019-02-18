import discord
from discord.ext.commands import bot
import random

import update_data


async def battle(client: bot, ctx, users, resources, skilltree):
    # User
    user = ctx.message.author
    player_death = False
    player_action = ""
    users[user.id]["escaped"] = False
    user_attack_formula = int(skilltree[user.id]["attack"] + (users[user.id]["attack"] * users[user.id]["level"] / 5))
    user_defense_formula = int(
        skilltree[user.id]["defense"] / 5 + (users[user.id]["defense"] * users[user.id]["level"] / 20)) + 1

    # Enemies
    enemies = ["Bunny", "Deer", "Wolf"]
    enemy = random.choice(enemies)
    enemy_death = False
    enemy_action = ""

    # Fight Statistics
    lvl_randomizer = random.randint(75, 125) / 100
    distance = "Melee"

    # Enemy Statistics
    enemy_lvl = int(lvl_randomizer * users[user.id]["level"])
    enemy_hp = int(enemy_lvl ** 1.5)
    enemy_attack = int(enemy_lvl / 2) + 1
    enemy_defense = int(lvl_randomizer * user_defense_formula) + 1

    # Enemy Specifics
    if enemy == "Bunny":
        fight_experience = int(enemy_lvl / 2)
        enemy_hp * 0.5
        enemy_attack * 0.5
        enemy_defense * 0.5
    elif enemy == "Deer":
        fight_experience = int(enemy_lvl / 1.5)
        enemy_hp * 0.75
        enemy_attack * 0.75
        enemy_defense * 0.75
    elif enemy == "Wolf":
        fight_experience = int(enemy_lvl / 1)
        enemy_hp * 1
        enemy_attack * 1
        enemy_defense * 1

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

    # Embed
    bat = discord.Embed(
        title="{}'s Battle Status".format(user.name),
        description="You got into a fight with a __**{}**__: *Level: {} | HP: {} "
                    "| Attack: {} | Defense: {}*\n"
                    "__**Your Stats:**__ *Level: {} | HP: {} | Attack: {} | Defense: {} | Bandages: {}*\n"
                    "\n"
                    "{} Start Battle\n"
            .format(enemy, enemy_lvl, enemy_hp, enemy_attack, enemy_defense,
                    users[user.id]["level"], users[user.id]["hp"],
                    user_attack_formula, user_defense_formula, users[user.id]["bandage"],
                    reaction_1,
                    colour=discord.Colour.darker_grey()))

    # Embed Variables
    player_name = ctx.message.author.name
    player_avatar_url = ctx.message.author.avatar_url
    server_name = ctx.message.server.name
    bot_icon = "https://cdn.discordapp.com/attachments/538124566527213598/539066367375048737/NGB-Logo.png"
    bat.set_thumbnail(url="https://cdn.discordapp.com/attachments/541395172622073869/543795494963642383/fighting.jpg")
    bat.set_image(url=bot_icon)
    bat.set_footer(text=server_name)
    bat.set_author(name="{}".format(player_name), icon_url=player_avatar_url)

    # Execute Embed
    battle_menu = await client.say(embed=bat)

    # Add Reactions
    await client.add_reaction(battle_menu, reaction_1)

    # Wait for User Reaction
    user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣'], message=battle_menu,
                                                   timeout=timeout)
    # No Reaction Error (Duplicate, needs optimization!)
    if user_reaction is None:
        battle = False
        users[user.id]["escaped"] = True
        users[user.id]["combat"] = 0
        users[user.id]["in_combat"] = False
        await client.say("{}, you just stood around, got killed and lost all your resources!".format(user.mention))
        users[user.id]["hp"] = users[user.id]["hpmax"]
        users[user.id]["location"] = "Home"
        users[user.id]["location_lvl"] = 0
        await client.delete_message(battle_menu)
        # Punishment
        for res_item in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore",
                         "plank", "rope", "copper_bar", "iron_bar", "gold_bar",
                         "meat", "milk", "eggs", "leather", "wool", "feathers",
                         "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
            # Stash Resources
            resources[user.id][res_item] = 0

    elif user_reaction.reaction.emoji == "1⃣":
        # Add Reactions
        await client.add_reaction(battle_menu, reaction_2)
        await client.add_reaction(battle_menu, reaction_3)
        await client.add_reaction(battle_menu, reaction_4)
        battle = True

    # Battle
    while battle:
        # Embed
        bat = discord.Embed(
            title="{}'s Battle Status".format(user.name),
            description=" __**{}**__'s Stats: *Level: {} | HP: {} | Attack: {} | Defense: {}*\n"
                        "__**Your Stats:**__ *Level: {} | HP: {} | Attack: {} | Defense: {} | Bandages: {}*\n"
                        "\n"
                        "{} Move (Current Distance: {}) (WIP)\n"
                        "{} Melee Attack\n"
                        "{} Ranged Attack (WIP)\n"
                        "{} Use Bandage\n"
                        "\n"
                        "Player: {}\n"
                        "Enemy: {}\n"
                .format(enemy, enemy_lvl, enemy_hp, enemy_attack, enemy_defense,
                        users[user.id]["level"], users[user.id]["hp"],
                        user_attack_formula, user_defense_formula, users[user.id]["bandage"],
                        reaction_1, distance,
                        reaction_2,
                        reaction_3,
                        reaction_4,
                        player_action,
                        enemy_action),
            colour=discord.Colour.darker_grey())
        await client.edit_message(battle_menu, embed=bat)

        # Wait for User Reaction
        user_reaction = await client.wait_for_reaction(user=user, emoji=['1⃣', '2⃣', '3⃣', '4⃣'],
                                                       message=battle_menu,
                                                       timeout=timeout)
        #  Attack
        dmg_randomizer_player = random.randint(75, 125) / 100
        dmg_randomizer_enemy = random.randint(75, 125) / 100
        # Player Attack
        temp_player_attack = dmg_randomizer_player * (user_attack_formula / (enemy_defense / 5))
        temp_player_attack = int(temp_player_attack)
        # Enemy Attack
        temp_enemy_attack = dmg_randomizer_enemy * (enemy_attack / (user_defense_formula / 5))
        temp_enemy_attack = int(temp_enemy_attack)
        # Player Death: No Action
        if user_reaction is None:
            await client.say("{}, You wasted your turn thinking what to do, giving {} the chance to finish you off!"
                             .format(user.mention, enemy))
            battle = False
            users[user.id]["escaped"] = True
            users[user.id]["combat"] = 0
            users[user.id]["in_combat"] = False
            await client.say("{}, you died and lost all your resources!".format(user.mention))
            users[user.id]["hp"] = users[user.id]["hpmax"]
            users[user.id]["location"] = "Home"
            users[user.id]["location_lvl"] = 0
            await client.delete_message(battle_menu)
            # Punishment
            for res_item in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore",
                             "plank", "rope", "copper_bar", "iron_bar", "gold_bar",
                             "meat", "milk", "eggs", "leather", "wool", "feathers",
                             "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
                # Stash Resources
                resources[user.id][res_item] = 0
        else:
            # Attack Option (2)
            if user_reaction.reaction.emoji == "2⃣":
                # User Attack
                enemy_hp -= temp_player_attack
                player_action = "You hit {} for {} hp!".format(enemy, temp_player_attack)
                # Attack Level
                attack_skill = skilltree[user.id]["attack"]
                base_xp = 30
                xp_per_swing = 2
                final_level = skilltree[user.id]["attack"] + 1

                # Attack Skill Level
                skilltree[user.id]["attack_exp"] += xp_per_swing
                if skilltree[user.id]["attack_exp"] >= skilltree[user.id]["attack_exp_need"]:
                    skilltree[user.id]["attack"] += 1
                    skilltree[user.id]["attack_exp"] = 0
                    skilltree[user.id]["attack_exp_need"] = base_xp + (xp_per_swing * final_level)

                if attack_skill < skilltree[user.id]["attack"]:
                    await client.say("{} has leveled up the ATTACK skill to {}"
                                     .format(user.mention, skilltree[user.id]["attack"]))
                # Enemy Death
                if enemy_hp <= 0:
                    enemy_death = True

                # Actions
                enemy_action = "{} hit you for {} hp!".format(enemy, temp_enemy_attack)
                # Defense Level
                defense_skill = skilltree[user.id]["defense"]
                base_xp = 30
                xp_per_hit = 1
                final_level = skilltree[user.id]["defense"] + 1
                skilltree[user.id]["defense_exp"] += xp_per_hit
                if skilltree[user.id]["defense_exp"] >= skilltree[user.id]["defense_exp_need"]:
                    skilltree[user.id]["defense"] += 1
                    skilltree[user.id]["defense_exp"] = 0
                    skilltree[user.id]["defense_exp_need"] = base_xp + (xp_per_hit * final_level)

                if defense_skill < skilltree[user.id]["defense"]:
                    await client.say("{} has leveled up the DEFENSE skill to {}"
                                     .format(user.mention, skilltree[user.id]["defense"]))

            # Use Bandage
            elif user_reaction.reaction.emoji == "4⃣":
                if users[user.id]["bandage"] > 0:
                    users[user.id]["bandage"] -= 1
                    max_heal = users[user.id]["hpmax"] - users[user.id]["hp"]
                    if max_heal >= users[user.id]["bandagehp"]:
                        max_heal = users[user.id]["bandagehp"]
                        users[user.id]["hp"] += max_heal
                    else:
                        users[user.id]["hp"] += max_heal
                    # Actions
                    player_action = "You healed yourself for {} hp!".format(max_heal)
                else:
                    player_action = "You have no bandages and wasted your turn looking for them!"

            # Enemy Attack
            if user_reaction.reaction.emoji == "2⃣" or user_reaction.reaction.emoji == "4⃣":
                if enemy_hp > 0:
                    users[user.id]["hp"] -= temp_enemy_attack
                    enemy_action = "{} hit you for {} hp!".format(enemy, temp_enemy_attack)
                    if users[user.id]["hp"] <= 0 or user_reaction is None:
                        player_death = True

            # Player Death
            if player_death:
                battle = False
                users[user.id]["escaped"] = True
                users[user.id]["combat"] = 0
                users[user.id]["in_combat"] = False
                await client.say("{}, you died and lost all your resources!".format(user.mention))
                users[user.id]["hp"] = users[user.id]["hpmax"]
                users[user.id]["location"] = "Home"
                users[user.id]["location_lvl"] = 0
                await client.delete_message(battle_menu)
                # Punishment
                for res_item in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore",
                                 "plank", "rope", "copper_bar", "iron_bar", "gold_bar",
                                 "meat", "milk", "eggs", "leather", "wool", "feathers",
                                 "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
                    # Stash Resources
                    resources[user.id][res_item] = 0

            elif enemy_death:
                battle = False
                await client.say("{}, {} died!".format(user.mention, enemy))
                await client.delete_message(battle_menu)
                users[user.id]["combat"] -= 1
                if users[user.id]["combat"] <= 0:
                    users[user.id]["escaped"] = True
                    users[user.id]["combat"] = 0
                    users[user.id]["in_combat"] = False
                else:
                    users[user.id]["in_combat"] = False

                # Rewards
                actions = fight_experience
                await update_data.level_up(client, user, users, actions)
                await client.say("{}, you received {} experience points!".format(user.mention, fight_experience))
