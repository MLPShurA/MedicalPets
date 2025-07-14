# Medical Pets - Sistema de Gestión Veterinaria

## Descripción

Medical Pets es un sistema completo de gestión veterinaria que permite administrar usuarios, mascotas, citas médicas, historiales clínicos y tratamientos. El sistema está construido con una arquitectura modular y escalable.

## Estructura del Proyecto

```
MedicalPets/
├── 📁 backend/                    # Backend principal
│   ├── 📁 config/                 # Configuraciones
│   │   ├── database.py           # Configuración de BD
│   │   ├── settings.py           # Configuraciones generales
│   │   └── __init__.py
│   ├── 📁 models/                # Modelos de datos
│   │   ├── usuario.py            # Modelo Usuario
│   │   ├── mascota.py            # Modelo Mascota
│   │   ├── cita.py              # Modelo Cita
│   │   ├── historial.py         # Modelo Historial Médico
│   │   ├── tratamiento.py       # Modelo Tratamiento
│   │   └── __init__.py
│   ├── 📁 services/              # Lógica de negocio
│   │   ├── auth_service.py       # Autenticación
│   │   ├── usuario_service.py    # Gestión de usuarios
│   │   ├── mascota_service.py    # Gestión de mascotas
│   │   ├── cita_service.py       # Gestión de citas
│   │   └── __init__.py
│   ├── 📁 repositories/          # Acceso a datos
│   │   ├── usuario_repository.py # Repositorio usuarios
│   │   ├── mascota_repository.py # Repositorio mascotas
│   │   ├── cita_repository.py    # Repositorio citas
│   │   └── __init__.py
│   ├── 📁 utils/                 # Utilidades
│   │   ├── validators.py         # Validaciones
│   │   ├── exceptions.py         # Excepciones personalizadas
│   │   ├── security.py           # Utilidades de seguridad
│   │   └── __init__.py
│   └── main.py                   # Punto de entrada del backend
├── 📁 frontend/                  # Frontend (Streamlit)
│   ├── 📁 pages/                # Páginas de la aplicación
│   ├── 📁 components/           # Componentes reutilizables
│   ├── 📁 forms/                # Formularios
│   └── main.py                  # Aplicación principal
├── 📁 tests/                    # Pruebas unitarias
├── 📁 docs/                     # Documentación
├── requirements.txt             # Dependencias
└── README.md                   # Este archivo
```

## Características Principales

### 🔐 Autenticación y Autorización
- Sistema de login seguro con bcrypt
- Gestión de roles (admin, veterinario, doctor, secretaria, paciente)
- Tokens JWT para sesiones
- Validación de permisos por rol

### 👥 Gestión de Usuarios
- CRUD completo de usuarios
- Generación automática de contraseñas
- Validación de datos
- Gestión de perfiles detallados

### 🐕 Gestión de Mascotas
- Registro de mascotas con información completa
- Asociación con dueños
- Cálculo automático de edad
- Estados de mascotas (activo, inactivo, fallecido)

### 📅 Gestión de Citas
- Programación de citas médicas
- Verificación de disponibilidad de veterinarios
- Estados de citas (programada, confirmada, completada, etc.)
- Filtros por veterinario, dueño, estado y fecha

### 📋 Historial Médico
- Registro de consultas, vacunaciones, cirugías
- Niveles de severidad
- Asociación con citas y tratamientos

### 💊 Gestión de Tratamientos
- Prescripción de medicamentos y terapias
- Seguimiento de estados de tratamientos
- Cálculo de costos

## Tecnologías Utilizadas

### Backend
- **Python 3.8+**: Lenguaje principal
- **MySQL**: Base de datos
- **bcrypt**: Hashing de contraseñas
- **PyJWT**: Tokens de autenticación
- **Pydantic**: Validación de datos
- **Logging**: Sistema de logs

### Frontend
- **Streamlit**: Framework web
- **Streamlit Option Menu**: Menú de navegación
- **Pandas**: Manipulación de datos
- **Pillow**: Procesamiento de imágenes

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd MedicalPets
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear base de datos MySQL
   - Configurar credenciales en `backend/config/database.py`
   - Ejecutar scripts de migración (si existen)

