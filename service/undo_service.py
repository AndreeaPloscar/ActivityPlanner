
class UndoService:
    def __init__(self):
        self._history = []
        self._index = -1

    def record(self, operation):
        """
        Records an operation into history
        """
        index_record = self._index + 1
        self._history = self._history[:index_record]
        self._history.append(operation)
        self._index += 1

    def undo(self):
        """
        Performs an undo if it is possible
        """
        if self._index == -1:
            return False

        self._history[self._index].undo()
        self._index -= 1
        return True

    def redo(self):
        """
        Performs a redo if it is possible
        """
        if self._index == len(self._history) - 1:
            return False

        self._index += 1
        self._history[self._index].redo()
        return True


class CascadedOperation:
    def __init__(self, *operations):
        self._operations = operations

    def undo(self):
        """
        Undo for cascaded operation
        """
        for operation in self._operations:
            operation.undo()

    def redo(self):
        """
        Redo for cascaded operation
        """
        for operation in self._operations:
            operation.redo()


class Operation:
    def __init__(self, function_call_undo, function_call_redo):
        self._function_call_undo = function_call_undo
        self._function_call_redo = function_call_redo

    def undo(self):
        self._function_call_undo()

    def redo(self):
        self._function_call_redo()


class FunctionCall:
    def __init__(self, function_reference, *function_parameters):
        self._function_reference = function_reference
        self._function_parameters = function_parameters

    def call(self):
        return self._function_reference(*self._function_parameters)

    def __call__(self):
        return self.call()
