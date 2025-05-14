from sqlalchemy.orm import Session
from src.sql.tables import Images


class DB_Images:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, tg_id: str) -> Images:
        data = Images(tg_id=tg_id)
        self.session.add(data)
        self.session.commit()
        return data

    def delete(self, tg_id: str) -> None:
        data = self.session.query(Images).filter(
            Images.tg_id == tg_id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def get(self, tg_id: str) -> Images | None:
        return self.session.query(Images).filter(
            Images.tg_id == tg_id).one_or_none()
    
    def get_by_id(self, id: str) -> Images | None:
        return self.session.query(Images).filter(
            Images.id == id).one_or_none()
    
    def get_all(self) -> Images | None:
        return self.session.query(Images).all()
