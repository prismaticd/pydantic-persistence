from typing import Any, Callable, Iterable, List, Optional, Type, TypeVar, Union

import pydantic

from pydantic_persitence.exceptions import PydanticPersitenceWrongSetup


class PersistenceModel(pydantic.BaseModel):
    """Persistence model"""

    _primary_key: Union[str, Callable]
    _backend: "BaseBackend"
    __slots__ = ["_primary_key", "_backend"]

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr in self.__slots__:
            object.__setattr__(self, attr, value)
        else:
            super().__setattr__(attr, value)

    def _init_slots(self) -> None:
        if not hasattr(self, "_primary_key"):
            raise PydanticPersitenceWrongSetup(
                "_primary_key is not defined, define an attribute or " "function returning the primary key field name"
            )
        if callable(self._primary_key):
            self._primary_key = self._primary_key()
        if not hasattr(self, self._primary_key):  # type: ignore
            raise PydanticPersitenceWrongSetup(
                f"_primary_key is not defined but can't find an attribute called "
                f"[{self._primary_key}] in class {self.__class__.__name__}"
            )

    def __init__(self, **kwargs) -> None:  # type: ignore
        super().__init__(**kwargs)
        self._init_slots()


class BaseBackendConfig:
    """Backend configuration placeholder, each backend will define it's own configuration"""


P = TypeVar("P", bound=PersistenceModel)


class BaseBackend:
    """Parent class for all backends"""

    table_name: str
    # prefix can represent the database, or a prefix per environment (dev, uat, prod)
    # backends may use this in different ways
    prefix: Optional[str]
    backend_config: BaseBackendConfig

    def __init__(self, table_name: str, backend_config: BaseBackendConfig, prefix: str = None) -> None:
        self.prefix = prefix
        self.table_name = table_name
        self.backend_config = backend_config

    def get(self, source_model: Type[P], object_id: Any) -> P:
        """Get an object by id, this is defined by the _primary_key attribute of the model"""
        raise NotImplementedError

    def multi_get(self, source_model: Type[P], object_ids: List[Any]) -> List[P]:
        """Get a list of objects by id, this is defined by the _primary_key attribute of the model"""
        raise NotImplementedError

    def filter(self, source_model: Type[P], field_name: str, filter_value: Any) -> List[P]:
        """Filter a field name by a value, return a list of Models"""
        raise NotImplementedError

    def list(self, source_model: Type[P], limit: Optional[int] = None) -> Iterable[P]:
        """List all objects or until the limit"""
        raise NotImplementedError

    def save(self, model_instance: P) -> None:
        """Persist a model instance in the backend"""
        raise NotImplementedError

    def delete(self, model_instance: P) -> None:
        """Delete a model instance from the backend"""
        raise NotImplementedError
