# pydantic-persistence
Pydantic Persistence allow you to load and save your Pydantic Models to different backends
To get started you only need to define an _backend

![Tests](https://github.com/prismaticd/pydantic-persistence/workflows/Tests/badge.svg?branch=master)
![Code Coverage](https://img.shields.io/badge/code%20coverage-100%25-success.svg)

## Example

```python
from enum import Enum

from pydantic_persistence import PersistenceModel
from pydantic_persistence.backend.json_local import JsonLocalStorage


class BeerType(Enum):
    IPA = "Indian Pale Ale"
    APA = "American Pale Ale"
    STOUT = "Stout"


class Beer(PersistenceModel):
    # Will create a beer.json in the current folder
    _backend = JsonLocalStorage("beer")
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

```


## Publish new release

locally run `bump2version patch ` or `bump2version minor` or `bump2version major`

This will update pyproject.toml and the __version__ in __init__.py will commit with message
`bump version from {old_version} to {new_version}` and tag with `v{new_version}`

You then need to do `git push --tags` or normal push if you have set `git config --global push.followTags true`

A few seconds later a Draft release will be visible in the releases tab on github, edit the content and press publish,
this will automatically publish the release on pypi
