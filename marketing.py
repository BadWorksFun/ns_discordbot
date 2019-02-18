from discord.ext.commands import bot


async def market(client: bot, ctx, users, user, trans, item, amount, equipment, resources, skilltree):
    # Buy Prices
    b_item_1 = "b_item1"
    b_item_1_cost = 49
    b_item_2 = "b_item2"
    b_item_2_cost = 99
    b_item_3 = "b_item3"
    b_item_3_cost = 52

    b_items = [{"name": b_item_1, "cost": b_item_1_cost},
               {"name": b_item_2, "cost": b_item_2_cost},
               {"name": b_item_3, "cost": b_item_3_cost}]

    # Sell Prices
    s_item_1 = "plank"
    s_item_1_cost = 20
    s_item_2 = "coal"
    s_item_2_cost = 13
    s_item_3 = "copper_bar"
    s_item_3_cost = 31

    s_items = [{"name": s_item_1, "cost": s_item_1_cost},
               {"name": s_item_2, "cost": s_item_2_cost},
               {"name": s_item_3, "cost": s_item_3_cost}]

    # Help Message
    if trans is None:
        await client.say("{}, use '.m b' to browse what you can buy and '.m s' to browse what you can sell!"
                         .format(user.mention))
    # Buy
    elif trans == "buy" or trans == "b":
        # Buy List
        if item is None:
            await client.say("{}, you can __buy__ the following things:\n"
                             "**{}** => Cost: {}$\n"
                             "**{}** => Cost: {}$\n"
                             "**{}** => Cost: {}$\n"
                             .format(user.mention, b_item_1, b_item_1_cost, b_item_2, b_item_2_cost,
                                     b_item_3, b_item_3_cost))
        # Buy Item
        elif item in (b_item_1, b_item_2, b_item_3):
            # Convert Amount Number
            if amount is None:
                amount = 1
            try:
                amount = int(amount)
            except ValueError:
                amount = 1
            amount = int(amount)

            # Define Costs
            if item == b_item_1:
                cost = b_item_1_cost
            elif item == b_item_2:
                cost = b_item_2_cost
            elif item == b_item_3:
                cost = b_item_3_cost
            else:
                await client.say("{}, '{}' is not something you can buy!".format(user.mention, item))

            # Execute Buy
            if users[user.id]["cash"] >= cost * amount:
                users[user.id]["cash"] -= cost * amount
                await client.say("{}, you just bought {} {} for {}$!".format(user.mention, amount, item, cost*amount))
            else:
                await client.say("{}, you don't have enough cash!".format(user.mention))
        else:
            await client.say("{}, this item ('{}') doesn't exit!".format(user.mention, item))

    # Sell
    elif trans == "sell" or trans == "s":
        # Sell List
        if item is None:
            await client.say("{}, you can __sell__ the following things:\n"
                             "**{}** => Worth: {}\n"
                             "**{}** => Worth: {}\n"
                             "**{}** => Worth: {}\n"
                             .format(user.mention, s_item_1, s_item_1_cost, s_item_2, s_item_2_cost,
                                     s_item_3, s_item_3_cost))
        # Sell Item
        elif item in (s_item_1, s_item_2, s_item_3):
            all_items = False
            # Convert Amount Number
            if amount is None:
                amount = 1
            elif amount == "a" or amount == "all":
                all_items = True
            try:
                amount = int(amount)
            except ValueError:
                amount = 1
            amount = int(amount)

            # Define Costs
            if item == s_item_1:
                cost = s_item_1_cost
            elif item == s_item_2:
                cost = s_item_2_cost
            elif item == s_item_3:
                cost = s_item_3_cost

            # Execute Sell
            if all_items:
                amount = resources[user.id][item]
            if resources[user.id][item] >= amount:
                resources[user.id][item] -= amount
                users[user.id]["cash"] += cost * amount
                await client.say("{}, you just sold {} {} for {}$!".format(user.mention, amount, item, cost*amount))

            # Not enough resources
            else:
                await client.say("{}, you don't have enough {} to sell.".format(user.mention, item))
        else:
            await client.say("{}, this item ('{}') doesn't exit!".format(user.mention, item))


