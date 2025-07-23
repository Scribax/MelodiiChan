# 🚀 Sistema de Automatización Premium - MelodiiChan

## 📋 Resumen

Ahora tienes **3 formas** de activar premium sin estar en el servidor:

1. 🖥️ **Consola** - Activación manual rápida
2. 🌐 **Webhook API** - Automatización con plataformas de pago
3. 🤖 **Comando mejorado** - Los usuarios pueden obtener su Server ID fácilmente

---

## 🖥️ 1. Activación por Consola

### Uso:
```bash
python activate_premium_console.py <guild_id> <meses> [nombre_servidor]
```

### Ejemplos:
```bash
# Activar premium por 1 mes
python activate_premium_console.py 123456789012345678 1 "Mi Servidor Kawaii"

# Activar premium por 12 meses (1 año)
python activate_premium_console.py 123456789012345678 12 "Servidor VIP"
```

### ✅ Ventajas:
- ✨ No necesitas estar en el servidor
- ⚡ Activación instantánea
- 🎯 Perfecto para activaciones manuales rápidas

---

## 🌐 2. Sistema de Webhook Automatizado

### Instalación:
```bash
pip install -r webhook_requirements.txt
```

### Ejecutar:
```bash
python payment_webhook.py
```

### 🔗 Endpoints Disponibles:

#### POST `/webhook/payment`
Automatiza la activación cuando se recibe un pago:

```json
{
  "guild_id": 123456789012345678,
  "months": 1,
  "payment_status": "completed",
  "transaction_id": "txn_123456",
  "guild_name": "Mi Servidor"
}
```

#### GET `/webhook/check-status/<guild_id>`
Verifica el estado premium de un servidor.

#### GET `/webhook/health`
Estado del servicio para monitoreo.

### 🔐 Integración con Plataformas de Pago:

#### Stripe:
```javascript
// En tu webhook de Stripe
const webhook_data = {
    guild_id: parseInt(session.metadata.guild_id),
    months: parseInt(session.metadata.months),
    payment_status: "completed",
    transaction_id: session.payment_intent,
    guild_name: session.metadata.guild_name
};

// Enviar a tu webhook
fetch('http://tu-servidor.com/webhook/payment', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Signature': signature
    },
    body: JSON.stringify(webhook_data)
});
```

#### PayPal:
```php
// En tu webhook de PayPal
$webhook_data = [
    'guild_id' => (int)$_POST['custom'],
    'months' => (int)$_POST['option_selection1'],
    'payment_status' => 'completed',
    'transaction_id' => $_POST['txn_id'],
    'guild_name' => $_POST['option_name1']
];

// Enviar a tu webhook
$ch = curl_init('http://tu-servidor.com/webhook/payment');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($webhook_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'X-Signature: ' . $signature
]);
curl_exec($ch);
```

---

## 🤖 3. Comando Mejorado en el Bot

### Nuevo Comando: `!serverid`
Los usuarios pueden obtener fácilmente el ID de su servidor:

```
!serverid
```

**Respuesta:**
```
🆔 ID del Servidor
ID de este servidor: 123456789012345678

📝 ¿Cómo obtener Premium?
1. Copia el ID: 123456789012345678
2. Contacta al desarrollador
3. Proporciona el ID y realiza el pago
4. ¡Premium se activa automáticamente!

💎 Precios
$1 USD/mes por servidor
$10 USD/año por servidor (2 meses gratis!)
```

---

## 🏪 4. Flujo de Compra Automatizado

### Para el Cliente:
1. 🆔 Ejecuta `!serverid` en su servidor
2. 📋 Copia el ID del servidor
3. 💰 Va a tu página de pago
4. 💳 Paga e ingresa el Server ID
5. ✅ Premium se activa automáticamente

### Para Ti:
1. 🔧 Configuras el webhook una vez
2. 💰 Los pagos llegan automáticamente
3. 🤖 El sistema activa premium automáticamente
4. 📊 Puedes monitorear con `!listpremium`

---

## 💡 5. Plataformas de Pago Recomendadas

### 🟦 Stripe
- ✅ Webhooks robustos
- ✅ Fácil integración
- ✅ Pagos internacionales
- 💰 2.9% + $0.30 por transacción

### 🟨 PayPal
- ✅ Muy conocido
- ✅ Webhooks disponibles
- ✅ Fácil para usuarios
- 💰 2.9% + $0.30 por transacción

### 🟪 Gumroad
- ✅ Súper fácil de configurar
- ✅ Webhooks simples
- ✅ Perfecto para productos digitales
- 💰 5% + $0.25 por transacción

---

## 🔐 6. Seguridad

### Cambiar Clave Secreta:
En `payment_webhook.py`, línea 15:
```python
WEBHOOK_SECRET = "tu_clave_secreta_super_segura_2024"
```

### Verificación de Firma:
Todos los webhooks deben incluir una firma HMAC-SHA256 para verificar autenticidad.

---

## 📊 7. Monitoreo

### Ver Servidores Premium:
```
!listpremium
```

### Verificar Estado:
```bash
curl http://localhost:5000/webhook/check-status/123456789012345678
```

### Estado del Servicio:
```bash
curl http://localhost:5000/webhook/health
```

---

## 🚀 Próximos Pasos

1. **Instala las dependencias del webhook:** `pip install -r webhook_requirements.txt`
2. **Configura tu plataforma de pago** (Stripe/PayPal/Gumroad)
3. **Despliega el webhook** en un servidor (Heroku, VPS, etc.)
4. **Prueba el sistema** con activaciones manuales primero
5. **¡Empieza a generar ingresos automáticamente!** 💰

---

¡Ahora tienes un sistema completamente automatizado para monetizar tu bot sin tener que estar en cada servidor! 🎉
