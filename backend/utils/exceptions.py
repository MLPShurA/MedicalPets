class MedicalPetsException(Exception):
    """Excepción base para Medical Pets"""
    pass

class ValidationError(MedicalPetsException):
    """Excepción para errores de validación"""
    pass

class DatabaseError(MedicalPetsException):
    """Excepción para errores de base de datos"""
    pass

class AuthenticationError(MedicalPetsException):
    """Excepción para errores de autenticación"""
    pass

class AuthorizationError(MedicalPetsException):
    """Excepción para errores de autorización"""
    pass

class NotFoundError(MedicalPetsException):
    """Excepción para recursos no encontrados"""
    pass

class BusinessLogicError(MedicalPetsException):
    """Excepción para errores de lógica de negocio"""
    pass
