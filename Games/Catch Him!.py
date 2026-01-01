import pygame
import random
import math

# Inisialisasi Pygame
pygame.init()

# --- KONSTANTA & PENGATURAN DASAR ---
GRID_WIDTH, GRID_HEIGHT = 15, 11
TILE_SIZE = 50
UI_WIDTH = 300
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE + UI_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
FPS = 60
ANIMATION_SPEED = 8

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (30, 30, 30)

# Pengaturan Layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch Him!")
clock = pygame.time.Clock()

# --- FUNGSI LOAD FONT EMOJI ---
def load_emoji_font(size=24):
    candidates = ["Segoe UI Emoji", "Noto Color Emoji", "Apple Color Emoji", "Twemoji Mozilla"]
    for name in candidates:
        try:
            return pygame.font.SysFont(name, size)
        except:
            continue
    return pygame.font.SysFont("Consolas", size)  # fallback

# Font UI
font = load_emoji_font(24)
# Font Popup lebih besar
popup_font = load_emoji_font(48)

# --- POPUP (non-blocking dengan fade-out) ---
popup_message = ""
popup_end_time = 0
popup_duration = 1500  # ms

def show_popup(message, duration=1500):
    global popup_message, popup_end_time, popup_duration
    popup_message = message
    popup_end_time = pygame.time.get_ticks() + duration
    popup_duration = duration

def draw_popup():
    if pygame.time.get_ticks() < popup_end_time and popup_message:
        now = pygame.time.get_ticks()
        remaining = popup_end_time - now
        alpha = max(0, min(255, int(255 * remaining / popup_duration)))

        text_surface = popup_font.render(popup_message, True, YELLOW)
        text_surface = text_surface.convert_alpha()
        text_surface.set_alpha(alpha)

        center_x = UI_WIDTH + (GRID_WIDTH * TILE_SIZE) // 2
        center_y = SCREEN_HEIGHT // 2
        rect = text_surface.get_rect(center=(center_x, center_y))
        screen.blit(text_surface, rect)

# --- FUNGSI BANTU ---
def is_path_clear(start_pos, end_pos, obstacles):
    x1, y1 = start_pos
    x2, y2 = end_pos
    if x1 == x2:
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            if (x1, y) in obstacles:
                return False
    elif y1 == y2:
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            if (x, y1) in obstacles:
                return False
    if end_pos in obstacles:
        return False
    return True

