import abc
import random
import time

from utils import swap


class Algorithm(abc.ABC):

    def __init__(self, data, display):
        self.data = data
        self.data_size = len(self.data)
        self.display = display
        self.running = True
    
    def stop(self):
        self.running = False
    
    @abc.abstractmethod
    def process(self, is_running):
        pass

class InsertionSort(Algorithm):

    def process(self, is_running):
        for i in range(1, self.data_size):
            j = i
            while j > 0 and self.data[j] < self.data[j-1]:
                if not is_running():
                    return None

                swap(self.data, j, j-1)
                j -= 1
                self.display.add_highlight(j)
                self.display.draw()



class SelectionSort(Algorithm):

    def process(self, is_running):
        for i in range(self.data_size):
            minor = i
            for j in range(i, self.data_size):
                if not is_running():
                    return None

                if self.data[minor] > self.data[j]:
                    minor = j
                self.display.add_highlight([i, j, minor])
                self.display.draw()

            if minor != i:
                swap(self.data, i, minor)


class BubbleSort(Algorithm):
    
    def process(self, is_running):
        swapped = True
        while swapped:
            swapped = False
            for i in range(self.data_size - 1):
                if not is_running():
                    return None
                if self.data[i] > self.data[i+1]:
                    swap(self.data, i, i+1)
                    swapped = True
                self.display.add_highlight([i, i+1])
                self.display.draw()


class CombSort(Algorithm):

    def __init__(self, factor=1.3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factor = factor

    def process(self, is_running):
        gap = self.data_size
        sorted = False

        while not sorted:
            gap = int(gap // self.factor)
            if gap <= 1:
                gap = 1
                sorted = True
            
            for i in range(self.data_size - gap):
                if not is_running():
                    return None

                if self.data[i] > self.data[i + gap]:
                    swap(self.data, i, i + gap)
                    sorted = False
                self.display.add_highlight([i, i+gap])
                self.display.draw()



class BogoSort(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sorted(self):
        for i in range(self.data_size-1):
            if self.data[i] > self.data[i+1]:
                return False
        return True

    def process(self, is_running):
        while not self.sorted():
            if not is_running():
                return None
            random.shuffle(self.data)
            self.display.draw()
        return None
        
