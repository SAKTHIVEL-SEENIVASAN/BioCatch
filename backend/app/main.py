from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, ml
from .database import engine, Base, get_db
from typing import List
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BioCatch MVP API")

# Allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/fishermen/', response_model=schemas.Fisherman)
def create_fisherman(fisherman: schemas.FishermanCreate, db: Session = Depends(get_db)):
    return crud.create_fisherman(db, fisherman)

@app.get('/fishermen/{fisherman_id}', response_model=schemas.Fisherman)
def get_fisherman(fisherman_id: int, db: Session = Depends(get_db)):
    db_f = crud.get_fisherman(db, fisherman_id)
    if not db_f:
        raise HTTPException(status_code=404, detail="Fisherman not found")
    return db_f

@app.post('/catches/', response_model=schemas.Catch)
def create_catch(catch: schemas.CatchCreate, db: Session = Depends(get_db)):
    if catch.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be > 0")
    return crud.create_catch(db, catch)

@app.get('/catches/', response_model=List[schemas.Catch])
def list_catches(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return crud.list_catches(db, skip, limit)

@app.get('/hotspots/')
def hotspots(db: Session = Depends(get_db)):
    # aggregated counts per rounded tile + predicted probability per tile
    tiles = crud.hotspot_counts(db, precision=2)
    enhanced = []
    for t in tiles:
        # features: in demo we use simple placeholders; in real app call satellite APIs
        features = {
            'sea_temp': 27.0,
            'salinity': 34.0,
            'tide_height': 1.0,
            'moon_phase': 0.5,
            'last_catch_count': t.get('count', 1)
        }
        prob = ml.predict_score(features)
        enhanced.append({**t, 'prob': prob})
    return enhanced

@app.post('/predict/')
def predict(features: dict):
    score = ml.predict_score(features)
    return {'score': score}
