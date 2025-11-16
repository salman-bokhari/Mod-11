import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.schemas import CalculationCreate, OpType
from app.crud import create_calculation, get_calculation

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(autouse=True)
def prepare_db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

def test_create_and_read_calculation():
    db = SessionLocal()
    payload = CalculationCreate(a=10, b=5, op_type=OpType.Divide)
    calc = create_calculation(db, payload, persist_result=True)
    assert calc.id is not None
    # fetch
    fetched = get_calculation(db, calc.id)
    assert fetched.result == 2.0

def test_error_invalid_op_type():
    db = SessionLocal()
    # simulate invalid type by bypassing schema and using crud with wrong op_type
    from app.schemas import CalculationCreate
    with pytest.raises(Exception):
        bad = CalculationCreate(a=1,b=2, op_type='Unknown')  # should raise since validation fails
