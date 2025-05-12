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
CELL_SIZE = 20
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
# Directions for maze generation
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# Directions for pathfinding
DIRECTIONS_PATHFINDING = [(0, 1), (1, 0), (0, -1), (-1, 0),
                           (1, 1), (1, -1), (-1, 1), (-1, -1)]
# Direction for DFS maze generation
DFS_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
CELL_SIZE = 10
# Initialize Pygame
init()
# Commenting out mixer.init() to avoid ALSA-related errors
# mixer.init()
# Load images
# Load images
def load_image(name: str) -> Surface:
    """Load an image from the images directory."""
    path = os.path.join('images', name)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image '{name}' not found in 'images' directory.")
    return image.load(path).convert_alpha()
# # Load sound


#write a function to genrate a maze using dfs
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

# Generate the maze once
maze = generate_maze_dfs(WINDOW_WIDTH, WINDOW_HEIGHT)

# Add start and stop points
start_point = (0, 0)  # Top-left corner
# Ensure the end point is within the visible grid
end_point = (min(len(maze[0]) - 1, GRID_WIDTH - 1), min(len(maze) - 1, GRID_HEIGHT - 1))  # Bottom-right corner

# Modify display_maze to include start and stop points
def display_maze(maze: List[List[int]], screen: Surface) -> None:
    """Display the maze on the screen."""
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (x, y) == start_point:
                color = RED  # Start point
            elif (x, y) == end_point:
                color = GREEN  # End point
            else:
                color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Initialize the game window
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Maze Generator")

# Generate the maze once
maze = generate_maze_dfs(WINDOW_WIDTH, WINDOW_HEIGHT)

# Add start and stop points
start_point = (0, 0)  # Top-left corner
# Ensure the end point is within the visible grid
end_point = (min(len(maze[0]) - 1, GRID_WIDTH - 1), min(len(maze) - 1, GRID_HEIGHT - 1))  # Bottom-right corner

# Modify display_maze to include start and stop points
def display_maze(maze: List[List[int]], screen: Surface) -> None:
    """Display the maze on the screen."""
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (x, y) == start_point:
                color = RED  # Start point
            elif (x, y) == end_point:
                color = GREEN  # End point
            else:
                color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Initialize the game window
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Maze Generator")

# Generate the maze once
maze = generate_maze_dfs(WINDOW_WIDTH, WINDOW_HEIGHT)

# Main game loop
running = True
while running:
    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            running = False

    # Display the maze
    display_maze(maze, screen)

    # Cap the frame rate
    pg_time.Clock().tick(FPS)

pygame.quit()