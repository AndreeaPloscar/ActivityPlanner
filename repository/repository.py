from validators.validators import RepositoryException
from iterable_module.collection import Collection


class Repository:
    def __init__(self):
        self._entities = Collection()

    def find_by_id(self, entity_id):
        """
        Checks if there is already an entity with given id in repository entities dictionary
        :param entity_id: given entity id (string)
        :return: True if id exists already, False otherwise
        """
        for entity in self._entities:
            if entity_id == entity.id:
                return True
        return False

    def save(self, entity):
        """
        Saves given entity into dictionary of entities having the id as key and the entity as value
        Raises RepositoryException if entity id already exists in the dictionary
        :param entity: given entity
        :return: -
        """
        if not self.find_by_id(entity.id):
            self._entities.add(entity)
        else:
            raise RepositoryException("This ID already exists!")

    def delete_by_id(self, entity_id):
        """
        Deletes the entity with given id from dictionary of entities if it exists, raises RepositoryException otherwise
        :param entity_id: given entity_id as string
        :return: -
        """
        if self.find_by_id(entity_id):
            for index in range(0, len(self._entities)):
                entity = self._entities.get_all()[index]
                if entity_id == entity.id:
                    object = entity
                    position = index
            self._entities.__delitem__(position)
            return object
        else:
            raise RepositoryException("ID not found!")

    def update(self, entity_id, entity):
        """
        Updates the entity having given entity id with given entity
        Raises RepositoryException if entity id does not exist in the dictionary
        :param entity_id: given entity id
        :param entity: entity having the same id but possibly different parameters
        :return: -
        """
        if self.find_by_id(entity_id):
            for index in range(0, len(self._entities)):
                if self._entities.get_all()[index].id == entity_id:
                    old_entity = self._entities.get_all()[index]
                    position = index
            self._entities[position] = entity
            return old_entity
        else:
            raise RepositoryException("ID not found!")

    def find_all(self):
        """
        Raises RepositoryException if dictionary of entities is empty, returns the values from it otherwise
        :return: values of entities dictionary
        """
        if len(self._entities) == 0:
            raise RepositoryException("List is empty!")
        return self._entities
