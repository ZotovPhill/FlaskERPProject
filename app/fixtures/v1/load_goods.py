from typing import Union
import random
from app.fixtures.abstract_fixture_loader import AbstractFixtureLoader
from app.orm.models import Product
from app.orm.repository.base import session_scope
from app.orm.repository import unit_repository, category_repository


class LoadGoods(AbstractFixtureLoader):
    def load(self, quantity: Union[int, None]) -> None:
        with session_scope() as session:
            units = unit_repository.find_all(session)
            categories = category_repository.find_all(session)
            units_count = len(units)
            categories_count = len(categories)
            objects = [
                Product(
                    name=self.fake.sentence(nb_words=4, variable_nb_words=True),
                    country_of_origin=self.fake.country_code(),
                    expiration_time=self.fake.date_between(start_date='today', end_date='+10y'),
                    unit_id=units[random.randint(0, units_count-1)].id,
                    category_id=categories[random.randint(0, categories_count-1)].id
                )
                for _ in range(quantity)
            ]
            session.bulk_save_objects(objects)


    def env_group(self) -> list:
        return ['dev', 'prod']