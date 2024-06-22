import pygame

class Waypoint:
    def __init__(self, position):
        self.position = position
    
    def render(self, screen):
        pygame.draw.circle(screen, 'green', (int(self.position.x), int(self.position.y)), 5)
