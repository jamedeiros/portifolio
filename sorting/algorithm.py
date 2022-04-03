import abc
import random

from utils import swap


class Algorithm(abc.ABC):

    def __init__(self, size, step=10):
        self.size = size
        self.step = step
    
    @abc.abstractmethod
    def process(self, data):
        pass

class InsertionSort(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = 0
        self.j = 0
    
    def process(self, data):
        for _ in range(self.step):
            if self.j == 0:
                self.i +=1
                self.j = self.i

            if self.i == self.size:
                return None

            highlight = self.j - 1

            if data[self.j] < data[self.j-1]:
                swap(data, self.j, self.j-1)
                self.j -= 1
            else:
                self.j = 0

        return highlight,


class SelectionSort(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = 0
        self.j = 0
        self.minor = 0
    
    def process(self, data):
        for _ in range(self.step):
            if self.j == self.size:
                if self.i != self.minor:
                    swap(data, self.i, self.minor)
                self.i += 1
                self.j = self.i
                self.minor = self.i

            if self.i >= self.size:
                return None

            if data[self.j] < data[self.minor]:
                self.minor = self.j
            
            self.j += 1
        return self.i, self.j, self.minor


class BubbleSort(Algorithm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = 0
        self.swapped = False
    
    def process(self, data):
        for _ in range(self.step):
            if self.i == self.size - 1:
                if not self.swapped:
                    return None
                self.i = 0
                self.swapped = False

            if data[self.i] > data[self.i + 1]:
                swap(data, self.i, self.i + 1)
                self.swapped = True
            self.i += 1
        return self.i, self.i + 1


class CombSort(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = 0
        self.gap = int(self.size // 1.3)

    def process(self, data):
        for _ in range(self.step):
            if self.i == self.size - 1:
                return None
                
            if (self.i + self.gap) < self.size:
                if data[self.i] > data[self.i + self.gap]:
                    swap(data, self.i, self.i + self.gap)
                self.i += 1
            else:
                self.i = 0
                self.gap = int(self.gap // 1.3)
        
        return self.i, self.i + self.gap


class BogoSort(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sorted(self, data):
        for i in range(self.size-1):
            if data[i] > data[i+1]:
                return False
        return True

    def process(self, data):
        if self.sorted(data):
            return None
        
        random.shuffle(data)
