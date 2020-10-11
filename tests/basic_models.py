from pydantic_persistence.base import BaseBackend, BaseBackendConfig
from pydantic_persistence import PersistenceModel, base


class TestPersistenceModelEmpty(PersistenceModel):
    """Empty model should not work because does not define primary key field"""
    __test__ = False


class TestPersistenceModelNoPkField(base.PersistenceModel):
    """Empty model should not work because does not have a field called t1"""
    __test__ = False

    _primary_key = "t1"


class TestPersistenceModelNoBackend(base.PersistenceModel):
    """Model with no backend"""
    __test__ = False

    t1: str
    _primary_key = "t1"


class TestPersistenceModel1(base.PersistenceModel):
    """Valid minimal model"""
    __test__ = False

    t1: str
    _primary_key = "t1"
    _backend = BaseBackend("TestPersistenceModel3", BaseBackendConfig())


class TestPersistenceModel2(base.PersistenceModel):
    """Valid minimal model"""
    __test__ = False

    t2: str
    _backend = BaseBackend("TestPersistenceModel3", BaseBackendConfig())

    def _primary_key(self) -> str:  # type: ignore
        return "t2"


class TestPersistenceModel3(base.PersistenceModel):
    """Valid minimal model with one additional attribute"""
    __test__ = False

    t3: str
    v1: str
    _primary_key = "t3"
    _backend = BaseBackend("TestPersistenceModel3", BaseBackendConfig())
