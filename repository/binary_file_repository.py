import pickle
from repository.repository import Repository
from validators.validators import RepositoryException


class BinaryFileRepository(Repository):

    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self._entities = self.__load_data()

    def __load_data(self):
        """
        Loads data from the file into the program
        """
        try:
            file = open(self.__file_name, "rb")
            result = pickle.load(file)
            file.close()
            return result
        except EOFError:
            return {}
        except IOError as error:
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
            with open(self.__file_name, 'wb') as file:
                pickle.dump(self._entities, file)
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
