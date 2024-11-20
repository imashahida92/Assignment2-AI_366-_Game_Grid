import pygame
import sys
from agent import Agent
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 200
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)
TASK_COLOR = (255, 0, 0)
AGENT_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
MOVEMENT_DELAY = 200  # Milliseconds between movements


def restart_simulation(environment, using_a_star):
    """Restart the agent and reset tasks while keeping the environment fixed."""
    environment.reset_tasks()  # Reset tasks to their initial state
    agent = Agent(environment, GRID_SIZE)
    agent.find_path_to = agent.find_path_to_a_star if using_a_star else agent.find_path_to_ucs
    return agent


def main():
    pygame.init()

    # Set up display with an additional status panel
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    # Clock to control frame rate
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize environment and agent
    using_a_star = True  # Default to A*
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent = restart_simulation(environment, using_a_star)

    # Button dimensions and positions
    button_width, button_height = 100, 50
    button_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2
    start_button_y = WINDOW_HEIGHT // 2 - button_height // 2
    toggle_button_y = start_button_y + 60

    start_button_rect = pygame.Rect(button_x, start_button_y, button_width, button_height)
    toggle_button_rect = pygame.Rect(button_x, toggle_button_y, button_width, button_height)

    simulation_started = False

    # Movement delay variables
    last_move_time = pygame.time.get_ticks()

    # Main loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not simulation_started and start_button_rect.collidepoint(event.pos):
                    # Start the simulation
                    simulation_started = True
                    if environment.task_locations:
                        agent.find_nearest_task()
                elif toggle_button_rect.collidepoint(event.pos):
                    # Toggle the algorithm and reset tasks
                    using_a_star = not using_a_star
                    agent = restart_simulation(environment, using_a_star)
                    simulation_started = False

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the grid and barriers
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Grid lines

        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        # Draw tasks
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        # Draw agent
        agent_rect = pygame.Rect(agent.position[0] * GRID_SIZE, agent.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, AGENT_COLOR, agent_rect)

        # Update agent movement
        if simulation_started:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > MOVEMENT_DELAY:
                if not agent.moving and environment.task_locations:
                    agent.find_nearest_task()  # Plan a new path if idle and tasks remain
                elif agent.moving:
                    agent.move()  # Move along the planned path
                last_move_time = current_time

        # Status panel
        status_x = WINDOW_WIDTH + 10
        algorithm_text = f"Algorithm: {'A*' if using_a_star else 'UCS'}"
        tasks_completed_text = f"Tasks Completed: {agent.task_completed}"
        total_cost_text = f"Total Cost: {agent.total_cost}"
        completed_tasks_text = f"Completed: {agent.completed_tasks}"
        current_position_text = f"Position: {agent.position}"

        # Render text
        algorithm_surface = font.render(algorithm_text, True, TEXT_COLOR)
        tasks_completed_surface = font.render(tasks_completed_text, True, TEXT_COLOR)
        total_cost_surface = font.render(total_cost_text, True, TEXT_COLOR)
        completed_tasks_surface = font.render(completed_tasks_text, True, TEXT_COLOR)
        current_position_surface = font.render(current_position_text, True, TEXT_COLOR)

        # Display text
        screen.blit(algorithm_surface, (status_x, 10))
        screen.blit(tasks_completed_surface, (status_x, 40))
        screen.blit(total_cost_surface, (status_x, 70))
        screen.blit(completed_tasks_surface, (status_x, 100))
        screen.blit(current_position_surface, (status_x, 130))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        # Start button
        button_color = BUTTON_HOVER_COLOR if start_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, start_button_rect)
        start_button_text = font.render("Start", True, BUTTON_TEXT_COLOR)
        start_text_rect = start_button_text.get_rect(center=start_button_rect.center)
        screen.blit(start_button_text, start_text_rect)

        # Toggle button
        button_color = BUTTON_HOVER_COLOR if toggle_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, toggle_button_rect)
        toggle_button_text = font.render("Toggle", True, BUTTON_TEXT_COLOR)
        toggle_text_rect = toggle_button_text.get_rect(center=toggle_button_rect.center)
        screen.blit(toggle_button_text, toggle_text_rect)

        # Draw panel separator
        pygame.draw.line(screen, (0, 0, 0), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
