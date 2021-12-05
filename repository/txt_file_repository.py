from repository.repository import Repository
from validators.validators import RepositoryException
from entities.person import Person
from entities.activity import Activity
import datetime


class TxtPersonFileRepository(Repository):

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
                for line in file:
                    tokens = line.split(",")
                    person = Person(tokens[0], tokens[1], tokens[2].strip())
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
                for entity in self._entities.values():
                    person_string = entity.id + "," + entity.name + "," + entity.phone_number
                    file.write(person_string)
                    file.write("\n")
        except Exception as e:
            raise RepositoryException("An error occurred -" + str(e))

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


class TxtActivityFileRepository(Repository):

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
                for line in file:
                    activity_id, persons, date, start, end, description = self.__parse_input_activity(line)
                    date = datetime.datetime.strptime(date, "%d/%m/%Y")
                    start = datetime.datetime.strptime(start, "%H:%M")
                    end = datetime.datetime.strptime(end, "%H:%M")
                    activity = Activity(activity_id, persons, date, start, end, description)
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
                for entity in self._entities.values():
                    activity_string = entity.id + ";" + ",".join(entity.person_id) + \
                                      ";" + datetime.datetime.strftime(entity.date, "%d/%m/%Y") + ";" + \
                                      datetime.datetime.strftime(entity.start_time, "%H:%M") + ";" + \
                                      datetime.datetime.strftime(entity.end_time, "%H:%M") + ";" + \
                                      entity.description
                    file.write(activity_string)
                    file.write("\n")
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

    @staticmethod
    def __parse_input_activity(string):
        activity_parameters = string.split(";")
        activity_id = activity_parameters[0].strip()
        persons = activity_parameters[1].strip()
        persons = persons.split(",")
        date = activity_parameters[2].strip()
        start = activity_parameters[3].strip()
        end = activity_parameters[4].strip()
        description = activity_parameters[5].strip()
        return activity_id, persons, date, start, end, description
