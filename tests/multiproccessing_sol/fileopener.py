import easygui
import multiprocessing

def pick_file():
    # we don't want a full GUI, so keep the root window from appearing
    filename = easygui.fileopenbox()
    print("Selected",filename)
    exit() #exit once thread is complete

def open_thread():
    queue = multiprocessing.Queue()  # For communication between processes
    process = multiprocessing.Process(target=pick_file, args=(queue,))
    process.start()
    return process, queue