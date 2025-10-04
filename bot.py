import discord
from discord.ext import commands
import json
import asyncio

# Set up bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')


@bot.command(name='delmsg')
@commands.has_permissions(manage_messages=True)
async def delete_messages(ctx, amount: int):
    """Delete a specified number of messages. Usage: !delmsg <amount>"""
    if amount < 1 or amount > 100:
        await ctx.send("Please specify a number between 1 and 100.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
    await ctx.send(f'Deleted {len(deleted) - 1} messages.', delete_after=3)


@bot.command(name='nuke')
@commands.has_permissions(manage_channels=True, manage_roles=True)
async def nuke_server(ctx):
    """Delete ALL channels and roles in the server. Usage: !nuke"""
    # Delete all channels
    channels = list(ctx.guild.channels)
    channel_tasks = [channel.delete() for channel in channels]
    channel_results = await asyncio.gather(*channel_tasks, return_exceptions=True)
    deleted_channels = sum(1 for r in channel_results if not isinstance(r, Exception))

    # Delete all roles
    roles = [role for role in ctx.guild.roles if role.name != '@everyone']
    role_tasks = [role.delete() for role in roles]
    role_results = await asyncio.gather(*role_tasks, return_exceptions=True)
    deleted_roles = sum(1 for r in role_results if not isinstance(r, Exception))

    print(f'Nuked {ctx.guild.name}: {deleted_channels} channels and {deleted_roles} roles deleted')


@bot.command(name='delchannel')
@commands.has_permissions(manage_channels=True)
async def delete_all_channels(ctx):
    """Delete ALL channels in the server. Usage: !delchannel"""
    channels = list(ctx.guild.channels)

    tasks = [channel.delete() for channel in channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    deleted = sum(1 for r in results if not isinstance(r, Exception))
    print(f'Deleted {deleted} channels from {ctx.guild.name}')


@bot.command(name='delrole')
@commands.has_permissions(manage_roles=True)
async def delete_all_roles(ctx):
    """Delete ALL roles in the server. Usage: !delrole"""
    roles = [role for role in ctx.guild.roles if role.name != '@everyone']

    tasks = [role.delete() for role in roles]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    deleted = sum(1 for r in results if not isinstance(r, Exception))
    print(f'Deleted {deleted} roles from {ctx.guild.name}')


@bot.command(name='help_mod')
async def help_command(ctx):
    """Display help for moderation commands"""
    embed = discord.Embed(
        title="Moderation Bot Commands",
        description="Available commands for server moderation",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="!delmsg <amount>",
        value="Delete specified number of messages (1-100)",
        inline=False
    )
    embed.add_field(
        name="!delchannel",
        value="Delete ALL channels in the server (requires confirmation)",
        inline=False
    )
    embed.add_field(
        name="!delrole",
        value="Delete ALL roles in the server (requires confirmation)",
        inline=False
    )
    await ctx.send(embed=embed)


# Error handlers
@delete_messages.error
@nuke_server.error
@delete_all_channels.error
@delete_all_roles.error
async def permission_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Use !help_mod for command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Use !help_mod for command usage.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")


# Run the bot
if __name__ == "__main__":
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            TOKEN = config.get('token')

        if not TOKEN:
            print("Error: 'token' not found in config.json")
        else:
            bot.run(TOKEN)
    except FileNotFoundError:
        print("Error: config.json not found")
        print("Create a config.json file with: {\"token\": \"your_bot_token_here\"}")
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON")
