#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
import json
import uuid
from os import path


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DTA = {}


class Base():
    """
    Base class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize Base instance
        """
        bs_class = str(self.__class__.__name__)
        if DTA.get(bs_class) is None:
            DTA[bs_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Equality
        """
        if type(self) is type(other):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert object JSON dictionary
        """
        res = {}
        for k, val in self.__dict__.items():
            if not for_serialization and k[0] == '_':
                continue
            if type(val) is datetime:
                res[k] = val.strftime(TIMESTAMP_FORMAT)
            else:
                res[k] = val
        return res

    @classmethod
    def load_from_file(cls):
        """ Load objects from file
        """
        bs_class = cls.__name__
        fl_pth = ".db_{}.json".format(bs_class)
        DTA[bs_class] = {}
        if not path.exists(fl_pth):
            return

        with open(fl_pth, 'r') as f:
            objs_json = json.load(f)
            for id_obj, obj_json in objs_json.items():
                DTA[bs_class][id_obj] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """ Save objects to file
        """
        bs_class = cls.__name__
        fl_pth = ".db_{}.json".format(bs_class)
        objs_json = {}
        for id_obj, obj in DTA[bs_class].items():
            objs_json[id_obj] = obj.to_json(True)

        with open(fl_pth, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """ Save current object
        """
        bs_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DTA[bs_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """ Remove object
        """
        bs_class = self.__class__.__name__
        if DTA[bs_class].get(self.id) is not None:
            del DTA[bs_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Count objects
        """
        bs_class = cls.__name__
        return len(DTA[bs_class].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return objects
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """ Return object by ID
        """
        bs_class = cls.__name__
        return DTA[bs_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search objects with matching attributes
        """
        bs_class = cls.__name__
        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, val in attributes.items():
                if (getattr(obj, k) != val):
                    return False
            return True

        return list(filter(_search, DTA[bs_class].values()))
