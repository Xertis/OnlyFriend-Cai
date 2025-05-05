from sqlalchemy.orm import Session
from src.sql.tables import Characters


class DB_Characters:
    def __init__(self, session: Session) -> None:
        self.session = session

    def has(self, owner_tg_id: str, name: str) -> Characters | None:
        return self.session.query(Characters).filter(
            Characters.name == name,
            Characters.owner_rel.has(tg_id=owner_tg_id)
        ).one_or_none()

    def add(
            self,
            name: str,
            owner: int,
            start_context: str,
            context: str = '') -> Characters:
        data = Characters(
            name=name,
            owner=owner,
            start_context=start_context,
            context=context
        )
        self.session.add(data)
        self.session.commit()
        return data

    def delete(self, character_id: int) -> None:
        data = self.session.query(Characters).filter(
            Characters.id == character_id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def get_by_id(self, character_id: int) -> Characters | None:
        return self.session.query(Characters).filter(
            Characters.id == character_id).one_or_none()

    def get_by_owner(self, owner_id: int) -> list[Characters]:
        return self.session.query(Characters).filter(
            Characters.owner == owner_id).all()

    def update_context(self, character_id: int, new_context: str) -> None:
        character = self.get_by_id(character_id)
        if character:
            character.context = new_context
            self.session.commit()
