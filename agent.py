import pygame
import heapq

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting position
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  # Current path
        self.moving = False  # Indicates if the agent is moving
        self.total_cost = 0  # Total path cost

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.total_cost += 1
            self.check_task_completion()
        else:
            self.moving = False  # Stop moving when path is exhausted

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def find_nearest_task(self):
        """Find the nearest task using the selected pathfinding algorithm."""
        nearest_task = None
        shortest_path = None
        for task_position in self.environment.task_locations.keys():
            path = self.find_path_to(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        if shortest_path:
            self.path = shortest_path[1:]  # Exclude the current position
            self.moving = True

    def find_path_to_ucs(self, target):
        """Find a path to the target position using UCS."""
        start = tuple(self.position)
        goal = target
        frontier = []
        heapq.heappush(frontier, (0, [start]))  # Priority queue with (cost, path)
        visited = set()  # Track visited nodes

        while frontier:
            current_cost, path = heapq.heappop(frontier)
            current_position = path[-1]

            if current_position in visited:
                continue
            visited.add(current_position)

            if current_position == goal:
                return path  # Return full path to the goal

            for neighbor in self.get_neighbors(*current_position):
                if neighbor not in visited:
                    new_cost = current_cost + 1  # Uniform cost is constant
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (new_cost, new_path))

        return None

    def find_path_to_a_star(self, target):
        """Find a path to the target position using A*."""
        start = tuple(self.position)
        goal = target
        frontier = []
        heapq.heappush(frontier, (0, [start]))  # Priority queue with (cost, path)
        visited = set()

        while frontier:
            current_cost, path = heapq.heappop(frontier)
            current_position = path[-1]

            if current_position in visited:
                continue
            visited.add(current_position)

            if current_position == goal:
                return path

            for neighbor in self.get_neighbors(*current_position):
                if neighbor not in visited:
                    g_cost = len(path)
                    h_cost = self.heuristic(neighbor, goal)
                    f_cost = g_cost + h_cost
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (f_cost, new_path))

        return None

    def heuristic(self, current, goal):
        """Heuristic function: Manhattan distance."""
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
