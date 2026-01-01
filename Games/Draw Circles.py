import pygame as py

# Initialize pygame
py.init()

# Set screen size and display
size = (500, 400)
screen = py.display.set_mode(size)
py.display.set_caption("Draw Circles")

# Set background color
screen.fill((0, 0, 0))

# Main loop
running = True
while running:
    for ev in py.event.get():
        if ev.type == py.QUIT:
            running = False
        elif ev.type == py.MOUSEBUTTONUP:
            pos = py.mouse.get_pos()
            col = (0, 255, 255)
            py.draw.circle(screen, col, pos, 20, 5)
            py.display.update()

# Quit pygame
py.quit()
