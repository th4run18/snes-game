import pygame
import sys
import subprocess  # Import to run another Python file
from globalv import *
from main import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800


# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (50, 150, 255)

# Font settings
font = pygame.font.Font(None, 50)

# Button settings
# BUTTON_WIDTH = 200
# BUTTON_HEIGHT = 50
# button_start = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
# button_start.centerx = WIDTH//2
# button_start.centery = HEIGHT//2
# button_quit = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
# button_quit.centerx = WIDTH//2
# button_quit.centery = HEIGHT//2

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

button_start = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
button_start.centerx = WIDTH // 2
button_start.centery = HEIGHT // 2 - 60

button_quit = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
button_quit.centerx = WIDTH // 2
button_quit.centery = HEIGHT // 2 + 20

def draw_text(text, font, color, surface, button_type):
    """Render text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(button_type.centerx, button_type.centery))
    surface.blit(text_obj, text_rect)

def main_menu():
    """Displays the main menu."""
    while True:
        screen.fill(WHITE)  # Clear screen

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Change button color if hovered
        start_color = BLUE if button_start.collidepoint(mouse_pos) else GRAY
        quit_color = BLUE if button_quit.collidepoint(mouse_pos) else GRAY

        # Draw buttons
        pygame.draw.rect(screen, start_color, button_start)
        pygame.draw.rect(screen, quit_color, button_quit)

        # Draw button text
        draw_text("Start Game", font, WHITE, screen,button_type = button_start )
        draw_text("Quit", font, WHITE, screen, button_type= button_quit)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    screen.fill((0,0,0))
                    game = Game()
                    game.run() 
                    #pygame.quit()  # Close the menu before starting the game
                    #subprocess.run(["python", "main.py"]) 
                     # Run the actual game file
                    #sys.exit()
                if button_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Run the main menu
main_menu()