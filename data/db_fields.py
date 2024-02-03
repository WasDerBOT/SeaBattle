from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Field(Base):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, size, name, matrix):
        self.size = size
        self.name = name
        self.matrix = matrix

    def __repr__(self):
        return f"<Field(size={self.size}, name={self.name})>"

    def get_matrix(self):
        return self.matrix

    def set_matrix(self, matrix):
        if isinstance(matrix, list) and len(matrix) == self.size * self.size:
            self.matrix = matrix
        else:
            raise ValueError("Matrix must be a list of size * size")

    def check_ship(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.matrix[row * self.size + col]
        else:
            raise ValueError("Row and column must be within the field size")

    def place_ship(self, row, col, ship_size):
        if 0 <= row + ship_size - 1 < self.size and 0 <= col < self.size:
            for i in range(ship_size):
                self.matrix[row * self.size + col + i] = 1
        else:
            raise ValueError("Ship cannot be placed outside the field")

    def remove_ship(self, row, col, ship_size):
        if 0 <= row + ship_size - 1 < self.size and 0 <= col < self.size:
            for i in range(ship_size):
                self.matrix[row * self.size + col + i] = 0
        else:
            raise ValueError("Ship cannot be removed outside the field")