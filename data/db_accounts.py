from werkzeug.security import generate_password_hash
from data.db_session import SqlAlchemyBase
import sqlalchemy


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    passwordhash = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __init__(self, name, role, password):
        self.name = name
        self.role = role
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return self.passwordhash == generate_password_hash(password)