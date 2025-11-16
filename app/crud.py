from sqlalchemy.orm import Session
from . import models
from .factory import OperationFactory
from .schemas import CalculationCreate

def create_calculation(db: Session, payload: CalculationCreate, persist_result: bool = True):
    calc = models.Calculation(a=payload.a, b=payload.b, op_type=payload.op_type.value)
    op = OperationFactory.get_operation(calc.op_type)
    result = op.compute(calc.a, calc.b)
    if persist_result:
        calc.result = result
        db.add(calc)
        db.commit()
        db.refresh(calc)
        return calc
    else:
        # return transient object with computed result but not persisted
        calc.result = result
        return calc

def get_calculation(db: Session, calc_id: int):
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
