import json
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar

import pydantic

from pydantic_persistence.exceptions import ObjectNotFound, PydanticPersistenceWrongSetup

PM = TypeVar("PM", bound="PersistenceModel")


class FilterType(Enum):
    """Possible filters for the filter functions"""

    EQUAL = "="


class PersistenceModel(pydantic.BaseModel):
    """Persistence model"""

    _primary_key: str
    _backend: "BaseBackend"
    __slots__ = ["_primary_key", "_backend"]

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr in self.__slots__:
            object.__setattr__(self, attr, value)
        else:
            super().__setattr__(attr, value)

    def _init_slots(self) -> None:
        if not hasattr(self, "_primary_key"):
            raise PydanticPersistenceWrongSetup(
                "_primary_key is not defined, define an attribute or function returning the primary key field name"
            )
        if callable(self._primary_key):
            self._primary_key = self._primary_key()
        if not hasattr(self, self._primary_key):  # type: ignore
            raise PydanticPersistenceWrongSetup(
                f"_primary_key is defined but can't find an attribute called "
                f"[{self._primary_key}] in class {self.__class__.__name__}"
            )
        if not hasattr(self, "_backend"):  # type: ignore
            raise PydanticPersistenceWrongSetup(f"_backend is not defined in class {self.__class__.__name__}")
        if callable(self._backend):
            self._backend = self._backend()

    def __init__(self, **kwargs) -> None:  # type: ignore
        super().__init__(**kwargs)
        self._init_slots()

    @classmethod
    def get_pk_field(cls) -> str:
        """Return the primary key field name"""
        return cls._primary_key

    def get_pk_value(self) -> Any:
        """Return the primary key value"""
        return getattr(self, self.get_pk_field())

    @classmethod
    def get(cls: Type[PM], instance_id: Any) -> PM:
        """Get an object by id, this is defined by the _primary_key attribute of the model"""
        return cls._backend.get(cls, instance_id)  # type: ignore

    @classmethod
    def batch_get(cls: Type[PM], instance_ids: List[Any], pool_size: int = 20) -> Dict[str, PM]:
        """Get a list of ids one by one with a thread pool"""
        future_list = {}
        with ThreadPoolExecutor(max_workers=pool_size) as e:
            for instance_id in instance_ids:
                future_list[instance_id] = e.submit(cls.get, instance_id)

        return_list = {}
        for instance_id, future in future_list.items():
            return_list[instance_id] = future.result()

        return return_list

    def save(self) -> None:
        """Persist a model instance in the backend"""
        return self._backend.save(self)

    @classmethod
    def batch_save(cls, models: List["PersistenceModel"], pool_size: int = 20) -> None:
        """Persist a a list model instance in the backend using a thread pool"""
        with ThreadPoolExecutor(max_workers=pool_size) as e:
            for model in models:
                e.submit(model.save)

    def delete(self) -> None:
        """Delete a model instance from the backend"""
        return self._backend.delete(self)

    @classmethod
    def filter(
        cls: Type[PM], field_name: str, filter_value: Any, filter_type: Optional[FilterType] = FilterType.EQUAL
    ) -> List[PM]:
        """Filter a model by filter_value for a given field_name, by default filter_type is FilterType.EQUAL"""
        return cls._backend.filter(cls, field_name, filter_value, filter_type)

    @classmethod
    def list(cls: Type[PM], limit: Optional[int] = None) -> Iterable[PM]:
        """List all objects or until the limit"""
        return cls._backend.list(cls, limit)


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

    def __init__(self, table_name: str, backend_config: Optional[BaseBackendConfig] = None, prefix: str = None) -> None:
        self.prefix = prefix
        self.table_name = table_name
        if not backend_config:
            backend_config = BaseBackendConfig()
        self.backend_config = backend_config

    def get(self, source_model: Type[P], object_id: Any) -> P:
        """Get an object by id, this is defined by the _primary_key attribute of the model"""
        raise NotImplementedError

    def multi_get(self, source_model: Type[P], object_ids: List[Any]) -> List[P]:
        """Get a list of objects by id, this is defined by the _primary_key attribute of the model"""
        raise NotImplementedError

    def filter(
        self,
        source_model: Type[P],
        field_name: str,
        filter_value: Any,
        filter_type: Optional[FilterType] = FilterType.EQUAL,
    ) -> List[P]:
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


class ListDictBackend(BaseBackend):
    """This backend is the base of any backend that reads a full list and saves a full list back"""

    def get_data(self) -> List[dict]:
        """Common method that returns a list of Dict, Backend Specific"""
        raise NotImplementedError

    def save_data(self, data: List[dict]) -> None:
        """Common method that save a list of Dict, Backend Specific"""
        raise NotImplementedError

    def get(self, source_model: Type[P], object_id: Any) -> P:
        """Return the instance by primary key"""
        for obj in self.get_data():
            pk = obj.get(source_model.get_pk_field())
            if pk == object_id:
                return source_model(**obj)
        raise ObjectNotFound(
            f"Could not find {source_model.__class__.__name__} "
            f"with field:{source_model.get_pk_field()} = {object_id}"
        )

    def multi_get(self, source_model: Type[P], object_ids: List[Any]) -> List[P]:
        """Return a list of instances by primary key"""
        return_list: List[P] = []
        for obj in self.get_data():
            pk = obj.get(source_model.get_pk_field())
            if pk in object_ids:
                return_list.append(source_model(**obj))

        return return_list

    def filter_equal(self, source_model: Type[P], field_name: str, filter_value: Any) -> List[P]:
        """Return a list of instance equal to the filter"""
        return_list: List[P] = []
        for obj in self.get_data():
            val = obj.get(field_name)
            if val == filter_value:
                return_list.append(source_model(**obj))
        return return_list

    def filter(
        self,
        source_model: Type[P],
        field_name: str,
        filter_value: Any,
        filter_type: Optional[FilterType] = FilterType.EQUAL,
    ) -> List[P]:
        """Return a list of instance equal to the filter for a given filter type"""
        if filter_type == FilterType.EQUAL:
            return self.filter_equal(source_model, field_name, filter_value)
        else:
            raise NotImplementedError

    def list(self, source_model: Type[P], limit: Optional[int] = None) -> Iterable[P]:
        """Return a all objects"""
        return_list: List[P] = []
        for index, obj in enumerate(self.get_data()):
            return_list.append(source_model(**obj))
            if limit and index + 1 == limit:
                return return_list
        return return_list

    def save(self, model_instance: P) -> None:
        """Save a instance back in the list, this does a full read again (in case something has changed in the list)"""
        to_save_return_list: List[dict] = []
        found = False
        for obj in self.get_data():
            pk = obj.get(model_instance.get_pk_field())
            if pk == model_instance.get_pk_value():
                # We use pydantic to serialise then load in as dict to serialise in the list again
                to_save_return_list.append(json.loads(model_instance.json()))
                found = True
            else:
                # Assume that all other objects are ok, not re-save them
                # Should this try to load before saving?
                to_save_return_list.append(obj)

        if not found:
            # Cannot find the Pk we are adding the object at the end of the list
            to_save_return_list.append(json.loads(model_instance.json()))

        self.save_data(to_save_return_list)

    def delete(self, model_instance: P) -> None:
        """Delete an instance the list, this does a full read again (in case something has changed in the list)"""
        to_save_return_list: List[dict] = []
        for obj in self.get_data():
            pk = obj.get(model_instance.get_pk_field())
            # add everything to the list but the primary key
            if pk != model_instance.get_pk_value():
                to_save_return_list.append(obj)

        self.save_data(to_save_return_list)
