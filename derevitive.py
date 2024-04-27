import math
import pygame
import sys
import pyautogui
import time
import sympy as sp


def render_text(screen, font, text, input_rect, all_taken):
    if not all_taken:
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=input_rect.center)
        screen.blit(text_surface, text_rect)


def get_input(screen, font, input_rect, all_taken):
    input_text = ''
    input_complete = False
    while not input_complete and not all_taken:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_complete = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        pygame.draw.rect(screen, (129 - 50, 104 - 50, 157 - 50), input_rect)
        render_text(screen, font, input_text, input_rect, all_taken)
        pygame.display.flip()
        pygame.time.delay(10)
    return input_text


def solve_quad(a, b, c):
    determ = b ** 2 - 4 * a * c
    if determ >= 0:
        ans1 = (-b + math.sqrt(determ)) / (2 * a)
        ans2 = (-b - math.sqrt(determ)) / (2 * a)
        return ans1, ans2
    else:
        return None


def vortex_point(a, b, c):
    h = float(-b / (2 * a))
    k = float((a * (h ** 2)) + (b * h) + c)
    return h, k


def graph_table(a, b, c, x_values, y_values):
    step = 0.1  
    for x in range(-100, 100):
        x_val = x * step
        y = a * x_val ** 2 + b * x_val + c
        x_values.append(round(x_val, 2))
        y_values.append(round(y, 2))
    return x_values, y_values


def graph_derivative_table(a, b, prime_x, prime_y):
    step = 0.1  
    for x in range(-100, 100):  
        x_val = x * step
        y = (a*x_val)+(b)
        prime_x.append(round(x_val, 2))
        prime_y.append(round(y, 2))
    return prime_x, prime_y


def draw_grid(screen, width, height):
    """Draw a grid with the origin in the center of the screen."""
    origin_x, origin_y = width // 2, height // 2

    for x in range(0, width, 20):
        font = pygame.font.Font(None, 20)
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, height))
        x_val = int((x - origin_x) / 20) 
        scale = font.render(str(x_val), True, (0, 0, 0))
        screen.blit(scale, (x + 3, origin_y + 15))
  
    for y in range(0, height, 20):
        font = pygame.font.Font(None, 20)
        pygame.draw.line(screen, (200, 200, 200), (0, y), (width, y))
        y_val = int((origin_y - y) / 20)
        scale = font.render(str(y_val), True, (0, 0, 0))
        screen.blit(scale, (origin_x + 3, y - 3))

    pygame.draw.line(screen, (255, 0, 0), (origin_x, 0), (origin_x, height), 2)
    pygame.draw.line(screen, (255, 0, 0), (0, origin_y), (width, origin_y), 2)

    return origin_x, origin_y


def plot_graph(screen, x_values, y_values, x_origin, y_origin, h, k, ans1, ans2,color):

    before_x, before_y = None, None


    pygame.draw.circle(screen, (255, 0, 0), (int(h), int(k)), 5)

    pygame.draw.circle(screen, (0, 255, 0), (int(ans1 * 20 + x_origin), y_origin), 5)
    pygame.draw.circle(screen, (0, 255, 0), (int(ans2 * 20 + x_origin), y_origin), 5)

   
    for x, y in zip(x_values, y_values):
        scaled_x = x * 20 + x_origin
        scaled_y = -y * 20 + y_origin
        pygame.draw.circle(screen, (0, 0, 0), (int(scaled_x), int(scaled_y)), 0, 0)
        if before_x is not None and before_y is not None:
            pygame.draw.aaline(screen, (color), (before_x, before_y), (scaled_x, scaled_y))
        before_x, before_y = scaled_x, scaled_y 
    pygame.display.flip()
    time.sleep(0.0)


def find_derv(a, b, c):
    x = sp.Symbol('x')

    f = (a * (x ** 2)) + (b * x) + (c * 1)

    f_prime = sp.diff(f, x)

    coefficients = f_prime.as_coefficients_dict()
    prime_a = int(coefficients[x])
    prime_b = int(coefficients[1])

    print("Original function:", f)
    print("Derivative:", f_prime)
    print(prime_a,',',prime_b)

    return f_prime, prime_a, prime_b


