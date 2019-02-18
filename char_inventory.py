import discord
from discord.ext.commands import bot


async def inventory(client: bot, ctx, stash, users, resources, stash_base, equipment, skilltree, icons):
    # User
    user = ctx.message.author
    user_attack_formula = int(skilltree[user.id]["attack"] + (users[user.id]["attack"] * users[user.id]["level"] / 5))  # Change in battling too
    user_defense_formula = int(
        skilltree[user.id]["defense"] / 5 + (users[user.id]["defense"] * users[user.id]["level"] / 20)) + 1
    # User Input Correction
    if stash is not None and stash != "base" and stash != "stash" and stash != "st" and stash != "b":
        stash = None

    # Inventory Embed Variables
    if stash is None:
        inv = discord.Embed(
            title="Character Stats",
            description="{} Level: {} | {} Cash: {}$ | {} Travel Power: {}/{}\n"
                        "{} Turn: {} | {} HP: {}/{} | {} Stamina: {}/{}\n"
                        "{} Nourishment: {}/100 | {} Bandages {}/{}"
                .format(icons["icon"]["level"], users[user.id]["level"],
                        icons["icon"]["cash"], users[user.id]["cash"],
                        icons["icon"]["travelpower"], users[user.id]["travelpower"], users[user.id]["travelpowermax"],
                        icons["icon"]["turn"], users[user.id]["turn"],
                        icons["icon"]["hp"], users[user.id]["hp"], users[user.id]["hpmax"],
                        icons["icon"]["stamina"], users[user.id]["stamina"], users[user.id]["staminamax"],
                        icons["icon"]["nourishment"], users[user.id]["nourishment"],
                        icons["icon"]["bandage"], users[user.id]["bandage"], users[user.id]["bandagemax"]),
            colour=discord.Colour.blue())

    # Stash Embed Variables
    else:
        inv = discord.Embed(
            title="Stash Inventory",
            description="",
            colour=discord.Colour.blue())

    # Main Title, Thumbnail, Big Image, Footer
    player_name = ctx.message.author.name
    player_avatar_url = ctx.message.author.avatar_url
    server_name = ctx.message.server.name
    bot_icon = "https://cdn.discordapp.com/attachments/538124566527213598/539066367375048737/NGB-Logo.png"
    inv.set_author(name="{}'s Inventory".format(player_name), icon_url=player_avatar_url)
    inv.set_thumbnail(url="https://cdn.discordapp.com/attachments/538124566527213598/539054078676697125/rucksack.png")
    inv.set_image(url=bot_icon)
    inv.set_footer(text=server_name)

    # Armour
    if stash is None:
        inv.add_field(name="Armour (def: {})".format(user_defense_formula),
                      value="{}{} ({}) | {}{} ({}) | {}{} ({}) | {}{} ({}) | {}{} ({}) | {}{} ({})"
                      .format(icons["icon"]["head"], equipment[user.id]["head"], equipment[user.id]["head_quality"],
                              icons["icon"]["shoulders"], equipment[user.id]["shoulders"], equipment[user.id]["shoulders_quality"],
                              icons["icon"]["chest"], equipment[user.id]["chest"], equipment[user.id]["chest_quality"],
                              icons["icon"]["hands"], equipment[user.id]["hands"], equipment[user.id]["hands_quality"],
                              icons["icon"]["legs"], equipment[user.id]["legs"], equipment[user.id]["legs_quality"],
                              icons["icon"]["feet"], equipment[user.id]["feet"], equipment[user.id]["feet_quality"]),
                      inline=True)

        # Weapons
        inv.add_field(name="Weapons (atk: {})".format(user_attack_formula),
                      value="{}{} ({}) | {}{} ({}) | {}{} ({}) | {}{} ({})"
                      .format(icons["icon"]["mainhand"], equipment[user.id]["mainhand"], equipment[user.id]["mainhand_quality"],
                              icons["icon"]["offhand"], equipment[user.id]["offhand"], equipment[user.id]["offhand_quality"],
                              icons["icon"]["ranged"], equipment[user.id]["ranged"], equipment[user.id]["ranged_quality"],
                              icons["icon"]["ring"], equipment[user.id]["ring"], equipment[user.id]["ring_quality"],),
                      inline=True)

        # Tools
        inv.add_field(name="Tools",
                      value="{}{} ({}) | Dur: {} | {}{} ({}) | Dur: {} | {}{} ({}) | Dur: {} | {}{} ({}) | Dur: {}"
                      .format(icons["icon"]["axe"], equipment[user.id]["axe"], equipment[user.id]["axe_quality"], equipment[user.id]["axe_durability"],
                              icons["icon"]["pickaxe"], equipment[user.id]["pickaxe"], equipment[user.id]["pickaxe_quality"], equipment[user.id]["pickaxe_durability"],
                              icons["icon"]["shovel"], equipment[user.id]["shovel"], equipment[user.id]["shovel_quality"], equipment[user.id]["shovel_durability"],
                              icons["icon"]["hammer"], equipment[user.id]["hammer"], equipment[user.id]["hammer_quality"], equipment[user.id]["hammer_durability"]),
                      inline=True)
        # Animals
        inv.add_field(name="Animals",
                      value="{}{} | {}{} | {}{}"
                      .format(icons["icon"]["cows"], resources[user.id]["cows"],
                              icons["icon"]["sheep"], resources[user.id]["sheep"],
                              icons["icon"]["chickens"], resources[user.id]["chickens"]),
                      inline=True)

    # Shared Resources (Inventory/Stash)
    if stash is None:
        source = resources
    else:
        source = stash_base
    # Raw Resources
    inv.add_field(name="Raw Resources",
                  value="{}{} | {}{} | {}{} | {}{} | {}{} | {}{}"
                  .format(icons["icon"]["wood"], source[user.id]["wood"],
                          icons["icon"]["stone"], source[user.id]["stone"],
                          icons["icon"]["coal"], source[user.id]["coal"],
                          icons["icon"]["copper_ore"], source[user.id]["copper_ore"],
                          icons["icon"]["iron_ore"], source[user.id]["iron_ore"],
                          icons["icon"]["gold_ore"], source[user.id]["gold_ore"]),
                  inline=True)

    # Refined Resources
    inv.add_field(name="Refined Resources",
                  value="{}{} | {}{} | {}{} | {}{} | {}{}"
                  .format(icons["icon"]["plank"], source[user.id]["plank"],
                          icons["icon"]["rope"], source[user.id]["rope"],
                          icons["icon"]["copper_bar"], source[user.id]["copper_bar"],
                          icons["icon"]["iron_bar"], source[user.id]["iron_bar"],
                          icons["icon"]["gold_bar"], source[user.id]["gold_bar"]),
                  inline=True)

    # Animal Produce
    inv.add_field(name="Animal Produce",
                  value="{}{} | {}{} | {}{} | {}{} | {}{} | {}{}"
                  .format(icons["icon"]["meat"], source[user.id]["meat"],
                          icons["icon"]["milk"], source[user.id]["milk"],
                          icons["icon"]["eggs"], source[user.id]["eggs"],
                          icons["icon"]["leather"], source[user.id]["leather"],
                          icons["icon"]["wool"], source[user.id]["wool"],
                          icons["icon"]["feathers"], source[user.id]["feathers"]),
                  inline=True)

    # Farm Produce
    inv.add_field(name="Farm Produce",
                  value="{}{} | {}{} | {}{} |"
                  .format(icons["icon"]["wheat"], source[user.id]["wheat"],
                          icons["icon"]["potatoes"], source[user.id]["potatoes"],
                          icons["icon"]["apples"], source[user.id]["apples"]),
                  inline=True)

    # Gathering
    inv.add_field(name="Gathering",
                  value="{}{} | {}{} | {}{}"
                  .format(icons["icon"]["fibre"], source[user.id]["fibre"],
                          icons["icon"]["stick"], source[user.id]["stick"],
                          icons["icon"]["berries"], source[user.id]["berries"]),
                  inline=True)

    # Execute Embed
    await client.say(embed=inv)
