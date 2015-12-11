import random
import math


class Heap:
    def __init__(self):
        self.data = []

    def insert(self, value):
        self.data.append(value)
        self.heapify_up()

    def heapify_up(self):
        i = len(self.data) - 1
        while i > 0:
            print(self)
            parent = (i - 1) // 2
            if self.compare(i, parent):
                self.swap(i, parent)
                i = parent
            else:
                break

    def peek(self):
        return self.data[0]

    def pop(self):
        value = self.data.pop(0)
        if len(self.data):
            self.data.insert(0, self.data.pop())
        self.heapify_down()
        return value

    def heapify_down(self):
        i = 0
        while i < len(self.data):
            print(self)
            left = 2 * i + 1
            right = 2 * i + 2
            if not self.compare(i, left) or not self.compare(i, right):
                to_swap = left
                if not self.compare(left, right):
                    to_swap = right
                self.swap(i, to_swap)
                i = to_swap
            else:
                break

    def swap(self, a, b):
        self.data[a], self.data[b] = self.data[b], self.data[a]

    def compare(self, a, b):
        if a >= len(self.data) or b >= len(self.data):
            return True
        return self.data[a] < self.data[b]

    def __repr__(self):
        tree = ''
        width = math.pow(2, math.floor(math.log2(len(self.data))))
        current_width = 1
        i = 0
        while current_width <= width:
            offset = '  ' * int((width / current_width) - 1)
            spacer = '  ' * int((width / current_width * 2) - 1)
            row = offset + spacer.join(str(value).rjust(2) for value in self.data[i:i + current_width])
            tree += row + '\n'
            i += current_width
            current_width *= 2
        return tree


def main():
    heap = Heap()
    for i in range(30):
        value = random.randint(0, 99)
        print('inserting: {}'.format(value))
        heap.insert(value)

    sorted_values = []
    for i in range(30):
        print('------------------------------')
        value = heap.pop()
        print('popped: {}'.format(value))
        sorted_values.append(value)

    print(sorted_values)


if __name__ == '__main__':
    main()
