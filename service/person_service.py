from entities.person import Person
from service.undo_service import FunctionCall, Operation, CascadedOperation
import copy
from iterable_module.functions import Functions


class PersonService:
    def __init__(self, undo_service, person_repository, person_validator, activity_service):
        self.__person_repository = person_repository
        self.__person_validator = person_validator
        self._undo_service = undo_service
        self._activity_service = activity_service

    def add_person(self, person_id, name, phone_number):
        """
        Adds person having person_id, name, phone_number into repository
        :param person_id: string
        :param name: string
        :param phone_number: string of 10 digits
        :return: -
        """
        person = Person(person_id, name, phone_number)
        self.__person_validator.validate(person)
        self.__person_repository.save(person)
        undo = FunctionCall(self.remove_person, person.id)
        redo = FunctionCall(self.add_person, person.id, person.name, person.phone_number)
        operation = Operation(undo, redo)
        return operation

    def get_all_persons(self):
        """
        Returns all persons from repository
        :return: all persons as list of dictionary values
        """
        return self.__person_repository.find_all()

    def remove_person(self, person_id):
        """
        Removes person having person_id from repository
        :param person_id: string
        :return: -
        """
        person = self.__person_repository.delete_by_id(person_id)
        undo = FunctionCall(self.add_person, person.id, person.name, person.phone_number)
        redo = FunctionCall(self.remove_person, person.id)
        operation = Operation(undo, redo)
        cascaded_list = [operation]
        for activity in self._activity_service.get_all_activities():
            if person_id in activity.person_id:
                persons_list = copy.deepcopy(activity.person_id)
                old_persons_list = copy.deepcopy(persons_list)
                index = 0
                while index < len(persons_list):
                    if persons_list[index] == person_id:
                        del persons_list[index]
                    else:
                        index += 1
                operation_cascade = self._activity_service.update_activity(activity.id, persons_list,
                                                                           activity.date.strftime("%d/%m/%Y"),
                                                                           activity.start_time.strftime("%H:%M"),
                                                                           activity.end_time.strftime("%H:%M"),
                                                                           activity.description)
                cascaded_list.append(operation_cascade)
        cascaded_operation = CascadedOperation(*cascaded_list)
        return cascaded_operation

    def find_person_by_id(self, person_id):
        """
        Finds person with given person id
        :param person_id: string
        :return: True/False depending on the return from repository find_by_id method
        """
        return self.__person_repository.find_by_id(person_id)

    def update_person(self, person_id, new_name, new_phone_number):
        """
        Updates the person having given person_id with new_name and new_phone_number
        :param person_id: string
        :param new_name: string
        :param new_phone_number: string having 10 digits
        :return: -
        """
        person = Person(person_id, new_name, new_phone_number)
        self.__person_validator.validate(person)
        old_person = self.__person_repository.update(person_id, person)
        undo = FunctionCall(self.update_person, person.id, old_person.name, old_person.phone_number)
        redo = FunctionCall(self.update_person, person.id, new_name, new_phone_number)
        operation = Operation(undo, redo)
        return operation

    @staticmethod
    def criteria_string_matching(person, string_to_search):
        """
        Checks if the string_to_search appears in a person's name or phone_number
        """
        if string_to_search in person.name.lower() or string_to_search in person.phone_number:
            return True
        return False

    def search_person(self, string_to_search):
        """
        Returns a list of persons having their name or phone number matching given string
        :param string_to_search: string
        :return: list of persons with given property
        """
        functions = Functions()
        return functions.filter(self.__person_repository.find_all(), self.criteria_string_matching, string_to_search)

    def add_test_data_persons(self):
        """
        Adds test persons into repository
        :return: -
        """
        return
        self.add_person("120", "Jules", "0751274477")
        self.add_person("121", "Alicia", "0785274907")
        self.add_person("122", "Ellie", "0741274677")
        self.add_person("123", "Olaf", "0781279470")
        self.add_person("124", "Tom", "0751274477")
