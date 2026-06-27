import discord
from discord.ext import commands
import random
import os
from aiohttp import web

# Configuración de los Intents necesarios
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Credenciales y Canales
CANAL_A_CUIDAR_ID = 1421926883179757637
TOKEN_BOT = os.environ.get('DISCORD_TOKEN')

# --- SERVIDOR WEB INTEGRADO PARA ENGAÑAR A RENDER ---
async def handle(request):
    return web.Response(text="Pichulin está despierto y cuidando las 260 horas de racha! ")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render nos pasa el puerto en la variable de entorno 'PORT'. Si no existe, usa el 8080.
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"[+] Servidor Web anti-suspensión iniciado en el puerto {port}")

web_server_started = False

@bot.event
async def on_ready():
    global web_server_started
    print(f'=============================================')
    print(f'   PICHULIN V3 - WEB SERVICE ONLINE (FREE)   ')
    print(f'=============================================')
    print(f'Conectado como: {bot.user.name}')
    
    # Arranca el servidor web una sola vez al iniciar
    if not web_server_started:
        bot.loop.create_task(start_web_server())
        web_server_started = True

    # Intento de conexión automática
    channel = bot.get_channel(CANAL_A_CUIDAR_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
        if not voice_client:
            try:
                await channel.connect()
                print(f'[+] Conectado automáticamente a Lounge.')
            except Exception as e:
                print(f'[-] Error automático de voz: {e}')

# Comando manual desde el chat
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

# Respuestas dinámicas en el chat
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        respuestas = [
            f"¿Cómo que mudo, {message.author.mention}? Soy el Guardián de Lounge. ¡Esas 260 horas no se van a perder bajo mi guardia! ",
            "Aquí observando quién quiere abandonar la racha... ",
            f"¿Qué pasó, {message.author.mention}? No soy mudo, solo hablo cuando la racha corre peligro.",
            "Soy una IA superior diseñada para que no te vayas a dormir sin dejar la llamada abierta. "
        ]
        await message.channel.send(random.choice(respuestas))

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return
    channel = bot.get_channel(CANAL_A_CUIDAR_ID)
    if not channel:
        return
    voice_client = discord.utils.get(bot.utils.get(bot.voice_clients, guild=member.guild) if hasattr(bot, 'utils') else discord.utils.get(bot.voice_clients, guild=member.guild))

    if after.channel and after.channel.id == CANAL_A_CUIDAR_ID and not voice_client:
        await channel.connect()

    if before.channel and before.channel.id == CANAL_A_CUIDAR_ID:
        miembros_reales = [m for m in channel.members if not m.bot]
        if len(miembros_reales) == 0:
            print(f'[!] Modo Guardián Activo.')

bot.run(TOKEN_BOT)
