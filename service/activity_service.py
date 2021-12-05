from entities.activity import Activity
import datetime
from validators.validators import RepositoryException
import re
from service.undo_service import FunctionCall, Operation
from iterable_module.functions import Functions


class ActivityService:
    def __init__(self, undo_service, activity_repository, activity_validator):
        self.__activity_repository = activity_repository
        self.__activity_validator = activity_validator
        self._undo_service = undo_service

    def add_activity(self, activity_id, person_id, date_str, start_str, end_str, description):
        """
        Validates activity having given parameters and saves it to the repository if it is alright
        :param activity_id: string
        :param person_id: list of string ids
        :param date_str: string as dd/mm/yyyy
        :param start_str: string as hh/mm
        :param end_str: string as hh/mm
        :param description: string
        :return: -
        """
        date, start, end = self.strings_to_datetime(date_str, start_str, end_str)
        activity = Activity(activity_id, person_id, date, start, end, description)
        try:
            activities_list = self.__activity_repository.find_all()
            self.__activity_validator.validate(activities_list, activity)
        except RepositoryException as error:
            pass
        self.__activity_repository.save(activity)
        undo = FunctionCall(self.remove_activity, activity.id)
        redo = FunctionCall(self.add_activity, activity.id, activity.person_id, date_str, start_str, end_str,
                            activity.description)
        operation = Operation(undo, redo)
        return operation

    def get_all_activities(self):
        """
        returns all activities from the repository
        :return: all activities as list of dictionary values
        """
        return self.__activity_repository.find_all()

    def remove_activity(self, activity_id):
        """
        Removes activity by given id
        :param activity_id: string
        :return: -
        """
        activity = self.__activity_repository.delete_by_id(activity_id)
        undo = FunctionCall(self.add_activity, activity.id, activity.person_id, activity.date.strftime("%d/%m/%Y"),
                            activity.start_time.strftime("%H:%M"), activity.end_time.strftime("%H:%M"),
                            activity.description)
        redo = FunctionCall(self.remove_activity, activity.id)
        operation = Operation(undo, redo)
        return operation

    def find_activity_by_id(self, activity_id):
        """
        Finds activity with given id in repository
        :param activity_id: string id
        :return: True/False depending on what the repository save method is returning
        """
        return self.__activity_repository.find_by_id(activity_id)

    def update_activity(self, activity_id, person_id, date_str, start_str, end_str, description):
        """
        Updates activity with given activity id with the other parameters
        :param activity_id: string
        :param person_id: list of strings
        :param date_str: string as dd/mm/yyyy
        :param start_str: string as hh/mm
        :param end_str: string as hh/mm
        :param description: string
        :return: -
        """
        date, start, end = self.strings_to_datetime(date_str, start_str, end_str)
        activity_to_update = Activity(activity_id, person_id, date, start, end, description)
        try:
            activities_list = self.__activity_repository.find_all()
            self.__activity_validator.validate(activities_list, activity_to_update)
        except RepositoryException as error:
            pass
        old_activity = self.__activity_repository.update(activity_id, activity_to_update)
        undo = FunctionCall(self.update_activity, activity_id, old_activity.person_id, old_activity.date.strftime("%d/%m/%Y"),
                            old_activity.start_time.strftime("%H:%M"), old_activity.end_time.strftime("%H:%M"),
                            old_activity.description)
        redo = FunctionCall(self.update_activity, activity_id, person_id, date_str, start_str, end_str, description)
        operation = Operation(undo, redo)
        return operation

    def add_test_data_activities(self):
        """
        Adds test activities
        :return: -
        """
        return
        self.add_activity("1", ["123", "124"], "12/12/2020", "14:00", "16:00", "Test Activity1")
        self.add_activity("2", ["121"], "1/12/2020", "11:00", "12:00", "Test Activity2")
        self.add_activity("3", ["124", "125"], "12/12/2020", "17:00", "18:00", "Test Activity3")
        self.add_activity("4", ["125"], "10/6/2020", "10:00", "11:00", "Test Activity4")
        self.add_activity("5", ["121", "124"], "9/7/2020", "19:00", "20:00", "Test Activity5")

    @staticmethod
    def criteria_search_activity_date(activity, string_to_search):
        """
        Checks if the date given as a string matches the date of the activity
        """
        format_string = re.compile('.*/.*/.*')
        date_or_description_index = 0
        if string_to_search[date_or_description_index] in activity.description.lower() or \
                (format_string.match(string_to_search[date_or_description_index]) and
                 datetime.datetime.strptime(string_to_search[date_or_description_index], "%d/%m/%Y") == activity.date):
            return True
        return False

    @staticmethod
    def criteria_search_activity_date_time(activity, string_to_search):
        """
        Checks if the date and time given as strings match the date and time of given activity
        """
        format_string = re.compile('.*/.*/.*')
        format_time = re.compile('.*:.*')
        date_or_description_index = 0
        hour_index = 1
        if format_string.match(string_to_search[date_or_description_index]) and \
                datetime.datetime.strptime(string_to_search[date_or_description_index], "%d/%m/%Y") \
                == activity.date and format_time.match(string_to_search[hour_index]) and \
                datetime.datetime.strptime(string_to_search[hour_index], "%H:%M") == activity.start_time:
            return True
        return False

    def search_activity(self, string_to_search):
        """
        Returns a list of activities that match their date/time or their description with given string
        :param string_to_search: string
        :return:list of activities with given property
        """
        date_length = 1
        string_to_search = string_to_search.split(" ")
        function = Functions()
        if len(string_to_search) == date_length:
            return function.filter(self.__activity_repository.find_all(),
                                   self.criteria_search_activity_date, string_to_search)
        else:
            return function.filter(self.__activity_repository.find_all(),
                                   self.criteria_search_activity_date_time, string_to_search)

    @staticmethod
    def criteria_same_date(activity, date):
        if activity.date == date:
            return True
        return False

    @staticmethod
    def comparison_start_time(first_activity, second_activity):
        if first_activity.start_time < second_activity.start_time:
            return True
        return False

    def activities_for_given_date(self, date_string):
        """
        Returns all activities happening on given date sorted by start time
        :param date_string:date as string
        :return: a sorted list of activities happening on given date
        """
        function = Functions()
        date = datetime.datetime.strptime(date_string, "%d/%m/%Y")
        filtered_list = function.filter(self.__activity_repository.find_all(), self.criteria_same_date, date)
        return function.bingo_sort(filtered_list, self.comparison_start_time)

    @staticmethod
    def criteria_with_person(activity, person):
        if person in activity.person_id and activity.date > datetime.datetime.today():
            return True
        return False

    def activities_with_person(self, person):
        """
        Returns a list of all upcoming activities to which a given person will participate
        :param person:given person id as string
        :return:a list of all activities with given property
        """
        function = Functions()
        return function.filter(self.__activity_repository.find_all(), self.criteria_with_person, person)

    def comparison_day(self, first_date, second_date):
        if self.total_minutes(first_date) < self.total_minutes(second_date):
            return True
        return False

    def busiest_days(self):
        """
        Returns a list of busiest upcoming days sorted in descending order of the free time in that day
        :return: a list of days (datetime)
        """
        function = Functions()
        date_list = [activity.date for activity in self.__activity_repository.find_all()
                     if activity.date > datetime.datetime.today()]
        date_list = list(dict.fromkeys(date_list))
        return function.bingo_sort(date_list, self.comparison_day)

    def total_minutes(self, date):
        """
        Computes the total number of minutes of activities in given date
        :param date: given date as datetime
        :return: total number of minutes of activities in given date
        """
        seconds = 60
        return sum((activity.end_time - activity.start_time).total_seconds() / seconds for activity
                   in self.__activity_repository.find_all()
                   if activity.date == date)

    @staticmethod
    def strings_to_datetime(date, start, end):
        """
        Converts strings with proper format into datetime type
        :param date: string as dd/mm/yyyy
        :param start: string as hh/mm
        :param end: string as hh/mm
        :return: date, start, end as datetime
        """
        date = datetime.datetime.strptime(date, "%d/%m/%Y")
        start = datetime.datetime.strptime(start, "%H:%M")
        end = datetime.datetime.strptime(end, "%H:%M")
        return date, start, end
