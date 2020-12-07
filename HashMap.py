class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self):
        self.capacity = 50
        self.size = 0
        self.__slots = [None] * self.capacity

    def hash(self, key):
        count = 0
        for position, i in enumerate(key):
            count += (position + len(key)) ** ord(i)
            count = count % self.capacity
        return count

    def add(self, key, value):
        self.size += 1
        index = self.hash(key)
        node = self.__slots[index]
        if node is None:
            self.__slots[index] = Node(key, value)
            return
        prev = node
        while node is not None:
            prev = node
            node = node.next
        prev.next = Node(key, value)

    def get(self, key):
        index = self.hash(key)
        node = self.__slots[index]
        while node is not None and node.key != key:
            node = node.next
        if node is None:
            print("Not found!")
            return None
        else:
            return node.value

    def remove(self, key):
        index = self.hash(key)
        node = self.__slots[index]
        prev = None
        while node is not None and node.key != key:
            prev = node
            node = node.next
        if node is None:
            print("Not found!")
            return None
        else:
            self.size -= 1
            result = node.value
            if prev is None:
                return None
            else:
                prev.next = prev.next.next
            return result


