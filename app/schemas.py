from enum import Enum
from pydantic import BaseModel, field_validator


class OpType(str, Enum):
    Add = "Add"
    Sub = "Sub"
    Multiply = "Multiply"
    Divide = "Divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    op_type: OpType

    @field_validator("b")
    def validate_divide_zero(cls, value, info):
        # info.data contains already-parsed fields
        op = info.data.get("op_type")
        if op == OpType.Divide and value == 0:
            raise ValueError("Division by zero is not allowed.")
        return value


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    op_type: OpType
    result: float

    model_config = {"from_attributes": True}
