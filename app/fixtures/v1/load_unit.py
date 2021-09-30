from typing import Union
from app.fixtures.abstract_fixture_loader import AbstractFixtureLoader
from app.orm.models import Unit
from app.orm.repository.base import session_scope


class LoadUnit(AbstractFixtureLoader):
    def load(self, quantity: Union[int, None]) -> None:
        objects = [
            Unit(
                name=self.fake.sentence(nb_words=4, variable_nb_words=True),
                description=self.fake.sentence(nb_words=4, variable_nb_words=True)
            )
            for _ in range(quantity)
        ]
        with session_scope() as session:
            session.bulk_save_objects(objects)


    def env_group(self) -> list:
        return ['dev', 'prod']