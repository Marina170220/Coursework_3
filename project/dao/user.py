from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_data):
        user = User(**user_data)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def delete(self, pk):
        user = self.get_one(pk)
        self._db_session.delete(user)
        self._db_session.commit()