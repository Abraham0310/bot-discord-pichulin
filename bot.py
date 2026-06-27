import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

CANAL_A_CUIDAR_ID = 1421926883179757637
TOKEN_BOT = 'MTUwODkxMjQ5MTQ4MzM2NTQ4Ng.GqZBHB.O6Ijl-wa_sLnk2NyJFKvD4vD4JqAQgAwfvi21o'

@bot.event
async def on_ready():
    print(f'=============================================')
    print(f'   PICHULIN V2 - AHORA HABLA Y CONVERSA      ')
    print(f'=============================================')
    channel = bot.get_channel(CANAL_A_CUIDAR_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
        if not voice_client:
            try:
                await channel.connect()
            except Exception as e:
                print(f'[-] Error automático: {e}')

@bot.command()
async def entrar(ctx):
    channel = bot.get_channel(CANAL_A_CUIDAR_ID)
    if channel:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            await channel.connect()
            await ctx.send("¡Ya estoy aquí cuidando la racha de las 260 horas! No se preocupen.")
        else:
            await voice_client.move_to(channel)

# INTERACCIÓN DINÁMICA CON EL CHAT
@bot.event
async def on_message(message):
    # Ignorar si el mensaje lo manda el propio bot
    if message.author == bot.user:
        return

    # Si alguien menciona al bot (@Pichulin)
    if bot.user.mentioned_in(message):
        respuestas = [
            f"¿Cómo que mudo, {message.author.mention}? Soy el Guardián de Lounge. ¡Esas 260 horas no se van a perder bajo mi guardia! ",
            "Aquí observando quién quiere abandonar la racha... ",
            f"¿Qué pasó, {message.author.mention}? No soy mudo, solo hablo cuando la racha corre peligro.",
            "Soy una inteligencia superior diseñada para que no te vayas a dormir sin dejar la llamada abierta. "
        ]
        await message.channel.send(random.choice(respuestas))

    # Importante para que los comandos como !entrar sigan funcionando
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return
    channel = bot.get_channel(CANAL_A_CUIDAR_ID)
    if not channel:
        return
    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

    if after.channel and after.channel.id == CANAL_A_CUIDAR_ID and not voice_client:
        await channel.connect()

    if before.channel and before.channel.id == CANAL_A_CUIDAR_ID:
        miembros_reales = [m for m in channel.members if not m.bot]
        if len(miembros_reales) == 0:
            print(f'[!] Modo Guardián Activo.')

bot.run(TOKEN_BOT)
