import time
import threading
import random
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

delay = 0.075
range = 0.03
left_key = KeyCode(char='c')
right_key = KeyCode(char='2')
stop_key = KeyCode(char='`')


mouse = Controller()


class ClickMouse(threading.Thread):
    def __init__(self, button):
        super(ClickMouse, self).__init__()
        self.running = False
        self.button = button
        self.start_delay = delay - range
        self.end_delay = delay + range
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(random.uniform(self.start_delay, self.end_delay))
            time.sleep(0.1)


left_click_thread = ClickMouse(Button.left)
right_click_thread = ClickMouse(Button.right)
left_click_thread.start()
right_click_thread.start()

def on_press(key):
    if key == left_key:
        if left_click_thread.running:
            left_click_thread.stop_clicking()
        else:
            left_click_thread.start_clicking()
    elif key == right_key:
        if right_click_thread.running:
            right_click_thread.stop_clicking()
        else:
            right_click_thread.start_clicking()
    elif key == stop_key:
        left_click_thread.exit()
        right_click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()