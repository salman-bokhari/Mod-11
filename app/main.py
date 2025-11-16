from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models import Base
from .schemas import CalculationCreate, CalculationRead
from .crud import create_calculation, get_calculation

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

# Prepare a single connect_args dict (no duplicate keyword)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # for psycopg2 compatible URLs, set a small connect timeout so tests don't hang
    connect_args["connect_timeout"] = 5

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title='Calculation Service (for assignment)')

@app.on_event("startup")
def on_startup():
    # Create SQLite tables automatically for local tests/dev.
    # For Postgres in CI, tests use per-test table creation or rely on the integration fixture.
    if DATABASE_URL.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/calculations', response_model=CalculationRead)
def post_calc(payload: CalculationCreate, db = Depends(get_db)):
    try:
        calc = create_calculation(db, payload, persist_result=True)
        return calc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/calculations/{calc_id}', response_model=CalculationRead)
def read_calc(calc_id: int, db = Depends(get_db)):
    c = get_calculation(db, calc_id)
    if not c:
        raise HTTPException(404, 'Not found')
    return c

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
