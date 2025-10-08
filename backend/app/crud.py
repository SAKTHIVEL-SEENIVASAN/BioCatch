from sqlalchemy.orm import Session
from . import models, schemas
from collections import defaultdict
from typing import List

def create_fisherman(db: Session, fisherman: schemas.FishermanCreate):
    db_f = models.Fisherman(name=fisherman.name, phone=fisherman.phone)
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

def get_fisherman(db: Session, fisherman_id: int):
    return db.query(models.Fisherman).filter(models.Fisherman.id == fisherman_id).first()

def create_catch(db: Session, catch: schemas.CatchCreate):
    db_c = models.Catch(
        fisherman_id=catch.fisherman_id,
        species=catch.species,
        quantity=catch.quantity,
        size_cm=catch.size_cm,
        lat=catch.lat,
        lon=catch.lon,
        photo_url=catch.photo_url,
    )
    db.add(db_c)
    db.commit()
    db.refresh(db_c)
    return db_c

def list_catches(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Catch).order_by(models.Catch.created_at.desc()).offset(skip).limit(limit).all()

def hotspot_counts(db: Session, precision: int = 2):
    counts = defaultdict(int)
    catches = db.query(models.Catch).all()
    for c in catches:
        key = (round(c.lat, precision), round(c.lon, precision))
        counts[(key, c.species)] += c.quantity
    # produce list entries with species, lat, lon, count
    out = []
    for ((latlon, species), count) in counts.items():
        lat, lon = latlon
        out.append({'species': species, 'lat': float(lat), 'lon': float(lon), 'count': int(count)})
    return out
