from discord.ext.commands import bot


# Level Up
async def level_up(client: bot, user, users, actions):

    if users[user.id]["level"] < 100:
        base_xp = 95
        users[user.id]["experience"] += actions
        experience = users[user.id]["experience"]
        current_level = users[user.id]["level"]
        final_level = current_level + 1
        final_exp = base_xp + (5 * final_level)
        xp_requirements = base_xp + (5 * current_level)
        if experience > xp_requirements:
            ucash = (10+(10*final_level))
            users[user.id]["level"] = final_level
            users[user.id]["experience"] = 0
            users[user.id]["experience_need"] = final_exp
            users[user.id]["cash"] += ucash
            users[user.id]["hpmax"] = round(final_level ** 1.5)
            users[user.id]["hp"] = users[user.id]["hpmax"]
            users[user.id]["staminamax"] = round(3+(final_level/5))
            users[user.id]["stamina"] = users[user.id]["staminamax"]
            users[user.id]["travelpowermax"] = round(5+(final_level/4))
            users[user.id]["travelpower"] = users[user.id]["travelpowermax"]
            users[user.id]["bandagemax"] = round(5+(final_level/5))
            users[user.id]["bandagehp"] = int(users[user.id]["hp"] / 3)
    else:
        users[user.id]["level"] = 100
        users[user.id]["experience"] = 0
        users[user.id]["experience_need"] = 0


# All User Data
async def update_data_users(client: bot, ctx, users, equipment, resources, skilltree, stash_base, user_plot):

    user = ctx.message.author
    await client.say("{}, your new character has been created!\n"
                     "Use your 10 <:wood:539190599094501398>Wood to craft an axe!".format(user.mention))
    # USERS
    if not user.id in users or user.id in users:
        users[user.id] = {}
        users[user.id]["name"] = user.name
        users[user.id]["turn"] = 1
        users[user.id]["location"] = "Home"
        users[user.id]["location_lvl"] = 0
        users[user.id]["forest_lvl"] = 1
        users[user.id]["mine_lvl"] = 1
        users[user.id]["treasure_lvl"] = 1
        users[user.id]["dungeon_lvl"] = 1

        # Levels
        users[user.id]["experience"] = 0
        users[user.id]["experience_need"] = 100
        users[user.id]["level"] = 1

        # Economy
        users[user.id]["cash"] = 0

        # Character
        users[user.id]["hp"] = 3
        users[user.id]["hpmax"] = 3
        users[user.id]["stamina"] = 4
        users[user.id]["staminamax"] = 4
        users[user.id]["travelpower"] = 5
        users[user.id]["travelpowermax"] = 5
        users[user.id]["nourishment"] = 100
        users[user.id]["attack"] = 0
        users[user.id]["defense"] = 0

        # Base
        users[user.id]["base_activated"] = False

        # Combat
        users[user.id]["combat"] = 0
        users[user.id]["in_combat"] = False
        users[user.id]["escaped"] = True
        users[user.id]["bandage"] = 0
        users[user.id]["bandagemax"] = 5
        users[user.id]["bandagehp"] = int(users[user.id]["hp"] / 3)

    # EQUIPMENT
    if not user.id in equipment or user.id in equipment:
        # User
        equipment[user.id] = {}
        equipment[user.id]["name"] = user.name

        # Equipment Names
        for name in ("head", "shoulders", "chest", "hands", "legs", "feet",
                     "mainhand", "offhand", "ranged", "ring",
                     "pickaxe", "axe", "shovel", "hammer"):
            equipment[user.id][name] = "Empty Slot"

        # Equipment Stats
        for stats in ("head_defense", "shoulders_defense", "chest_defense", "hands_defense", "legs_defense", "feet_defense",
                      "mainhand_attack", "mainhand_defense", "offhand_attack", "offhand_defense",
                      "pickaxe_durability", "axe_durability", "shovel_durability", "hammer_durability",
                      "pickaxe_yield_boost", "axe_yield_boost", "shovel_yield_boost", "hammer_yield_boost"):
            equipment[user.id][stats] = 0

        # Quality Stats
        for quality in ("head_quality", "shoulders_quality", "chest_quality", "hands_quality", "legs_quality",
                        "feet_quality", "mainhand_quality", "offhand_quality", "ranged_quality", "ring_quality",
                        "axe_quality", "pickaxe_quality", "shovel_quality", "hammer_quality"):
            equipment[user.id][quality] = "None"

        # Equipment Enchantments
        for enchantment in ("head_enchantment", "shoulders_enchantment", "chest_enchantment", "hands_enchantment", "legs_enchantment", "feet_enchantment",
                            "mainhand_enchantment", "offhand_enchantment", "ranged_enchantment", "ring_enchantment"):
            equipment[user.id][enchantment] = "No Enchantment"

    # RESOURCES
    if not user.id in resources or user.id in resources:

        # User
        resources[user.id] = {}
        resources[user.id]["name"] = user.name

        # Raw Resources
        for name in ("wood", "stone", "coal", "iron_ore", "copper_ore", "gold_ore", "plank", "rope", "copper_bar",
                     "iron_bar", "gold_bar", "meat", "milk", "eggs", "leather", "wool", "feathers", "cows", "sheep",
                     "chickens", "wheat", "potatoes", "apples", "fibre", "stick", "berries"):
            resources[user.id][name] = 0

        # TEMP SOLUTION TO STARTING AXE PROBLEM
        resources[user.id]["wood"] = 10
        resources[user.id]["stick"] = 5

    # STASH BASE
    if not user.id in stash_base or user.id in stash_base:

        # User
        stash_base[user.id] = {}
        stash_base[user.id]["name"] = user.name

        # Raw Resources
        for name in ("wood", "stone", "coal", "copper_ore", "iron_ore", "gold_ore", "plank", "rope", "copper_bar",
                     "iron_bar", "gold_bar", "meat", "milk", "eggs", "leather", "wool", "feathers", "wheat",
                     "potatoes", "apples", "fibre", "stick", "berries"):
            stash_base[user.id][name] = 0

    # SKILLTREE
    if not user.id in skilltree or user.id in skilltree:
        skilltree[user.id] = {}
        skilltree[user.id]["name"] = user.name

        # XP Calculations
        base_xp = 25
        xp_per_action = 5
        xp_requirements = base_xp + (xp_per_action * 1)

        # Skill Names
        for name in ("gathering", "lumbering", "mining", "farming",
                     "trader", "scientist", "engineer", "smith",
                     "attack", "defense"):
            skilltree[user.id][name] = 1
        for exp in ("gathering_exp", "lumbering_exp", "mining_exp", "farming_exp",
                    "trader_exp", "scientist_exp", "engineer_exp", "smith_exp",
                    "attack_exp", "defense_exp"):
            skilltree[user.id][exp] = 0
        for exp_need in ("gathering_exp_need", "lumbering_exp_need", "mining_exp_need", "farming_exp_need",
                         "trader_exp_need", "scientist_exp_need", "engineer_exp_need", "smith_exp_need",
                         "attack_exp_need", "defense_exp_need"):
            skilltree[user.id][exp_need] = xp_requirements

    if not user.id in user_plot or user.id in user_plot:

        # User
        user_plot[user.id] = {}
        user_plot[user.id]["name"] = user.name

        # Plot Setup
        for name in ("plot", "workbench", "furnace"):
            user_plot[user.id][name] = False

