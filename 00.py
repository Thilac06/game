# this coding for flappy bird like game 



import pygame
import random

pygame.init()

# Window dimensions
WIDTH = 300
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

# Game variables
gravity = 0.25
bird_movement = 0
floor_x_pos = 0

# Load images
floor_surface = pygame.image.load("base.png") #add base image 
bg_surface = pygame.image.load("background-night.png").convert() # background image
bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))

bird_surface = pygame.image.load("chr2.png").convert_alpha() # add cj\haractor img
bird_surface = pygame.transform.scale(bird_surface, (80, 100))
bird_rect = bird_surface.get_rect(center=(100, HEIGHT / 3))

pipe_surface = pygame.image.load("pipe-green.png").convert_alpha()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_heights = [200, 300, 400]

game_font = pygame.font.Font("04B_03B_.TTF", 40) # add sutable font
score = 0
high_score = 0

# Function to draw the score
def draw_score():
    score_surface = game_font.render(str(score), True, WHITE)
    score_rect = score_surface.get_rect(center=(WIDTH / 2, 50))
    window.blit(score_surface, score_rect)

# Function to update the high score
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score

# Function to display the high score
def display_high_score():
    high_score_surface = game_font.render("High Score: " + str(high_score), True, WHITE)
    high_score_rect = high_score_surface.get_rect(center=(WIDTH / 2, HEIGHT - 50))
    window.blit(high_score_surface, high_score_rect)

# Function to draw the floor
def draw_floor():
    window.blit(floor_surface, (floor_x_pos, HEIGHT - 100))
    window.blit(floor_surface, (floor_x_pos + WIDTH, HEIGHT - 100))

# Function to create pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop=(WIDTH + 100, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(WIDTH + 100, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT - 100:
            window.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            window.blit(flipped_pipe, pipe)

# Function to check collision with pipes
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= -100 or bird_rect.bottom >= HEIGHT - 100:
        return True
    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    window.blit(bg_surface, (0, 0))

    bird_movement += gravity
    rotated_bird = pygame.transform.rotate(bird_surface, -bird_movement * 3)
    bird_rect.centery += bird_movement
    window.blit(rotated_bird, bird_rect)

    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    if check_collision(pipe_list):
        update_high_score()
        pipe_list = []
        bird_rect.centery = HEIGHT / 2
        bird_movement = 0
        score = 0

    if pipe_list:
        if pipe_list[0].centerx == bird_rect.centerx:
            score += 1

    floor_x_pos -= 1
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0
    draw_floor()
    draw_score()
    display_high_score()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
