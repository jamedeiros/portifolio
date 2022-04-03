import algorithm
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget


WINDOWS_WIDTH = 500
WINDOWS_HEIGHT = 300
SIZE = 5
TIMEOUT = 0.1
STEPS = 10


class MyDisplay(Widget):
    
    def __init__(self, data, algorithm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.bar_size = WINDOWS_WIDTH // len(self.data)
        self.algorithm = algorithm

        self.trigger = Clock.create_trigger(
            self.update_data, timeout=TIMEOUT
        )
        self.trigger()

    def update_data(self, *args):
        highlight = self.algorithm.process(self.data)
        if highlight is None:
            highlight = []
        self.update(highlight)
        self.trigger()
    
    def update(self, highlight):
        self.canvas.clear()
        with self.canvas:
            for idx, value in enumerate(self.data):
                Color(1, 1, 1)
                if idx in highlight:
                    Color(1, 0, 0)
                Rectangle(pos=(idx * self.bar_size, 0), size=(self.bar_size, value))


class Application(App):

    def __init__(self, algorithm, step, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.algorithm = algorithm
        self.step = step
        self.data = [random.randint(1, WINDOWS_HEIGHT + 1) for _ in  range(SIZE)]

    def build(self):
        myDisplay = MyDisplay(
            data=self.data, 
            algorithm=self.algorithm(size=len(self.data), step=self.step)
        )
        return myDisplay

def main():
    Config.set('graphics', 'width', WINDOWS_WIDTH)
    Config.set('graphics', 'height', WINDOWS_HEIGHT)
    Config.write()    

    # Application(algorithm=algorithm.InsertionSort, step=STEPS).run()
    # Application(algorithm=algorithm.SelectionSort, step=STEPS).run()
    # Application(algorithm=algorithm.BubbleSort, step=STEPS).run()
    # Application(algorithm=algorithm.CombSort, step=STEPS).run()
    Application(algorithm=algorithm.BogoSort, step=STEPS).run()
    


if __name__ == "__main__":
        
    main()