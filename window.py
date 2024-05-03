import pygame
import sys

class GameWindow:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.DISPLAYSURF = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.game = None
        self.back_button_rect = None
        self.viewing_records = False  # Initialize viewing_records flag

    
    
    def view_records(self):


        with open('records.txt', 'r') as f:
            records = f.readlines()
        self.DISPLAYSURF.fill((255, 255, 255))
        font = pygame.font.Font(None, 50)
        # Load background image
        records_background = pygame.image.load("./images/nen.png")
        records_background = pygame.transform.scale(records_background, (self.WIDTH, self.HEIGHT))
        self.DISPLAYSURF.blit(records_background, (0, 0))
        
        # Display "Game Records" text
        title_text = font.render("Game Records", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 30))
        self.DISPLAYSURF.blit(title_text, title_rect)
        
        y_offset = 50
        for i, record in enumerate(records):
            text = font.render(f"{i+1}. {record.strip()}", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 8 + y_offset))
            self.DISPLAYSURF.blit(text, text_rect)
            y_offset += 30
        back_button_text = font.render("Back to Main Menu", True, (0, 0, 0))
        self.back_button_rect = back_button_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 50))
        pygame.draw.rect(self.DISPLAYSURF, (0, 255, 0), self.back_button_rect, border_radius=10)
        self.DISPLAYSURF.blit(back_button_text, self.back_button_rect)
        pygame.display.flip()
        self.viewing_records = True  # Set viewing_records flag to True



    def handle_start_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    button_x = (self.WIDTH - 200) // 2
                    start_button_y = (self.HEIGHT - (50 * 3 + 30 * 2)) // 2
                    continue_button_y = start_button_y + 50 + 30
                    view_records_button_y = continue_button_y + 50 + 30
                    exit_button_y = view_records_button_y + 50 + 30
                    if not self.viewing_records:  # Check if not viewing records
                        if button_x <= mouse_pos[0] <= button_x + 200:
                            if start_button_y <= mouse_pos[1] <= start_button_y + 50:
                                self.game.reset()
                                self.game.run_game()
                                running = False
                            elif continue_button_y <= mouse_pos[1] <= continue_button_y + 50:
                                self.game.run_game()
                                running = False
                            elif view_records_button_y <= mouse_pos[1] <= view_records_button_y + 50:
                                self.view_records()
                            elif exit_button_y <= mouse_pos[1] <= exit_button_y + 50:
                                pygame.quit()
                                sys.exit()
                    else:  # If viewing records
                        if self.back_button_rect.collidepoint(mouse_pos):
                            self.draw_start_menu()  # Return to the main menu
                            self.viewing_records = False  # Reset viewing_records flag


    def draw_start_menu(self):
        self.DISPLAYSURF.fill((255, 255, 255))

        # Load images
        start_menu_frame = pygame.image.load("./images/Untitled design.png")
        start_image = pygame.image.load("./images/nen.png")
        continue_image = pygame.image.load("./images/nen.png")
        view_records_image = pygame.image.load("./images/nen.png")  
        save_image = pygame.image.load("./images/nen.png")
        intro_background = pygame.image.load("./images/nen.png")

        # Scale images
        screen_width, screen_height = pygame.display.get_surface().get_size()
        start_menu_frame = pygame.transform.scale(start_menu_frame, (screen_width, screen_height))
        button_width = screen_width * 0.25  # Use relative value for the width of the buttons
        button_height = 50  # Height of the buttons
        start_image = pygame.transform.scale(start_image, (int(button_width), button_height))
        continue_image = pygame.transform.scale(continue_image, (int(button_width), button_height))
        view_records_image = pygame.transform.scale(view_records_image, (int(button_width), button_height))  # Scale image for the "View Records" button
        save_image = pygame.transform.scale(save_image, (int(button_width), button_height))
        intro_background = pygame.transform.scale(intro_background, (500, 100))

        # Blit images onto the display surface
        self.DISPLAYSURF.blit(start_menu_frame, start_menu_frame.get_rect(center=(screen_width // 2, screen_height // 2 + 30)))
        self.DISPLAYSURF.blit(start_image, start_image.get_rect(center=(screen_width // 2, 230)))
        self.DISPLAYSURF.blit(continue_image, continue_image.get_rect(center=(screen_width // 2, 310)))
        self.DISPLAYSURF.blit(view_records_image, view_records_image.get_rect(center=(screen_width // 2, 390)))  # Blit image for the "View Records" button
        self.DISPLAYSURF.blit(save_image, save_image.get_rect(center=(screen_width // 2, 470)))  # Shift the "Exit and Save" button down
        self.DISPLAYSURF.blit(intro_background, intro_background.get_rect(center=(screen_width // 2, 100)))

        # Render text
        font = pygame.font.Font(None, 35)
        font_intro = pygame.font.Font(None, 60)
        text_start = font.render("New Game", True, (0, 0, 0))
        text_continue = font.render("Continue", True, (0, 0, 0))
        text_view_records = font.render("View Records", True, (0, 0, 0))  # Render text for the "View Records" button
        text_save = font.render("Exit ", True, (0, 0, 0))
        intro_text = font_intro.render("Game Minesweeper", True, (0, 0, 0))

        # Blit text onto the display surface
        self.DISPLAYSURF.blit(text_start, text_start.get_rect(center=(screen_width // 2, 230)))
        self.DISPLAYSURF.blit(text_continue, text_continue.get_rect(center=(screen_width // 2, 310)))
        self.DISPLAYSURF.blit(text_view_records, text_view_records.get_rect(center=(screen_width // 2, 390)))  # Blit text for the "View Records" button
        self.DISPLAYSURF.blit(text_save, text_save.get_rect(center=(screen_width // 2, 470)))  # Shift the text of the "Exit and Save" button down
        self.DISPLAYSURF.blit(intro_text, intro_text.get_rect(center=(screen_width // 2, 100)))

        pygame.display.flip()
