from enum import Enum
from pathlib import Path

import pytest

from pydantic_persitence import PersistenceModel, exceptions
from pydantic_persitence.backend.jsonfs import JsonFs, JsonFsConfig

CURRENT_FOLDER = Path(__file__).parent
TEST_DATA_FOLDER = CURRENT_FOLDER / "./temp_test_data/"
BEER_TEST_FILE = TEST_DATA_FOLDER / "beer.json"


def rm_tree(pth: Path) -> None:
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


class BeerType(Enum):
    IPA = "Indian Pale Ale"
    APA = "American Pale Ale"
    STOUT = "Stout"


class Beer(PersistenceModel):
    _backend = JsonFs("beer", JsonFsConfig(base_folder=TEST_DATA_FOLDER))
    _primary_key = "beer_id"
    beer_id: str
    beer_name: str
    beer_type: BeerType


def test_backend() -> None:
    JsonFsConfig(base_folder=None)

    if TEST_DATA_FOLDER.exists():
        rm_tree(TEST_DATA_FOLDER)
    TEST_DATA_FOLDER.mkdir()
    b = Beer(beer_id="epic-thunder", beer_name="Epic Thunder IPA", beer_type=BeerType.IPA)
    b.save()

    t = Beer.get("epic-thunder")
    assert t.beer_name == "Epic Thunder IPA"

    with pytest.raises(exceptions.ObjectNotFound):
        Beer.get("benos-stout")

    s = Beer(beer_id="benos-stout", beer_name="Benos Stout", beer_type=BeerType.STOUT)
    s.save()
