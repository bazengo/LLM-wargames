import pygame

# Barrier map
h, v = 1280, 720
barrier_map = pygame.Surface((h, v))
barrier_map.fill((255, 255, 255))  # Fill with white (passable) by default

# Load and scale the barrier image
barrier_image = pygame.image.load("../basic-map.png")  # Replace with your image path
barrier_image = pygame.transform.scale(barrier_image, (h, v))
barrier_map.blit(barrier_image, (0, 0))

class barrier_map:
    def __init__(self, image_path):
        # Barrier map
        h, v = 1280, 720
        self.surface = pygame.Surface((h, v))
        self.surface.fill((255, 255, 255))  # Fill with white (passable) by default

        # Load and scale the barrier image
        self.barrier_image = pygame.image.load(image_path)  # Replace with your image path
        self.barrier_image = pygame.transform.scale(barrier_image, (h, v))
        self.surface.blit(barrier_image, (0, 0))
        
    def get_at(self, position):
        if position[0] < 0 or position[0] >= h or position[1] < 0 or position[1] >= v:
            return 0
        return sum(self.surface.get_at(position)[0:3])