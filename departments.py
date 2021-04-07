import sqlalchemy
from data.db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from flask_login import UserMixin


class Departments(SqlAlchemyBase, UserMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')

    def __repr__(self):
        return f"<Department> {self.id} {self.title} {self.email}"
