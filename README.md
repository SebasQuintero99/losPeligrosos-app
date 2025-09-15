# 🏌️‍♂️ Golf Tournament Backend API

Modern FastAPI backend for golf tournament management system with PostgreSQL.

## 🚀 Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Production database
- **JWT** - Authentication and authorization
- **WebSockets** - Real-time updates
- **Pydantic** - Data validation

## 📋 Features

- ✨ **Multi-tournament management**
- 👥 **Role-based access** (Admin authentication)
- 🔐 **JWT authentication** with bcrypt
- ⚡ **Real-time updates** via WebSocket
- 📊 **Automatic score calculations**
- 🏆 **Tournament liquidation system**
- 🔄 **SQLAlchemy ORM** with migrations

## 🛠️ Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run development server
uvicorn main_postgres:app --host 0.0.0.0 --port 8000 --reload
```

## ⚙️ Environment Variables

```env
DATABASE_URL=postgresql://postgres:password@hostname:5432/railway
SECRET_KEY=your-super-secret-jwt-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
```

## 🚀 Railway Deployment

1. Connect this repository to Railway
2. Add PostgreSQL service
3. Set environment variables
4. Deploy automatically

## 📚 API Endpoints

### Authentication
- `POST /admin/login` - Admin login
- `POST /admin/register` - Register admin (development)

### Tournaments
- `POST /admin/tournament` - Create tournament
- `GET /admin/tournaments` - List all tournaments
- `GET /tournament/{code}` - Get tournament by code
- `PUT /admin/tournament/{id}/complete` - Complete tournament

### Players
- `POST /player/join` - Join tournament
- `PUT /player/{id}/scores` - Update player scores
- `GET /tournament/{id}/players` - Get tournament players

### WebSocket
- `WS /ws/{tournament_id}` - Real-time tournament updates

### Health
- `GET /health` - Service health check

## 🗄️ Database Schema

- **AdminUser** - Admin authentication
- **Tournament** - Tournament information
- **Player** - Player registration and scores
- **Liquidation** - Tournament results and payouts

## 🔗 Related

- **Frontend**: [Golf Tournament Frontend](https://github.com/SebasQuintero99/golf-tournament-frontend)

---

Built with ❤️ for golf tournament management