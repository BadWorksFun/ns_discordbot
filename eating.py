from discord.ext.commands import bot


async def eat(client: bot, ctx, users, resources, food_type, amount, icons):

    # User
    user = ctx.message.author
    nourishment_needed = 100 - users[user.id]["nourishment"]

    # Check Input Food
    if food_type is None:
        await client.say("{}, here's a list of food items you can eat:\n"
                         "{}Berries (1 Nourishment)\n"
                         "{}Apples (5 Nourishment)\n"
                         "...WIP...".format(user.mention, icons["icon"]["berries"], icons["icon"]["apples"]))
    else:
        # Possible Food Items
        if food_type == "berries":
            ufood_amount = resources[user.id]["berries"]
            ufood_nourishment = 1
        elif food_type == "apples":
            ufood_amount = resources[user.id]["apple"]
            ufood_nourishment = 5
        else:
            ufood_amount = 0
            ufood_nourishment = 0
            food_type = "unknown"
        ufood_amount = int(ufood_amount)

        # Check Input Amount
        amount_until_full = nourishment_needed / ufood_nourishment
        if amount_until_full >= ufood_amount:
            amount_until_full = ufood_amount
        if amount == "all":
            amount = amount_until_full
        elif amount == "a":
            amount = amount_until_full
        elif amount is None:
            amount = amount_until_full
        try:
            amount = int(amount)
        except ValueError:
            amount = 1
        amount = int(amount)

        # Food Required
        if users[user.id]["nourishment"] == 100:
            await client.say("{}, you're already full!".format(user.mention))
        elif food_type == "unknown":
            await client.say("{}, this is an unknown type of food, check your spelling!".format(user.mention))
        elif ufood_amount == 0:
            await client.say("{}, you don't have enough of that type of food!".format(user.mention))
        else:
            resources[user.id][food_type] -= amount
            replenished_nourishment = ufood_nourishment * amount
            users[user.id]["nourishment"] += replenished_nourishment
            await client.say("{}, you ate {} food items and replenished {} nourishment!"
                             .format(user.mention, amount, replenished_nourishment))

            # Reset to 100 if to high
            if users[user.id]["nourishment"] > 100:
                users[user.id]["nourishment"] = 100





