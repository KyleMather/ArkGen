import discord
from discord.ext import commands
from discord import app_commands
import json
from keep_alive import keep_alive

# Load the dinos.json file
with open("dinos.json", "r") as f:
    dino_data = json.load(f)

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Autocomplete function
async def autocomplete_dinos(interaction: discord.Interaction, current: str):
    suggestions = [name for name in dino_data.keys() if current.lower() in name.lower()]
    return [app_commands.Choice(name=suggestion, value=suggestion) for suggestion in suggestions[:25]]

# /spawn command
@bot.tree.command(name="spawn", description="Generate an ARK dino spawn command.")
@app_commands.autocomplete(name=autocomplete_dinos)
async def spawn(
    interaction: discord.Interaction,
    name: str,
    level: int,
    health: int,
    stamina: int,
    oxygen: int,
    food: int,
    weight: int,
    melee: int,
    custom_name: str,
):
    if name not in dino_data:
        await interaction.response.send_message(f"Error: Dino '{name}' not found.", ephemeral=True)
        return

    # Get the command template and format it
    command_template = dino_data[name]
    spawn_command = command_template.format(
        level=level,
        health=health,
        stamina=stamina,
        oxygen=oxygen,
        food=food,
        weight=weight,
        melee=melee,
        name=custom_name,
    )
    
    await interaction.response.send_message(f"Spawn Command:\n```\n{spawn_command}\n```")
    await interaction.followup.send(f"{spawn_command}")


# Start the bot
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# Run the bot
bot.run("MTMwOTA2NTcxMDA4MDc1Mzc3Nw.G5cG8Y.TbTaJ6_DcszH7uR5bkMHw0JcJAdHtEnJjwTVXk")
keep_alive()