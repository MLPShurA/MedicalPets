#!/usr/bin/env python3
"""
Script para verificar específicamente los datos de mascotas y dueños
"""

import mysql.connector
from mysql.connector import Error

def verificar_mascotas_y_duenos():
    """Verifica los datos de mascotas y dueños"""
    
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
        
        # Verificar estructura de mascotas
        print("\n🐾 Estructura de la tabla 'mascotas':")
        cursor.execute("DESCRIBE mascotas")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"  - {column['Field']}: {column['Type']}")
        
        # Verificar mascotas con información de dueños
        print("\n📋 Mascotas con información de dueños:")
        cursor.execute("""
            SELECT m.id, m.nombre, m.raza, m.sexo, m.id_dueño,
                   u.nombre_usuario, u.apellidos, u.correo
            FROM mascotas m
            LEFT JOIN usuarios u ON m.id_dueño = u.id
            ORDER BY m.nombre
        """)
        mascotas = cursor.fetchall()
        
        if mascotas:
            for mascota in mascotas:
                print(f"  - Mascota: {mascota['nombre']} ({mascota['raza']})")
                print(f"    Dueño: {mascota['nombre_usuario']} {mascota['apellidos']}")
                print(f"    Correo: {mascota['correo']}")
                print(f"    ID Dueño: {mascota['id_dueño']}")
                print("    ---")
        else:
            print("  ❌ No hay mascotas registradas")
        
        # Verificar veterinarios/doctores
        print("\n👨‍⚕️ Veterinarios/Doctores:")
        cursor.execute("""
            SELECT id, nombre_usuario, apellidos, rol, correo
            FROM usuarios
            WHERE rol IN ('veterinario', 'doctor')
            ORDER BY nombre_usuario
        """)
        veterinarios = cursor.fetchall()
        
        if veterinarios:
            for vet in veterinarios:
                print(f"  - ID: {vet['id']}, Nombre: {vet['nombre_usuario']} {vet['apellidos']}")
                print(f"    Rol: {vet['rol']}, Correo: {vet['correo']}")
                print("    ---")
        else:
            print("  ❌ No hay veterinarios/doctores registrados")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Verificación completada")
        
    except Error as e:
        print(f"❌ Error de MySQL: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🔍 Verificando datos de mascotas y dueños...")
    verificar_mascotas_y_duenos() 