import random
import threading
import time
import algorithm

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget



WINDOWS_WIDTH = 500
WINDOWS_HEIGHT = 300
SIZE = 50
TIMEOUT = 0.01
STEPS = 10


class SortingWidet(Widget):
    
    def __init__(self, data, algorithm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.data_size = len(data)
        self.bar_size = WINDOWS_WIDTH // len(self.data)

        self.highlight = list()

        self.algorithm = algorithm(data=self.data, display=self)
        self.is_running = True

        self.algorithm_thread = threading.Thread(
            target=self.algorithm.process, args=(lambda: self.is_running,)
        )
        self.algorithm_thread.start()
        
    def on_request_close(self, *args, **kwargs):
        self.is_running = False
        self.algorithm_thread.join()

    def add_highlight(self, element):
        if isinstance(element, list):
            self.highlight.extend(element)
        else:
            self.highlight.append(element)

    def draw(self, *args, **kwargs):
        Clock.schedule_once(self.update_data, 0)
        time.sleep(TIMEOUT)

    def update_data(self, *args):
        self.update()
    
    def update(self):
        self.canvas.clear()
        with self.canvas:
            for idx, value in enumerate(self.data):
                Color(1, 1, 1)
                if idx in self.highlight:
                    Color(1, 0, 0)
                Rectangle(pos=(idx * self.bar_size, 0), size=(self.bar_size, value))
        self.highlight.clear()


class Application(App):

    def __init__(self, algorithm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.algorithm = algorithm
        self.data = [random.randint(1, WINDOWS_HEIGHT + 1) for _ in  range(SIZE)]

    def build(self):
        myDisplay = SortingWidet(
            data=self.data, 
            algorithm=self.algorithm
        )
        Window.bind(on_request_close=myDisplay.on_request_close)
        return myDisplay

def main():
    Config.set('graphics', 'width', WINDOWS_WIDTH)
    Config.set('graphics', 'height', WINDOWS_HEIGHT)
    Config.write()    

    # Application(algorithm=algorithm.InsertionSort).run()
    # Application(algorithm=algorithm.SelectionSort).run()
    Application(algorithm=algorithm.BubbleSort).run()
    # Application(algorithm=algorithm.CombSort).run()
    # Application(algorithm=algorithm.BogoSort).run()
    


if __name__ == "__main__":
        
    main()