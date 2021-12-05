import unittest
from iterable_module.collection import Collection
from iterable_module.functions import Functions


class Test(unittest.TestCase):

    def setUp(self):
        self.structure = Collection()
        self.service = Functions()
        self.structure.add(2)
        self.structure.add(0)
        self.structure.add(3)
        self.structure.add(3)
        self.structure.add(0)
        self.structure.add(4)
        self.structure.add(4)

    def test_delete(self):
        self.structure.__delitem__(2)
        self.assertListEqual(list(self.structure), [2, 0, 3, 0, 4, 4])
        self.structure.add(3)

    def test_comparison(self):
        self.assertFalse(self.comparison(3, 2))

    def test_get_item(self):
        self.assertEqual(self.structure.__getitem__(0), 2)

    @staticmethod
    def comparison(first_item, second_item):
        if first_item < second_item:
            return True
        return False

    @staticmethod
    def criteria(item, parameter):
        if item > parameter:
            return True
        return False

    def test_iterator(self):
        count = 0
        for item in self.structure:
            for item2 in self.structure:
                count += 1

    def testSort(self):
        self.service.bingo_sort(self.structure, self.comparison)
        self.assertListEqual(list(self.structure), [0, 0, 2, 3, 3, 4, 4])
        self.assertListEqual(self.service.bingo_sort([], self.comparison), [])

    def testFilter(self):
        list = self.service.filter(self.structure, self.criteria, 3)
        self.assertEqual(list, [4, 4])