5. **Ejecutar la aplicación**
   ```bash
   # Desde el directorio raíz
   streamlit run frontend/main.py
   ```

## Configuración

### Base de Datos
Editar `backend/config/database.py`:
```python
HOST = "localhost"
USER = "tu_usuario"
PASSWORD = "tu_contraseña"
DATABASE = "medical_pets_db"
PORT = 3306
```

### Configuraciones Generales
Editar `backend/config/settings.py` para personalizar:
- Roles y permisos
- Reglas de validación
- Configuraciones de seguridad
- Límites del sistema

## Uso del Backend

### Inicialización
```python
from backend.main import get_backend

backend = get_backend()
```

### Autenticación
```python
result = backend.authenticate_user("usuario", "contraseña")
if result['success']:
    user = result['user']
    token = result['token']
```

### Gestión de Usuarios
```python
# Obtener todos los usuarios
usuarios = backend.get_usuarios()

# Crear usuario
nuevo_usuario = backend.create_usuario({
    'nombres': 'Juan',
    'apellidos': 'Pérez',
    'cedula': '1234567890',
    'correo_electronico': 'juan@email.com',
    'rol': 'paciente'
})
```

### Gestión de Mascotas
```python
# Obtener mascotas de un dueño
mascotas = backend.get_mascotas(dueno_id=1)

# Crear mascota
nueva_mascota = backend.create_mascota({
    'nombre': 'Luna',
    'sexo': 'Hembra',
    'edad_anos': 2,
    'edad_meses': 6,
    'raza': 'Golden Retriever',
    'id_dueño': 1
})
```

### Gestión de Citas
```python
# Obtener citas de un veterinario
citas = backend.get_citas(veterinario_id=1)

# Crear cita
nueva_cita = backend.create_cita({
    'fecha_hora': datetime.now(),
    'id_mascota': 1,
    'id_veterinario': 1,
    'id_dueño': 1,
    'tipo': 'consulta_general',
    'motivo': 'Revisión anual'
})
```

## Estructura de Base de Datos

### Tablas Principales
- **usuarios**: Información básica de usuarios
- **usuarios_detalle**: Información detallada de usuarios
- **mascotas**: Información de mascotas
- **citas**: Programación de citas médicas
- **historial_medico**: Registro de historiales clínicos
- **tratamientos**: Gestión de tratamientos médicos

## Desarrollo

### Agregar Nuevos Servicios
1. Crear modelo en `backend/models/`
2. Crear servicio en `backend/services/`
3. Crear repositorio en `backend/repositories/` (si es necesario)
4. Agregar métodos al backend principal
5. Crear pruebas unitarias

### Agregar Nuevas Validaciones
1. Crear validador en `backend/utils/validators.py`
2. Implementar reglas de validación
3. Integrar en los servicios correspondientes

### Logging
El sistema utiliza logging estructurado:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Mensaje informativo")
logger.error("Mensaje de error")
```

## Pruebas

### Ejecutar Pruebas
```bash
pytest tests/
```

### Cobertura de Código
```bash
pytest --cov=backend tests/
```

## Seguridad

### Contraseñas
- Hashing con bcrypt
- Salt automático
- Verificación segura

### Autenticación
- Tokens JWT con expiración
- Validación de sesiones
- Control de acceso por roles

### Validación de Datos
- Sanitización de entradas
- Validación de tipos
- Prevención de inyección SQL

## Mantenimiento

### Logs
Los logs se guardan en `medical_pets.log` y también se muestran en consola.

### Base de Datos
- Realizar backups regulares
- Monitorear rendimiento
- Optimizar consultas según sea necesario

### Actualizaciones
1. Actualizar dependencias: `pip install -r requirements.txt --upgrade`
2. Revisar cambios en la base de datos
3. Ejecutar pruebas
4. Actualizar documentación

## Contribución

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Agregar pruebas
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Contacto

Para soporte técnico o consultas:
- Email: soporte@medicalpets.com
- Documentación: [docs.medicalpets.com](https://docs.medicalpets.com)

---

**Medical Pets** - Cuidando a tus mascotas con tecnología avanzada 🐾
