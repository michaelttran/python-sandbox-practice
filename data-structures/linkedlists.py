# Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists

from typing import List


class Node:
    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, val):
        node = Node(val)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def reverse(self):
        curr = self.head
        while curr is not None:
            curr.prev, curr.next = curr.next, curr.prev
            curr = curr.prev  # after swap, old next is now prev
        self.head, self.tail = self.tail, self.head

    def pprint(self):
        curr = self.head
        vals = []
        while curr is not None:
            vals.append(str(curr.val))
            curr = curr.next
        print(" <-> ".join(vals))


def main():
    print("Started...\n")

    ll = DLinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)

    print("Original:")
    ll.pprint()

    ll.reverse()
    print("Reversed:")
    ll.pprint()

    print("\nFinished.")


if __name__ == "__main__":
    main()
