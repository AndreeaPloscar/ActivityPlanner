class Collection:

    class Iterator:
        """
        Iterator class
        """
        def __init__(self, collection):
            self._collection = collection
            self._position = 0

        def __next__(self):
            """
            Getting the next item from iterable object
            """
            if self._position == len(self._collection):
                raise StopIteration()
            self._position += 1
            return self._collection[self._position - 1]

    def __init__(self):
        self._data = []

    def add(self, element):
        self._data.append(element)

    def __iter__(self):
        return self.Iterator(self)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def clear(self):
        self._data.clear()

    def extend(self, l):
        self._data.extend(l)

#
# from collections import Iterator
#
#
# class IterableCollection:
#     class MyIterator(Iterator):
#         def __init__(self, col):
#             self._collection = col
#             self._poz = 0
#
#         def __next__(self):
#             # Stop iteration when other elements are not available
#             if self._poz == len(self._collection._data.keys()):
#                 raise StopIteration()
#             # Move to the next element
#             self._poz += 1
#             return list(self._collection._data.keys())[self._poz - 1]
#
#     def __init__(self):
#         self._data = {}
#
#     def __setitem__(self, key, value):
#         self._data[key] = value
#
#     def __getitem__(self, key):
#         return self._data[key] if key in self._data else None
#
#     def __len__(self):
#         return len(self._data)
#
#     def __delitem__(self, key):
#         del self._data[key]
#
#     def __iter__(self):
#         return self.MyIterator(self)
#
#     def __contains__(self, key):
#         return key in self._data.keys()
#
#     def values(self):
#         return self._data
#
# def gnome_sort(list_to_sort, function):
#     index = 0
#     while index < len(list_to_sort):
#         if index == 0:
#             index = index + 1
#         if not function(list_to_sort[index], list_to_sort[index - 1]):
#             index = index + 1
#         else:
#             list_to_sort[index], list_to_sort[index - 1] = list_to_sort[index - 1], list_to_sort[index]
#             index = index - 1
#
#     return list_to_sort
#
#
# def filter_list(list_to_filter, function):
#
#     return [item for item in list_to_filter if function(item)]