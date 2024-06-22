import pygame
import random
from pathing import astar


class Troop:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = 1
        self.max_speed = 3
        self.path = []
        self.radius = 10  # Collision radius
        self.max_separation_force = 2
    
    def render(self, screen):
        pygame.draw.circle(screen, 'red', (int(self.position.x), int(self.position.y)), self.radius)
    
    def move_to_waypoint(self, target_position, troops, grid_size, barrier_map):
        if not self.path:
            self.path = astar(self.position, target_position, grid_size, barrier_map)
        
        if self.path:
            next_point = pygame.Vector2(self.path[0])
            direction = (next_point - self.position).normalize()
            self.velocity = direction * self.max_speed * self.position.distance_to(next_point)
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
            
            # Combine forces
            self.acceleration = self.separate(troops) / self.mass
            ## add a gravity force to the acceleration
            self.acceleration += pygame.Vector2(0, 0.1)
            # Update velocity
            self.velocity += self.acceleration

            if barrier_map.get_at( vector2_to_tuple(self.position + self.velocity) ) == 0:
                ## rotate the vector CW and CCW until one does not collide
                for i in range(1, 18):
                    self.velocity.rotate_ip(i*10)
                    if barrier_map.get_at( vector2_to_tuple(self.position + self.velocity) ) != 0:
                        break
                    self.velocity.rotate_ip(-i*20)
                    if barrier_map.get_at( vector2_to_tuple(self.position + self.velocity) ) != 0:
                        break
                    self.velocity.rotate_ip(i*10)
                
            self.position +=self.velocity

            

            if self.position.distance_to(next_point) < self.radius * 2:
                self.path.pop(0)
    
    def separate(self, troops):
        steering_force = pygame.Vector2()
        maximum_distance = self.radius * 3  # maximum distance troops can affect eachother from
        
        for other in troops:
            if other != self:
                d = self.position.distance_to(other.position)
                if 0 < d < maximum_distance:
                    diff = self.position - other.position
                    
                    # Calculate force with smooth falloff
                    force_magnitude = self.max_separation_force * (1 - (d / maximum_distance)**2)
                    force = diff.normalize() * force_magnitude
                    
                    steering_force += force
        
        return steering_force

def vector2_to_tuple(vector):
    return int(vector.x), int(vector.y)

def spawn_troop(h, v, barrier_map):
    while True:
        x, y = random.randint(0, h), random.randint(0, v)
        if barrier_map.get_at((x, y)) != 0:
            return Troop(x, y)
