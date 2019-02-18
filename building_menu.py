from discord.ext.commands import bot


async def build(client: bot, ctx, item, users, equipment, resources, user_plot, icons):
    user = ctx.message.author
    if users[user.id]["nourishment"] >= 20:
        if users[user.id]["location"] == "Home":
            if equipment[user.id]["hammer"] == "Wooden Hammer" or equipment[user.id]["hammer"] == "Stone Hammer" or equipment[user.id]["hammer"] == "Iron Hammer":
                # Cost & Available Resources
                stick_cost_plot = 75
                stick_cost_workbench = 25
                ustick = resources[user.id]["stick"]
                wood_cost_plot = 75
                wood_cost_workbench = 75
                uwood = resources[user.id]["wood"]
                stone_cost_plot = 150
                stone_cost_furnace = 250
                stone_cost_workbench = 50
                coal_cost_furnace = 100
                ustone = resources[user.id]["stone"]
                berries_cost_plot = 250
                uberries = resources[user.id]["berries"]
                ucoal = resources[user.id]["coal"]

                if item is None:
                    plot_built = user_plot[user.id]["plot"]
                    workbench_built = user_plot[user.id]["workbench"]
                    furnace_built = user_plot[user.id]["furnace"]
                    await client.say("{}, You can build the following items:\n"
                                     # Plot
                                     "__**Plot:**__ *Needed for everything else in your base.* ({})\n:arrow_right:"
                                     "{}Sticks: {}/{}  | {}Wood: {}/{}  | {}Stone: {}/{} | {}Berries: {}/{}\n"
                                     # Workbench
                                     "__**Workbench:**__ *Needed for other base buildings.* ({})\n:arrow_right:"
                                     "{}Sticks: {}/{}  | {}Wood: {}/{}  | {}Stone: {}/{}\n"
                                     # Furnace
                                     "__**Furnace:**__ *Used to smelt ore into bars. ({})\n:arrow_right:"
                                     "{}Stone: {}/{} | {}Coal: {}/{}"
                                     .format(user.mention, plot_built,
                                             icons["icon"]["stick"], ustick, stick_cost_plot,
                                             icons["icon"]["wood"], uwood, wood_cost_plot,
                                             icons["icon"]["stone"], ustone, stone_cost_plot,
                                             icons["icon"]["berries"], uberries, berries_cost_plot,
                                             workbench_built,
                                             icons["icon"]["stick"], ustick, stick_cost_workbench,
                                             icons["icon"]["wood"], uwood, wood_cost_workbench,
                                             icons["icon"]["stone"], ustone, stone_cost_workbench,
                                             furnace_built,
                                             icons["icon"]["stone"], ustone, stone_cost_furnace,
                                             icons["icon"]["coal"], ucoal, coal_cost_furnace))
                # Plot
                elif item == "plot" or item == "Plot":
                    if not user_plot[user.id]["plot"]:
                        if uwood >= wood_cost_plot and ustick >= stick_cost_plot and uberries >= berries_cost_plot and ustone >= stone_cost_plot:
                            user_plot[user.id]["plot"] = True
                            await client.say("{}, you made a building plot!".format(user.mention))
                            resources[user.id]["wood"] -= wood_cost_plot
                            resources[user.id]["stick"] -= stick_cost_plot
                            resources[user.id]["berries"] -= berries_cost_plot
                            resources[user.id]["stone"] -= stone_cost_plot
                        else:
                            await client.say("{}, you don't have enough building materials!".format(user.mention))
                    else:
                        await client.say("{}, You already own a plot!".format(user.mention))
                #  Workbench
                elif item == "workbench" or item == "Workbench":
                    if user_plot[user.id]["plot"]:
                        if not user_plot[user.id]["workbench"]:
                            if ustick >= stick_cost_workbench and uwood >= wood_cost_workbench and ustone >= stone_cost_workbench:
                                user_plot[user.id]["workbench"] = True
                                await client.say("{}, you built a workbench at your base!".format(user.mention))
                                resources[user.id]["wood"] -= wood_cost_workbench
                                resources[user.id]["stick"] -= stick_cost_plot
                                resources[user.id]["stone"] -= stone_cost_plot
                            else:
                                await client.say("{}, you don't have enough building materials!".format(user.mention))
                        else:
                            await client.say("{}, You already own a workbench!".format(user.mention))
                    else:
                        await client.say("{}, you don't own a plot yet!".format(user.mention))
                # Furnace
                elif item == "furnace" or item == "Furnace":
                    if user_plot[user.id]["plot"]:
                        if not user_plot[user.id]["furnace"]:
                            if ustone >= stone_cost_furnace and ucoal >= coal_cost_furnace:
                                user_plot[user.id]["furnace"] = True
                                await client.say("{}, you built a furnace at your base!".format(user.mention))
                                resources[user.id]["stone"] -= stone_cost_plot
                                resources[user.id]["coal"] -= coal_cost_furnace
                            else:
                                await client.ssay("{}, you don't have enough building materials!".format(user.mention))
                        else:
                            await client.say("{}, You already own a furnace!".format(user.mention))
                    else:
                        await client.say("{}, you don't own a plot yet!".format(user.mention))

                # Error Message (Spelling)
                else:
                    await client.say("{}, '{}' is not an item you can build!".format(user.mention, item))

            # Error Message (Hammer)
            else:
                await client.say("{}, you don't have a hammer!".format(user.mention))

        # Error Message (Location)
        else:
            await (client.say("{}, you must be at Home to build, use .tr home to go there!".format(user.mention)))
    # Too Hungry Message
    else:
        await client.say("{}, you're too hungry to do that!".format(user.mention))
