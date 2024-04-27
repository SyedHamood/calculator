import pygame
import sys
from Trignometric import maintrig
from derevitive import main  # Corrected import statement

# Initialize Pygame
pygame.init()

# Background color
background = (31, 37, 68)

# Highlight color
highlight_color = (100, 100, 100)

# Set the dimensions of the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Calculator')

# Load the icon
#icon = pygame.image.load(r'C:\Users\user\Downloads\image.png')
#pygame.display.set_icon(icon)

# Create a font object
font = pygame.font.SysFont(None, 48)

# Render the text
text = font.render('Calculator', True, (71, 79, 122))
text_rect = text.get_rect(center=(width // 2, 50))

# Define button properties
button_width, button_height = 200, 50
button_color = (129, 104, 157)
button_highlight = (100, 100, 100)  # Added highlight color
button1_text = font.render('Exit', True, (255, 255, 255))
button2_text = font.render('Unit circle', True, (255, 255, 255))
button3_text = font.render("Derivative", True, (255, 255, 255))
button1_rect = pygame.Rect(width // 2 - 110, height // 2 + 60, button_width, button_height)
button3_rect = pygame.Rect(width // 2 - 110, height // 2 - 60, button_width, button_height)
button2_rect = pygame.Rect(width // 2 - 110, height // 2, button_width, button_height)
button1_text_rect = button1_text.get_rect(center=button1_rect.center)
button2_text_rect = button2_text.get_rect(center=button2_rect.center)
button3_text_rect = button3_text.get_rect(center=button3_rect.center)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1_rect.collidepoint(event.pos):
                running = False  # Close the application
            if button2_rect.collidepoint(event.pos):
                maintrig()  # Open the grid window
            if button3_rect.collidepoint(event.pos):
                main()

    # Fill the screen with the background color
    screen.fill(background)

    # Check if the mouse is over the buttons and change color accordingly
    if button1_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_highlight, button1_rect)
    else:
        pygame.draw.rect(screen, button_color, button1_rect)

    if button2_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_highlight, button2_rect)
    else:
        pygame.draw.rect(screen, button_color, button2_rect)

    if button3_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_highlight, button3_rect)
    else:
        pygame.draw.rect(screen, button_color, button3_rect)

    # Blit the button text
    screen.blit(button1_text, button1_text_rect)
    screen.blit(button2_text, button2_text_rect)
    screen.blit(button3_text, button3_text_rect)

    # Blit the text
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
