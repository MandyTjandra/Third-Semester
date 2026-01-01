import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CIRCLE_LIFESPAN = 120  # How long a circle lasts in frames (2 seconds at 60 FPS)

# --- Initialize Pygame ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Colorful Fading Circles with Score")
clock = pygame.time.Clock()

# --- Game Variables ---
circles = []
score = 0
font = pygame.font.Font(None, 50)

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Create New Circles & Update Score ---
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        score += 1

        new_circle = {
            'pos': pos,
            'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
            'radius': random.randint(10, 40),
            'life': CIRCLE_LIFESPAN
        }
        circles.append(new_circle)

    # --- Update and Draw ---
    screen.fill((20, 20, 30))

    # Update and draw each circle
    for i in range(len(circles) - 1, -1, -1):
        circle = circles[i]
        circle['life'] -= 1

        if circle['life'] <= 0:
            circles.pop(i)
        else:
            radius = circle['radius']
            circle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                surface=circle_surf,
                color=circle['color'],
                center=(radius, radius),
                radius=radius
            )
            alpha = 255 * (circle['life'] / CIRCLE_LIFESPAN)
            circle_surf.set_alpha(alpha)
            screen.blit(circle_surf, (circle['pos'][0] - radius, circle['pos'][1] - radius))

    # --- Draw Score UI ---
    score_text = f"Score: {score}"
    text_surface = font.render(score_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    # --- Finalize Frame ---
    pygame.display.flip()
    clock.tick(60)

# --- Clean up and quit ---
pygame.quit()
