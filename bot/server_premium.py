import json
import os
from datetime import datetime, timedelta

# Archivo para almacenar servidores premium
PREMIUM_SERVERS_FILE = "premium_servers.json"

def load_premium_servers():
    """Carga la lista de servidores premium"""
    if os.path.exists(PREMIUM_SERVERS_FILE):
        with open(PREMIUM_SERVERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_premium_servers(premium_data):
    """Guarda la lista de servidores premium"""
    with open(PREMIUM_SERVERS_FILE, 'w') as f:
        json.dump(premium_data, f, indent=2)

def is_premium_server(guild_id):
    """Verifica si un servidor tiene premium activo"""
    premium_servers = load_premium_servers()
    guild_id = str(guild_id)
    
    if guild_id in premium_servers:
        expiry_date = datetime.fromisoformat(premium_servers[guild_id]['expires'])
        return datetime.now() < expiry_date
    return False

def add_premium_server(guild_id, guild_name, owner_id, months=1):
    """Agrega un servidor premium por X meses"""
    premium_servers = load_premium_servers()
    guild_id = str(guild_id)
    
    expiry_date = datetime.now() + timedelta(days=30 * months)
    premium_servers[guild_id] = {
        'guild_name': guild_name,
        'owner_id': str(owner_id),
        'expires': expiry_date.isoformat(),
        'activated': datetime.now().isoformat(),
        'months_purchased': months
    }
    
    save_premium_servers(premium_servers)
    return expiry_date

def get_server_premium_status(guild_id):
    """Obtiene el estado premium de un servidor"""
    premium_servers = load_premium_servers()
    guild_id = str(guild_id)
    
    if guild_id in premium_servers:
        server_data = premium_servers[guild_id]
        expiry_date = datetime.fromisoformat(server_data['expires'])
        if datetime.now() < expiry_date:
            return {
                'is_premium': True,
                'expires': expiry_date,
                'days_left': (expiry_date - datetime.now()).days,
                'guild_name': server_data['guild_name'],
                'owner_id': server_data['owner_id']
            }
    
    return {'is_premium': False, 'expires': None, 'days_left': 0}

def get_all_premium_servers():
    """Obtiene todos los servidores premium activos"""
    premium_servers = load_premium_servers()
    active_servers = {}
    
    for guild_id, data in premium_servers.items():
        expiry_date = datetime.fromisoformat(data['expires'])
        if datetime.now() < expiry_date:
            active_servers[guild_id] = {
                **data,
                'days_left': (expiry_date - datetime.now()).days
            }
    
    return active_servers

def remove_expired_servers():
    """Remueve servidores con suscripción expirada"""
    premium_servers = load_premium_servers()
    active_servers = {}
    
    for guild_id, data in premium_servers.items():
        expiry_date = datetime.fromisoformat(data['expires'])
        if datetime.now() < expiry_date:
            active_servers[guild_id] = data
    
    save_premium_servers(active_servers)
    return len(premium_servers) - len(active_servers)  # Servidores removidos

# Límites para servidores gratuitos
FREE_SERVER_LIMITS = {
    'daily_songs': 10,  # 10 canciones por día para todo el servidor
    'queue_limit': 3,   # Cola máxima de 3 canciones
    'session_time': 30  # 30 minutos por sesión
}

# Contadores de uso para servidores gratuitos
server_usage = {}

def check_server_limits(guild_id, action):
    """Verifica los límites para servidores gratuitos"""
    if is_premium_server(guild_id):
        return True, "Servidor Premium - sin límites"
    
    guild_id = str(guild_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if guild_id not in server_usage:
        server_usage[guild_id] = {}
    
    if today not in server_usage[guild_id]:
        server_usage[guild_id][today] = {'songs': 0, 'queue_size': 0}
    
    usage_today = server_usage[guild_id][today]
    
    if action == 'play_song':
        if usage_today['songs'] >= FREE_SERVER_LIMITS['daily_songs']:
            return False, f"🚫 Límite diario del servidor alcanzado ({FREE_SERVER_LIMITS['daily_songs']} canciones).\n💎 **¡Obtén Premium para tu servidor por solo $1/mes!**\n✨ Música ilimitada para todos los miembros"
        usage_today['songs'] += 1
        return True, f"Canciones del servidor hoy: {usage_today['songs']}/{FREE_SERVER_LIMITS['daily_songs']}"
    
    elif action == 'add_to_queue':
        if usage_today['queue_size'] >= FREE_SERVER_LIMITS['queue_limit']:
            return False, f"🚫 Cola del servidor llena ({FREE_SERVER_LIMITS['queue_limit']} máximo).\n💎 **¡Obtén Premium para cola ilimitada!**"
        usage_today['queue_size'] += 1
        return True, f"Cola del servidor: {usage_today['queue_size']}/{FREE_SERVER_LIMITS['queue_limit']}"
    
    return True, "OK"
