from repository.repository import Repository
from validators.validators import RepositoryException
from entities.person import Person
from entities.activity import Activity
import datetime
import json


class JsonPersonFileRepository(Repository):

    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__load_data()

    def __load_data(self):
        """
        Loads data from the file into the program
        """
        try:
            with open(self.__file_name, 'r') as file:
                persons = json.load(file)
                for person in persons:
                    person = Person(person["id"], person["name"], person["phone number"])
                    super().save(person)
        except Exception as error:
            raise error

    def save(self, entity):
        """
        Saves an entity into self._entities and into the file
        """
        super().save(entity)
        self.__save_to_file()

    def __save_to_file(self):
        """
        Saves the list of entities into the file
        """
        try:
            with open(self.__file_name, 'w') as file:
                persons = []
                for person in self._entities.values():
                    dictionary_person = {
                        "id": person.id,
                        "name": person.name,
                        "phone number": person.phone_number
                    }
                    persons.append(dictionary_person)
                json.dump(persons, file)
        except Exception as error:
            raise RepositoryException("An error occurred -" + str(error))

    def delete_by_id(self, entity_id):
        """
        Deletes entity having entity_id as id from self._entities and from the file
        """
        entity = super().delete_by_id(entity_id)
        self.__save_to_file()
        return entity

    def update(self, entity_id, entity):
        """
        Updates the entity having entity_id as id with the new entity
        """
        entity = super().update(entity_id, entity)
        self.__save_to_file()
        return entity


class JsonActivityFileRepository(Repository):

    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__load_data()

    def __load_data(self):
        """
        Loads data from the file into the program
        """
        try:
            with open(self.__file_name, 'r') as file:
                activities = json.load(file)
                for activity in activities:
                    activity = Activity(activity["id"], activity["person_id"],
                                        datetime.datetime.strptime(activity["date"], "%d/%m/%Y"),
                                        datetime.datetime.strptime(activity["start_time"], "%H:%M"),
                                        datetime.datetime.strptime(activity["end_time"], "%H:%M"),
                                        activity["description"])
                    super().save(activity)
        except Exception as error:
            raise error

    def save(self, entity):
        """
        Saves an entity into self._entities and into the file
        """
        super().save(entity)
        self.__save_to_file()

    def __save_to_file(self):
        """
        Saves the list of entities into the file
        """
        try:
            with open(self.__file_name, 'w') as file:
                activities = []
                for activity in self._entities.values():
                    dictionary_activity = {
                        "id": activity.id,
                        "person_id": activity.person_id,
                        "date": datetime.datetime.strftime(activity.date, "%d/%m/%Y"),
                        "start_time": datetime.datetime.strftime(activity.start_time, "%H:%M"),
                        "end_time":datetime.datetime.strftime(activity.end_time, "%H:%M"),
                        "description": activity.description
                    }
                    activities.append(dictionary_activity)
                json.dump(activities, file)
        except Exception as error:
            raise RepositoryException("An error occurred -" + str(error))

    def delete_by_id(self, entity_id):
        """
        Deletes entity having entity_id as id from self._entities and from the file
        """
        entity = super().delete_by_id(entity_id)
        self.__save_to_file()
        return entity

    def update(self, entity_id, entity):
        """
        Updates the entity having entity_id as id with the new entity
        """
        entity = super().update(entity_id, entity)
        self.__save_to_file()
        return entity
