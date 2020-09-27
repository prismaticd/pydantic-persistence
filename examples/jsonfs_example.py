from enum import Enum

from pydantic_persitence import PersistenceModel
from pydantic_persitence.backend.jsonfs import JsonFs


class BeerType(Enum):
    IPA = "Indian Pale Ale"
    APA = "American Pale Ale"
    STOUT = "Stout"


class Beer(PersistenceModel):
    # Will create a beer.json in the current folder
    _backend = JsonFs("beer")
    # Will use the field beer_id as a primary key
    _primary_key = "beer_id"

    beer_id: str
    beer_name: str
    beer_type: BeerType


if __name__ == "__main__":
    b1 = Beer(beer_id="epic-thunder", beer_name="Epic Thunder IPA", beer_type=BeerType.IPA)
    b1.save()
    b2 = Beer(beer_id="benos-stout", beer_name="Benos Stout", beer_type=BeerType.STOUT)
    b2.save()

    # You can open beer.json and see those 2 beers in the json list

    b = Beer.get("epic-thunder")
    assert b.beer_type == BeerType.IPA

    # print all beer we have
    for beer in Beer.list():
        print(beer)

    # Transform a stout into an IPA
    b2.beer_type = BeerType.IPA
    b2.save()

    # Default filter is equal, returns all the beers of type IPA
    for ipa_beer in Beer.filter("beer_type", BeerType.IPA):
        print(f"{ipa_beer} is an IPA")
