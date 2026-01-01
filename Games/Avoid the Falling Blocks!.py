import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Falling Blocks!")

# Font for displaying text
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Clock to control the frame rate
clock = pygame.time.Clock()

# --- Game State Variables ---
def reset_game():
    global player_rect, enemies, score, enemy_speed, game_over
    
    # Player setup
    player_rect = pygame.Rect(
        (SCREEN_WIDTH - PLAYER_WIDTH) // 2, 
        SCREEN_HEIGHT - PLAYER_HEIGHT - 10, 
        PLAYER_WIDTH, 
        PLAYER_HEIGHT
    )
    
    # Enemy setup
    enemies = []
    enemy_speed = 5
    
    # Score and game state
    score = 0
    game_over = False

# Call reset_game() once to initialize variables at the start
reset_game()

# --- Main Game Loop ---
running = True
while running:
    # Set the frame rate
    clock.tick(60)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    # --- Game Logic (Only runs if the game is not over) ---
    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 7
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += 7
        # ADDED: Vertical movement
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= 7
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += 7

        # Add a new enemy randomly
        if random.randint(1, 20) == 1:
            enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemy_rect = pygame.Rect(enemy_x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
            enemies.append(enemy_rect)
        
        # Update enemy positions and check for collisions
        for enemy in enemies[:]: # Iterate over a copy
            enemy.y += enemy_speed
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
                score += 1
            
            if player_rect.colliderect(enemy):
                game_over = True
        
        # Increase difficulty
        if score > 0 and score % 10 == 0:
            enemy_speed = 5 + (score // 10)

    # --- Drawing ---
    screen.fill(BLACK) 

    if game_over:
        # Display Game Over screen
        game_over_text = font.render("Game Over!", True, RED)
        restart_text = small_font.render("Press 'R' to Restart", True, WHITE)
        final_score_text = small_font.render(f"Final Score: {score}", True, WHITE)
        
        screen.blit(game_over_text, (
            (SCREEN_WIDTH - game_over_text.get_width()) // 2, 
            SCREEN_HEIGHT // 2 - 50
        ))
        screen.blit(final_score_text, (
            (SCREEN_WIDTH - final_score_text.get_width()) // 2, 
            SCREEN_HEIGHT // 2
        ))
        screen.blit(restart_text, (
            (SCREEN_WIDTH - restart_text.get_width()) // 2, 
            SCREEN_HEIGHT // 2 + 50
        ))

    else:
        # Draw game elements during play
        pygame.draw.rect(screen, BLUE, player_rect)
        
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)
            
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()

# --- Quit the game ---
pygame.quit()
sys.exit()