# 🟪 Guía Completa: Configurar Gumroad con MelodiiChan

## 📋 Resumen

Gumroad es perfecto para empezar porque:
- ✅ **Súper fácil de configurar** (15 minutos máximo)
- ✅ **Webhooks integrados** para automatización
- ✅ **Procesamiento de pagos seguro**
- ✅ **No necesitas ser programador**
- 💰 **Solo 5% + $0.25 por transacción**

---

## 🚀 Paso 1: Crear Cuenta en Gumroad

1. **Ve a** [gumroad.com](https://gumroad.com)
2. **Regístrate** con tu email
3. **Verifica tu cuenta** (revisa tu email)
4. **Completa tu perfil** (nombre, bio, etc.)

---

## 💎 Paso 2: Crear Productos Premium

### Producto 1: MelodiiChan Mensual ($1)

1. **Clic en "Create"** → "Product"
2. **Información del producto:**
   - **Nombre:** `MelodiiChan Premium - 1 Mes`
   - **Precio:** `$1.00`
   - **Descripción:**
     ```
     🌸 MelodiiChan Premium - 1 Mes 🎵
     
     ✨ Música ilimitada para tu servidor de Discord
     🎧 Cola de reproducción ilimitada
     🎀 Sin límites de tiempo
     💎 Calidad de audio superior
     🌟 Para TODOS los miembros del servidor
     
     ⚡ Activación automática en segundos!
     
     🔧 Instrucciones:
     1. Copia el ID de tu servidor Discord (usa !serverid en tu bot)
     2. Incluye el ID en la sección "Mensaje al vendedor" al comprar
     3. ¡Premium se activa automáticamente!
     ```
   - **Tipo:** Digital Product
   - **Archivo:** Sube una imagen kawaii del bot

3. **Configurar campos personalizados:**
   - **Clic en "Customize"** → "Custom Fields"
   - **Agregar campo:**
     - **Label:** `ID del Servidor Discord`
     - **Type:** `Text`
     - **Required:** `Yes`
     - **Placeholder:** `123456789012345678`

### Producto 2: MelodiiChan Anual ($10)

1. **Repetir proceso anterior** con estos cambios:
   - **Nombre:** `MelodiiChan Premium - 1 Año (¡2 meses gratis!)`
   - **Precio:** `$10.00`
   - **Descripción:** (igual pero menciona "12 meses por el precio de 10")

---

## 🔗 Paso 3: Configurar Webhooks

1. **Ve a tu Dashboard** → "Settings" → "Advanced"
2. **Clic en "Ping URL"** (sección Webhooks)
3. **Configurar:**
   - **URL:** `http://tu-dominio.com/gumroad/webhook`
   - **Enable:** `Yes`

### 📝 Nota sobre la URL del Webhook:
Necesitas hostear tu webhook en un servidor público. Opciones:
- **ngrok** (para pruebas): `ngrok http 5000`
- **Heroku** (gratis): Deploy automático
- **VPS** (DigitalOcean, Vultr): $5/mes

---

## 🔧 Paso 4: Configurar el Webhook Local

### 1. Instalar dependencias:
```bash
pip install -r webhook_requirements.txt
```

### 2. Configurar clave secreta:
En `gumroad_webhook.py`, línea 17:
```python
GUMROAD_SECRET = "tu_clave_secreta_gumroad_2024"
```

### 3. Ejecutar el webhook:
```bash
python gumroad_webhook.py
```

---

## 🌐 Paso 5: Subir la Landing Page

### Opción A: GitHub Pages (GRATIS)
1. **Crear repositorio** en GitHub
2. **Subir** `landing_page.html`
3. **Activar GitHub Pages** en Settings
4. **Tu URL será:** `https://tu-usuario.github.io/tu-repo`

### Opción B: Netlify (GRATIS)
1. **Ve a** [netlify.com](https://netlify.com)
2. **Arrastra** `landing_page.html` a Netlify
3. **¡Listo!** Tu URL se genera automáticamente

### Opción C: Tu propio dominio
1. **Compra un dominio** (Namecheap, GoDaddy)
2. **Sube** `landing_page.html` a tu hosting
3. **Actualiza** las URLs en el archivo HTML

---

## ⚙️ Paso 6: Personalizar URLs en Landing Page

En `landing_page.html`, línea 168, cambia:
```javascript
const productUrl = months === 1 
    ? 'https://gumroad.com/l/TU-PRODUCTO-MENSUAL' 
    : 'https://gumroad.com/l/TU-PRODUCTO-ANUAL';
```

**Encuentra tus URLs en Gumroad:**
1. **Ve a tu producto** en Gumroad
2. **Copia el "Permalink"** (ej: `https://gumroad.com/l/abc123`)
3. **Reemplaza** en el código

---

## 🧪 Paso 7: Probar el Sistema

### 1. Probar webhook localmente:
```bash
curl -X POST http://localhost:5000/gumroad/test \
  -H "Content-Type: application/json" \
  -d '{"test": "webhook funcionando"}'
```

### 2. Probar activación manual:
```bash
python activate_premium_console.py 123456789012345678 1 "Servidor Test"
```

### 3. Simular compra de Gumroad:
```bash
curl -X POST http://localhost:5000/gumroad/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "seller_id=123&product_id=456&email=test@test.com&price=1.00&gumroad_fee=0.25&sale_id=test123&product_name=Server ID: 123456789012345678"
```

---

## 📊 Paso 8: Monitorear Ventas

### Ver servidores premium activos:
```
!listpremium
```

### Logs del webhook:
Los verás en la consola cuando ejecutes `python gumroad_webhook.py`

### Dashboard de Gumroad:
Ve a tu dashboard para ver estadísticas de ventas.

---

## 🚀 Paso 9: Marketing y Promoción

### 1. Actualizar el comando !premium:
Ya está configurado para mostrar tu enlace de contacto.

### 2. Crear contenido promocional:
- **Screenshots** del bot funcionando
- **Videos** de demostración
- **Testimonios** de usuarios satisfechos

### 3. Promocionar en:
- **Servers de Discord** relacionados con bots
- **Reddit** (r/discordapp, r/Discord_Bots)
- **Twitter/X** con hashtags #Discord #MusicBot

---

## 🔒 Paso 10: Seguridad y Mantenimiento

### 1. Backup de datos:
```bash
# Backup de servidores premium
cp premium_servers.json premium_servers_backup.json
```

### 2. Monitoreo automático:
```bash
# Verificar estado del webhook
curl http://tu-dominio.com/gumroad/health
```

### 3. Actualizar dependencias:
```bash
pip install --upgrade discord.py yt-dlp flask
```

---

## 💰 Proyección de Ingresos

### Escenario Conservador:
- **10 servidores premium/mes** = $10/mes
- **50% renovaciones** = $5/mes adicional
- **Total:** ~$15/mes

### Escenario Optimista:
- **50 servidores premium/mes** = $50/mes
- **70% renovaciones** = $35/mes adicional
- **Total:** ~$85/mes

### Escenario Exitoso:
- **200 servidores premium/mes** = $200/mes
- **80% renovaciones** = $160/mes adicional
- **Total:** ~$360/mes

---

## 🎯 Próximos Pasos

1. ✅ **Crear cuenta en Gumroad**
2. ✅ **Configurar productos** ($1 y $10)
3. ✅ **Subir landing page** (GitHub Pages)
4. ✅ **Configurar webhook** (ngrok para pruebas)
5. ✅ **Hacer primera venta de prueba**
6. 🚀 **¡Empezar a promocionar!**

---

¿Necesitas ayuda con algún paso específico? ¡Estoy aquí para ayudarte! 🌸
