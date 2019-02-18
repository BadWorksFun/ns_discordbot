from discord.ext.commands import bot
import random


async def sleep(client: bot, ctx, amount, users, resources, icons):
    # User
    user = ctx.message.author
    users[user.id]["experience"] -= 1

    # Relevant Information
    channel = ctx.message.channel
    ustamina = users[user.id]["stamina"]
    ustaminamax = users[user.id]["staminamax"]
    utravelpower = users[user.id]["travelpower"]
    utravelpowermax = users[user.id]["travelpowermax"]

    # Find Lowest Stat
    potential_amount_stamina = ustaminamax - ustamina
    potential_amount_travelpower = utravelpowermax - utravelpower
    if potential_amount_stamina > potential_amount_travelpower:
        potential_amount = potential_amount_stamina
    else:
        potential_amount = potential_amount_travelpower

    # Check & Convert Input
    if amount == "all":
        amount = potential_amount
    elif amount == "a":
        amount = potential_amount
    elif amount is None:
        amount = 1
    try:
        amount = int(amount)
    except ValueError:
        amount = 1
    if potential_amount <= amount:
        amount = potential_amount
    elif amount <= 0:
        amount = 1
    amount = int(amount)

    # Error Message
    if potential_amount == 0:
        await client.send_message(channel, "{}, you can't sleep anymore!".format(user.mention))

    # Cost & Reward
    if users[user.id]["stamina"] + amount > users[user.id]["staminamax"]:
        amount_stamina = users[user.id]["staminamax"] - users[user.id]["stamina"]
    else:
        amount_stamina = amount
    if users[user.id]["travelpower"] + amount > users[user.id]["travelpowermax"]:
        amount_travelpower = users[user.id]["travelpowermax"] - users[user.id]["travelpower"]
    else:
        amount_travelpower = amount
    users[user.id]["stamina"] += amount_stamina
    users[user.id]["travelpower"] += amount_travelpower

    # Reset if above max
    if users[user.id]["stamina"] > users[user.id]["staminamax"]:
        users[user.id]["stamina"] = users[user.id]["staminamax"]
    if users[user.id]["travelpower"] > users[user.id]["travelpowermax"]:
        users[user.id]["travelpower"] = users[user.id]["travelpowermax"]

    # Main While Loop
    loop_num = amount
    enemies = 0
    food_rot = 0
    while loop_num > 0:
        loop_num -= 1
        users[user.id]["turn"] += 1
        temp_enemies = random.randint(1, 5)
        if temp_enemies == 1 and users[user.id]["level"] > 4 and users[user.id]["location"] != "Home":
            enemies += 1
            users[user.id]["combat"] += 1
        # Turn Check (10)
        turn_check = users[user.id]["turn"] / 20
        if turn_check == int(turn_check):
            food_rot += 1

    # Bot Message
    if amount_stamina > 0 or amount_travelpower > 0:
        await client.send_message(channel, "{}, you gained {}{} Stamina and {}{} Travel Power!\n"
                                           "You slept for {}{} Turn(s) and have {} enemies waiting for you."
                                  .format(user.mention, icons["icon"]["stamina"], amount_stamina,
                                          icons["icon"]["travelpower"], amount_travelpower,
                                          icons["icon"]["turn"], amount, enemies))
    # Food Rot
    temp_berries = 0
    if food_rot > 0:
        while food_rot > 0:
            food_rot -= 1
            loss_randomizer_berries = random.randint(10, 30) / 100
            berry_loss = resources[user.id]["berries"] * loss_randomizer_berries
            berry_loss = int(berry_loss)
            temp_berries += berry_loss
            resources[user.id]["berries"] -= berry_loss
            # Loss Message
            if temp_berries > 0:
                await client.say("{}, {} of your {}Berries have rotten!\n"
                                 "Make sure to stash them in your base or cook them."
                                 .format(user.mention, temp_berries, icons["icon"]["berries"]))
