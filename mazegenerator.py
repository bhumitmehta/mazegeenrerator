import pygame
import random
import math
import time
import os
import sys

from collections import deque
from typing import List, Tuple, Dict, Any
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_RETURN
from pygame import Color, Rect, Surface

from pygame import event
from pygame import init, display, time as pg_time

from pygame import image


# Set the SDL_AUDIODRIVER environment variable to 'dummy' to bypass ALSA-related warnings
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Constants
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 10   # Use this consistently
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
LIGHT_RED = (255, 150, 150) # For visited path
# Directions for maze generation
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# Directions for pathfinding
DIRECTIONS_PATHFINDING = [(0, 1), (1, 0), (0, -1), (-1, 0),
                           (1, 1), (1, -1), (-1, 1), (-1, -1)]
# Direction for DFS maze generation
DFS_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# Initialize Pygame
pygame.init()

# Load images
def load_image(name: str) -> Surface:
    """Load an image from the images directory."""
    path = os.path.join('images', name)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image '{name}' not found in 'images' directory.")
    return image.load(path).convert_alpha()

# Generate a maze using depth-first search
def generate_maze_dfs(width: int, height: int) -> List[List[int]]:
    """Generate a maze using depth-first search."""
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = deque()
    start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
    maze[start_y][start_x] = 0
    stack.append((start_x, start_y))

    while stack:
        x, y = stack.pop()
        neighbors = []
        for dx, dy in DFS_DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((dx, dy))
        if neighbors:
            stack.append((x, y))
            dx, dy = random.choice(neighbors)
            maze[y + dy][x + dx] = 0
            maze[y + dy * 2][x + dx * 2] = 0
            stack.append((x + dx * 2, y + dy * 2))
    return maze

# Add a border to the maze
def add_border(maze: List[List[int]]) -> List[List[int]]:
    width = len(maze[0])
    height = len(maze)
    bordered_maze = [[1] * (width + 2)]  # Top border
    for row in maze:
        bordered_maze.append([1] + row + [1])  # Add left and right borders
    bordered_maze.append([1] * (width + 2))  # Bottom border
    return bordered_maze

# Display the maze on the screen
def display_maze(maze_data: List[List[int]], screen_surface: Surface, current_start_point: Tuple[int, int], current_end_point: Tuple[int, int], visited_cells: set) -> None:
    """Display the maze on the screen."""
    screen_surface.fill(BLACK)  # Clear screen for fresh draw
    for y_coord in range(len(maze_data)):
        for x_coord in range(len(maze_data[0])):
            cell_value = maze_data[y_coord][x_coord]
            current_cell = (x_coord, y_coord)
            
            color_to_draw = BLACK # Default for walls

            if current_cell == current_start_point:
                color_to_draw = RED
            elif current_cell == current_end_point:
                color_to_draw = GREEN
            elif current_cell in visited_cells:
                color_to_draw = LIGHT_RED
            elif cell_value == 0: # Path cell
                color_to_draw = WHITE
            
            pixel_x, pixel_y = x_coord * CELL_SIZE, y_coord * CELL_SIZE
            if pixel_x < WINDOW_WIDTH and pixel_y < WINDOW_HEIGHT:
                 pygame.draw.rect(screen_surface, color_to_draw, (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Initialize the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Generator")

# Generate the base maze
base_maze = generate_maze_dfs(GRID_WIDTH, GRID_HEIGHT)

# Define initial start and end points for the base maze
initial_start_point = (0, 0)
initial_end_point = (GRID_WIDTH - 1, GRID_HEIGHT - 1)

# Ensure start and end points are paths in the base_maze
if 0 <= initial_start_point[1] < len(base_maze) and 0 <= initial_start_point[0] < len(base_maze[0]):
    base_maze[initial_start_point[1]][initial_start_point[0]] = 0
if 0 <= initial_end_point[1] < len(base_maze) and 0 <= initial_end_point[0] < len(base_maze[0]):
    base_maze[initial_end_point[1]][initial_end_point[0]] = 0

# Add border to the maze
final_maze = add_border(base_maze)

# Adjust start and end points for the border
final_start_point = (initial_start_point[0] + 1, initial_start_point[1] + 1)
final_end_point = (initial_end_point[0] + 1, initial_end_point[1] + 1)

# Ensure start/end points are paths in the final_maze as well
if 0 <= final_start_point[1] < len(final_maze) and 0 <= final_start_point[0] < len(final_maze[0]):
    final_maze[final_start_point[1]][final_start_point[0]] = 0
if 0 <= final_end_point[1] < len(final_maze) and 0 <= final_end_point[0] < len(final_maze[0]):
    final_maze[final_end_point[1]][final_end_point[0]] = 0

# Redefine final_end_point for display to be the bottom-right visible cell
# The visible grid is GRID_WIDTH x GRID_HEIGHT cells.
# So, the bottom-right visible cell has indices (GRID_WIDTH - 1, GRID_HEIGHT - 1).
# These are also the indices in final_maze for that cell, as display_maze shows final_maze[0:GRID_HEIGHT][0:GRID_WIDTH].
final_end_point_display_x = max(0, GRID_WIDTH - 1)
final_end_point_display_y = max(0, GRID_HEIGHT - 1)
final_end_point = (final_end_point_display_x, final_end_point_display_y)

# Ensure this specific display point is also a path in final_maze
if 0 <= final_end_point[1] < len(final_maze) and 0 <= final_end_point[0] < len(final_maze[0]):
    final_maze[final_end_point[1]][final_end_point[0]] = 0

# Keep track of visited path
visited_path = set()
visited_path.add(final_start_point) # Add initial start point

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event_item in pygame.event.get():
        if event_item.type == QUIT:
            running = False
        if event_item.type == KEYDOWN:
            if event_item.key == K_ESCAPE:
                running = False
            
    # Get the state of all keyboard keys for continuous movement
    keys = pygame.key.get_pressed()
    
    new_start_x, new_start_y = final_start_point

    if keys[pygame.K_UP]:
        potential_y = new_start_y - 1
        if 0 <= potential_y < len(final_maze) and \
           0 <= new_start_x < len(final_maze[0]) and \
           final_maze[potential_y][new_start_x] == 0:
            new_start_y = potential_y
    elif keys[pygame.K_DOWN]:
        potential_y = new_start_y + 1
        if 0 <= potential_y < len(final_maze) and \
           0 <= new_start_x < len(final_maze[0]) and \
           final_maze[potential_y][new_start_x] == 0:
            new_start_y = potential_y
    elif keys[pygame.K_LEFT]:
        potential_x = new_start_x - 1
        if 0 <= new_start_y < len(final_maze) and \
           0 <= potential_x < len(final_maze[0]) and \
           final_maze[new_start_y][potential_x] == 0:
            new_start_x = potential_x
    elif keys[pygame.K_RIGHT]:
        potential_x = new_start_x + 1
        if 0 <= new_start_y < len(final_maze) and \
           0 <= potential_x < len(final_maze[0]) and \
           final_maze[new_start_y][potential_x] == 0:
            new_start_x = potential_x
            
    final_start_point = (new_start_x, new_start_y)
    visited_path.add(final_start_point) # Add current position to visited path

    display_maze(final_maze, screen, final_start_point, final_end_point, visited_path)
    clock.tick(FPS)

pygame.quit()