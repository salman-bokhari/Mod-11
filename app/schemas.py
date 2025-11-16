from enum import Enum
from pydantic import BaseModel, field_validator


class OpType(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    op: OpType

    # Validate division by zero
    @field_validator("b")
    def validate_divide_zero(cls, value, values):
        if "op" in values and values["op"] == OpType.divide and value == 0:
            raise ValueError("Division by zero is not allowed.")
        return value


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    op: OpType
    result: float

    model_config = {"from_attributes": True}
