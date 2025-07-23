import discord
from discord.ext import commands
import asyncio
import yt_dlp
import os
from discord import FFmpegPCMAudio
from datetime import datetime
from server_premium import is_premium_server, check_server_limits, get_server_premium_status, add_premium_server, get_all_premium_servers
from config import YOUR_USER_ID, BOT_TOKEN, PATREON_LINK, CONTACT_LINK

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Descripción kawaii del bot
bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    description="🌸 ¡Hola! Soy MelodiiChan, tu bot de música kawaii favorito! 🎵\n" +
                "¡Puedo reproducir toda la música que quieras desde YouTube! ✨\n" +
                "¡Usa !help para ver todos mis comandos adorables! 💖",
    help_command=None  # Desactivamos el comando help por defecto
)

# Variables globales para manejar la música
voice_clients = {}
music_queue = {}
is_playing = {}

# Configuración de yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
    'extract_flat': False,
    'no_check_certificate': True
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='⏸️ Pausar', style=discord.ButtonStyle.primary)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("🎵 **Música pausada** 💤", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No hay música reproduciéndose", ephemeral=True)
    
    @discord.ui.button(label='▶️ Reanudar', style=discord.ButtonStyle.success)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("🎵 **Música reanudada** ✨", ephemeral=True)
        else:
            await interaction.response.send_message("❌ La música no está pausada", ephemeral=True)
    
    @discord.ui.button(label='⏹️ Detener', style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = voice_clients.get(interaction.guild.id)
        if voice_client:
            voice_client.stop()
            music_queue[interaction.guild.id] = []
            is_playing[interaction.guild.id] = False
            await interaction.response.send_message("🛑 **Música detenida** 🌙", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No hay música reproduciéndose", ephemeral=True)
    
    @discord.ui.button(label='⏭️ Saltar', style=discord.ButtonStyle.secondary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ **Canción saltada** 🎀", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No hay música reproduciéndose", ephemeral=True)

@bot.event
async def on_ready():
    print(f'🌸 {bot.user} está conectado y listo para tocar música kawaii! 🎵')
    print(f'ID del bot: {bot.user.id}')
    print('------')

@bot.command(name='help', help='¡Muestra todos mis comandos kawaii!')
async def help_command(ctx):
    embed = discord.Embed(
        title="🌸 ¡Comandos de MelodiiChan! 🎵",
        description="¡Hola! Soy tu bot de música kawaii favorito! ✨\n¡Aquí tienes todos mis comandos adorables! 💖",
        color=0xFF69B4
    )
    
    # Comandos de música
    music_commands = [
        "🎵 `!play <link>` - Reproduce música desde YouTube",
        "⏸️ `!stop` - Detiene la música y limpia la cola",
        "⏭️ `!skip` - Salta la canción actual",
        "📜 `!queue` - Muestra la cola de reproducción",
        "👋 `!leave` - Me desconecto del canal de voz"
    ]
    
    # Comandos de información
    info_commands = [
        "💎 `!premium` - Información sobre Premium",
        "📊 `!status` - Estado del servidor (gratuito/premium)",
        "❓ `!help` - Muestra esta ayuda kawaii"
    ]
    
    embed.add_field(
        name="🎶 Comandos de Música", 
        value="\n".join(music_commands), 
        inline=False
    )
    
    embed.add_field(
        name="📱 Comandos de Información", 
        value="\n".join(info_commands), 
        inline=False
    )
    
    # Verificar si es servidor premium
    status = get_server_premium_status(ctx.guild.id)
    if status['is_premium']:
        embed.add_field(
            name="💎 Estado Premium", 
            value=f"¡Este servidor tiene Premium! ✨\nExpira: {status['expires'].strftime('%d/%m/%Y')}", 
            inline=False
        )
    else:
        embed.add_field(
            name="🆓 Versión Gratuita", 
            value="10 canciones/día • Cola de 3 canciones\n[💎 ¡Obtén Premium por $1/mes!](" + CONTACT_LINK + ")", 
            inline=False
        )
    
    # Usar la imagen kawaii como thumbnail
    try:
        file = discord.File("tmpj48fcvq1.webp", filename="kawaii_help.webp")
        embed.set_thumbnail(url="attachment://kawaii_help.webp")
        
        embed.set_footer(
            text="🌸 ¡Espero que disfrutes la música kawaii! 🌸", 
            icon_url="attachment://kawaii_help.webp"
        )
        
        await ctx.send(embed=embed, file=file)
    except:
        # Si no se puede cargar la imagen, enviar sin ella
        embed.set_footer(text="🌸 ¡Espero que disfrutes la música kawaii! 🌸")
        await ctx.send(embed=embed)

@bot.command(name='play', help='Reproduce música desde YouTube')
async def play(ctx, *, url):
    try:
        # Verificar límites para el servidor
        can_play, message = check_server_limits(ctx.guild.id, 'play_song')
        if not can_play:
            embed = discord.Embed(
                title="💎 Límite Alcanzado",
                description=f"{message}\n\n[🎵 ¡Obtén Premium para tu servidor por solo $1/mes!](https://patreon.com/tu_enlace)",
                color=0xFFD700
            )
            await ctx.send(embed=embed)
            return
        
        # Verificar si el usuario está en un canal de voz
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Error",
                description="¡Necesitas estar en un canal de voz para reproducir música! 🎧",
                color=0xFF69B4
            )
            await ctx.send(embed=embed)
            return

        # Conectar al canal de voz
        channel = ctx.author.voice.channel
        voice_client = voice_clients.get(ctx.guild.id)
        
        if not voice_client:
            voice_client = await channel.connect()
            voice_clients[ctx.guild.id] = voice_client

        # Inicializar la cola si no existe
        if ctx.guild.id not in music_queue:
            music_queue[ctx.guild.id] = []
            is_playing[ctx.guild.id] = False

        # Obtener información del video
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            
        # Agregar a la cola
        music_queue[ctx.guild.id].append(player)
        
        # Crear embed kawaii
        embed = discord.Embed(
            title="🎵 Música Agregada",
            description=f"**{player.title}** ha sido agregada a la cola! ✨",
            color=0xFF1493
        )
        
        # Usar la imagen kawaii como thumbnail
        file = discord.File("tmpj48fcvq1.webp", filename="kawaii_avatar.webp")
        embed.set_thumbnail(url="attachment://kawaii_avatar.webp")
        
        # Crear vista con botones
        view = MusicControls()
        
        # Enviar mensaje con botones y la imagen
        await ctx.send(embed=embed, file=file, view=view)
        
        # Reproducir si no hay nada reproduciéndose
        if not is_playing[ctx.guild.id]:
            await play_next(ctx)

    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"Ocurrió un error al reproducir la música: {str(e)} 😢",
            color=0xFF0000
        )
        await ctx.send(embed=embed)

async def play_next(ctx):
    guild_id = ctx.guild.id
    
    if music_queue[guild_id]:
        is_playing[guild_id] = True
        player = music_queue[guild_id].pop(0)
        
        def after_playing(error):
            if error:
                print(f'Error en la reproducción: {error}')
            
            # Reproducir siguiente canción
            coro = play_next(ctx)
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            try:
                fut.result()
            except:
                pass
        
        voice_clients[guild_id].play(player, after=after_playing)
        
        # Mensaje de reproducción actual
        embed = discord.Embed(
            title="🎶 Reproduciendo Ahora",
            description=f"**{player.title}** 🎀",
            color=0xFF69B4
        )
        await ctx.send(embed=embed)
    else:
        is_playing[guild_id] = False

@bot.command(name='stop', help='Detiene la música y limpia la cola')
async def stop(ctx):
    voice_client = voice_clients.get(ctx.guild.id)
    if voice_client:
        voice_client.stop()
        music_queue[ctx.guild.id] = []
        is_playing[ctx.guild.id] = False
        
        embed = discord.Embed(
            title="🛑 Música Detenida",
            description="La música ha sido detenida y la cola limpiada 🌙",
            color=0x9932CC
        )
        await ctx.send(embed=embed)

@bot.command(name='skip', help='Salta la canción actual')
async def skip(ctx):
    voice_client = voice_clients.get(ctx.guild.id)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        embed = discord.Embed(
            title="⏭️ Canción Saltada",
            description="Saltando a la siguiente canción 🎀",
            color=0xFF1493
        )
        await ctx.send(embed=embed)

@bot.command(name='queue', help='Muestra la cola de reproducción')
async def queue(ctx):
    guild_id = ctx.guild.id
    if guild_id in music_queue and music_queue[guild_id]:
        queue_list = []
        for i, player in enumerate(music_queue[guild_id][:10], 1):
            queue_list.append(f"{i}. {player.title}")
        
        embed = discord.Embed(
            title="🎵 Cola de Reproducción",
            description="\n".join(queue_list) if queue_list else "La cola está vacía 💤",
            color=0xFF69B4
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="🎵 Cola de Reproducción",
            description="La cola está vacía 💤",
            color=0xFF69B4
        )
        await ctx.send(embed=embed)

@bot.command(name='leave', help='Desconecta el bot del canal de voz')
async def leave(ctx):
    voice_client = voice_clients.get(ctx.guild.id)
    if voice_client:
        await voice_client.disconnect()
        del voice_clients[ctx.guild.id]
        if ctx.guild.id in music_queue:
            del music_queue[ctx.guild.id]
        if ctx.guild.id in is_playing:
            del is_playing[ctx.guild.id]
        
        embed = discord.Embed(
            title="👋 Hasta luego!",
            description="Me desconecto del canal de voz 🌸",
            color=0xFF69B4
        )
        await ctx.send(embed=embed)

@bot.command(name='premium', help='Información sobre Premium para el Servidor')
async def premium_info(ctx):
    status = get_server_premium_status(ctx.guild.id)
    
    if status['is_premium']:
        embed = discord.Embed(
            title="💎 Servidor Premium",
            description=f"¡Este servidor tiene Premium! ✨\n\n📅 **Expira:** {status['expires'].strftime('%d/%m/%Y')}\n⏰ **Días restantes:** {status['days_left']}",
            color=0xFFD700
        )
    else:
        embed = discord.Embed(
            title="🎵 Premium para Servidores",
            description="**¡Solo $1/mes por servidor!** 💖\n\n**Beneficios Premium para TODOS los miembros:**\n🎵 Canciones ilimitadas\n📜 Cola ilimitada\n🎧 Mejor calidad de audio\n⚡ Sin anuncios\n💎 Comandos exclusivos\n🎆 Acceso para todo el servidor\n\n[🌸 ¡Contacta para obtener Premium!](https://discord.com/users/TU_USER_ID)",
            color=0xFF69B4
        )
        embed.add_field(name="🆓 Versión Gratuita", value="10 canciones/día\nCola de 3 canciones", inline=True)
        embed.add_field(name="💎 Versión Premium", value="Canciones ilimitadas\nCola ilimitada", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='activate', help='Activar Premium para Servidor (solo administradores)')
async def activate_premium(ctx, months: int = 1):
    if str(ctx.author.id) != YOUR_USER_ID:
        embed = discord.Embed(
            title="❌ Acceso Denegado",
            description="Solo el propietario del bot puede activar el Premium en servidores.",
            color=0xFF4500
        )
        await ctx.send(embed=embed)
        return
    
    # Limitar meses a un número razonable (máximo 120 meses = 10 años)
    if months < 1 or months > 120:
        embed = discord.Embed(
            title="❌ Error",
            description="El número de meses debe estar entre 1 y 120 (10 años máximo) 😅",
            color=0xFF4500
        )
        await ctx.send(embed=embed)
        return
    guild_id = ctx.guild.id
    guild_name = ctx.guild.name
    owner_id = ctx.guild.owner_id
    expiry_date = add_premium_server(guild_id, guild_name, owner_id, months)
    
    embed = discord.Embed(
        title="💎 Premium Activado",
        description=f"Premium activado para el servidor **{guild_name}**\n\n📅 **Expira:** {expiry_date.strftime('%d/%m/%Y')}\n⏰ **Duración:** {months} mes(es)",
        color=0xFFD700
    )
    
    await ctx.send(embed=embed)
    
    # Mensaje directo al dueño del servidor
    try:
        owner = await ctx.guild.fetch_member(owner_id)
        dm_embed = discord.Embed(
            title="🎉 ¡Premium Activado para tu Servidor!",
            description="¡El servidor **{guild_name}** tiene ahora Premium! ✨\n\n¡Disfruta de música ilimitada para todos! 🎵",
            color=0xFFD700
        )
        await owner.send(embed=dm_embed)
    except:
        pass

@bot.command(name='status', help='Ver el estado del servidor')
async def server_status(ctx):
    status = get_server_premium_status(ctx.guild.id)
    
    if status['is_premium']:
        embed = discord.Embed(
            title="💎 Servidor Premium",
            color=0xFFD700
        )
        embed.add_field(name="Plan", value="Premium 💎", inline=True)
        embed.add_field(name="Expira", value=status['expires'].strftime('%d/%m/%Y'), inline=True)
        embed.add_field(name="Días restantes", value=f"{status['days_left']} días", inline=True)
    else:
        from server_premium import server_usage
        guild_id = str(ctx.guild.id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        songs_today = 0
        if guild_id in server_usage and today in server_usage[guild_id]:
            songs_today = server_usage[guild_id][today].get('songs', 0)
        
        embed = discord.Embed(
            title="🆓 Servidor Gratuito",
            color=0xFF69B4
        )
        embed.add_field(name="Plan", value="Gratuito 🆓", inline=True)
        embed.add_field(name="Canciones hoy", value=f"{songs_today}/10", inline=True)
        embed.add_field(name="Mejora", value="[Premium $1/mes](https://patreon.com/tu_enlace)", inline=True)
    
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name='listpremium', help='Lista todos los servidores premium (solo propietario)')
async def list_premium_servers(ctx):
    if str(ctx.author.id) != YOUR_USER_ID:
        embed = discord.Embed(
            title="❌ Acceso Denegado",
            description="Solo el propietario del bot puede ver esta información.",
            color=0xFF4500
        )
        await ctx.send(embed=embed)
        return
    
    premium_servers = get_all_premium_servers()
    
    if not premium_servers:
        embed = discord.Embed(
            title="📊 Servidores Premium",
            description="No hay servidores premium activos.",
            color=0xFF69B4
        )
        await ctx.send(embed=embed)
        return
    
    server_list = []
    for guild_id, data in premium_servers.items():
        server_list.append(f"**{data['guild_name']}** - {data['days_left']} días restantes")
    
    embed = discord.Embed(
        title="💎 Servidores Premium Activos",
        description="\n".join(server_list[:10]),  # Mostrar solo los primeros 10
        color=0xFFD700
    )
    embed.set_footer(text=f"Total: {len(premium_servers)} servidores premium")
    await ctx.send(embed=embed)

@bot.command(name='serverid', help='Obtener el ID de este servidor')
async def get_server_id(ctx):
    """Muestra el ID del servidor actual para activación de premium"""
    embed = discord.Embed(
        title="🆔 ID del Servidor",
        description=f"**ID de este servidor:** `{ctx.guild.id}`\n\n📝 **¿Cómo obtener Premium?**\n1. Copia el ID: `{ctx.guild.id}`\n2. [Contacta al desarrollador]({CONTACT_LINK})\n3. Proporciona el ID y realiza el pago\n4. ¡Premium se activa automáticamente!",
        color=0x3498DB
    )
    
    embed.add_field(
        name="💎 Precios", 
        value="**$1 USD/mes** por servidor\n**$10 USD/año** por servidor (2 meses gratis!)", 
        inline=False
    )
    
    embed.set_footer(text=f"Servidor: {ctx.guild.name} • Miembros: {ctx.guild.member_count}")
    await ctx.send(embed=embed)

@bot.command(name='deactivate', help='Desactivar premium de un servidor (solo propietario)')
async def deactivate_premium(ctx, guild_id: int = None):
    if str(ctx.author.id) != YOUR_USER_ID:
        embed = discord.Embed(
            title="❌ Acceso Denegado",
            description="Solo el propietario del bot puede desactivar premium.",
            color=0xFF4500
        )
        await ctx.send(embed=embed)
        return
    
    target_guild_id = guild_id or ctx.guild.id
    
    from server_premium import load_premium_servers, save_premium_servers
    premium_servers = load_premium_servers()
    
    if str(target_guild_id) in premium_servers:
        guild_name = premium_servers[str(target_guild_id)]['guild_name']
        del premium_servers[str(target_guild_id)]
        save_premium_servers(premium_servers)
        
        embed = discord.Embed(
            title="❌ Premium Desactivado",
            description=f"Premium desactivado para **{guild_name}**",
            color=0xFF4500
        )
    else:
        embed = discord.Embed(
            title="ℹ️ Información",
            description="Este servidor no tiene premium activo.",
            color=0x3498DB
        )
    
    await ctx.send(embed=embed)

# Ejecutar el bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
