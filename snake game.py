import pygame
import time
import random

# Window size
window_x = 720
window_y = 480

# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Defining snake default position
snake_position = [100, 50]

# Defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# Fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

# Setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# Initial score
score = 0

# Speed variables
initial_snake_speed = 10  # Initial speed of the snake
snake_speed = initial_snake_speed  # Current snake speed
speed_increment = 1  # Amount of speed increase
speed_increment_interval = 5  # Interval in which the speed increases (e.g., every 5 points)

# Obstacles
obstacles = [[200, 200, 20, 20],  # [x, y, width, height]
             [300, 300, 30, 30],
             [400, 400, 40, 40]
             ]  # Example obstacle positions


# Displaying Score function
def show_score(choice, color, font, size):
    # Creating font object score_font
    score_font = pygame.font.SysFont(font, size)
    # Create the display surface object score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
    # Create a rectangular object for the text surface object
    score_rect = score_surface.get_rect()
    # Displaying text
    game_window.blit(score_surface, score_rect)


# Game over function
def game_over():
    # Creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    # Creating a text surface on which text will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    # Create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()
    # Setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    # Blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    # After 2 seconds, quit the program
    time.sleep(2)
    pygame.quit()
    quit()


# Main Function
while True:
    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    for obstacle in obstacles:
        pygame.draw.rect(game_window, red,
                         pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if (
            snake_position[0] < 0
            or snake_position[0] > window_x - 10
            or snake_position[1] < 0
            or snake_position[1] > window_y - 10
    ):
        game_over()

    # Touching the snake body or obstacles
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    for obstacle in obstacles:
        if (
            snake_position[0] >= obstacle[0]
            and snake_position[0] < obstacle[0] + obstacle[2]
            and snake_position[1] >= obstacle[1]
            and snake_position[1] < obstacle[1] + obstacle[3]
        ):
            game_over()

    # displaying score continuously
    show_score(1, white, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