def main():
    a = 0
    b = 0
    c = 0
    ans1 = 0
    ans2 = 0
    x_values = []
    y_values = []
    prime_x = []
    prime_y = []
    a_taken = False
    b_taken = False
    c_taken = False
    all_taken = False
    white = (255, 255, 255)

    pygame.init()
    width, height = pyautogui.size()
    width -= 200
    height -= 200

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("calculator")
    font = pygame.font.Font(None, 32)
    font2 = pygame.font.Font(None, 52)

    input_box_width = 200
    total_width = input_box_width * 3
    start_x = (width - total_width) / 2

    input_a = pygame.Rect(start_x - 200, height / 2, input_box_width, 32)
    input_b = pygame.Rect(start_x + input_box_width, height / 2, input_box_width, 32)
    input_c = pygame.Rect(start_x + 200 + 2 * input_box_width, height / 2, input_box_width, 32)

    input_text = ''

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not all_taken:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    if input_a.collidepoint(x, y) and not a_taken:
                        input_text = get_input(screen, font, input_a, all_taken)
                        a = int(input_text)
                        a_taken = True
                    if input_b.collidepoint(x, y) and not b_taken:
                        input_text = get_input(screen, font, input_b, all_taken)
                        b = int(input_text)
                        b_taken = True
                    if input_c.collidepoint(x, y) and not c_taken:
                        input_text = get_input(screen, font, input_c, all_taken)
                        c = int(input_text)
                        c_taken = True
                    if a_taken and b_taken and c_taken:
                        all_taken = True

        screen.fill((31, 37, 68))  
        if not all_taken:
            pygame.draw.rect(screen, (129, 104, 157), input_a)
            pygame.draw.rect(screen, (129, 104, 157), input_b)
            pygame.draw.rect(screen, (129, 104, 157), input_c)

            # text
            text_a = font.render("A: ", True, (255, 255, 255))
            text_b = font.render("B: ", True, (255, 255, 255))
            text_c = font.render("C: ", True, (255, 255, 255))
            text_a1 = font2.render("x² ", True, (255, 255, 255))
            text_b1 = font2.render("x ", True, (255, 255, 255))
            text_d = font2.render('Derevetives ', True, (71, 79, 122))
            text_e = font2.render('Enter Quadratic Equation:  ', True, (71, 79, 122))
            screen.blit(text_a, (input_a.x - 30, input_a.y + 10))
            screen.blit(text_b, (input_b.x - 30, input_b.y + 10))
            screen.blit(text_c, (input_c.x - 30, input_c.y + 10))
            screen.blit(text_d, (input_b.x , 170))
            screen.blit(text_e, (input_b.x - 80, 300))
            screen.blit(text_a1, (input_a.x + 210, input_a.y + 0))
            screen.blit(text_b1, (input_b.x + 210, input_b.y + 0))

            text_at_a = font.render(str(a), True, (255, 255, 255))
            text_at_b = font.render(str(b), True, (255, 255, 255))
            text_at_c = font.render(str(c), True, (255, 255, 255))
            screen.blit(text_at_a, (input_a.x + 100, input_a.y + 5))
            screen.blit(text_at_b, (input_b.x + 100, input_b.y + 5))
            screen.blit(text_at_c, (input_c.x + 100, input_c.y + 5))

        if all_taken:
            screen.fill(white)
            x_origin, y_origin = draw_grid(screen, width, height)

        
        pygame.display.flip()
        
        if a != 0 and b != 0 and c != 0:
            try:
                ans1, ans2 = solve_quad(a, b, c)
            except TypeError:
                no_text = font.render('NO SOLUTION',True,(71-50, 79-50, 122-50))
                screen.blit(no_text,(width-400,height-90))
            h, k = vortex_point(a, b, c)
            f_prime, prime_a, prime_b = find_derv(a, b, c)
            x_values, y_values = graph_table(a, b, c, x_values, y_values)
            prime_x, prime_y = graph_derivative_table(prime_a, prime_b, prime_x, prime_y)
            eq_text = font.render(f'Original equation: {a}x² + {b}x + {c}',True,(0,0,0))
            prime_text = font.render(f'Derevitive: {f_prime}',True,(255,100,0))
            screen.blit(eq_text,(width-400,height-60))
            screen.blit(prime_text,(width-400,height-30))
            count = 19
            count += 1
            if count <= 20:
                plot_graph(screen, x_values, y_values, x_origin, y_origin, h, k, ans1, ans2,(0,0,0))
                plot_graph(screen,prime_x,prime_y,x_origin,y_origin,0,0,0,0,(255,100,0))
            
    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
