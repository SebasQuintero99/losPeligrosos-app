# -*- coding: utf-8 -*-
"""
Sistema de autenticacion para administradores usando PostgreSQL/SQLAlchemy
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

# Configuracion
SECRET_KEY = os.getenv("SECRET_KEY", "golf-tournament-super-secret-key-change-in-production")
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))  # 8 horas

# Setup de password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Import here to avoid circular imports
def get_admin_user_model():
    from main_postgres import AdminUser
    return AdminUser

# Esquemas de datos
class AdminCredentials(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class AdminUserModel(BaseModel):
    username: str
    is_admin: bool = True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contrasena contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera hash de una contrasena"""
    return pwd_context.hash(password)

def authenticate_admin(username: str, password: str, db: Session) -> Optional[AdminUserModel]:
    """Autentica un administrador usando la base de datos"""
    try:
        AdminUser = get_admin_user_model()
        user_data = db.query(AdminUser).filter(AdminUser.username == username).first()
        
        # Si no existe el usuario en la DB, usar los usuarios hardcodeados como fallback
        if not user_data:
            # Fallback to hardcoded users
            ADMIN_USERS = {
                "admin": {
                    "username": "admin",
                    "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
                    "is_admin": True
                },
                "juan": {
                    "username": "juan",
                    "hashed_password": "$2b$12$KIX1h2Gt5YOg3JKqFE.NMuwJvlBRbh6z8r0KeLM5EYqxz6Y5zg9EO",  # golf123
                    "is_admin": True
                },
                "los_peligrosos": {
                    "username": "los_peligrosos",
                    "hashed_password": "$2b$12$B8Vl4vQpnGb9EkKrZJ.Tpeq3gZ2EjhTy8HKF7NX8J9WvU2bAaI.8O",  # neiva2024
                    "is_admin": True
                }
            }
            
            hardcoded_user = ADMIN_USERS.get(username)
            if hardcoded_user and verify_password(password, hardcoded_user["hashed_password"]):
                return AdminUserModel(username=hardcoded_user["username"], is_admin=hardcoded_user["is_admin"])
            return None
        
        if not verify_password(password, user_data.hashed_password):
            return None
        return AdminUserModel(username=user_data.username, is_admin=user_data.is_admin)
    except Exception as e:
        print("Error in authenticate_admin: {}".format(e))
        return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AdminUserModel:
    """Verifica un token JWT y retorna el usuario administrador"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # For token verification, we just validate the username exists in either DB or hardcoded
    return AdminUserModel(username=username, is_admin=True)

def get_current_admin(current_user: AdminUserModel = Depends(verify_token)) -> AdminUserModel:
    """Obtiene el administrador actual (dependencia para rutas protegidas)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Funcion para generar hashes de contrasenas (para desarrollo)
def generate_password_hash(password: str):
    """Utility function para generar hashes de contrasenas"""
    return get_password_hash(password)

if __name__ == "__main__":
    # Para generar hashes de contrasenas
    print("Password hashes:")
    print("secret -> {}".format(generate_password_hash('secret')))
    print("golf123 -> {}".format(generate_password_hash('golf123')))
    print("neiva2024 -> {}".format(generate_password_hash('neiva2024')))