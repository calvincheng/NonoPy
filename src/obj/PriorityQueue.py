import itertools
import heapq

class PriorityQueue:
    '''
    https://docs.python.org/3/library/heapq.html
    '''
    def __init__(self):
        self.items = []
        self.item_finder = {}
        self.counter = itertools.count()
        self.REMOVED = "<removed>"

    def add_item(self, value, priority = 0):
        if value in self.item_finder:
            self.remove_item(value)
        count = next(self.counter)
        item = [priority, count, value]
        self.item_finder[value] = item
        heapq.heappush(self.items, item)

    def remove_item(self, value):
        entry = self.item_finder.pop(value)
        entry[-1] = self.REMOVED

    def pop_item(self):
        while self.items:
            priority, count, value = heapq.heappop(self.items)
            if value is not self.REMOVED:
                del self.item_finder[value]
                return value
        raise KeyError('pop from an empty priority queue')
