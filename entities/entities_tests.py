import unittest
from entities.person import Person
from entities.activity import Activity
import datetime


class PersonTests(unittest.TestCase):

    def test_person(self):
        test_person = Person("120", "Name", "0751274477")
        self.assertEqual(test_person.id, "120")
        self.assertEqual(test_person.name, "Name")
        self.assertEqual(test_person.phone_number, "0751274477")
        self.assertEqual(str(test_person), "Id - 120, Name - Name, Phone number - 0751274477")


class ActivityTest(unittest.TestCase):

    def test_activity(self):
        test_activity = Activity("1", ["123", "124"], datetime.datetime.strptime("12/12/2020", "%d/%m/%Y"),
                                 datetime.datetime.strptime("14:00", "%H:%M"),
                                 datetime.datetime.strptime("16:00", "%H:%M"), "Test Activity1")
        self.assertEqual(test_activity.id, "1")
        self.assertEqual(test_activity.person_id, ["123", "124"])
        self.assertEqual(test_activity.description, "Test Activity1")
        self.assertEqual(test_activity.date, datetime.datetime.strptime("12/12/2020", "%d/%m/%Y"))
        self.assertEqual(test_activity.start_time, datetime.datetime.strptime("14:00", "%H:%M"))
        self.assertEqual(test_activity.end_time, datetime.datetime.strptime("16:00", "%H:%M"))
        self.assertEqual(str(test_activity), "Id - 1\nPerson IDs - 123, 124\nDate - Sat, 12 December, 2020"
                                             "\nStarting Time - 14:00\nEnding Time - 16:00"
                                             "\nDescription - Test Activity1\n")


