How to Run the Simulation
    Install the required libraries:
        pip install pygame
    Save all the required files (agent.py, environment.py, run.py, etc.) in the same directory.
    Navigate to the directory in your terminal/command prompt.
    Run the simulation using:
        python run.py   

Observed Differences in Path Costs Between UCS and A*
    UCS always produces the optimal path but may explore unnecessary nodes due to its lack of heuristic guidance.
    A* uses a heuristic to prioritize paths closer to the goal, often reducing search time while still finding an optimal solution.
    If the heuristic is well-designed, A* performs significantly better in complex scenarios with multiple tasks.

Challenges Faced and Resolutions
    Smooth Agent Movement:
        The agent was completing tasks without visually moving on the grid.
    Resetting the Environment on Toggle :
        When switching between UCS and A*, the agent would continue from its last position instead of restarting.
    