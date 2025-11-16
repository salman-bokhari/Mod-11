import pytest
from app.factory import OperationFactory, Add, Sub, Multiply, Divide
from app.schemas import CalculationCreate, OpType

def test_factory_add():
    op = OperationFactory.get_operation('Add')
    assert isinstance(op, Add)
    assert op.compute(2,3) == 5

def test_factory_divide_by_zero():
    op = OperationFactory.get_operation('Divide')
    with pytest.raises(ZeroDivisionError):
        op.compute(1,0)

def test_schema_validation_divide_zero():
    with pytest.raises(ValueError):
        CalculationCreate(a=1, b=0, op_type=OpType.Divide)

def test_schema_ok_add():
    payload = CalculationCreate(a=2, b=3, op_type=OpType.Add)
    assert payload.a == 2 and payload.b == 3 and payload.op_type == OpType.Add
