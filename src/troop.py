import pygame
import random
from pathing import astar
from map import barrier_map


class Troop:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 3
        self.path = []
        self.radius = 10  # Collision radius
    
    def render(self, screen):
        pygame.draw.circle(screen, 'red', (int(self.position.x), int(self.position.y)), self.radius)
    
    def move_to_waypoint(self, target_position, troops, grid_size):
        if not self.path:
            self.path = astar(self.position, target_position, grid_size)
        
        if self.path:
            next_point = pygame.Vector2(self.path[0])
            direction = (next_point - self.position).normalize()
            desired_velocity = direction * self.speed
            
            # Apply separation force
            separation = self.separate(troops)
            
            # Combine forces
            steering = desired_velocity + separation
            steering = steering.normalize() * self.speed if steering.length() > 0 else steering
            
            self.velocity = steering
            self.position += self.velocity
            
            if self.position.distance_to(next_point) < self.speed:
                self.path.pop(0)
    
    def separate(self, troops):
        steering = pygame.Vector2()
        desired_separation = self.radius * 4  # Increased separation distance for smoother effect
        max_separation_force = self.speed * 2  # Maximum separation force
        
        for other in troops:
            if other != self:
                d = self.position.distance_to(other.position)
                if 0 < d < desired_separation:
                    diff = self.position - other.position
                    
                    # Calculate force with smooth falloff
                    force_magnitude = max_separation_force * (1 - (d / desired_separation)**2)
                    force = diff.normalize() * force_magnitude
                    
                    steering += force
        
        return steering

def spawn_troop(h, v, barrier_map):
    while True:
        x, y = random.randint(0, h), random.randint(0, v)
        if barrier_map.get_at((x, y))[0:3] != (0, 0, 0):
            return Troop(x, y)
