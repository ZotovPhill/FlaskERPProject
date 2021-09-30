import click
import os
import re
import tracemalloc
import textwrap
from flask import Blueprint
import yaml
import importlib

from app.core.settings import settings

fixtures = Blueprint("fixtures", __name__)


@fixtures.cli.command("load-fixtures")
@click.argument("config_path")
@click.option(
    "-i" "--no-interaction",
    "to_skip_interaction",
    is_flag=True,
    default=True,
    help=f"Pointing this argument for no disable interactions and \n"
    f"console input. WARNING! Automatic consent to the deletion \n"
    f"of all data and database and applying fixtures.",
)
def create_user(config_path, to_skip_interaction):
    Command(config_path, to_skip_interaction).handle()


class Command:
    def __init__(self, config_path: str, to_skip_interaction: bool) -> None:
        self.config_path = config_path
        self.to_skip_interaction = to_skip_interaction

        self.successful_load = 0

    def handle(self):
        if not self.to_skip_interaction:
            question = input(
                print(
                    textwrap.fill(
                        "This command will drop all your data and generate new "
                        "fixtures. Would you like to continue? (yes / no): ",
                        55,
                    )
                )
            )
            if not re.search("(y|yes)", question.lower()):
                return

        # Load models that presented in config file fixtures.yaml
        load_fixtures = self.load_fixtures_from_config()

        tracemalloc.start()

        for fixture in load_fixtures.values():
            self._fill_db(fixture["class"], fixture["attributes"])

        current, peak = tracemalloc.get_traced_memory()
        print(f"\nSuccessfully loaded {self.successful_load} fixtures!")
        print(
            f"Current memory usage: {current / 10 ** 3} KB; Peak usage: {peak / 10 ** 3} KB"
        )

    def _fill_db(self, fixture, attrs: dict) -> None:
        try:
            obj = fixture()
            if settings.environment not in obj.env_group():
                return
            obj.load(attrs.get("quantity", None))
            self.successful_load += 1
        except Exception as e:
            print(f"Error processing {fixture.__name__} fixture: \n {e}")
            return
        print(f"{fixture.__name__} fixtures loaded successfully")

    def load_fixtures_from_config(self) -> dict:
        with open(
            os.path.join(
                settings.root_path, "app/config/fixtures", self.config_path
            )
        ) as config:
            try:
                config = yaml.safe_load(config)
                load_fixtures = {}
                base_dir = config["fixtures"]["base_dir"]
                fixture_classes = config["fixtures"].get("load", {})
                for fixture in fixture_classes.values():
                    module = importlib.import_module(f"{base_dir}.{fixture['module']}")
                    load_fixtures[fixture["class"]] = {
                        "class": getattr(module, fixture["class"]),
                        "attributes": fixture.get("attributes", {}),
                    }
            except (yaml.MarkedYAMLError, KeyError, AttributeError) as exc:
                raise SyntaxError("Configuration file error: " + exc)
        return load_fixtures
