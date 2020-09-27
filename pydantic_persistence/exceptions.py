class PydanticPersistenceException(Exception):
    """Base Exception for pydandic persistence"""


class ObjectNotFound(PydanticPersistenceException):
    """Exception raised when no objects where found

    ex:
    """


class MultipleObjectsFound(PydanticPersistenceException):
    """Exception raised when multiple objects were found but only one was supposed to be found

    ex:
    """


class PydanticPersistenceWrongSetup(PydanticPersistenceException):
    """Exception raised when the configuration of the model is wrong

    ex:
    """
