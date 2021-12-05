import unittest
from .repository import Repository
from validators.validators import RepositoryException
from entities.person import Person


class TestRepository(unittest.TestCase):
    def setUp(self):
        self._test_repository = Repository()
        self._test_repository.save(Person("121", "Alina", "0751274477"))
        self._test_repository.save(Person("120", "Andreea", "0754487543"))
        self._test_repository.save(Person("122", "Alina", "0741274477"))
        self._test_repository.save(Person("123", "Alina", "0751275477"))

    def test_repository_save(self):
        self.assertEqual(len(self._test_repository.find_all()), 4)
        self.assertRaises(RepositoryException, self._test_repository.save, Person("121", "Name", "0786124365"))

    def test_repository_find_all(self):
        self.assertEqual(len(self._test_repository.find_all()), 4)

    def test_repository_delete_by_id(self):
        self._test_repository.delete_by_id("121")
        self._test_repository.delete_by_id("120")
        self._test_repository.delete_by_id("122")
        self._test_repository.delete_by_id("123")
        self.assertRaises(RepositoryException, self._test_repository.delete_by_id, "124")
        self.assertRaises(RepositoryException, self._test_repository.find_all)

    def test_repository_find_by_id(self):
        self.assertTrue(self._test_repository.find_by_id("120"))
        self.assertFalse(self._test_repository.find_by_id("124"))

    def test_repository_update(self):
        self._test_repository.update("120", Person("120", "NewName", "0751274477"))
        self.assertTrue(self._test_repository.find_by_id("120"))
        self.assertRaises(RepositoryException,self._test_repository.update, "124", Person("124", "NewName", "0751274477"))

    def tearDown(self):
        print('TORN DOWN')
