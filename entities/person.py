from dataclasses import dataclass


@dataclass
class Person:
    """
    Person data type having person_id as str, name as str, phone_number as str
    """
    __id: str
    name: str
    phone_number: str

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return "Id - " + self.id + ", Name - " + self.name + ", Phone number - " + self.phone_number
