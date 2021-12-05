
class PlannerException(Exception):
    pass


class PersonValidatorException(PlannerException):
    pass


class ActivityValidatorException(PlannerException):
    pass


class RepositoryException(PlannerException):
    pass


class InputException(PlannerException):
    pass


class PersonValidator:

    def validate(self, person):
        if not self.check_phone_number(person):
            raise PersonValidatorException("Phone number should have 10 digits!")

    @staticmethod
    def check_phone_number(person):
        proper_phone_number_length = 10
        if len(person.phone_number) != proper_phone_number_length:
            return False
        for digit in person.phone_number:
            try:
                digit = int(digit)
            except ValueError:
                return False
        return True


class ActivityValidator:

    def validate(self, activities, activity):
        """
        Validates given activity by checking if it overlaps with another activity from activities list
        Raises ActivityValidatorException if activity overlaps
        :param activities: list of activities
        :param activity: new activity to validate
        :return: -
        """
        if not self.check_overlap(activities, activity):
            raise ActivityValidatorException("Activity overlaps!")

    @staticmethod
    def check_overlap(activities_list, activity_to_add):
        """
        Checks if activity_to_add overlaps with other activities from activities_list
        :param activities_list: list of activities
        :param activity_to_add:  new activity to validate
        :return: True if activity does not overlap, false otherwise
        """
        for activity in activities_list:
            existing_start = activity.start_time
            existing_end = activity.end_time
            existing_date = activity.date
            if existing_date == activity_to_add.date and activity_to_add.id != activity.id:
                if existing_start <= activity_to_add.start_time <= existing_end:
                    return False
                if existing_start <= activity_to_add.end_time <= existing_end:
                    return False
                if activity_to_add.start_time <= existing_start and existing_end <= activity_to_add.end_time:
                    return False
        return True
