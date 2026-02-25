import threading
import pyperclip
import time
from pynput import keyboard

# this function is the "polling" function to monitor any changes
# from the clipboard and add to our stack
def monitor_clipboard(stack, lock):
    prev_clipboard = ""

    while True:
        curr_clipboard = pyperclip.paste()

        # this loop is to add any changes onto the stack
        if curr_clipboard and curr_clipboard != prev_clipboard:
            if stack and curr_clipboard != stack[-1] or not stack:
                with lock:
                    stack.append(curr_clipboard)
                    
        prev_clipboard = curr_clipboard
        time.sleep(0.2)


def paste_from_stack(stack, lock):

    current_keys = set()
    controller = keyboard.Controller()
    
    # this function checks runs when any key is pressed
    def on_press(key):
        current_keys.add(key)

        if (
            keyboard.Key.cmd in current_keys
            and keyboard.Key.shift in current_keys
            and keyboard.KeyCode.from_char('v') in current_keys
        ):
            if stack:
                with lock:
                    item_to_paste = stack.pop()
                    pyperclip.copy(item_to_paste)

                time.sleep(0.01)

                with controller.pressed(keyboard.Key.cmd):
                    controller.press('v')
                    controller.release('v')

    def on_release(key):
        current_keys.discard(key)
    
    listener = keyboard.Listener(
        on_press=on_press, 
        on_release=on_release)
    
    listener.start()
    listener.join()



        
if __name__ == "__main__":
    stack = []
    lock = threading.Lock()

    thread = threading.Thread(target=monitor_clipboard, args=(stack, lock))
    thread.start()

    print("Monitoring clipboard... copy some things!")
    time.sleep(15)

    print("Copied items: ", stack)