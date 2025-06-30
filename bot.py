import discord
from discord.ext import commands
import os, json
from dotenv import load_dotenv

# 🔐 Load secrets
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
print(f"🔑 Loaded token snippet: {DISCORD_TOKEN[:6]}...")

# 🤖 Intents & bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 🌀 When the bot awakens
@bot.event
async def on_ready():
    print(f"🌌 AniOmics has awakened as {bot.user}")

    # ✅ Verification Embed
    verify_channel = discord.utils.find(lambda c: "verify" in c.name.lower(), bot.get_all_channels())
    if verify_channel:
        embed = discord.Embed(
            title="🔓 Unlock the Veil",
            description="React with ✅ to enter. We may not stop you, but we will remember you.",
            color=0x2ecc71
        )
        embed.set_footer(text="AniOmics • Verification Gateway")
        message = await verify_channel.send(embed=embed)
        await message.add_reaction("✅")
        print(f"✅ Posted verification embed in #{verify_channel.name}")

    # 🎭 Role Picker Portal
    role_channel = discord.utils.get(bot.get_all_channels(), name="😎┇get-roles")
    if role_channel:
        # Pronouns
        pronouns = discord.Embed(
            title="🎭 Choose Your Pronouns",
            description="🙋‍♂️ He/Him 🙋‍♀️ She/Her 🧑‍🤝‍🧑 They/Them ❓ Ask",
            color=0x9b59b6
        )
        pronouns.set_footer(text="AniOmics • Role Selector")
        msg1 = await role_channel.send(embed=pronouns)
        for emoji in ["🙋‍♂️", "🙋‍♀️", "🧑‍🤝‍🧑", "❓"]:
            await msg1.add_reaction(emoji)

        # Interests
        interests = discord.Embed(
            title="🧠 Claim Your Interests",
            description="🎧 Melomaniac 🍥 Otaku 🧭 Adventurer 🧠 Nerd",
            color=0x3498db
        )
        interests.set_footer(text="AniOmics • Identity Gateway")
        msg2 = await role_channel.send(embed=interests)
        for emoji in ["🎧", "🍥", "🧭", "🧠"]:
            await msg2.add_reaction(emoji)

# 🔁 Reaction Add → Give roles + Welcome DM
@bot.event
async def on_raw_reaction_add(payload):
    emoji = str(payload.emoji)
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if not guild or not member or member.bot:
        return

    # ✅ Verification
    if emoji == "✅":
        role = discord.utils.get(guild.roles, name="Homie")
        if role:
            await member.add_roles(role)
            log = discord.utils.get(guild.text_channels, name="🛠️┇log-channel")
            if log:
                embed = discord.Embed(
                    description=f"✅ {member.mention} crossed the threshold.",
                    color=0x1abc9c
                )
                embed.set_footer(text="AniOmics • Entry Echo")
                await log.send(embed=embed)
            try:
                await member.send(
                    "🌀 You made it through the Veil. Not gonna lie — we weren’t sure you would.\n\nWelcome to **AniOmics** — part myth, part glitch, part found family..."
                )
            except:
                print(f"📪 Couldn't DM {member.display_name}")

    # 🎭 Role Reactions
    roles = {
        "🙋‍♂️": "He/Him", "🙋‍♀️": "She/Her", "🧑‍🤝‍🧑": "They/Them", "❓": "Ask",
        "🎧": "Melomaniac", "🍥": "Otaku", "🧭": "Adventurer", "🧠": "Nerd"
    }
    if emoji in roles:
        role = discord.utils.get(guild.roles, name=roles[emoji])
        if role:
            await member.add_roles(role)

# 🔄 Reaction Remove → Remove roles
@bot.event
async def on_raw_reaction_remove(payload):
    emoji = str(payload.emoji)
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if not guild or not member or member.bot:
        return

    roles = {
        "🙋‍♂️": "He/Him", "🙋‍♀️": "She/Her", "🧑‍🤝‍🧑": "They/Them", "❓": "Ask",
        "🎧": "Melomaniac", "🍥": "Otaku", "🧭": "Adventurer", "🧠": "Nerd"
    }
    if emoji in roles:
        role = discord.utils.get(guild.roles, name=roles[emoji])
        if role and role in member.roles:
            await member.remove_roles(role)

# 🫂 Farewell Echo
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="🛠️┇log-channel")
    if channel:
        await channel.send(
            f"👤 {member.name} slipped through the weave...\n\nBut no worries — we’ll keep your cookies warm, your glyphs glowing, and your echo humming in the background."
        )

# 🌌 Cultivation Leveling System
XP_FILE = "level_data.json"

def load_xp():
    try:
        with open(XP_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=2)

def calculate_level(msg_count):
    level, total = 1, 0
    while True:
        needed = 10 * (2 ** (level - 1))
        total += needed
        if msg_count < total or level >= 100:
            return min(level, 100)
        level += 1

def get_role_for_level(level):
    tiers = {
        range(1, 10): "Spirit Initiate",
        range(10, 20): "Essence Gatherer",
        range(20, 30): "Core Veiler",
        range(30, 40): "Astral Binder",
        range(40, 50): "Veil Walker",
        range(50, 60): "Fracture Forged",
        range(60, 70): "Soul Weaver",
        range(70, 80): "Echo Sage",
        range(80, 90): "Dreamfire Ascendant",
        range(90, 101): "Mythic Paragon"
    }
    for r in tiers:
        if level in r:
            return tiers[r]
    return None

async def send_level_up_embed(member, new_level, role_name):
    channel = discord.utils.get(member.guild.text_channels, name="🎚️┇leveling-up")
    if channel:
        embed = discord.Embed(
            title="🌌 Cultivation Breakthrough!",
            description=(
                f"**{member.mention}** has reached **Level {new_level}**\n"
                f"You are now recognized as **{role_name}** — the weave deepens.\n\n"
                "_Keep echoing. Keep rising._"
            ),
            color=0x8e44ad
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="AniOmics • Echo Ascension")
        await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    data = load_xp()
    user_id = str(message.author.id)

    if user_id not in data:
        data[user_id] = {"messages": 0, "level": 1}

    data[user_id]["messages"] += 1
    new_level = calculate_level(data[user_id]["messages"])

    if new_level > data[user_id]["level"]:
        data[user_id]["level"] = new_level
        save_xp(data)

        role_name = get_role_for_level(new_level)
        if role_name:
            guild = message.guild
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                all_roles = [r for r in guild.roles if r.name in [
    "Spirit Initiate", "Essence Gatherer", "Core Veiler", "Astral Binder",
    "Veil Walker", "Fracture Forged", "Soul Weaver",
    "Echo Sage", "Dreamfire Ascendant", "Mythic Paragon"
]]
print("🧪 Attempting to run bot...")
bot.run(DISCORD_TOKEN)
