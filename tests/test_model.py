import pytest

from pydantic_persistence import base, exceptions
from tests.basic_models import TestPersistenceModelEmpty, TestPersistenceModelNoPkField, TestPersistenceModel1, \
    TestPersistenceModel2, TestPersistenceModel3


def test_base_model() -> None:
    """Test import of model"""
    with pytest.raises(exceptions.PydanticPersistenceWrongSetup):
        TestPersistenceModelEmpty()

    with pytest.raises(exceptions.PydanticPersistenceWrongSetup):
        TestPersistenceModelNoPkField()

    with pytest.raises(exceptions.PydanticPersistenceWrongSetup):
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
