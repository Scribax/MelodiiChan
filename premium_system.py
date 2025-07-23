import json
import os
from datetime import datetime, timedelta

# Archivo para almacenar usuarios premium
PREMIUM_FILE = "premium_users.json"

def load_premium_users():
    """Carga la lista de usuarios premium"""
    if os.path.exists(PREMIUM_FILE):
        with open(PREMIUM_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_premium_users(premium_data):
    """Guarda la lista de usuarios premium"""
    with open(PREMIUM_FILE, 'w') as f:
        json.dump(premium_data, f, indent=2)

def is_premium_user(user_id):
    """Verifica si un usuario tiene premium activo"""
    premium_users = load_premium_users()
    user_id = str(user_id)
    
    if user_id in premium_users:
        expiry_date = datetime.fromisoformat(premium_users[user_id]['expires'])
        return datetime.now() < expiry_date
    return False

def add_premium_user(user_id, months=1):
    """Agrega un usuario premium por X meses"""
    premium_users = load_premium_users()
    user_id = str(user_id)
    
    expiry_date = datetime.now() + timedelta(days=30 * months)
    premium_users[user_id] = {
        'expires': expiry_date.isoformat(),
        'activated': datetime.now().isoformat()
    }
    
    save_premium_users(premium_users)
    return expiry_date

def get_premium_status(user_id):
    """Obtiene el estado premium de un usuario"""
    premium_users = load_premium_users()
    user_id = str(user_id)
    
    if user_id in premium_users:
        expiry_date = datetime.fromisoformat(premium_users[user_id]['expires'])
        if datetime.now() < expiry_date:
            return {
                'is_premium': True,
                'expires': expiry_date,
                'days_left': (expiry_date - datetime.now()).days
            }
    
    return {'is_premium': False, 'expires': None, 'days_left': 0}

# Límites para usuarios gratuitos
FREE_LIMITS = {
    'daily_songs': 3,
    'queue_limit': 5,
    'session_time': 60  # minutos
}

# Contadores de uso para usuarios gratuitos
user_usage = {}

def check_free_limits(user_id, action):
    """Verifica los límites para usuarios gratuitos"""
    if is_premium_user(user_id):
        return True, "Premium user - no limits"
    
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in user_usage:
        user_usage[user_id] = {}
    
    if today not in user_usage[user_id]:
        user_usage[user_id][today] = {'songs': 0, 'queue_size': 0}
    
    usage_today = user_usage[user_id][today]
    
    if action == 'play_song':
        if usage_today['songs'] >= FREE_LIMITS['daily_songs']:
            return False, f"Límite diario alcanzado ({FREE_LIMITS['daily_songs']} canciones). ¡Mejora a Premium por $1/mes! 💎"
        usage_today['songs'] += 1
        return True, f"Canciones usadas hoy: {usage_today['songs']}/{FREE_LIMITS['daily_songs']}"
    
    elif action == 'add_to_queue':
        if usage_today['queue_size'] >= FREE_LIMITS['queue_limit']:
            return False, f"Cola llena ({FREE_LIMITS['queue_limit']} máximo). ¡Mejora a Premium para cola ilimitada! 💎"
        usage_today['queue_size'] += 1
        return True, f"Cola: {usage_today['queue_size']}/{FREE_LIMITS['queue_limit']}"
    
    return True, "OK"
