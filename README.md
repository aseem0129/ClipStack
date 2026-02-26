ClipStack
A lightweight LIFO (Last In, First Out) clipboard manager for macOS that allows you to copy multiple items and paste them one by one in reverse order.
Overview
ClipStack enhances your clipboard workflow by maintaining a stack of your copied items. Instead of being limited to a single clipboard item, you can copy multiple things in succession and paste them in reverse order using a simple keyboard shortcut.
Example Use Case:
Copy: "Apple" → "Banana" → "Cherry"
Paste: "Cherry" → "Banana" → "Apple"
Perfect for scenarios where you need to copy multiple items from one location and paste them elsewhere without constantly switching back and forth.
Features

Multi-item clipboard history - Copy as many items as you need
LIFO stack behavior - Most recent copy pastes first
Native integration - Works seamlessly with macOS clipboard
Universal copy detection - Captures copies from any method (Cmd+C, right-click, Edit menu)
Lightweight - Runs in the background with minimal resource usage
Thread-safe - Properly handles concurrent operations

Requirements

macOS (tested on macOS 10.14+)
Python 3.7+
Accessibility permissions (one-time setup)

Dependencies:

pyperclip - Clipboard access
pynput - Keyboard monitoring and control

Usage

Run the application:

python clipstack.py

Grant Accessibility permissions when prompted:

Go to System Preferences → Security & Privacy → Privacy
Select "Accessibility" from the left sidebar
Click the lock icon and enter your password
Add Terminal (or your Python interpreter) to the allowed apps
Check the box to enable


Use the application:

Copy items normally using Cmd+C (or any copy method)
Paste from stack using Cmd+Shift+V
Items paste in reverse order (most recent first)


How It Works
ClipStack runs two concurrent threads:

Clipboard Monitor Thread

Polls the system clipboard every 0.2 seconds
Detects changes and adds new items to the stack
Filters out empty clipboard and duplicate entries


Paste Handler Thread

Listens for Cmd+Shift+V keyboard shortcut
Pops the most recent item from the stack
Writes it to the clipboard and simulates Cmd+V
Thread-safe operations using locks

Technical Details
Threading & Concurrency:

Uses Python's threading module for concurrent operations
Lock-based synchronization for thread-safe stack access
Event-driven keyboard monitoring with pynput.Listener

Clipboard Integration:

Works with macOS's native pasteboard system
Compatible with all copy methods (keyboard, menu, right-click)
Maintains compatibility with normal Cmd+C/Cmd+V workflow

Performance:

Minimal CPU usage (~0.1% idle)
Efficient polling with 0.2s intervals
Smart duplicate detection to avoid redundant entries

Limitations

macOS only (uses macOS-specific keyboard APIs)
Text-only (does not support images or files)
Requires Accessibility permissions
Stack clears when application exits (no persistence between sessions)

Troubleshooting
"This process is not trusted!" error:

You need to grant Accessibility permissions
See Installation step 2 for instructions
Restart the application after granting permissions

Items not being captured:

Verify the application is running
Check that you're copying text (not images/files)
Ensure clipboard is not empty

Multiple items pasting at once:

Release Cmd+Shift+V immediately after pressing
Don't hold the keys down

Future Enhancements
Potential improvements for future versions:

Persistent stack (save across sessions)
Visual menu bar interface showing stack contents
Configurable keyboard shortcuts
Maximum stack size limit
Support for images and rich text
Stack search functionality

Development
Built as a learning project to explore:

Multi-threaded programming in Python
System-level integrations (clipboard, keyboard)
Event-driven architecture
macOS application development
