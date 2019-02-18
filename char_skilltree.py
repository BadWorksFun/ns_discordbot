import discord
from discord.ext.commands import bot


async def skilltree(client: bot, ctx, users, skilltree, icons):

    # User
    user = ctx.message.author

    # Embed Variables
    tal = discord.Embed(
        title="Character Skills",
        description="{}Level: {} | {}Experience: {}/{}"
            .format(icons["icon"]["level"], users[user.id]["level"],
                    icons["icon"]["experience"], users[user.id]["experience"], users[user.id]["experience_need"]),
        colour=discord.Colour.purple())
    player_name = ctx.message.author.name
    player_avatar_url = ctx.message.author.avatar_url
    server_name = ctx.message.server.name
    bot_icon = "https://cdn.discordapp.com/attachments/538124566527213598/539066367375048737/NGB-Logo.png"
    tal.set_author(name="{}'s Skilltree".format(player_name), icon_url=player_avatar_url)
    tal.set_thumbnail(url="https://cdn.discordapp.com/attachments/538124566527213598/539460112834887681/skills.png")
    tal.set_image(url=bot_icon)
    tal.set_footer(text=server_name)

    # Labouring Skills
    tal.add_field(name="Labouring Skills",
                  value="Gathering: **{}** | *Exp: {}/{}*\n"
                        "Lumbering: **{}** | *Exp: {}/{}*\n"
                        "Mining:    **{}** | *Exp: {}/{}*\n"
                        "Farming:   **{}** | *Exp: {}/{}*"
                  .format(skilltree[user.id]["gathering"], skilltree[user.id]["gathering_exp"],
                          skilltree[user.id]["gathering_exp_need"],
                          skilltree[user.id]["lumbering"], skilltree[user.id]["lumbering_exp"],
                          skilltree[user.id]["lumbering_exp_need"],
                          skilltree[user.id]["mining"], skilltree[user.id]["mining_exp"],
                          skilltree[user.id]["mining_exp_need"],
                          skilltree[user.id]["farming"], skilltree[user.id]["farming_exp"],
                          skilltree[user.id]["farming_exp_need"]),
                  inline=True)

    # Trade Skills
    tal.add_field(name="Trade Skills",
                  value="Trader:    **{}** | *Exp: {}/{}*\n"
                        "Scientist: **{}** | *Exp: {}/{}*\n"
                        "Engineer:  **{}** | *Exp: {}/{}*\n"
                        "Smith:     **{}** | *Exp: {}/{}*"
                  .format(skilltree[user.id]["trader"], skilltree[user.id]["trader_exp"],
                          skilltree[user.id]["trader_exp_need"],
                          skilltree[user.id]["scientist"], skilltree[user.id]["scientist_exp"],
                          skilltree[user.id]["scientist_exp_need"],
                          skilltree[user.id]["engineer"], skilltree[user.id]["engineer_exp"],
                          skilltree[user.id]["engineer_exp_need"],
                          skilltree[user.id]["smith"], skilltree[user.id]["smith_exp"],
                          skilltree[user.id]["smith_exp_need"]))

    # Combat Skills
    tal.add_field(name="Combat Skills",
                  value="Attack:  **{}** | *Exp: {}/{}*\n"
                        "Defense: **{}** | *Exp: {}/{}*"
                  .format(skilltree[user.id]["attack"], skilltree[user.id]["attack_exp"],
                          skilltree[user.id]["attack_exp_need"],
                          skilltree[user.id]["defense"], skilltree[user.id]["defense_exp"],
                          skilltree[user.id]["defense_exp_need"]),
                  inline=True)

    # Execute Embed
    await client.say(embed=tal)
