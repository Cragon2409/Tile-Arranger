import multiprocessing

import easygui

def open_file_dialog(queue):
    """Process function to open a file dialog."""
    selected_file = easygui.fileopenbox()
    if selected_file:
        queue.put(selected_file)  # Pass the selected file back to the main process
    else:
        queue.put(None)  # Signal that the user canceled the dialog

# Function to start the file dialog process
def start_file_dialog():
    queue = multiprocessing.Queue()  # For communication between processes
    process = multiprocessing.Process(target=open_file_dialog, args=(queue,))
    process.start()
    return process, queue
