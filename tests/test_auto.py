from enum import Enum

import pytest

from pydantic_persistence import base, exceptions
from pydantic_persistence.base import BaseBackend, PersistenceModel


def full_suite(backend: BaseBackend) -> None:
    """Test base backend"""

    class BeerType(Enum):
        """An enum for testing"""

        IPA = "Indian Pale Ale"
        APA = "American Pale Ale"
        STOUT = "Stout"

    class Beer(PersistenceModel):
        """A Beer for testing"""

        _backend = backend
        _primary_key = "beer_id"
        beer_id: str
        beer_name: str
        beer_type: BeerType

    b = Beer(beer_id="epic-thunder", beer_name="Epic Thunder IPA", beer_type=BeerType.IPA)
    b.save()

    t = Beer.get("epic-thunder")
    assert t.beer_name == "Epic Thunder IPA"

    with pytest.raises(exceptions.ObjectNotFound):
        Beer.get("benos-stout")

    s = Beer(beer_id="benos-stout", beer_name="Benos Stout", beer_type=BeerType.STOUT)
    s.save()
