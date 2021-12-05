from validators.validators import PersonValidatorException
from validators.validators import RepositoryException
from validators.validators import ActivityValidatorException
from validators.validators import InputException


class UI:

    def __init__(self, activity_service, person_service, undo_service):
        self.__activity_service = activity_service
        self.__person_service = person_service
        self.__undo_service = undo_service

    @staticmethod
    def print_menu():
        print("1 - add person\n"
              "2 - add activity\n"
              "3 - list persons\n"
              "4 - list activities\n"
              "5 - delete person\n"
              "6 - delete activity\n"
              "7 - update person\n"
              "8 - update activity\n"
              "9 - search person\n"
              "10 - search activity\n"
              "11 - activities for date\n"
              "12 - busiest days\n"
              "13 - activities with person\n"
              "14 - undo\n"
              "15 - redo\n"
              "x - exit\n")

    def ui_add_person(self):
        person_id = input("Person ID = ")
        if person_id == "":
            raise InputException("Input should not be empty!")
        name = input("Name = ")
        if name == "":
            raise InputException("Input should not be empty!")
        phone_number = input("Phone number = ")
        try:
            operation = self.__person_service.add_person(person_id, name, phone_number)
            self.__undo_service.record(operation)
        except PersonValidatorException as error:
            print(error)

    def ui_read_activity(self):
        persons = []
        index = 0
        done = False
        while not done:
            person_id = input("Person ID = ")
            if person_id == "":
                raise InputException("Input should not be empty!")
            if self.__person_service.find_person_by_id(person_id):
                persons.append(person_id)
                stop = input("Press s to stop adding persons and anything else to continue: ")
                if stop == 's':
                    done = True
            else:
                print("This person does not exist in your friends list")
                stop = input("Press s to stop adding persons and anything else to continue: ")
                if stop == 's':
                    done = True
        date = input("Date = ")
        if date == "":
            raise InputException("Input should not be empty!")
        start = input("Start hour = ")
        if start == "":
            raise InputException("Input should not be empty!")
        end = input("End hour = ")
        if end == "":
            raise InputException("Input should not be empty!")
        description = input("Description = ")
        return persons, date, start, end, description

    def ui_add_activity(self):
        activity_id = input("Activity ID = ")
        if activity_id == "":
            raise InputException("Input should not be empty!")
        persons, date, start, end, description = self.ui_read_activity()
        try:
            operation = self.__activity_service.add_activity(activity_id, persons, date, start, end, description)
            self.__undo_service.record(operation)
        except ActivityValidatorException as error:
            print(error)

    def ui_print_persons(self):
        try:
            all_persons = self.__person_service.get_all_persons()
            for person in all_persons:
                print(str(person))
            print()
        except RepositoryException as error:
            print(error)

    def ui_print_activities(self):
        try:
            all_activities = self.__activity_service.get_all_activities()
            for activity in all_activities:
                print(str(activity))
            print()
        except RepositoryException as error:
            print(error)

    def ui_remove_person(self):
        try:
            person_id = input("Person ID to be removed = ")
            if person_id == "":
                raise InputException("Input should not be empty!")
            operation = self.__person_service.remove_person(person_id)
            self.__undo_service.record(operation)
        except RepositoryException as error:
            print(error)

    def ui_remove_activity(self):
        try:
            activity_id = input("Activity ID to be removed = ")
            if activity_id == "":
                raise InputException("Input should not be empty!")
            operation = self.__activity_service.remove_activity(activity_id)
            self.__undo_service.record(operation)
        except RepositoryException as error:
            print(error)

    def ui_update_person(self):
        update_id = input("Person ID for update = ")
        if update_id == "":
            raise InputException("Input should not be empty!")
        new_phone_number = input("Phone number = ")
        if new_phone_number == "":
            raise InputException("Input should not be empty!")
        new_name = input("Name = ")
        if new_name == "":
            raise InputException("Input should not be empty!")
        try:
            operation = self.__person_service.update_person(update_id, new_name, new_phone_number)
            self.__undo_service.record(operation)
        except RepositoryException as error:
            print(error)

    def ui_update_activity(self):
        update_id = input("Activity ID to update = ")
        new_persons, new_date, new_start, new_end, new_description = self.ui_read_activity()
        try:
            operation = self.__activity_service.update_activity(update_id, new_persons, new_date, new_start, new_end,
                                                                new_description)
            self.__undo_service.record(operation)
        except RepositoryException as error:
            print(error)

    def add_test_data(self):
        self.__activity_service.add_test_data_activities()
        self.__person_service.add_test_data_persons()

    def ui_search_person(self):
        string_to_search = input("Search by = ")
        for person in self.__person_service.search_person(string_to_search.lower()):
            print(str(person))

    def ui_search_activity(self):
        string_to_search = input("Search by = ")
        for activity in self.__activity_service.search_activity(string_to_search.lower()):
            print(str(activity))

    def ui_activity_for_date(self):
        date = input("Date = ")
        for activity in self.__activity_service.activities_for_given_date(date):
            print(str(activity))

    def ui_activities_with_person(self):
        person = input("Person Id = ")
        for activity in self.__activity_service.activities_with_person(person):
            print(str(activity))

    def ui_busiest_days(self):
        for date in self.__activity_service.busiest_days():
            print(date.strftime("%B %d, %Y"))

    def ui_undo(self):
        self.__undo_service.undo()

    def ui_redo(self):
        self.__undo_service.redo()

    def run(self):
        self.add_test_data()
        commands = {"1": self.ui_add_person,
                    "2": self.ui_add_activity,
                    "3": self.ui_print_persons,
                    "4": self.ui_print_activities,
                    "5": self.ui_remove_person,
                    "6": self.ui_remove_activity,
                    "7": self.ui_update_person,
                    "8": self.ui_update_activity,
                    "9": self.ui_search_person,
                    "10": self.ui_search_activity,
                    "11": self.ui_activity_for_date,
                    "12": self.ui_busiest_days,
                    "13": self.ui_activities_with_person,
                    "14":self.ui_undo,
                    "15":self.ui_redo
                    }
        while True:
            self.print_menu()

            try:
                command = input("Enter a command: ").lower()
                if command == 'x':
                    return
                elif command in commands:
                    commands[command]()
                else:
                    raise Exception("Bad command!")
            except Exception as exception:
                print(exception)
