from dataclasses import fields
from datetime import datetime
from typing import Literal

AM_OR_PM = Literal["am", "pm"]


def convert_datetime(var: str | datetime) -> datetime:
    """
    This function converts a string or datetime object to a datetime object.

    Args:
        var (str | datetime): The parameter `var` can be either a string or a `datetime` object.

    Returns:
        The function `convert_datetime` takes a variable `var` which can be either a string or a datetime
    object and returns a datetime object. If `var` is already a datetime object, it is returned as is.
    Otherwise, it is assumed to be a string in ISO format and converted to a datetime object using the
    `fromisoformat` method.
    """
    if isinstance(var, datetime) or not isinstance(var, str):
        return var
    else:
        return datetime.fromisoformat(var)


class Create:
    classFieldCache = {}

    @classmethod
    def instantiate(cls, classToInstantiate: object, argDict: dict):
        """
        The function takes in a class and a dictionary of arguments, filters the arguments based on the
        class's fields, and returns an instance of the class with the filtered arguments.

        Args:
            classToInstantiate (object): The class object that needs to be instantiated.
            argDict (dict): argDict is a dictionary that contains the arguments to be passed to the
        constructor of the class that is being instantiated. The keys of the dictionary represent the names
        of the arguments, and the values represent the values to be passed for those arguments.

        Returns:
            An instance of the class specified in the `classToInstantiate` parameter, with the arguments
        specified in the `argDict` parameter. The function first checks if the class has already been cached
        in `classFieldCache`, and if not, it caches the fields of the class that can be initialized. It then
        filters the arguments in `argDict` to only include those that correspond to the class fields.
        """
        if classToInstantiate not in cls.classFieldCache:
            cls.classFieldCache[classToInstantiate] = {
                f.name for f in fields(classToInstantiate) if f.init
            }

        fieldSet = cls.classFieldCache[classToInstantiate]
        filteredArgDict = {k: v for k, v in argDict.items() if k in fieldSet}
        return classToInstantiate(**filteredArgDict)
