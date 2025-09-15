# -*- coding: utf-8 -*-
"""
Golf Tournament API with PostgreSQL (SQLAlchemy version)
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional, Dict
import random, string, math, enum, json, asyncio
from datetime import datetime, timedelta
import os
from auth_postgres import (
    AdminCredentials, Token, AdminUserModel, authenticate_admin, 
    create_access_token, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Database setup - usar SQLite si no hay PostgreSQL configurado
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./golf_tournament.db")

# Para PostgreSQL, el formato es: "postgresql://user:password@localhost/dbname"
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL)
else:
    # SQLite fallback
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums
class TournamentType(str, enum.Enum):
    REGULAR = "regular"
    PELIGROSO = "peligroso"

class TournamentStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

# Models with PostgreSQL improvements
class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Tournament(Base):
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String(6), unique=True, nullable=False, index=True)
    tournament_type = Column(Enum(TournamentType), nullable=False, default=TournamentType.REGULAR)
    status = Column(Enum(TournamentStatus), nullable=False, default=TournamentStatus.ACTIVE)
    case_individual = Column(Integer, nullable=False, default=30000)
    multiplicador = Column(Integer, nullable=False, default=3000)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    players = relationship("Player", back_populates="tournament", cascade="all, delete-orphan")

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    handicap = Column(Integer, nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    gross1 = Column(Integer, nullable=True)
    gross2 = Column(Integer, nullable=True)
    gross_total = Column(Integer, nullable=True)
    neto = Column(Integer, nullable=True)
    putts = Column(Integer, nullable=True)
    neto2 = Column(Float, nullable=True)
    paga_neto = Column(Float, default=0.0)
    paga_putts = Column(Float, default=0.0)
    total_a_pagar = Column(Float, default=0.0)
    scores_submitted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    tournament = relationship("Tournament", back_populates="players")

# Create tables
Base.metadata.create_all(bind=engine)

# Schemas
class TournamentCreate(BaseModel):
    name: str
    tournament_type: TournamentType = TournamentType.REGULAR

class PlayerJoin(BaseModel):
    name: str
    handicap: int
    tournament_code: str

class PlayerScores(BaseModel):
    gross1: int
    gross2: int
    putts: int

# FastAPI app
app = FastAPI(title="Golf Tournament API with PostgreSQL", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint for Railway
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "golf-tournament-api"}

# Utilities
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def redondear_decenas_mil(valor: float) -> int:
    resto = valor % 10000
    return int(valor - resto if resto < 5000 else valor + (10000 - resto))

async def auto_calculate_liquidation(tournament_id: int, db: Session):
    """Calcula automaticamente la liquidacion si hay al menos 2 jugadores con scores"""
    try:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
        if not tournament:
            return None
        
        players_with_scores = db.query(Player).filter(
            Player.tournament_id == tournament_id,
            Player.scores_submitted == True
        ).all()
        
        if len(players_with_scores) < 2:
            return None
        
        # Convert to list of dicts for easier manipulation
        players_data = []
        for p in players_with_scores:
            players_data.append({
                "id": p.id,
                "name": p.name,
                "handicap": p.handicap,
                "neto": p.neto,
                "putts": p.putts,
                "neto2": p.neto2
            })
        
        # Sort by neto and putts
        neto_sorted = sorted(players_data, key=lambda x: (x["neto"], x["neto2"], x["putts"]))
        putts_sorted = sorted(players_data, key=lambda x: (x["putts"], x["neto"]))
        
        total_jugadores = len(players_data)
        num_to_pay = math.ceil(total_jugadores / 2)
        
        # Identify players who pay
        indices_pagan_neto = set(p["id"] for p in neto_sorted[-num_to_pay:])
        indices_pagan_putts = set(p["id"] for p in putts_sorted[-num_to_pay:])
        
        mejor_neto = neto_sorted[0]["neto"]
        mejor_putts = putts_sorted[0]["putts"]
        
        total_pagos = 0
        
        # Calculate payments
        for player_data in players_data:
            player_id = player_data["id"]
            
            paga_neto = 0
            if player_id in indices_pagan_neto:
                paga_neto = (player_data["neto"] - mejor_neto) * tournament.multiplicador
            
            paga_putts = 0
            if player_id in indices_pagan_putts:
                paga_putts = (player_data["putts"] - mejor_putts) * tournament.multiplicador
            
            total_individual = redondear_decenas_mil(paga_neto + paga_putts)
            
            player_data["paga_neto"] = paga_neto
            player_data["paga_putts"] = paga_putts
            player_data["total_a_pagar"] = total_individual
            
            total_pagos += total_individual
            
            # Update player in database
            db_player = db.query(Player).filter(Player.id == player_id).first()
            if db_player:
                db_player.paga_neto = paga_neto
                db_player.paga_putts = paga_putts
                db_player.total_a_pagar = total_individual
        
        # Commit changes to database
        db.commit()
        
        # Final calculations
        total_case = total_jugadores * tournament.case_individual
        total_recaudo = total_case + total_pagos
        atencion = redondear_decenas_mil(total_recaudo * 0.3)
        premios = total_recaudo - atencion
        
        # Calculate prize distribution exactly like the original
        premiacion = []
        
        if total_jugadores <= 12:
            # Rule for 12 or fewer players: prize top 2 (65% and 35%)
            premios_porcentajes = [0.65, 0.35]
            premios_distribuidos = 0
            
            for i in range(min(2, len(neto_sorted))):
                jugador = neto_sorted[i]
                if i == 1:  # Second place gets remaining prize
                    monto = premios - premios_distribuidos
                else:  # First place
                    monto = redondear_decenas_mil(premios * premios_porcentajes[i])
                premios_distribuidos += monto
                
                premiacion.append({
                    "posicion": i + 1,
                    "nombre": jugador["name"],
                    "neto": jugador["neto"],
                    "monto": monto,
                    "tipo": "premio"
                })
        else:
            # Rule for more than 12 players: prize top 3 (50%, 30%, 20%) and show top 5
            premios_top3 = [0.50, 0.30, 0.20]
            premios_distribuidos = 0
            
            for i in range(min(5, len(neto_sorted))):
                jugador = neto_sorted[i]
                
                if i < 3:  # Top 3 get prizes
                    if i == 2:  # Third place gets remaining prize
                        monto = premios - premios_distribuidos
                    else:
                        monto = redondear_decenas_mil(premios * premios_top3[i])
                    premios_distribuidos += monto
                    
                    premiacion.append({
                        "posicion": i + 1,
                        "nombre": jugador["name"],
                        "neto": jugador["neto"],
                        "monto": monto,
                        "tipo": "premio"
                    })
                else:  # 4th and 5th place are honorary positions
                    premiacion.append({
                        "posicion": i + 1,
                        "nombre": jugador["name"],
                        "neto": jugador["neto"],
                        "monto": 0,
                        "tipo": "honor"
                    })
        
        result = {
            "summary": {
                "total_jugadores": total_jugadores,
                "total_case": total_case,
                "total_pagos": total_pagos,
                "total_recaudo": total_recaudo,
                "atencion": atencion,
                "premios": premios,
                "ganador_neto": neto_sorted[0]["name"],
                "ganador_putts": putts_sorted[0]["name"]
            },
            "players": players_data,
            "rankings": {
                "neto": neto_sorted,
                "putts": putts_sorted
            },
            "premiacion": premiacion
        }
        
        return result
        
    except Exception as e:
        print("Error in auto_calculate_liquidation: {}".format(e))
        return None

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
    
    async def connect(self, websocket: WebSocket, tournament_id: int):
        await websocket.accept()
        if tournament_id not in self.active_connections:
            self.active_connections[tournament_id] = []
        self.active_connections[tournament_id].append(websocket)
        print("WebSocket connected to tournament {}".format(tournament_id))
    
    def disconnect(self, websocket: WebSocket, tournament_id: int):
        if tournament_id in self.active_connections:
            if websocket in self.active_connections[tournament_id]:
                self.active_connections[tournament_id].remove(websocket)
                if not self.active_connections[tournament_id]:
                    del self.active_connections[tournament_id]
        print("WebSocket disconnected from tournament {}".format(tournament_id))
    
    async def broadcast_to_tournament(self, tournament_id: int, message: dict):
        if tournament_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[tournament_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for conn in disconnected:
                self.disconnect(conn, tournament_id)
    
    async def broadcast_to_all(self, message: dict):
        for tournament_id in list(self.active_connections.keys()):
            await self.broadcast_to_tournament(tournament_id, message)

manager = ConnectionManager()

# Routes
@app.get("/")
def root():
    db_type = "PostgreSQL" if DATABASE_URL.startswith("postgresql") else "SQLite"
    return {"message": "Golf Tournament API with {}".format(db_type), "status": "active"}

@app.post("/auth/login", response_model=Token)
def login_admin(credentials: AdminCredentials, db: Session = Depends(get_db)):
    """Endpoint para login de administradores"""
    admin = authenticate_admin(credentials.username, credentials.password, db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/auth/me", response_model=AdminUserModel)
def get_current_user(current_admin: AdminUserModel = Depends(get_current_admin)):
    """Obtiene informacion del administrador actual"""
    return current_admin

@app.websocket("/ws/tournament/{tournament_id}")
async def websocket_endpoint(websocket: WebSocket, tournament_id: int):
    await manager.connect(websocket, tournament_id)
    try:
        while True:
            data = await websocket.receive_text()
            print("Received message from tournament {}: {}".format(tournament_id, data))
    except WebSocketDisconnect:
        manager.disconnect(websocket, tournament_id)

@app.post("/tournaments/")
async def create_tournament(
    tournament_data: TournamentCreate, 
    current_admin: AdminUserModel = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # Generate unique code
    while True:
        code = generate_code()
        existing = db.query(Tournament).filter(Tournament.code == code).first()
        if not existing:
            break
    
    # Set values based on type
    case_individual = 30000 if tournament_data.tournament_type == TournamentType.REGULAR else 60000
    multiplicador = 3000 if tournament_data.tournament_type == TournamentType.REGULAR else 2000
    
    tournament = Tournament(
        name=tournament_data.name,
        code=code,
        tournament_type=tournament_data.tournament_type,
        case_individual=case_individual,
        multiplicador=multiplicador
    )
    
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    
    # Send WebSocket notification
    await manager.broadcast_to_all({
        "type": "tournament_created",
        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "code": tournament.code,
            "type": tournament.tournament_type.value,
            "case_individual": tournament.case_individual,
            "multiplicador": tournament.multiplicador
        }
    })
    
    return {
        "id": tournament.id,
        "name": tournament.name,
        "code": tournament.code,
        "type": tournament.tournament_type.value,
        "case_individual": tournament.case_individual,
        "multiplicador": tournament.multiplicador
    }

@app.get("/tournaments/")
def get_tournaments(db: Session = Depends(get_db)):
    tournaments = db.query(Tournament).filter(Tournament.status == TournamentStatus.ACTIVE).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "code": t.code,
            "type": t.tournament_type.value,
            "case_individual": t.case_individual,
            "multiplicador": t.multiplicador,
            "created_at": t.created_at.isoformat()
        } for t in tournaments
    ]

@app.post("/players/join")
async def join_tournament(player_data: PlayerJoin, db: Session = Depends(get_db)):
    # Find tournament
    tournament = db.query(Tournament).filter(Tournament.code == player_data.tournament_code).first()
    if not tournament:
        return {"error": "Codigo de torneo invalido"}
    
    # Check if player already exists
    existing = db.query(Player).filter(
        Player.tournament_id == tournament.id,
        Player.name.ilike("%{}%".format(player_data.name))
    ).first()
    if existing:
        return {"error": "Ya existe un jugador con ese nombre"}
    
    # Create player
    player = Player(
        name=player_data.name,
        handicap=player_data.handicap,
        tournament_id=tournament.id
    )
    
    db.add(player)
    db.commit()
    db.refresh(player)
    
    # Send WebSocket notification
    await manager.broadcast_to_tournament(tournament.id, {
        "type": "player_joined",
        "tournament_id": tournament.id,
        "player": {
            "id": player.id,
            "name": player.name,
            "handicap": player.handicap
        }
    })
    
    return {
        "success": True,
        "player_id": player.id,
        "tournament_name": tournament.name
    }

@app.post("/players/{player_id}/scores")
async def submit_scores(player_id: int, scores: PlayerScores, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return {"error": "Jugador no encontrado"}
    
    # Update scores
    player.gross1 = scores.gross1
    player.gross2 = scores.gross2
    player.putts = scores.putts
    player.gross_total = scores.gross1 + scores.gross2
    player.neto = player.gross_total - player.handicap
    player.neto2 = scores.gross2 - (player.handicap / 2)
    player.scores_submitted = True
    
    db.commit()
    
    # Send WebSocket notification for score update
    await manager.broadcast_to_tournament(player.tournament_id, {
        "type": "scores_updated",
        "tournament_id": player.tournament_id,
        "player": {
            "id": player.id,
            "name": player.name,
            "handicap": player.handicap,
            "gross1": player.gross1,
            "gross2": player.gross2,
            "gross_total": player.gross_total,
            "neto": player.neto,
            "putts": player.putts,
            "scores_submitted": player.scores_submitted
        }
    })
    
    # Auto-calculate liquidation if there are enough players
    liquidation_result = await auto_calculate_liquidation(player.tournament_id, db)
    if liquidation_result:
        # Send WebSocket notification for auto-calculated liquidation
        await manager.broadcast_to_tournament(player.tournament_id, {
            "type": "liquidation_auto_calculated",
            "tournament_id": player.tournament_id,
            "liquidation": liquidation_result
        })
        
        print("Auto-calculated liquidation for tournament {}".format(player.tournament_id))
    
    return {"success": True, "message": "Scores guardados exitosamente"}

@app.get("/tournaments/{tournament_id}/players")
def get_tournament_players(tournament_id: int, db: Session = Depends(get_db)):
    players = db.query(Player).filter(Player.tournament_id == tournament_id).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "handicap": p.handicap,
            "gross_total": p.gross_total,
            "neto": p.neto,
            "putts": p.putts,
            "scores_submitted": p.scores_submitted
        } for p in players
    ]

@app.post("/tournaments/{tournament_id}/liquidation")
async def calculate_liquidation(
    tournament_id: int,
    current_admin: AdminUserModel = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # Same liquidation logic as auto_calculate_liquidation but manually triggered
    result = await auto_calculate_liquidation(tournament_id, db)
    if not result:
        return {"error": "No se pudo calcular la liquidacion"}
    
    # Send WebSocket notification
    await manager.broadcast_to_tournament(tournament_id, {
        "type": "liquidation_calculated",
        "tournament_id": tournament_id,
        "liquidation": result
    })
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)