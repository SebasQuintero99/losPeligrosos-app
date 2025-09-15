# 🚀 Railway Deployment Guide

## Prerrequisitos
1. Cuenta en [Railway.app](https://railway.app)
2. Proyecto limpio y listo
3. Variables de entorno configuradas

## 📋 Pasos de Deployment

### 1. Backend API (FastAPI + PostgreSQL)

#### Crear servicio en Railway:
```bash
# Conectar repositorio
railway login
railway init
railway link [PROJECT_ID]
```

#### Variables de entorno requeridas:
```
DATABASE_URL=postgresql://postgres:password@hostname:5432/railway
SECRET_KEY=your-super-secret-jwt-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
```

#### Configuración automática:
- ✅ `requirements.txt` - Dependencias Python
- ✅ `Procfile` - Comando de inicio
- ✅ `railway.toml` - Configuración Railway
- ✅ `/health` endpoint - Health check

### 2. Frontend (Next.js)

#### Variables de entorno:
```
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
PORT=3000
```

#### Configuración automática:
- ✅ `package.json` - Scripts optimizados para Railway
- ✅ `railway.toml` - Configuración Railway
- ✅ Engine versions especificadas

### 3. Base de Datos PostgreSQL

#### En Railway:
1. Crear servicio PostgreSQL
2. Copiar DATABASE_URL al backend
3. Ejecutar setup inicial:

```sql
-- Usar setup_database.sql para crear tablas
```

## 🔧 Comandos de Deploy

### Backend:
```bash
cd backend
railway up
```

### Frontend:
```bash
cd frontend
railway up
```

## ✅ Verificación Post-Deploy

1. **Backend Health Check**: `https://your-backend.railway.app/health`
2. **Frontend**: `https://your-frontend.railway.app`
3. **Database**: Verificar conexión desde backend

## 🔄 Orden de Deploy Recomendado

1. **PostgreSQL Database** (crear primero)
2. **Backend API** (configurar con DATABASE_URL)
3. **Frontend** (configurar con NEXT_PUBLIC_API_URL)

## 🔒 Seguridad

- ✅ Variables sensibles en Railway (no en código)
- ✅ CORS configurado para producción
- ✅ JWT con SECRET_KEY fuerte
- ✅ .env.example como template

## 📝 Notas

- El backend escucha en `0.0.0.0:$PORT` (Railway asigna puerto)
- Frontend usa `next start -p $PORT` para Railway
- Health checks configurados para ambos servicios
- Logs disponibles en Railway dashboard