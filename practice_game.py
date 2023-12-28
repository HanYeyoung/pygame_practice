import random
import pygame
############################################################
# Basic Initialization
pygame.init()

# Set Screen Size
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# Screen Title
pygame.display.set_caption("POO")

# FPS
clock = pygame.time.Clock()
############################################################

# 1. User Game Initialization (Background, Game Image, Coordinate, Speed, Font, etc)

background = pygame.image.load("/Users/yeyounghan/Desktop/pygame_basic/background.png")
character = pygame.image.load("/Users/yeyounghan/Desktop/pygame_basic/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

to_x = 0
character_speed = 10

poo = pygame.image.load("/Users/yeyounghan/Desktop/pygame_basic/enemy.png")
poo_size = poo.get_rect().size
poo_width = poo_size[0]
poo_height = poo_size[1]
poo_x_pos = random.randint(0, screen_width - poo_width)
poo_y_pos = 0
poo_speed = 10

running = True
while running:
    dt = clock.tick(30)

    # 2. Event Handling (Keyboard, Mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_LEFT:
                to_x -= character_speed
            elif event.type == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 3. Game Character Location
    character_x_pos += to_x * dt

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    poo_y_pos += poo_speed

    if poo_y_pos > screen_height:
        poo_y_pos = 0
        poo_x_pos = random.randint(0, screen_width - poo_width)

    # 4. Collision Handling
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    poo_rect = poo.get_rect()
    poo_rect.left = poo_x_pos
    poo_rect.top = poo_y_pos

    if character_rect.colliderect(poo_rect):
        print("Collided")
        running = False

    # 5. Display
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(poo, (poo_x_pos, poo_y_pos))

    pygame.display.update()

pygame.quit()