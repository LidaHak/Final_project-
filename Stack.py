import Linked_List

class Stack:
    def __init__(self):
        self.values = Linked_List.Linked_List("head")
        self.size = 0

    def empty(self):
        return self.size is 0

    def size(self):
        return self.size

    def push(self, value):
        self.values.add(value)
        self.size += 1

    def pop(self):
        if not self.empty():
            self.size -= 1
            return self.values.remove_from_end()
