import pygame
import random
from src.wator.fish import Fish
from src.wator.planet import Planet


window_width = 400
window_height = 300

cell_size = 20
cols = window_width // cell_size
rows = window_height // cell_size

num_fish = 20 

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Wa-Tor Grid - Initial and After Move")


planet = Planet(cols, rows)
fish_list = []

positions = [(x, y) for x in range(cols) for y in range(rows)]
random.shuffle(positions)

for i in range(num_fish):
    if not positions:
        break
    x, y = positions.pop()
    fish = Fish(x, y)
    planet.add(fish, x, y)
    fish_list.append(fish)


def draw_grid():
    screen.fill((255, 255, 255))
    for x in range(cols):
        for y in range(rows):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            entity = planet.get(x, y)
            if entity is None:
                pygame.draw.rect(screen, (230, 230, 230), rect)  # vide
            elif entity.__class__.__name__ == "Fish":
                pygame.draw.rect(screen, (0, 102, 204), rect)    # poisson bleu
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)   # contour
    pygame.display.flip()

draw_grid()
pygame.time.wait(1000) 


for fish in fish_list:
    fish.move(planet)


draw_grid()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()