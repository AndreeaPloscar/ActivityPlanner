import unittest
from entities.activity import Activity
from validators.validators import ActivityValidator
from validators.validators import ActivityValidatorException
from service.activity_service import ActivityService
from repository.repository import Repository
from validators.validators import RepositoryException
import datetime
from service.undo_service import UndoService


class TestActivityService(unittest.TestCase):

    def setUp(self):
        self.activity_validator = ActivityValidator()
        self.activity_repository = Repository()
        self.undo_service = UndoService()
        self.activity_service = ActivityService(self.undo_service, self.activity_repository, self.activity_validator)
        self.activity_service.add_activity("10", ["123", "124"], "12/2/2020", "14:00", "16:00", "Test Activity1")

    def test_add_activity(self):
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          "2", ["123", "124"], "12/2/2020", "14:00", "16:00", "Test Activity1")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          "2", ["123", "124"], "12/2/2020", "12:00", "18:00", "Test Activity1")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          "2", ["123", "124"], "12/2/2020", "12:00", "15:00", "Test Activity1")
        self.assertEqual(len(self.activity_service.get_all_activities()), 1)

    def test_remove_activity(self):
        self.activity_service.remove_activity("10")
        self.assertFalse(self.activity_service.find_activity_by_id("10"))

    def test_update_activity(self):
        self.activity_service.update_activity("10", ["123", "124"], "14/2/2020", "15:00", "16:00", "Test Activity2")
        self.assertTrue(self.activity_service.find_activity_by_id("10"))
        self.activity_service.remove_activity("10")
        self.assertRaises(RepositoryException, self.activity_service.update_activity, "10", ["123", "124"], "14/2/2020",
                          "15:00", "16:00", "Test Activity2")

    def test_add_test_data(self):
        self.activity_service.add_test_data_activities()
        self.assertEqual(len(self.activity_service.get_all_activities()), 1)

    def test_search_activity(self):
        self.assertEqual(self.activity_service.search_activity("12/2/2020"),
                         [Activity("10", ["123", "124"], datetime.datetime.strptime("12/2/2020", "%d/%m/%Y"),
                                   datetime.datetime.strptime("14:00", "%H:%M"),
                                   datetime.datetime.strptime("16:00", "%H:%M"), "Test Activity1")])
        self.assertEqual(self.activity_service.search_activity("12/2/2020 14:00"),
                         [Activity("10", ["123", "124"], datetime.datetime.strptime("12/2/2020", "%d/%m/%Y"),
                                   datetime.datetime.strptime("14:00", "%H:%M"),
                                   datetime.datetime.strptime("16:00", "%H:%M"), "Test Activity1")])

    def test_activities_for_given_date(self):
        self.assertEqual(self.activity_service.activities_for_given_date("12/2/2020"),
                         [Activity("10", ["123", "124"], datetime.datetime.strptime("12/2/2020", "%d/%m/%Y"),
                                   datetime.datetime.strptime("14:00", "%H:%M"),
                                   datetime.datetime.strptime("16:00", "%H:%M"), "Test Activity1")])

    def test_activities_with_person(self):
        self.assertEqual(self.activity_service.activities_with_person("123"), [])

    def test_busiest_days(self):
        self.activity_service.add_activity("11", ["123", "124"], "12/12/2021", "14:00", "16:00", "Test Activity1")
        self.activity_service.add_activity("12", [], "1/12/2021", "15:00", "16:00", "Test Activity2")
        self.assertEqual(self.activity_service.busiest_days(), [datetime.datetime(2021, 12, 1, 0, 0),
                                                                datetime.datetime(2021, 12, 12, 0, 0)])

    def tearDown(self):
        print("Torn Down")
