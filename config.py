# Configuración del Bot MelodiiChan
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Tu ID de usuario de Discord (para comandos administrativos)
# Para obtenerlo: Configuración de Discord > Avanzado > Modo desarrollador > Click derecho en tu nombre > Copiar ID
YOUR_USER_ID = os.getenv('YOUR_USER_ID')

# Token del bot
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Enlaces para contacto y pago
PATREON_LINK = "https://patreon.com/tu_enlace"
CONTACT_LINK = "https://discord.com/users/522850760799813632"

# Límites para servidores gratuitos
FREE_LIMITS = {
    'daily_songs': 10,
    'queue_limit': 3,
    'session_time': 30  # minutos
}
