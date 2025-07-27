#!/usr/bin/env python3
"""
Script para verificar la estructura de la base de datos y usuarios existentes
"""

import mysql.connector
from mysql.connector import Error

def verificar_base_datos():
    """Verifica la estructura de la base de datos y usuarios"""
    
    # Configuración de la base de datos
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'FurryFriends001',
        'database': 'furryfriendsdbb'
    }
    
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        
        print("✅ Conectado a la base de datos MySQL")
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n📋 Tablas existentes:")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"  - {table_name}")
        
        # Verificar estructura de usuarios
        print("\n👥 Estructura de la tabla 'usuarios':")
        cursor.execute("DESCRIBE usuarios")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"  - {column['Field']}: {column['Type']}")
        
        # Verificar usuarios existentes
        print("\n👤 Usuarios existentes:")
        cursor.execute("SELECT id, username, rol FROM usuarios")
        usuarios = cursor.fetchall()
        
        if usuarios:
            for usuario in usuarios:
                print(f"  - ID: {usuario['id']}, Usuario: {usuario['username']}, Rol: {usuario['rol']}")
        else:
            print("  ❌ No hay usuarios registrados")
        
        # Verificar usuarios_detalle
        print("\n📝 Estructura de la tabla 'usuarios_detalle':")
        cursor.execute("DESCRIBE usuarios_detalle")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"  - {column['Field']}: {column['Type']}")
        
        # Verificar usuarios_detalle existentes
        print("\n📋 Usuarios con detalles:")
        cursor.execute("""
            SELECT u.id, u.username, u.rol, ud.nombres, ud.apellidos
            FROM usuarios u
            LEFT JOIN usuarios_detalle ud ON u.id = ud.usuario_id
        """)
        usuarios_detalle = cursor.fetchall()
        
        if usuarios_detalle:
            for usuario in usuarios_detalle:
                print(f"  - ID: {usuario['id']}, Usuario: {usuario['username']}, Rol: {usuario['rol']}, Nombre: {usuario['nombres']} {usuario['apellidos']}")
        else:
            print("  ❌ No hay usuarios con detalles")
        
        # Verificar veterinarios/doctores específicamente
        print("\n👨‍⚕️ Veterinarios/Doctores:")
        cursor.execute("""
            SELECT u.id, u.username, u.rol, ud.nombres, ud.apellidos
            FROM usuarios u
            LEFT JOIN usuarios_detalle ud ON u.id = ud.usuario_id
            WHERE u.rol IN ('veterinario', 'doctor')
        """)
        veterinarios = cursor.fetchall()
        
        if veterinarios:
            for vet in veterinarios:
                print(f"  - ID: {vet['id']}, Usuario: {vet['username']}, Rol: {vet['rol']}, Nombre: {vet['nombres']} {vet['apellidos']}")
        else:
            print("  ❌ No hay veterinarios/doctores registrados")
        
        # Verificar mascotas
        print("\n🐾 Mascotas existentes:")
        cursor.execute("""
            SELECT m.id, m.nombre, m.raza, ud.nombres, ud.apellidos
            FROM mascotas m
            LEFT JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
        """)
        mascotas = cursor.fetchall()
        
        if mascotas:
            for mascota in mascotas:
                print(f"  - ID: {mascota['id']}, Nombre: {mascota['nombre']}, Raza: {mascota['raza']}, Dueño: {mascota['nombres']} {mascota['apellidos']}")
        else:
            print("  ❌ No hay mascotas registradas")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Verificación completada")
        
    except Error as e:
        print(f"❌ Error de MySQL: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🔍 Iniciando verificación de base de datos...")
    verificar_base_datos() 