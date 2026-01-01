import pygame
import math
import random

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Shooter")
clock = pygame.time.Clock()

# --- COLORS (NEON PALETTE) ---
BG_COLOR = (10, 10, 20)
NEON_CYAN = (0, 255, 255)
NEON_RED = (255, 50, 50)
NEON_GREEN = (50, 255, 50)
NEON_YELLOW = (255, 255, 100)
WHITE = (255, 255, 255)

# --- HELPER FUNCTIONS ---
def draw_glow_circle(surf, color, pos, radius, glow_radius):
    if radius <= 0 or glow_radius <= 0: return # Safety check
    
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*color, 50), (glow_radius, glow_radius), glow_radius)
    surf.blit(glow_surf, (pos[0] - glow_radius, pos[1] - glow_radius))
    pygame.draw.circle(surf, color, pos, radius)

# --- CLASSES ---

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 6.28)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 255
        self.size = random.randint(3, 6) # Sedikit diperbesar agar aman

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 10
        self.size -= 0.1
        
        # PERBAIKAN: Jika size <= 0, matikan partikel
        if self.size <= 0:
            self.life = 0

    def draw(self, screen):
        # PERBAIKAN: Cek size > 0
        if self.life > 0 and self.size > 0:
            # Cast size ke int agar valid untuk Surface
            draw_size = int(self.size)
            if draw_size > 0:
                s = pygame.Surface((draw_size * 2, draw_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, self.life), (draw_size, draw_size), draw_size)
                screen.blit(s, (self.x - draw_size, self.y - draw_size))

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 2)
        self.size = random.uniform(1, 2)
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            
    def draw(self, screen):
        pygame.draw.circle(screen, (100, 100, 150), (int(self.x), int(self.y)), int(self.size))

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 20
        self.speed = 5
        self.health = 100
        self.max_health = 100
        
    def move(self, keys):
        if keys[pygame.K_w] and self.y > self.size: self.y -= self.speed
        if keys[pygame.K_s] and self.y < HEIGHT - self.size: self.y += self.speed
        if keys[pygame.K_a] and self.x > self.size: self.x -= self.speed
        if keys[pygame.K_d] and self.x < WIDTH - self.size: self.x += self.speed
    
    def draw(self, screen, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        angle = math.atan2(dy, dx)
        
        tip = (self.x + math.cos(angle) * self.size, self.y + math.sin(angle) * self.size)
        left = (self.x + math.cos(angle + 2.5) * self.size, self.y + math.sin(angle + 2.5) * self.size)
        right = (self.x + math.cos(angle - 2.5) * self.size, self.y + math.sin(angle - 2.5) * self.size)
        
        pygame.draw.polygon(screen, NEON_GREEN, [tip, left, right], 2)
        pygame.draw.polygon(screen, (0, 100, 0), [tip, left, right], 0)

    def get_pos(self):
        return (self.x, self.y)

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x, self.y = x, y
        self.size = 4
        self.speed = 12
        self.trail = []
        
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0: dist = 1
        
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed
        
    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
            
        self.x += self.vx
        self.y += self.vy
        
    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, NEON_YELLOW, False, self.trail, 2)
        draw_glow_circle(screen, NEON_YELLOW, (int(self.x), int(self.y)), self.size, self.size + 4)

    def is_off_screen(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT
    
    def get_pos(self):
        return (self.x, self.y)

class Enemy:
    def __init__(self):
        side = random.randint(0, 3)
        if side == 0: self.x, self.y = random.randint(0, WIDTH), -20
        elif side == 1: self.x, self.y = WIDTH + 20, random.randint(0, HEIGHT)
        elif side == 2: self.x, self.y = random.randint(0, WIDTH), HEIGHT + 20
        else: self.x, self.y = -20, random.randint(0, HEIGHT)
            
        self.size = 15
        self.speed = random.uniform(2, 4)
        self.health = 3
        self.pulse = 0
        
    def update(self, player_pos):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        
        self.pulse += 0.2

    def draw(self, screen):
        pulse_size = self.size + math.sin(self.pulse) * 2
        # Safety int conversion
        r = int(pulse_size)
        gr = int(pulse_size) + 5
        draw_glow_circle(screen, NEON_RED, (int(self.x), int(self.y)), r, gr)

    def get_pos(self): return (self.x, self.y)
    
    def collides_with(self, pos, size):
        dist = math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)
        return dist < self.size + size

# --- MAIN GAME ---
def main():
    player = Player()
    bullets = []
    enemies = []
    particles = []
    stars = [Star() for _ in range(50)]
    
    score = 0
    shake_timer = 0
    
    last_shot = 0
    shoot_cooldown = 150
    enemy_timer = 0
    
    running = True
    game_over = False
    
    font = pygame.font.SysFont("arial", 30, bold=True)
    
    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player = Player()
                bullets, enemies, particles = [], [], []
                score = 0
                game_over = False
        
        if not game_over:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_btn = pygame.mouse.get_pressed()
            
            player.move(keys)
            
            if mouse_btn[0] and current_time - last_shot > shoot_cooldown:
                bullets.append(Bullet(player.x, player.y, mouse_pos[0], mouse_pos[1]))
                last_shot = current_time
            
            if current_time - enemy_timer > 1000:
                enemies.append(Enemy())
                enemy_timer = current_time
                
            for star in stars: star.update()
            
            for b in bullets[:]:
                b.update()
                if b.is_off_screen(): bullets.remove(b)
            
            for p in particles[:]:
                p.update()
                if p.life <= 0: particles.remove(p)
                
            for e in enemies[:]:
                e.update(player.get_pos())
                
                if e.collides_with(player.get_pos(), player.size):
                    player.health -= 10
                    shake_timer = 10
                    enemies.remove(e)
                    for _ in range(10): 
                        particles.append(Particle(e.x, e.y, NEON_RED))
                    
                    if player.health <= 0: game_over = True
                
                for b in bullets[:]:
                    if e.collides_with(b.get_pos(), b.size):
                        e.health -= 1
                        bullets.remove(b)
                        for _ in range(3):
                            particles.append(Particle(e.x, e.y, NEON_YELLOW))
                        
                        if e.health <= 0:
                            if e in enemies: enemies.remove(e)
                            score += 10
                            for _ in range(15):
                                particles.append(Particle(e.x, e.y, NEON_RED))
                        break

        screen.fill(BG_COLOR)
        
        render_offset = [0, 0]
        if shake_timer > 0:
            shake_timer -= 1
            render_offset[0] = random.randint(-4, 4)
            render_offset[1] = random.randint(-4, 4)
        
        game_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        for star in stars: star.draw(game_surf)
        
        if not game_over:
            for p in particles: p.draw(game_surf)
            for b in bullets: b.draw(game_surf)
            for e in enemies: e.draw(game_surf)
            player.draw(game_surf, pygame.mouse.get_pos())
        
        screen.blit(game_surf, render_offset)
        
        # UI
        pygame.draw.rect(screen, (50, 50, 50), (10, 10, 200, 20))
        pygame.draw.rect(screen, NEON_GREEN if player.health > 30 else NEON_RED, (10, 10, player.health * 2, 20))
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)
        
        score_text = font.render(f"SCORE: {score}", True, NEON_CYAN)
        screen.blit(score_text, (10, 40))
        
        if game_over:
            over_text = font.render("GAME OVER", True, NEON_RED)
            restart_text = font.render("Press SPACE to Restart", True, WHITE)
            screen.blit(over_text, (WIDTH//2 - 80, HEIGHT//2 - 20))
            screen.blit(restart_text, (WIDTH//2 - 140, HEIGHT//2 + 20))
            
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()