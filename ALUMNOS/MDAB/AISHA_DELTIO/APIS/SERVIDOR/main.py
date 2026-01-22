# http://localhost:8001/docs

import os, json, time, secrets
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from mastodon import Mastodon
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. Iniciar API
app = FastAPI(title="Aisha API ")
security = HTTPBasic()

DB_PATH = "/data/drafts.json"

# 2. Seguridad API
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")

def auth(credentials: HTTPBasicCredentials = Depends(security)):
    # Verificar si el usuario y la contraseña coinciden
    is_user_ok = secrets.compare_digest(credentials.username, API_USER)
    is_pass_ok = secrets.compare_digest(credentials.password, API_PASS)
    if not (is_user_ok and is_pass_ok):
        # Si fallan, lanzamos un error 401 (No autorizado)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# 3. Base de datos SQL
DATABASE_URL = "sqlite:////data/stravabot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# modelo base de datos
class DraftDB(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    status = Column(String, default="draft")

# modelo recibir datos
class Draft(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    status: str = "draft"
    
    class Config:
        orm_mode = True
    
Base.metadata.create_all(bind=engine)
    
# 4. Funciones base de datos y funcion auxiliar para ayudar a buscar ids
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_draft(data, draft_id):
    return next((d for d in data if d["id"] == draft_id), None)

# 5. Endpoint
@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Aisha funcionando"}

@app.get("/drafts", response_model=List[Draft], dependencies=[Depends(auth)])
def list_drafts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    drafts = db.query(DraftDB).offset(skip).limit(limit).all()
    return drafts

@app.post("/drafts", status_code=201, dependencies=[Depends(auth)])
def create_draft(draft: Draft, db: Session = Depends(get_db)):
    nuevo_draft = DraftDB(
        title=draft.title,
        content=draft.content,
        status="draft"
    )
    db.add(nuevo_draft) 
    db.commit()         
    db.refresh(nuevo_draft) 
    return nuevo_draft

@app.put("/drafts/{draft_id}", response_model=Draft, dependencies=[Depends(auth)])
def update_draft(draft_id: int, updated_content: Draft, db: Session = Depends(get_db)):
    draft = db.query(DraftDB).filter(DraftDB.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Borrador no encontrado")
    draft.title = updated_content.title
    draft.content = updated_content.content
    # Cambiar el estado manualmente:
    draft.status = updated_content.status
    db.commit()
    db.refresh(draft)
    return draft
    # Si no encontramos el id (error 404)
    raise HTTPException(status_code=404, detail="Borrador no encontrado")


@app.delete("/drafts/{draft_id}", dependencies=[Depends(auth)])
def delete_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.query(DraftDB).filter(DraftDB.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    db.delete(draft)
    db.commit()
    return {"mensaje": f"Borrador {draft_id} eliminado de la base de datos"}


@app.post("/drafts/{draft_id}/publish", dependencies=[Depends(auth)])
def publish_draft(draft_id: int, db: Session = Depends(get_db)):
    # Buscamos el borrador en la base de datos
    draft = db.query(DraftDB).filter(DraftDB.id == draft_id).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Borrador no encontrado")
    
    if draft.status == "published":
        return {"mensaje": "Este borrador ya se publicó anteriormente"}

    m = Mastodon(
        access_token=os.getenv("M_TOKEN_ACCESO"),
        api_base_url=os.getenv("MASTODON_API")
    )

    texto_final = f"📝 {draft.title}\n\n{draft.content}"

    try:
        m.status_post(texto_final)
        # Actualizamos el estado en la base de datos
        draft.status = "published"
        db.commit()
        return {"mensaje": "Publicado con éxito", "id": draft_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))