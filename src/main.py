import pygame
import random
from troop import Troop, spawn_troop
from waypoint import Waypoint
from pathing import astar
from map import barrier_map

# Initialize Pygame
pygame.init()

window_width = h = 1280
window_height = v = 720
hv = (h, v)
screen = pygame.display.set_mode(hv)
clock = pygame.time.Clock()

# Grid for pathfinding
grid_size = 10

# Initialize troops
troop_count = 10
troop_list = [spawn_troop(h, v, barrier_map) for _ in range(troop_count)]

# Initialize waypoint
waypoint = None

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if barrier_map.get_at(mouse_pos)[0:3] != (0, 0, 0):  # Ensure waypoint is not on a barrier
                    waypoint = Waypoint(pygame.Vector2(mouse_pos))
                    # Reset paths for all troops when waypoint changes
                    for troop in troop_list:
                        troop.path = []
    
    # Screen refresh event
    screen.fill('black')
    
    # Draw barrier map
    screen.blit(barrier_map, (0, 0))
    
    # Render waypoint
    if waypoint:
        waypoint.render(screen)
    
    # Render troops and move them
    for unit in troop_list:
        unit.render(screen)
        if waypoint:
            unit.move_to_waypoint(waypoint.position, troop_list, grid_size)
    
    # Flip screen event
    pygame.display.flip()
    
    # Clock frame event
    clock.tick(60)

pygame.quit()
