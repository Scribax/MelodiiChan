#!/usr/bin/env python3
"""
Webhook específico para Gumroad - MelodiiChan Premium
Automatiza la activación de premium cuando se recibe un pago de Gumroad
"""

from flask import Flask, request, jsonify
import hashlib
import hmac
import json
from datetime import datetime
from bot.server_premium import add_premium_server, get_server_premium_status
import logging
import re

# Configuración
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Clave secreta de Gumroad (la obtienes de tu dashboard)
GUMROAD_SECRET = "tu_clave_secreta_gumroad"

def verify_gumroad_signature(payload, signature, secret):
    """Verifica que el webhook de Gumroad sea legítimo"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

@app.route('/gumroad/webhook', methods=['POST'])
def handle_gumroad_webhook():
    """Maneja webhooks de Gumroad para activación automática"""
    try:
        # Verificar contenido
        if request.content_type != 'application/x-www-form-urlencoded':
            return jsonify({'error': 'Invalid content type'}), 400
        
        # Obtener datos del formulario (Gumroad envía como form data)
        data = request.form.to_dict()
        
        # Log de datos recibidos (para debugging)
        app.logger.info(f"Gumroad webhook received: {data}")
        
        # Verificar campos requeridos de Gumroad
        required_fields = ['seller_id', 'product_id', 'email', 'price', 'gumroad_fee']
        if not all(field in data for field in required_fields):
            app.logger.error(f"Missing required fields: {list(data.keys())}")
            return jsonify({'error': 'Missing required Gumroad fields'}), 400
        
        # Extraer información del producto
        product_name = data.get('product_name', '')
        buyer_email = data.get('email', '')
        sale_id = data.get('sale_id', 'unknown')
        price = float(data.get('price', 0))
        
        # Extraer Server ID del nombre del producto o campos personalizados
        server_id = None
        months = 1
        
        # Buscar Server ID en campos personalizados de Gumroad
        for key, value in data.items():
            if 'server_id' in key.lower() or 'guild_id' in key.lower():
                try:
                    server_id = int(value)
                    break
                except ValueError:
                    continue
        
        # Si no se encuentra en campos personalizados, buscar en el nombre del producto
        if not server_id and product_name:
            # Buscar patrones como "Server: 123456789" o "ID: 123456789"
            match = re.search(r'(?:server|id|guild)[\s:]+(\d{15,20})', product_name, re.IGNORECASE)
            if match:
                server_id = int(match.group(1))
        
        # Determinar duración basada en el precio
        if price >= 10:
            months = 12  # $10+ = 1 año
        elif price >= 5:
            months = 6   # $5+ = 6 meses
        else:
            months = 1   # $1+ = 1 mes
        
        # Validar que tenemos el Server ID
        if not server_id:
            app.logger.error(f"No server ID found in product: {product_name}")
            return jsonify({
                'error': 'Server ID not found',
                'message': 'Please include the Discord Server ID in the product name or custom fields'
            }), 400
        
        # Validar Server ID
        if server_id <= 0 or len(str(server_id)) < 15:
            return jsonify({'error': 'Invalid Discord Server ID'}), 400
        
        # Crear nombre del servidor
        server_name = f"Servidor_{server_id}"
        if product_name:
            # Extraer nombre del servidor del nombre del producto si está disponible
            name_match = re.search(r'nombre[\s:]+([^|]+)', product_name, re.IGNORECASE)
            if name_match:
                server_name = name_match.group(1).strip()
        
        # Activar premium
        expiry_date = add_premium_server(server_id, server_name, 0, months)
        
        # Log del evento exitoso
        app.logger.info(f"Premium activated via Gumroad - Server: {server_id}, Months: {months}, Sale: {sale_id}, Email: {buyer_email}")
        
        # Respuesta exitosa para Gumroad
        response_data = {
            'success': True,
            'message': 'Premium activated successfully',
            'server_id': server_id,
            'server_name': server_name,
            'months': months,
            'expires': expiry_date.isoformat(),
            'sale_id': sale_id,
            'buyer_email': buyer_email
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error processing Gumroad webhook: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/gumroad/check-status/<int:server_id>', methods=['GET'])
def check_server_premium_status(server_id):
    """Endpoint para verificar el estado premium de un servidor"""
    try:
        status = get_server_premium_status(server_id)
        
        return jsonify({
            'server_id': server_id,
            'is_premium': status['is_premium'],
            'expires': status['expires'].isoformat() if status['expires'] else None,
            'days_left': status['days_left']
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error checking status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/gumroad/health', methods=['GET'])
def health_check():
    """Endpoint de salud para monitoreo"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'MelodiiChan Gumroad Integration'
    }), 200

@app.route('/gumroad/test', methods=['POST'])
def test_webhook():
    """Endpoint para probar la integración"""
    try:
        data = request.get_json() or request.form.to_dict()
        
        return jsonify({
            'message': 'Test webhook received successfully',
            'data_received': data,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🟪 Iniciando Webhook de Gumroad para MelodiiChan...")
    print("🔗 Endpoints disponibles:")
    print("   POST /gumroad/webhook - Procesar ventas de Gumroad")
    print("   GET  /gumroad/check-status/<server_id> - Verificar estado")
    print("   GET  /gumroad/health - Estado del servicio")
    print("   POST /gumroad/test - Probar integración")
    print("⚠️  IMPORTANTE: Configura GUMROAD_SECRET con tu clave real")
    print("💡 URL del webhook para Gumroad: http://tu-dominio.com/gumroad/webhook")
    print("-" * 80)
    
    # Ejecutar en modo desarrollo
    app.run(host='0.0.0.0', port=5000, debug=True)
