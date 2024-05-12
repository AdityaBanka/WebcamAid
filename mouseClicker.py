import time
from pynput import mouse
from pynput.mouse import Button, Listener

def on_click(x, y, button, pressed):
    global button_state  # Track button state across events
    global exitState
    if button == Button.left:
        button_state = pressed
    if button == Button.right:
        exitState = True
        return(False)


def call_your_function():
    print("Mouse button held!")  # Your actual function goes here

button_state = False  # Initial state
exitState = False
def check_and_call():
    global button_state
    if button_state:
        call_your_function()

# Collect mouse events
listener = Listener(on_click=on_click)
listener.start()
while not exitState:
    check_and_call()
    time.sleep(0.01)  # Shorter delay for responsiveness
listener.join()