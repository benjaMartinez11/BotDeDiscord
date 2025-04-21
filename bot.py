import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Habilita la lectura del contenido de mensajes

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def hola(ctx):
    await ctx.send(f'¡Hola {ctx.author.name}! ¿Cómo estás?')

# Reemplazá "TU_TOKEN_AQUÍ" con el token real de tu bot
bot.run('token')
