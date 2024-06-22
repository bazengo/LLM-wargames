import pygame
import random
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

window_width = h = 1280
window_height = v = 720
hv = (h, v)
screen = pygame.display.set_mode(hv)
clock = pygame.time.Clock()

# Barrier map
barrier_map = pygame.Surface((h, v))
barrier_map.fill((255, 255, 255))  # Fill with white (passable) by default

# Load and scale the barrier image
barrier_image = pygame.image.load("basic-map.png")  # Replace with your image path
barrier_image = pygame.transform.scale(barrier_image, (h, v))
barrier_map.blit(barrier_image, (0, 0))

# Grid for pathfinding
grid_size = 10
cols, rows = h // grid_size, v // grid_size

# Troop class
class Troop:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 3
        self.path = []
        self.radius = 10  # Collision radius
    
    def render(self):
        pygame.draw.circle(screen, 'red', (int(self.position.x), int(self.position.y)), self.radius)
    
    def move_to_waypoint(self, target_position, troops):
        if not self.path:
            self.path = astar(self.position, target_position)
        
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

# Waypoint class
class Waypoint:
    def __init__(self, position):
        self.position = position
    
    def render(self):
        pygame.draw.circle(screen, 'green', (int(self.position.x), int(self.position.y)), 5)

# A* pathfinding algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < cols and 0 <= y < rows:
            pixel_x, pixel_y = x * grid_size, y * grid_size
            if barrier_map.get_at((pixel_x, pixel_y))[0:3] != (0, 0, 0):  # Check if not black
                neighbors.append((x, y))
    return neighbors

def astar(start, goal):
    start_node = (int(start.x // grid_size), int(start.y // grid_size))
    goal_node = (int(goal.x // grid_size), int(goal.y // grid_size))
    
    frontier = PriorityQueue()
    frontier.put((0, start_node))
    came_from = {start_node: None}
    cost_so_far = {start_node: 0}
    
    while not frontier.empty():
        current = frontier.get()[1]
        
        if current == goal_node:
            break
        
        for next_node in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal_node, next_node)
                frontier.put((priority, next_node))
                came_from[next_node] = current
    
    # Reconstruct path
    path = []
    current = goal_node
    while current != start_node:
        path.append((current[0] * grid_size + grid_size // 2, current[1] * grid_size + grid_size // 2))
        current = came_from.get(current)
        if current is None:
            return []  # No path found
    path.reverse()
    return path

# Initialize troops
def spawn_troop():
    while True:
        x, y = random.randint(0, h), random.randint(0, v)
        if barrier_map.get_at((x, y))[0:3] != (0, 0, 0):
            return Troop(x, y)

troop_count = 10
troop_list = [spawn_troop() for _ in range(troop_count)]

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
        waypoint.render()
    
    # Render troops and move them
    for unit in troop_list:
        unit.render()
        if waypoint:
            unit.move_to_waypoint(waypoint.position, troop_list)
    
    # Flip screen event
    pygame.display.flip()
    
    # Clock frame event
    clock.tick(60)

pygame.quit()