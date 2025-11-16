from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    op_type = Column(String(20), nullable=False)  # 'Add','Sub','Multiply','Divide'
    result = Column(Float, nullable=True)
    # Example optional FK:
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    # user = relationship('User', backref='calculations')

    def compute(self):
        # compute on demand as well (not used when result stored)
        if self.op_type == 'Add':
            return self.a + self.b
        if self.op_type == 'Sub':
            return self.a - self.b
        if self.op_type == 'Multiply':
            return self.a * self.b
        if self.op_type == 'Divide':
            if self.b == 0:
                raise ZeroDivisionError("Division by zero")
            return self.a / self.b
        raise ValueError('Unknown operation')
