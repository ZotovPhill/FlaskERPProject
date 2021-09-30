import os
from abc import ABCMeta, abstractmethod
from typing import Union
from app.core.settings import settings
import faker


class AbstractFixtureLoader(metaclass=ABCMeta):
    BATCH_SIZE = 100
    CATALOG_FOLDER = os.path.join(settings.root_path, 'fixtures', 'catalog')

    def __init__(self):
        self.fake = faker.Faker()

    @abstractmethod
    def load(self, quantity: Union[int, None]) -> None:
        pass

    @abstractmethod
    def env_group(self) -> list:
        return []