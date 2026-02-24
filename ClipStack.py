import threading
import pyperclip
import time

# this function is the "polling" function to monitor any changes
# from the clipboard and add to our stack
def monitor_clipboard(stack, lock):
    prev_clipboard = ""

    # while true so that it runs forever
    while True:
        curr_clipboard = pyperclip.paste() # here we read what the clipboard holds

        # this loop is to add any changes onto the stack
        if curr_clipboard and curr_clipboard != prev_clipboard: # we need to check if our clipboard is not empty and if it is not the same as the previous clipboard (this is how we know there is a change)
            # if our stack isnt empty and the top of our stack is not the same string as our clipboard then there is a change, if stack is empty its our first time pushing from the clipboard to the stack
            if stack and curr_clipboard != stack[-1] or not stack:
                # we then acquire the lock to make sure only this function is modding our stack and then we append whatever is on our current clipboard to our stack
                with lock:
                    stack.append(curr_clipboard)

        # we then update our prev_clipboard to our current one so we compare with the most updated one each time
        prev_clipboard = curr_clipboard
        time.sleep(0.2)






# Initialize last_clipboard to empty string
#
# Loop forever:
#     Read current clipboard content
#     
#     If current_clipboard is different from last_clipboard:
#         If stack is not empty AND current_clipboard equals top of stack:
#             Ignore (it's our own paste)
#         Else:
#             Acquire lock
#             Add current_clipboard to stack
#             Release lock
#         
#         Update last_clipboard to current_clipboard
#     
#     Sleep for 0.2 seconds