class PydanticPersitenceException(Exception):
    """Base Exception for pydandic persitence"""


class ObjectNotFound(PydanticPersitenceException):
    """Exception raised when no objects where found

    ex:
    """


class MultipleObjectsFound(PydanticPersitenceException):
    """Exception raised when multiple objects were found but only one was supposed to be found

    ex:
    """


class PydanticPersitenceWrongSetup(PydanticPersitenceException):
    """Exception raised when the configuration of the model is wrong

    ex:
    """
