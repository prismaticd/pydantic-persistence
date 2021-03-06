from enum import Enum
from pathlib import Path

import pytest

from pydantic_persistence import PersistenceModel, exceptions
from pydantic_persistence.backend.json_local import JsonLocalStorage, JsonLocalStorageConfig

CURRENT_FOLDER = Path(__file__).parent
TEST_DATA_FOLDER = CURRENT_FOLDER / "./temp_test_data/"
BEER_TEST_FILE = TEST_DATA_FOLDER / "beer.json"


def rm_tree(pth: Path) -> None:
    """Utility function delete a tree in a recursive way"""
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def test_backend() -> None:
    """Main testing function"""
    backend = JsonLocalStorage("beer", JsonLocalStorageConfig(base_folder=TEST_DATA_FOLDER))
    JsonLocalStorageConfig(base_folder=None)

    if TEST_DATA_FOLDER.exists():
        rm_tree(TEST_DATA_FOLDER)
    TEST_DATA_FOLDER.mkdir()

    from tests.test_auto import full_suite
    full_suite(backend)