# --- KELAS KARAKTER ---
class Character:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.pixel_x = self.x * TILE_SIZE
        self.pixel_y = self.y * TILE_SIZE
        self.color = color

    def draw(self, surface):
        center_x = self.pixel_x + TILE_SIZE // 2
        center_y = self.pixel_y + TILE_SIZE // 2
        pygame.draw.circle(surface, self.color, (center_x, center_y), TILE_SIZE // 2 - 5)

    def set_target(self, target_x, target_y):
        self.x = target_x
        self.y = target_y

class Police(Character):
    def __init__(self, x, y):
        super().__init__(x, y, BLUE)
        self.bombs = 3
        self.steps = 3

    def use_bomb(self, obstacles, destroyed_obstacles):
        if self.bombs > 0:
            self.bombs -= 1
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx==0 and dy==0:
                        continue
                    check_x, check_y = self.x + dx, self.y + dy
                    if (check_x, check_y) in obstacles:
                        destroyed_obstacles[(check_x, check_y)] = pygame.time.get_ticks()

class Robber(Character):
    def __init__(self, x, y):
        super().__init__(x, y, RED)

    def find_best_move(self, police, obstacles, robbers, max_steps=4):
        best_move_target = None
        max_dist = -1
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for dx, dy in directions:
            for steps in range(1, max_steps+1):
                target_x = self.x + dx*steps
                target_y = self.y + dy*steps
                if 0<=target_x<GRID_WIDTH and 0<=target_y<GRID_HEIGHT:
                    if is_path_clear((self.x,self.y),(target_x,target_y),obstacles):
                        occupied = any(r.x==target_x and r.y==target_y for r in robbers if r is not self)
                        if not occupied:
                            dist = math.hypot(target_x - police.x, target_y - police.y)
                            if dist > max_dist:
                                max_dist = dist
                                best_move_target = (target_x, target_y)
        return best_move_target

# --- FUNGSI GAME ---
def generate_level(level, current_bombs=3):
    obstacles = set()
    num_obstacles = min(35 + level*8, (GRID_WIDTH*GRID_HEIGHT)//2)
    for _ in range(num_obstacles):
        obstacles.add((random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)))

    def get_valid_spawn(existing_pos):
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in obstacles and pos not in existing_pos:
                return pos

    occupied_positions = set()
    police_pos = get_valid_spawn(occupied_positions)
    police = Police(police_pos[0], police_pos[1])
    police.bombs = current_bombs
    occupied_positions.add(police_pos)

    robbers = []
    num_robbers = min(1 + level, 8)
    for _ in range(num_robbers):
        robber_pos = get_valid_spawn(occupied_positions)
        robbers.append(Robber(robber_pos[0], robber_pos[1]))
        occupied_positions.add(robber_pos)
    
    return police, robbers, obstacles

def draw_game_state(police, robbers, obstacles, destroyed_obstacles):
    screen.fill(DARK_GRAY, (0,0,UI_WIDTH,SCREEN_HEIGHT))
    screen.fill(BLACK, (UI_WIDTH,0,GRID_WIDTH*TILE_SIZE, SCREEN_HEIGHT))

    for x in range(GRID_WIDTH+1):
        pygame.draw.line(screen, GRAY, (UI_WIDTH+x*TILE_SIZE,0), (UI_WIDTH+x*TILE_SIZE,SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT+1):
        pygame.draw.line(screen, GRAY, (UI_WIDTH, y*TILE_SIZE), (UI_WIDTH+GRID_WIDTH*TILE_SIZE, y*TILE_SIZE))

    now = pygame.time.get_ticks()
    to_remove = []
    for (ox,oy) in obstacles:
        rect = pygame.Rect(UI_WIDTH+ox*TILE_SIZE, oy*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if (ox,oy) in destroyed_obstacles:
            elapsed = now - destroyed_obstacles[(ox,oy)]
            if elapsed < 500:
                pygame.draw.rect(screen, YELLOW, rect)
            else:
                to_remove.append((ox,oy))
        else:
            pygame.draw.rect(screen, GREEN, rect)
    for pos in to_remove:
        obstacles.remove(pos)
        del destroyed_obstacles[pos]

    center_x = UI_WIDTH + police.pixel_x + TILE_SIZE//2
    center_y = police.pixel_y + TILE_SIZE//2
    pygame.draw.circle(screen, police.color, (center_x, center_y), TILE_SIZE//2-5)

    for robber in robbers:
        center_x = UI_WIDTH + robber.pixel_x + TILE_SIZE//2
        center_y = robber.pixel_y + TILE_SIZE//2
        pygame.draw.circle(screen, robber.color, (center_x, center_y), TILE_SIZE//2-5)

def draw_text(text, position, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_ui(police, robbers, level, turn, message=None):
    ui_rect = pygame.Rect(0,0,UI_WIDTH,SCREEN_HEIGHT)
    pygame.draw.rect(screen, (30,30,30), ui_rect)

    draw_text(f"Level 📈: {level}", (10,20))
    draw_text(f"Maling 🥷: {len(robbers)}", (10,60))
    draw_text(f"Bom 💣: {police.bombs}", (10,100))
    draw_text(f"Langkah 🚶‍➡️: {police.steps}", (10,140))
    draw_text("(1-5 + Arrow)", (10,170), GRAY)

    box_x = 10
    box_y = 210
    box_w = UI_WIDTH-20
    box_h = 40
    if turn=="POLICE":
        pygame.draw.rect(screen, BLUE, (box_x, box_y, box_w, box_h), border_radius=8)
        draw_text("Giliran: POLISI 👮", (box_x+10, box_y+8), WHITE)
    else:
        pygame.draw.rect(screen, RED, (box_x, box_y, box_w, box_h), border_radius=8)
        draw_text("Giliran: MALING 🥷", (box_x+10, box_y+8), WHITE)

# --- GAME LOOP ---
def main():
    running = True
    level = 1
    police, robbers, obstacles = generate_level(level)
    
    turn = 'POLICE'
    is_animating = False
    anim_char = None
    anim_target_pos = None
    robber_turn_index = 0
    destroyed_obstacles = {}

    while running:
        dt = clock.tick(FPS)/1000.0*ANIMATION_SPEED

        if not is_animating:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if turn=='POLICE' and event.type==pygame.KEYDOWN:
                    target_pos = None
                    if event.key in [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5]:
                        police.steps = int(event.unicode)
                    elif event.key == pygame.K_UP:
                        target_pos = (police.x, police.y - police.steps)
                        if target_pos[1] < 0:
                            target_pos = None
                            show_popup("Terhalang Batas Map")
                    elif event.key == pygame.K_DOWN:
                        target_pos = (police.x, police.y + police.steps)
                        if target_pos[1] >= GRID_HEIGHT:
                            target_pos = None
                            show_popup("Terhalang Batas Map")
                    elif event.key == pygame.K_LEFT:
                        target_pos = (police.x - police.steps, police.y)
                        if target_pos[0] < 0:
                            target_pos = None
                            show_popup("Terhalang Batas Map")
                    elif event.key == pygame.K_RIGHT:
                        target_pos = (police.x + police.steps, police.y)
                        if target_pos[0] >= GRID_WIDTH:
                            target_pos = None
                            show_popup("Terhalang Batas Map")

                    if target_pos and target_pos != (police.x, police.y):
                        if is_path_clear((police.x, police.y), target_pos, obstacles):
                            is_animating = True
                            anim_char = police
                            anim_target_pos = target_pos
                        else:
                            show_popup("Terhalang Tembok")
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and not target_pos:
                        pass
                    elif event.key == pygame.K_SPACE:
                        police.use_bomb(obstacles, destroyed_obstacles)
                        turn = 'ROBBER_THINKING'

        if turn=='ROBBER_THINKING' and not is_animating:
            if robber_turn_index < len(robbers):
                robber = robbers[robber_turn_index]
                target_pos = robber.find_best_move(police, obstacles, robbers)
                if target_pos:
                    is_animating = True
                    anim_char = robber
                    anim_target_pos = target_pos
                robber_turn_index += 1
            else:
                robber_turn_index = 0
                turn = 'POLICE'

        if is_animating:
            target_pixel_x = anim_target_pos[0]*TILE_SIZE
            target_pixel_y = anim_target_pos[1]*TILE_SIZE
            dx = target_pixel_x - anim_char.pixel_x
            dy = target_pixel_y - anim_char.pixel_y
            anim_char.pixel_x += dx*dt
            anim_char.pixel_y += dy*dt
            if abs(target_pixel_x - anim_char.pixel_x) < 1 and abs(target_pixel_y - anim_char.pixel_y) < 1:
                anim_char.pixel_x = target_pixel_x
                anim_char.pixel_y = target_pixel_y
                anim_char.set_target(anim_target_pos[0], anim_target_pos[1])
                is_animating = False
                if anim_char == police:
                    robbers = [r for r in robbers if not (r.x==police.x and r.y==police.y)]
                    turn = 'ROBBER_THINKING'
                if not robbers:
                    level += 1
                    police, robbers, obstacles = generate_level(level, current_bombs=3)
                    turn = 'POLICE'

        # --- DRAW ---
        draw_game_state(police, robbers, obstacles, destroyed_obstacles)
        draw_ui(police, robbers, level, turn)
        draw_popup()
        pygame.display.flip()

    pygame.quit()

if __name__=='__main__':
    main()