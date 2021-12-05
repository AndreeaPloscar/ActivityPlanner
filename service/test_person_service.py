import unittest
from service.person_service import PersonService
from repository.repository import Repository
from validators.validators import PersonValidator
from validators.validators import PersonValidatorException
from entities.person import Person
from validators.validators import RepositoryException
from service.undo_service import UndoService
from validators.validators import ActivityValidator
from service.activity_service import ActivityService


class TestPersonService(unittest.TestCase):
    def setUp(self):
        self.person_repository = Repository()
        self.person_validator = PersonValidator()
        self.undo_service = UndoService()
        self.activity_validator = ActivityValidator()
        self.activity_repository = Repository()
        self.activity_service = ActivityService(self.undo_service, self.activity_repository, self.activity_validator)
        self.person_service = PersonService(self.undo_service, self.person_repository, self.person_validator, self.activity_service)
        self.person_service.add_person("129", "Andreea", "0751274477")
        self.activity_service.add_activity("10", ["129", "124"], "12/2/2020", "14:00", "16:00", "Test Activity1")

    def test_add_person(self):
        person_id, name, phone_number = "120", "Andreea", "0751274477"
        add_person = Person(person_id, name, phone_number)
        self.person_service.add_person(person_id, name, phone_number)
        self.assertEqual(len(self.person_service.get_all_persons()), 2)
        self.assertRaises(PersonValidatorException, self.person_service.add_person, "120", "Andreea", "0777")
        self.assertRaises(PersonValidatorException, self.person_service.add_person, "120", "Andreea", "073454367x")

    def test_find_person_by_id(self):
        self.assertTrue(self.person_service.find_person_by_id("129"))
        self.assertFalse(self.person_service.find_person_by_id("124"))

    def test_remove_person(self):
        self.person_service.remove_person("129")
        self.assertRaises(RepositoryException, self.person_service.get_all_persons)

    def test_update_person(self):
        self.person_service.update_person("129", "NewName", "0786173642")
        self.assertTrue(self.person_service.find_person_by_id("129"))

    def test_search_person(self):
        self.assertEqual(self.person_service.search_person("075"), [Person("129", "Andreea", "0751274477")])

    def test_add_test_data(self):
        self.person_service.add_test_data_persons()
        self.assertEqual(len(self.person_service.get_all_persons()), 1)

    def test_undo(self):
        self.person_service.add_person("128", "Name", "0751274477")
        operation = self.person_service.remove_person("129")
        self.undo_service.record(operation)
        self.undo_service.undo()
        assert len(self.person_service.get_all_persons()) == 2

    def test_redo(self):
        self.person_service.add_person("128", "Name", "0751274477")
        self.assertFalse(self.undo_service.undo())
        self.assertFalse(self.undo_service.redo())
        operation = self.person_service.remove_person("129")
        self.undo_service.record(operation)
        self.undo_service.undo()
        assert len(self.person_service.get_all_persons()) == 2
        self.undo_service.redo()
        assert len(self.person_service.get_all_persons()) == 1

    def tearDown(self):
        print('TORN DOWN')
