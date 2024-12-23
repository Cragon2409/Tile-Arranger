
# Initialize Pygame
if __name__ == "__main__":
    import pygame
    import import_open
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Image Selector")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


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
                            file_dialog_process, file_dialog_queue = import_open.start_file_dialog()

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
