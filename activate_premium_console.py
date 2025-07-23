#!/usr/bin/env python3
"""
Script para activar premium desde consola usando ID de servidor
Uso: python activate_premium_console.py <guild_id> <meses>
"""

import sys
from server_premium import add_premium_server
from datetime import datetime

def activate_premium_by_id(guild_id, guild_name, months=1):
    """Activa premium para un servidor por su ID"""
    try:
        # Activar premium (usamos 0 como owner_id ya que no lo conocemos)
        expiry_date = add_premium_server(guild_id, guild_name, 0, months)
        
        print(f"✅ Premium activado exitosamente!")
        print(f"🏷️  Servidor: {guild_name}")
        print(f"🆔 ID: {guild_id}")
        print(f"📅 Expira: {expiry_date.strftime('%d/%m/%Y')}")
        print(f"⏰ Duración: {months} mes(es)")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error al activar premium: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("❌ Uso incorrecto")
        print("📝 Uso: python activate_premium_console.py <guild_id> <meses> [nombre_servidor]")
        print("📝 Ejemplo: python activate_premium_console.py 123456789 1 'Mi Servidor'")
        return
    
    try:
        guild_id = int(sys.argv[1])
        months = int(sys.argv[2])
        guild_name = sys.argv[3] if len(sys.argv) > 3 else f"Servidor_{guild_id}"
        
        if months < 1 or months > 120:
            print("❌ El número de meses debe estar entre 1 y 120")
            return
        
        print("🌸 Activando Premium para MelodiiChan...")
        print(f"🆔 ID del Servidor: {guild_id}")
        print(f"📅 Duración: {months} mes(es)")
        print(f"🏷️  Nombre: {guild_name}")
        print("-" * 50)
        
        success = activate_premium_by_id(guild_id, guild_name, months)
        
        if success:
            print("🎉 ¡Premium activado con éxito!")
            print("💡 El servidor ahora tiene acceso ilimitado a música")
        
    except ValueError:
        print("❌ Error: guild_id y meses deben ser números")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
