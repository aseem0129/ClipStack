import threading
import pyperclip
import time
from pynput import keyboard

# this function is the "polling" function to monitor any changes
# from the clipboard and add to our stack
def monitor_clipboard(stack, lock, suppress):
    prev_clipboard = ""

    while True:
        curr_clipboard = pyperclip.paste()

        with lock: #FIXED ISSUE
            if not suppress.is_set():
                if curr_clipboard and curr_clipboard != prev_clipboard:
                    if stack and curr_clipboard != stack[-1] or not stack:
                        stack.append(curr_clipboard)
                    
        prev_clipboard = curr_clipboard
        time.sleep(0.2)


def paste_from_stack(stack, lock, suppress):

    current_keys = set()
    controller = keyboard.Controller()
    
    # this function checks runs when any key is pressed
    def on_press(key):
        current_keys.add(key)

        if (
            keyboard.Key.cmd in current_keys
            and keyboard.Key.shift in current_keys
            and key == keyboard.KeyCode.from_char('v')
        ):
            if stack:
                suppress.set()
                with lock:
                    item_to_paste = stack.pop()
                    pyperclip.copy(item_to_paste)
                
                with controller.pressed(keyboard.Key.cmd):
                    controller.press('v')
                    controller.release('v')
                suppress.clear()

                time.sleep(0.1)

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
    suppress = threading.Event()

    copy_thread = threading.Thread(target=monitor_clipboard, args=(stack, lock, suppress))
    paste_thread = threading.Thread(target=paste_from_stack, args=(stack, lock, suppress))

    copy_thread.start()
    paste_thread.start()

    print("Monitoring clipboard... copy some things!")
    time.sleep(45)

    print("Copied items: ", stack)
