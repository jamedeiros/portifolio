from cgitb import text
import random
import threading
import time
import algorithm

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 300
SIZE = 50
TIMEOUT = 0.01
STEPS = 10


KNOWN_ALGORITHIMS = {
    "InsertionSort": algorithm.InsertionSort,
    "SelectionSort": algorithm.SelectionSort,
    "BubbleSort": algorithm.BubbleSort,
    "CombSort": algorithm.CombSort,
    "BogoSort": algorithm.BogoSort,
}

class SortingWidet(Widget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.highlight = list()
        self.is_running = True
        self.algorithm_thread = None
        self.delay = TIMEOUT

    def set_data(self, data_size):
        self.data = [random.randint(1, WINDOWS_HEIGHT + 1) for _ in  range(data_size)]
        self.data_size = data_size
        self.bar_size = int((WINDOWS_WIDTH*0.75) / self.data_size)
    
    def set_delay(self, delay):
        self.delay = delay
    
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm(data=self.data, display=self)

    def start(self):
        if self.algorithm_thread:
            self.is_running = False
            self.algorithm_thread.join()

        self.algorithm_thread = threading.Thread(
            target=self.algorithm.process, args=(lambda: self.is_running,)
        )
        self.is_running = True
        self.algorithm_thread.start()

    def on_request_close(self, *args, **kwargs):
        if self.algorithm_thread:
            self.is_running = False
            self.algorithm_thread.join()

    def add_highlight(self, element):
        if isinstance(element, list):
            self.highlight.extend(element)
        else:
            self.highlight.append(element)

    def draw(self, *args, **kwargs):
        Clock.schedule_once(self.update_data, 0)
        time.sleep(self.delay)

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


class Form(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = 'vertical' 
        self.cols = 2

        self.add_widget(Label(text="Elements"))
        self.elements = TextInput(text="100", multiline=False)
        self.add_widget(self.elements)

        self.add_widget(Label(text="Delay"))
        self.delay = TextInput(text=str(TIMEOUT), multiline=False)
        self.add_widget(self.delay)

        dropdown = DropDown()

        for name in KNOWN_ALGORITHIMS:
            btn = Button(
                text=name,
                size_hint_y=None,
                height=44
            )
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        
        self.algorithmBtn = Button(text="Select")
        self.algorithmBtn.bind(on_release=dropdown.open)

        dropdown.bind(on_select=lambda instance, x: setattr(self.algorithmBtn, 'text', x))

        self.add_widget(Label(text="Algorithms"))
        self.add_widget(self.algorithmBtn)

class Application(App):

    def build(self):
        self.window = GridLayout(cols=2)
        self.main_widget = SortingWidet()
        self.form = Form()

        btn1 = Button(text='Run ...')
        btn1.bind(on_release = self.execute)

        formGrid = GridLayout(cols=1, size_hint=(0.5, 1))
        formGrid.add_widget(self.form)
        formGrid.add_widget(btn1)

        side = GridLayout(cols=1)
        side.add_widget(self.main_widget)
        
        self.window.add_widget(side)
        self.window.add_widget(formGrid)

        Window.bind(on_request_close=self.main_widget.on_request_close)

        return self.window

    def execute(self, *args, **kwargs):
        self.main_widget.set_data(int(self.form.elements.text))
        self.main_widget.set_delay(float(self.form.delay.text))
        self.main_widget.set_algorithm(KNOWN_ALGORITHIMS[self.form.algorithmBtn.text])
        self.main_widget.start()

def main():
    Window.size = (WINDOWS_WIDTH, WINDOWS_HEIGHT)
    Application().run()
    


if __name__ == "__main__":
        
    main()