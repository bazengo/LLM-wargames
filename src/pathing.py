import pygame
from queue import PriorityQueue
from map import barrier_map

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, cols, rows, barrier_map, grid_size):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < cols and 0 <= y < rows:
            pixel_x, pixel_y = x * grid_size, y * grid_size
            if barrier_map.get_at((pixel_x, pixel_y))[0:3] != (0, 0, 0):  # Check if not black
                neighbors.append((x, y))
    return neighbors

def astar(start, goal, grid_size):
    h, v = 1280, 720
    cols, rows = h // grid_size, v // grid_size
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
        
        for next_node in get_neighbors(current, cols, rows, barrier_map, grid_size):
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
