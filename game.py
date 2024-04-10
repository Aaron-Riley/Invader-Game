import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 10
OBJECT_WIDTH, OBJECT_HEIGHT = 20, 20
PLAYER_SPEED = 5
BASE_OBJECT_SPEED = 2
RED_OBJECT_SPEED = 3
MAX_OBJECT_SPEED = 8
OBJECT_COUNT = 5
RED_OBJECT_PROBABILITY = 0.1
LIVES = 3

# Power-up settings
POWER_UP_PROBABILITY = 0.02
POWER_UP_DURATION = 300
POWER_UP_SPEED_BOOST = 2

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Objects")

# Player
player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

# Initialize game variables
objects = [[random.randint(0, WIDTH - OBJECT_WIDTH), 0, OBJECT_WIDTH, OBJECT_HEIGHT, BASE_OBJECT_SPEED] for _ in range(OBJECT_COUNT)]
score = 0
speed_increase_interval = 20
speed_increase_counter = 0
lives = LIVES

# Power-up
power_up = None
power_up_active = False
power_up_timer = 0

# Game state
game_over = False

# Clock
clock = pygame.time.Clock()

def display_game_over():
    game_over_font = pygame.font.Font(None, 36)
    game_over_text = game_over_font.render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

def reset_game():
    global player, objects, score, speed_increase_interval, speed_increase_counter, lives, power_up, power_up_active, power_up_timer, game_over
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    objects = [[random.randint(0, WIDTH - OBJECT_WIDTH), 0, OBJECT_WIDTH, OBJECT_HEIGHT, BASE_OBJECT_SPEED] for _ in range(OBJECT_COUNT)]
    score = 0
    speed_increase_interval = 20
    speed_increase_counter = 0
    lives = LIVES
    power_up = None
    power_up_active = False
    power_up_timer = 0
    game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        # Move and update objects
        for obj in objects:
            if obj[1] >= HEIGHT:
                obj[0] = random.randint(0, WIDTH - OBJECT_WIDTH)
                obj[1] = 0
                obj[4] = RED_OBJECT_SPEED if random.random() < RED_OBJECT_PROBABILITY else BASE_OBJECT_SPEED

            obj[1] += obj[4]
            obj_rect = pygame.Rect(obj[0], obj[1], obj[2], obj[3])
            if obj_rect.colliderect(player):
                if obj[4] == RED_OBJECT_SPEED:
                    lives -= 1  # Decrease lives when the player hits a red block
                    if lives <= 0:
                        game_over = True
                        display_game_over()
                    else:
                        obj[0] = random.randint(0, WIDTH - OBJECT_WIDTH)
                        obj[1] = 0
                        obj[4] = BASE_OBJECT_SPEED
                else:
                    obj[0] = random.randint(0, WIDTH - OBJECT_WIDTH)
                    obj[1] = 0
                    obj[4] = BASE_OBJECT_SPEED
                    score += 1

        # Handle power-up
        if power_up is None and random.random() < POWER_UP_PROBABILITY:
            power_up = [random.randint(0, WIDTH - OBJECT_WIDTH), 0]

        if power_up:
            power_up[1] += BASE_OBJECT_SPEED
            power_up_rect = pygame.Rect(power_up[0], power_up[1], OBJECT_WIDTH, OBJECT_HEIGHT)
            if power_up_rect.colliderect(player):
                power_up_active = True
                power_up_timer = POWER_UP_DURATION
                power_up = None

        if power_up_active:
            power_up_timer -= 1
            if power_up_timer <= 0:
                power_up_active = False

        # Increase object speed after a certain number of points
        speed_increase_counter += 1
        if speed_increase_counter >= speed_increase_interval:
            BASE_OBJECT_SPEED = min(BASE_OBJECT_SPEED + 1, MAX_OBJECT_SPEED)
            RED_OBJECT_SPEED = min(RED_OBJECT_SPEED + 1, MAX_OBJECT_SPEED)
            speed_increase_counter = 0

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    for obj in objects:
        if obj[4] == RED_OBJECT_SPEED:
            pygame.draw.rect(screen, RED, pygame.Rect(obj[0], obj[1], obj[2], obj[3]))
        else:
            pygame.draw.rect(screen, BLUE, pygame.Rect(obj[0], obj[1], obj[2], obj[3]))
        if power_up_active:
            pygame.draw.rect(screen, GREEN, pygame.Rect(player.x, player.y, player.width, player.height))

    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 FPS

    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
