# 🏌️‍♂️ Golf Tournament System - Modern Stack

Sistema moderno de liquidación de torneos de golf con Next.js + FastAPI

## 📦 Stack Tecnológico

### Backend
- **FastAPI** - API REST moderna y rápida
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **JWT** - Autenticación stateless
- **WebSockets** - Actualizaciones en tiempo real

### Frontend  
- **Next.js 14** - Framework React con SSR
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Diseño moderno y responsivo
- **shadcn/ui** - Componentes UI de alta calidad
- **TanStack Query** - Estado del servidor
- **Zustand** - Estado local

## 🚀 Fase de Desarrollo

### ✅ Fase 1: Backend Foundation (Semanas 1-2)
- [x] Estructura del proyecto
- [ ] Configuración FastAPI
- [ ] Modelos de base de datos
- [ ] Migración de lógica de cálculo
- [ ] APIs básicas

### 🔄 Fase 2: Frontend Base (Semanas 3-4)  
- [ ] Setup Next.js + TypeScript
- [ ] Componentes UI base
- [ ] Páginas principales
- [ ] Integración con API

### 🎯 Fase 3: Funcionalidades Avanzadas (Semanas 5-6)
- [ ] Autenticación JWT
- [ ] WebSockets tiempo real
- [ ] PWA capabilities
- [ ] Testing y deployment

## 📋 Comandos de Desarrollo

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend  
npm install
npm run dev
```

## 🌟 Funcionalidades Principales

- ✨ **Multi-torneo**: Gestión de múltiples torneos simultáneos
- 👥 **Roles**: Admin (crea torneos) y Jugadores (se unen con código)
- 📱 **Responsive**: Diseño mobile-first
- ⚡ **Tiempo Real**: Updates instantáneos de scores
- 🔐 **Seguro**: Autenticación JWT y validaciones
- 📊 **Dashboard**: Analytics y reportes avanzados