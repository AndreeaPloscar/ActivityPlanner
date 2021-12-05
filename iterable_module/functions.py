from iterable_module.collection import Collection


class Functions:

    @staticmethod
    def filter(iterable, criteria, parameter):
        """
        Filtering function for iterable object with given criteria function and parameter for criteria function
        :param criteria: function that receives an item from iterable object and the parameter and determines if
        the item needs to be kept or not
        :param iterable: iterable object
        :param parameter: anything that can be used in criteria function
        """
        new_iterable = []
        for index in range(len(iterable)):
            if criteria(iterable[index], parameter):
                new_iterable.append(iterable[index])
        return new_iterable[:]

    @staticmethod
    def bingo_sort(iterable, comparison):
        """
        Bingo sort for iterable object
        :param iterable: iterable object
        :param comparison: comparison function that determines the correct order of two items from iterable object
        """
        if len(iterable) == 0:
            return []
        maximum = len(iterable) - 1
        next_value = iterable[maximum]
        for index in range(maximum - 1, -1, -1):
            if not comparison(iterable[index], next_value):
                next_value = iterable[index]
        while (maximum > 0) and (iterable[maximum] == next_value):
            maximum = maximum - 1
        while maximum > 0:
            value = next_value
            next_value = iterable[maximum]
            for index in range(maximum - 1, -1, -1):
                if iterable[index] == value:
                    iterable[index], iterable[maximum] = iterable[maximum], iterable[index]
                    maximum = maximum - 1
                elif iterable[index] > next_value:
                    next_value = iterable[index]
            while (maximum > 0) and (iterable[maximum] == next_value):
                maximum = maximum - 1
        return iterable

    def merge_sort(self, l):
        if len(l) < 2:
            return l

        mid = len(l) // 2
        leftHalf = l[:mid]
        rightHalf = l[mid:]
        self.merge_sort(leftHalf)
        self.merge_sort(rightHalf)
        self.merge(leftHalf, rightHalf, l)

    @staticmethod
    def merge(l1, l2, lrez):
        i = 0
        j = 0
        l = []
        while i < len(l1) and j < len(l2):
            if l1[i] < l2[j]:
                l.append(l1[i])
                i = i + 1
            else:
                l.append(l2[j])
                j = j + 1
        while i < len(l1):
            l.append(l1[i])
            i = i + 1
        while j < len(l2):
            l.append(l2[j])
            j = j + 1
        lrez.clear()
        lrez.extend(l)


c = Collection()
c.add(1)
c.add(2)
c.add(5)
c.add(3)
c.add(10)
c.add(0)
for el in c:
    print(el)
function = Functions()
function.merge_sort(c)
for el in c:
    print(el)