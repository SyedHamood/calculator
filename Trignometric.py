import pygame
import sys
import pyautogui as py
import math
import keyboard



# Initialize Pygame
def maintrig():
    pygame.init()

    # Set up the display
    width, height = py.size()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Draw Line Example")


    # Set up font
    font = pygame.font.Font(None, 50)
    color = (255, 255, 255)

    # List to store the previous positions of the circle
    circle_path = []

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if the left mouse button is pressed
        mouse = pygame.mouse.get_pressed()

        if mouse[0]:
            # Get the current mouse position
            x, y = py.position()

            # Convert mouse coordinates for drawing in Pygame window
            rx = int(-width/2 + x)
            ry = int(height/2 - y)

            # Calculate the normalized vector from the center of the circle to the mouse position
            dir_vector = pygame.Vector2(x - width/2, y - height/2)
            dir_vector.normalize_ip()

            # Scale the vector to the radius of the circle (200 pixels)
            scaled_vector = dir_vector * 200
            end_x = width/2 + scaled_vector.x
            end_y = height/2 + scaled_vector.y

            # Calculate side lengths
            line_opp = float(math.sqrt((end_y - height/2) ** 2 + (end_x - end_x) ** 2) / 200)
            line_adj = float(math.sqrt((end_x - width/2) ** 2 + (height/2 - height/2) ** 2) / 200)
            line_hyp = 1
            if rx < 0 and ry < 0:
                line_adj *= -1
                line_opp *= -1
            elif rx < 0:
                line_adj *= -1
            elif ry < 0:
                line_opp *= -1

            # Calculate ratios
            sine = float(line_opp / line_hyp)
            cos = float(line_adj / line_hyp)
            tan = float(line_opp / line_adj) if line_adj != 0 else "Infinite"
            calc_rad = math.asin(sine)
            angle = int(abs(math.degrees(calc_rad)))

            # Draw the lines and circles
            screen.fill((0, 0, 0))  # Clear the screen with a white background
            if rx >= 0 and ry >= 0:
                pygame.draw.rect(screen, (128 - 50, 128 - 50, 128 - 50), (width/2, 0, width/2, height/2))
            elif rx <= 0 and ry >= 0:
                pygame.draw.rect(screen, (128 - 50, 128 - 50, 128 - 50), (0, 0, width/2, height/2))
            elif rx <= 0 and ry <= 0:
                pygame.draw.rect(screen, (128 - 50, 128 - 50, 128 - 50), (0, height/2, width/2, height/2))
            else:
                pygame.draw.rect(screen, (128 - 50, 128 - 50, 128 - 50), (width/2, height/2, width/2, height/2))

            # Draw lines to represent the path of the last circle
            for i in range(1, len(circle_path)):
                if angle != 0 and keyboard.is_pressed('space'):
                    pygame.draw.aaline(screen, color, circle_path[i - 1], circle_path[i], 2)
                    pygame.draw.circle(screen, color, (angle * width/90, int((math.sin(angle) * 100) * 2) + height/2), 10, 2)
                else:
                    circle_path = []
            # Draw the current circle
            pygame.draw.aaline(screen, (255, 255, 0), (width/2, height/2), (end_x, end_y), 5)  # Hypotenuse
            pygame.draw.circle(screen, (255, 255, 255), (width/2, height/2), 200, 2)  # Circle
            pygame.draw.circle(screen, (255, 255, 255), (int(end_x), int(end_y)), 10, 2)  # End point marker
            pygame.draw.aaline(screen, (255, 127, 127), (int(end_x), int(end_y)), (int(end_x), height/2), 5)  # Opposite
            pygame.draw.aaline(screen, (255, 255, 255), (width/2, 0), (width/2, height), 2)  # Vertical axis
            pygame.draw.aaline(screen, (255, 255, 255), (0, height/2), (width, height/2), 2)  # Horizontal axis
            pygame.draw.aaline(screen, (0, 0, 255), (width/2, height/2), (int(end_x), height/2), 5)  # Adjacent

            # Append the current position to the circle path
            circle_path.append((angle * width/90, int((math.sin(angle) * 100) * 2) + height/2))

            # Render text
            text_adj = font.render(f'Adjacent: {line_adj:.2f}', True, (255, 255, 255))
            text_opp = font.render(f'Opposite: {line_opp:.2f}', True, (255, 255, 255))
            text_hyp = font.render(f'Hypotenuse: {line_hyp:.2f}', True, (255, 255, 255))
            text_sin = font.render(f'Sin(θ)= {sine:.2f}', True, (255, 255, 255))
            text_cos = font.render(f'Cos(θ)= {cos:.2f}', True, (255, 255, 255))
            text_tan = font.render(f'Tan(θ)= {tan}', True, (255, 255, 255))
            text_angle = font.render(f'{angle}°', True, (255, 255, 255))
            instruction = font.render('Hold "Space" to draw graph of sine' , True,(255,255,255))

            # Draw text on the screen
            screen.blit(instruction, (width/4, height - 100))
            screen.blit(text_adj, (10, 30))
            screen.blit(text_opp, (10, 100))
            screen.blit(text_hyp, (10, 170))
            screen.blit(text_sin, (width -400, 30))
            screen.blit(text_cos, (width -400, 100))
            screen.blit(text_tan, (width -400, 170))
            screen.blit(text_angle, (width/3, 100))

        pygame.display.flip()  # Update the display
        pygame.time.Clock().tick(60)  # Cap the frame rate

    # Quit Pygame
    pygame.quit()
    sys.exit()
