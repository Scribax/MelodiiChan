#!/usr/bin/env python3
"""
Webhook API para automatizar la activación de premium
Se integra con plataformas de pago como Stripe, PayPal, etc.
"""

from flask import Flask, request, jsonify
import hashlib
import hmac
import json
from datetime import datetime
from server_premium import add_premium_server, get_server_premium_status
import logging

# Configuración
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Clave secreta para verificar webhooks (cámbiala por una segura)
WEBHOOK_SECRET = "tu_clave_secreta_super_segura_2024"

def verify_webhook_signature(payload, signature, secret):
    """Verifica que el webhook sea legítimo"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/webhook/payment', methods=['POST'])
def handle_payment_webhook():
    """Maneja webhooks de pago automatizados"""
    try:
        # Verificar firma del webhook (seguridad)
        signature = request.headers.get('X-Signature')
        if not signature:
            return jsonify({'error': 'Missing signature'}), 400
        
        payload = request.get_data()
        if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
            return jsonify({'error': 'Invalid signature'}), 403
        
        # Procesar datos del pago
        data = request.get_json()
        
        # Datos requeridos
        required_fields = ['guild_id', 'months', 'payment_status', 'transaction_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        guild_id = data['guild_id']
        months = data['months']
        payment_status = data['payment_status']
        transaction_id = data['transaction_id']
        guild_name = data.get('guild_name', f'Servidor_{guild_id}')
        
        # Solo activar si el pago fue exitoso
        if payment_status.lower() != 'completed':
            app.logger.info(f"Payment not completed for guild {guild_id}: {payment_status}")
            return jsonify({'message': 'Payment not completed'}), 200
        
        # Validar datos
        if not isinstance(guild_id, int) or guild_id <= 0:
            return jsonify({'error': 'Invalid guild_id'}), 400
        
        if not isinstance(months, int) or months < 1 or months > 120:
            return jsonify({'error': 'Invalid months (1-120)'}), 400
        
        # Activar premium
        expiry_date = add_premium_server(guild_id, guild_name, 0, months)
        
        # Log del evento
        app.logger.info(f"Premium activated - Guild: {guild_id}, Months: {months}, Transaction: {transaction_id}")
        
        # Respuesta exitosa
        return jsonify({
            'success': True,
            'message': 'Premium activated successfully',
            'guild_id': guild_id,
            'guild_name': guild_name,
            'months': months,
            'expires': expiry_date.isoformat(),
            'transaction_id': transaction_id
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/check-status/<int:guild_id>', methods=['GET'])
def check_premium_status(guild_id):
    """Endpoint para verificar el estado premium de un servidor"""
    try:
        status = get_server_premium_status(guild_id)
        
        return jsonify({
            'guild_id': guild_id,
            'is_premium': status['is_premium'],
            'expires': status['expires'].isoformat() if status['expires'] else None,
            'days_left': status['days_left']
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error checking status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/health', methods=['GET'])
def health_check():
    """Endpoint de salud para monitoreo"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'MelodiiChan Premium Webhook'
    }), 200

if __name__ == '__main__':
    print("🌸 Iniciando Webhook de MelodiiChan Premium...")
    print("🔗 Endpoints disponibles:")
    print("   POST /webhook/payment - Procesar pagos")
    print("   GET  /webhook/check-status/<guild_id> - Verificar estado")
    print("   GET  /webhook/health - Estado del servicio")
    print("⚠️  IMPORTANTE: Cambia WEBHOOK_SECRET por una clave segura")
    print("-" * 60)
    
    # Ejecutar en modo desarrollo (para producción usar gunicorn)
    app.run(host='0.0.0.0', port=5000, debug=False)
