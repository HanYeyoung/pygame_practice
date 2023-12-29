import pygame
import os

##############################################################
# Basic Initialization
pygame.init()

# Set Screen Size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set Screen Title
pygame.display.set_caption("Dog Pang Game")

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. User Game Initialization (Background, Game Image, Coordinate, Speed, Font, etc)
current_path = os.path.dirname(__file__)  # current file's location
image_path = os.path.join(current_path, "images")  # images folder location

# background setup
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage setup
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# character setup
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

# character moving direction
character_to_x = 0

# character moving speed
character_speed = 5

# weapon setup
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# weapon can be used multiple times at a time
weapons = []

# weapon moving speed
weapon_speed = 10

# ball setup
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# initial speed based on weapon size
ball_speed_y = [-18, -15, -12, -9]
balls = []

# add ball that is made when the game starts
balls.append({
    "pos_x": 50,
    "pos_y": 50,
    "img_index": 0,
    "to_x": 3,
    "to_y": -6,
    "init_speed_y": ball_speed_y[0]
})

weapon_to_remove = -1
ball_to_remove = -1

# font

game_font = pygame.font.SysFont('Comic Sans', 28)
total_time = 10
start_ticks = pygame.time.get_ticks()


# Game result message / Time Over, Mission Complete, Game Over
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)

    # 2. Event Handling (Keyboard, Mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # character to left
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  # character to right
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # use weapon
                weapon_x_pos = character_x_pos + \
                    (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. Game Character Location
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # Weapon location setup
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140. ...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  # have weapon to go up

    # Remove weapon that reached top
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # Ball location
    for ball_index, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_index = ball_val["img_index"]

        ball_size = ball_images[ball_img_index].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # Bounce effect on horizontal wall
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # Vertical location
        # Bounce stage
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]
        else:  # Increase speed
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. Collision Handling

    # Character rect information update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_index, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_index = ball_val["img_index"]

        # Ball rect information update
        ball_rect = ball_images[ball_img_index].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # Check for collision
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # Collision Handling
        for weapon_index, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # Weapon rect information update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # Check for collision
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_index  # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_index # 해당 공 없애기 위한 값 설정

                # if the ball is not the smallest, divide to the next smaller size
                if ball_img_index < 3:
                    # Current ball size info
                    ball_width = ball_rect.size[0]
                    ball_heigth = ball_rect.size[1]

                    # Divided ball info
                    small_ball_rect = ball_images[ball_img_index + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # bounce to left
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_index": ball_img_index + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_speed_y": ball_speed_y[ball_img_index + 1]
                    })

                    # bounce to right
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_index": ball_img_index + 1,  # 공의 이미지 인덱스
                        "to_x": 3,
                        "to_y": -6,
                        "init_speed_y": ball_speed_y[ball_img_index + 1]
                    })
                break
        else:  # continue game
            continue  # 안쪽 for 문 조건이 맞지 않으면 continue. 바깥 for 문 계쏙 수행
        break  # 안쪽 for 문에서 break를 만나면 여기로 진입 가능. 이중 for문 한번에 탈출

    # Remove collided ball/weapon
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # if success (no ball left)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. Display
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for index, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_index = val["img_index"]
        screen.blit(ball_images[ball_img_index], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # Calculate elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(
        int(total_time - elapsed_time)), True, (255, 255, 0))
    screen.blit(timer, (10, 10))

    # if time is over
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False
    pygame.display.update()

# save game over message
msg = game_font.render(game_result, True, (255, 0, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# wait 2 seconds before exiting the game
pygame.time.delay(2000)

# quit pygame
pygame.quit()