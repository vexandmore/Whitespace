WORD_TYPE = 'l'


class HeapError(Exception):
    pass

class StackError(Exception):
    pass

class CannotFindJumpTarget(Exception):
    pass

class DuplicateLabels(Exception):
    pass
