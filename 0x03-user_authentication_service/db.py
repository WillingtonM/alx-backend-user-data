"""
DB module that connects & intializes database
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session obj
        """
        if self.__session is None:
            DBSess = sessionmaker(bind=self._engine)
            self.__session = DBSess()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Uses email and hashed password to create new user
        Returns: user
        """
        try:
            usr = User(email=email, hashed_password=hashed_password)
            self._session.add(usr)
            self._session.commit()
        except Exception:
            self._session.rollback()
            usr = None
        return usr

    def find_user_by(self, **kwargs) -> User:
        """
        Filters for user utilizing kwargs
        returns: user
        """
        flds, vals = [], []
        for k, val in kwargs.items():
            if hasattr(User, k):
                flds.append(getattr(User, k))
                vals.append(val)
            else:
                raise InvalidRequestError()
        res = self._session.query(User).filter(
            tuple_(*flds).in_([tuple(vals)])
        ).first()
        if res is None:
            raise NoResultFound()
        return res

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user based on a given id, or raises ValueError
        if attribute not present.
        """
        usr = self.find_user_by(id=user_id)
        for k, val in kwargs.items():
            if getattr(usr, str(k), 'None') == 'None':
                raise ValueError
            setattr(usr, str(k), val)
        self._session.commit()
