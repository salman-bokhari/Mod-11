from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        pass

class Add(Operation):
    def compute(self, a, b):
        return a + b

class Sub(Operation):
    def compute(self, a, b):
        return a - b

class Multiply(Operation):
    def compute(self, a, b):
        return a * b

class Divide(Operation):
    def compute(self, a, b):
        if b == 0:
            raise ZeroDivisionError('Division by zero')
        return a / b

class OperationFactory:
    mapping = {
        'Add': Add,
        'Sub': Sub,
        'Multiply': Multiply,
        'Divide': Divide,
    }

    @classmethod
    def get_operation(cls, op_name: str) -> Operation:
        op_cls = cls.mapping.get(op_name)
        if not op_cls:
            raise ValueError(f'Unknown operation: {op_name}')
        return op_cls()
