from pydantic import BaseModel, field_validator
from enum import Enum


class OperationType(str, Enum):
    Add = "Add"
    Sub = "Sub"
    Multiply = "Multiply"
    Divide = "Divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: OperationType

    # Validate division by zero
    @field_validator("b")
    def validate_divide_zero(cls, value, values):
        # If "type" is Divide AND b == 0 → raise ValueError
        if "type" in values and values["type"] == OperationType.Divide and value == 0:
            raise ValueError("Division by zero is not allowed.")
        return value


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: OperationType
    result: float

    model_config = {
        "from_attributes": True
    }
