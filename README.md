# 🌸 VoiceMaster - Premium Discord Bot 🌸

> ✨ *Un bot kawaii para gestionar canales de voz automáticamente con características premium* ✨

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-7289DA.svg?style=for-the-badge&logo=discord)
![Status](https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge)

## 💫 Descripción

VoiceMaster es un bot de Discord súper kawaii que gestiona automáticamente los canales de voz temporales. Cuando alguien se une a un canal especial, ¡el bot crea automáticamente un canal personal para ellos! 🎵

### ✨ Características Principales

- 🎤 **Canales de voz automáticos**: Crea canales temporales cuando alguien se une
- 👑 **Sistema Premium**: Características exclusivas para servidores premium
- 🌟 **Fácil configuración**: Solo unos comandos y ¡listo!
- 💝 **Interfaz kawaii**: Respuestas adorables con emojis
- 🔒 **Seguro**: Variables de entorno para proteger tokens
- 💰 **Monetización**: Sistema integrado de pagos con Gumroad

### 🎀 Características Premium

- ⭐ Límites personalizados de canales
- 🎨 Nombres personalizados para canales
- 🔧 Configuraciones avanzadas
- 💎 Soporte prioritario

## 🚀 Instalación Rápida

### 📋 Requisitos

- Python 3.8 o superior
- Una aplicación de Discord Bot
- Servidor web para webhooks (opcional)

### 💻 Configuración

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/voicemaster-bot.git
   cd voicemaster-bot
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura las variables de entorno**
   ```bash
   # Crea un archivo .env
   touch .env
   ```
   
   Agrega estas variables a tu archivo `.env`:
   ```env
   DISCORD_TOKEN=tu_token_del_bot_aqui
   GUMROAD_SECRET=tu_secret_de_gumroad
   WEBHOOK_SECRET=tu_secret_del_webhook
   ```

4. **Ejecuta el bot**
   ```bash
   python bot.py
   ```

## 🎮 Comandos

### 📝 Comandos Básicos

- `!setup` - Configura el bot en tu servidor
- `!help` - Muestra la ayuda kawaii
- `!ping` - ¡Pong! Verifica que el bot esté funcionando

### 👑 Comandos de Administrador

- `!activate [guild_id]` - Activa premium en un servidor (solo owner)
- `!status [guild_id]` - Verifica el estado premium de un servidor
- `!serverid` - Obtiene el ID del servidor actual

### 🌟 Uso del Sistema Premium

1. **Para activar premium:**
   - Obtén el ID de tu servidor con `!serverid`
   - Visita nuestra [página de compra](tu-landing-page.html)
   - Completa el pago ($1/mes)
   - ¡El premium se activará automáticamente! ✨

## 🛠️ Estructura del Proyecto

```
voicemaster-bot/
├── 📁 static/
│   ├── 🎨 style.css
│   └── 🖼️ background.jpg
├── 📄 bot.py              # Bot principal
├── ⚙️ config.py           # Configuración
├── 🔗 webhook.py          # Webhook de Gumroad
├── 🌐 landing.html        # Página de compra
├── 📋 requirements.txt    # Dependencias
├── 🚫 .gitignore         # Archivos ignorados
├── 🔐 .env.example       # Ejemplo de variables
└── 📖 README.md          # Este archivo
```

## 🔧 Configuración Avanzada

### 🌐 Webhook Setup (Opcional)

Para activación automática del premium:

1. Configura un servidor web (Flask incluido)
2. Ejecuta el webhook:
   ```bash
   python webhook.py
   ```
3. Configura la URL del webhook en Gumroad

### 🎨 Personalización

Puedes personalizar:
- Mensajes del bot en `bot.py`
- Estilos de la landing page en `static/style.css`
- Configuraciones en `config.py`

## 💰 Monetización

Este bot incluye un sistema completo de monetización:

- 💵 **Precio**: $1 USD por mes por servidor
- 🛒 **Plataforma**: Gumroad
- 🔄 **Activación**: Automática via webhook
- 📊 **Gestión**: Panel de admin incluido

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 💕

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 💖 Soporte

¿Necesitas ayuda? ¡Estamos aquí para ti!

- 📧 **Email**: tu-email@ejemplo.com
- 💬 **Discord**: Tu servidor de Discord
- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/voicemaster-bot/issues)

## 🌟 Agradecimientos

- 💜 A la comunidad de Discord.py
- 🎨 A todos los contribuidores kawaii
- ✨ A nuestros usuarios premium por el apoyo

---

<div align="center">

**¡Hecho con 💖 para la comunidad de Discord!**

*Si te gusta este proyecto, ¡dale una ⭐ en GitHub!*

</div>
