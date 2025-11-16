from pydantic import BaseModel, Field, validator
from enum import Enum

class OpType(str, Enum):
    Add = 'Add'
    Sub = 'Sub'
    Multiply = 'Multiply'
    Divide = 'Divide'

class CalculationCreate(BaseModel):
    a: float = Field(..., description='Left operand')
    b: float = Field(..., description='Right operand')
    op_type: OpType

    @validator('b')
    def check_division_by_zero(cls, v, values):
        # only apply when op_type is Divide
        op = values.get('op_type')
        if op == OpType.Divide and v == 0:
            raise ValueError('b (divisor) cannot be zero for Divide operation')
        return v

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    op_type: OpType
    result: float | None = None

    class Config:
        orm_mode = True
