
import multiprocessing
import easygui
import time

# Initialize Pygame
if __name__ == "__main__":
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Image Selector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

# Main Pygame loop
if __name__ == "__main__":
    running = True
    menu_active = True
    file_dialog_process = None
    file_dialog_queue = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Terminate the file dialog process if running
                if file_dialog_process and file_dialog_process.is_alive():
                    file_dialog_process.terminate()
                    file_dialog_process.join()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Simulate menu navigation
                    menu_active = not menu_active
                    print(f"Menu active: {menu_active}")
                    if not menu_active and file_dialog_process and file_dialog_process.is_alive():
                        file_dialog_process.terminate()
                        file_dialog_process.join()
                elif event.key == pygame.K_f:  # Start file dialog
                    if menu_active and not file_dialog_process:
                        file_dialog_process, file_dialog_queue = start_file_dialog()

        # Check if the file dialog process completed
        if file_dialog_process and not file_dialog_process.is_alive():
            if not file_dialog_queue.empty():
                selected_file = file_dialog_queue.get()
                if selected_file:
                    print(f"Selected file: {selected_file}")
                else:
                    print("File dialog canceled.")
            file_dialog_process = None  # Reset the process

        # Draw screen
        screen.fill(WHITE if menu_active else BLACK)
        pygame.display.flip()

    pygame.quit()
