import os
from app.schemas import CalculationCreate, OpType
from app.crud import create_calculation, get_calculation

def test_create_and_read_calculation(db_session):
    payload = CalculationCreate(a=10, b=5, op_type=OpType.Divide)
    calc = create_calculation(db_session, payload, persist_result=True)
    assert calc.id is not None
    fetched = get_calculation(db_session, calc.id)
    assert fetched.result == 2.0

def test_post_endpoint(client):
    # Using FastAPI TestClient, test the POST endpoint
    resp = client.post("/calculations", json={"a": 4, "b": 2, "op_type": "Divide"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == 2.0
