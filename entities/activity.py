from dataclasses import dataclass
from datetime import datetime


@dataclass
class Activity:
    """
    Activity data type having activity_id as str, person_id as [str], date as datetime, start_time as datetime,
    end_time as datetime, description as str
    """
    __id: str
    person_id: [str]
    date: datetime
    start_time: datetime
    end_time: datetime
    description: str

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return "Id - " + self.__id + "\nPerson IDs - " + ", ".join(self.person_id) + "\nDate - " + \
               self.date.strftime("%a, %d %B, %Y") + "\nStarting Time - " + self.start_time.strftime("%H:%M") +\
               "\nEnding Time - " + self.end_time.strftime("%H:%M") + "\nDescription - " + self.description + "\n"
