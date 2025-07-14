import mysql.connector
from mysql.connector import Error
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Configuración de la base de datos"""
    
    HOST = "localhost"
    USER = "root"
    PASSWORD = "FurryFriends001"
    DATABASE = "furryfriendsdbb"
    PORT = 3306
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Retorna la cadena de conexión"""
        return f"mysql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}"
    
    @classmethod
    def get_connection(cls) -> Optional[mysql.connector.MySQLConnection]:
        """Obtiene una conexión a la base de datos"""
        try:
            connection = mysql.connector.connect(
                host=cls.HOST,
                user=cls.USER,
                password=cls.PASSWORD,
                database=cls.DATABASE,
                port=cls.PORT,
                autocommit=False
            )
            return connection
        except Error as e:
            logger.error(f"Error conectando a la base de datos: {e}")
            return None
    
    @classmethod
    def test_connection(cls) -> bool:
        """Prueba la conexión a la base de datos"""
        connection = cls.get_connection()
        if connection:
            connection.close()
            return True
        return False

# Función de compatibilidad con el código existente
def get_connection():
    """Función de compatibilidad para mantener el código existente funcionando"""
    return DatabaseConfig.get_connection()
