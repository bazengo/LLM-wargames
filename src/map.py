import pygame

# Barrier map
h, v = 1280, 720
barrier_map = pygame.Surface((h, v))
barrier_map.fill((255, 255, 255))  # Fill with white (passable) by default

# Load and scale the barrier image
barrier_image = pygame.image.load("../basic-map.png")  # Replace with your image path
barrier_image = pygame.transform.scale(barrier_image, (h, v))
barrier_map.blit(barrier_image, (0, 0))