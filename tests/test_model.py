import pytest

from pydantic_persitence import PersistenceModel, base, exceptions
from pydantic_persitence.base import BaseBackend, BaseBackendConfig


class TestPersistenceModelEmpty(PersistenceModel):
    """Empty model should not work because does not define primary key field"""


class TestPersistenceModelNoPkField(base.PersistenceModel):
    """Empty model should not work because does not have a field called t1"""

    _primary_key = "t1"


class TestPersistenceModelNoBackend(base.PersistenceModel):
    """Model with no backend"""

    t1: str
    _primary_key = "t1"


class TestPersistenceModel1(base.PersistenceModel):
    """Valid minimal model"""

    t1: str
    _primary_key = "t1"
    _backend = BaseBackend("TestPersistenceModel3", BaseBackendConfig())


class TestPersistenceModel2(base.PersistenceModel):
    """Valid minimal model"""

    t2: str
    _backend = BaseBackend("TestPersistenceModel3", BaseBackendConfig())

    def _primary_key(self) -> str:  # type: ignore
        return "t2"


class TestPersistenceModel3(base.PersistenceModel):
    """Valid minimal model with one additional attribute"""

    t3: str
    v1: str
    _primary_key = "t3"
    _backend = BaseBackend("TestPersistenceModel3", BaseBackendConfig())


def test_base_model() -> None:
    """Test import of model"""
    with pytest.raises(exceptions.PydanticPersitenceWrongSetup):
        TestPersistenceModelEmpty()

    with pytest.raises(exceptions.PydanticPersitenceWrongSetup):
        TestPersistenceModelNoPkField()

    p1 = TestPersistenceModel1(t1="abc")
    assert p1._primary_key == "t1"
    p2 = TestPersistenceModel2(t2="abc")
    assert p2._primary_key == "t2"
    p3 = TestPersistenceModel3(t3="hello", v1="Nothing")
    assert p3._primary_key == "t3"
    p3.v1 = "Hello"


def test_base_backend() -> None:
    """Test base backend"""
    bc = base.BaseBackendConfig()
    b = base.BaseBackend(table_name="table1", backend_config=bc)

    with pytest.raises(NotImplementedError):
        b.get(TestPersistenceModel3, "1234")

    with pytest.raises(NotImplementedError):
        b.multi_get(TestPersistenceModel3, ["1234", "1235"])

    with pytest.raises(NotImplementedError):
        b.filter(TestPersistenceModel3, "v1", "1234")

    with pytest.raises(NotImplementedError):
        b.list(TestPersistenceModel3)

    with pytest.raises(NotImplementedError):
        b.list(TestPersistenceModel3, 10)

    pm1 = TestPersistenceModel3(t3="t3", v1="v1")
    with pytest.raises(NotImplementedError):
        b.save(pm1)

    pm2 = TestPersistenceModel3(t3="t3", v1="v1")
    with pytest.raises(NotImplementedError):
        b.delete(pm2)
