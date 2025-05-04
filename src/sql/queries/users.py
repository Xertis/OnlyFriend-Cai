from sqlalchemy.orm import Session
from src.sql.tables import Users


class DB_Users:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, tg_id: str) -> Users:
        data = Users(tg_id=tg_id)
        self.session.add(data)
        self.session.commit()
        return data

    def delete(self, tg_id: str) -> None:
        data = self.session.query(Users).filter(
            Users.tg_id == tg_id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def get(self, tg_id: str) -> Users | None:
        return self.session.query(Users).filter(
            Users.tg_id == tg_id).one_or_none()
