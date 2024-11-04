import subprocess
import sys
import heapq
import random

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
max_size = min(screen_width, screen_height) - 130
pygame.display.set_caption("Kare Maze")

font = pygame.font.SysFont("Calibri", 23)
input_box = pygame.Rect(50, 80, 180, 50)

window_width = max_size
window_height = max_size
window = pygame.display.set_mode((window_width, window_height))

columns = int(max_size / 17)
rows = int(max_size / 17)
box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []

delay_speed = 50

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        self.cost = 1

    def draw(self, win, color):
        pygame.draw.rect(
            win,
            color,
            (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2),
        )

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def __lt__(self, other):
        return False

pygame.font.init()

for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

for i in range(columns):
    grid[i][0].wall = True
    grid[i][rows - 1].wall = True

for j in range(rows):
    grid[0][j].wall = True
    grid[columns - 1][j].wall = True

def bfs(start_box, target_box):
    queue.append(start_box)
    while queue:
        pygame.time.delay(delay_speed)
        current_box = queue.pop(0)
        current_box.visited = True
        if current_box == target_box:
            return reconstruct_path(start_box, current_box)
        for neighbour in current_box.neighbours:
            if not neighbour.queued and not neighbour.wall:
                neighbour.queued = True
                neighbour.prior = current_box
                queue.append(neighbour)
        draw_grid()

def dfs(start_box, target_box):
    stack = [start_box]
    reset_after_dead_end = False

    while stack:
        pygame.time.delay(delay_speed)

        if reset_after_dead_end:
            stack = [start_box]
            reset_after_dead_end = False

        current_box = stack.pop()
        current_box.visited = True

        if current_box == target_box:
            return reconstruct_path(start_box, current_box)

        dead_end = True

        for neighbour in current_box.neighbours:
            if not neighbour.visited and not neighbour.wall:
                neighbour.prior = current_box
                stack.append(neighbour)
                dead_end = False

        if dead_end:
            reset_after_dead_end = True

        draw_grid()

def ucs(start_box, target_box, random_cost=False):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_box))
    start_box.queued = True
    costs = {start_box: 0}
    while priority_queue:
        pygame.time.delay(delay_speed)
        current_cost, current_box = heapq.heappop(priority_queue)
        current_box.visited = True
        if current_box == target_box:
            return reconstruct_path(start_box, current_box)
        for neighbour in current_box.neighbours:
            if not neighbour.wall:
                new_cost = current_cost + (neighbour.cost if random_cost else 1)
                if neighbour not in costs or new_cost < costs[neighbour]:
                    costs[neighbour] = new_cost
                    neighbour.prior = current_box
                    heapq.heappush(priority_queue, (new_cost, neighbour))
                    neighbour.queued = True
        draw_grid()

def reconstruct_path(start_box, end_box):
    path.clear()
    while end_box.prior != start_box:
        path.append(end_box.prior)
        end_box = end_box.prior

def draw_grid():
    window.fill((0, 0, 0))
    for i in range(columns):
        for j in range(rows):
            box = grid[i][j]
            box.draw(window, (100, 100, 100))
            if box.queued:
                box.draw(window, (0, 255, 0))
            if box.visited:
                box.draw(window, (0, 150, 0))
            if box in path:
                box.draw(window, (255, 255, 255))
            if box.start:
                box.draw(window, (200, 0, 0))
            if box.wall:
                box.draw(window, (10, 10, 10))
            if box.target:
                box.draw(window, (255, 191, 0))
    instructions = ["Sol Tık: Başlangıç Noktası, Sağ Tık: Goal, 1: BFS, 2: DFS, 3: UCS, 4: UCS (Random Cost)",]
    for i, instruction in enumerate(instructions):
        text_surface = font.render(instruction, True, (255, 255, 255))
        window.blit(
            text_surface, (0, window_height - (len(instructions) - i) * 20 - 10)
        )
    pygame.display.flip()

def set_random_costs():
    for i in range(columns):
        for j in range(rows):
            if not grid[i][j].wall and not grid[i][j].start and not grid[i][j].target:
                grid[i][j].cost = random.randint(1, 1000)

def main():
    start_box_set = False
    target_box_set = False
    target_box = None
    selected_algorithm = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        start_box_set = True
                elif event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not target_box_set:
                        target_box = grid[i][j]
                        target_box.target = True
                        target_box_set = True
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                i = x // box_width
                j = y // box_height
                if event.buttons[0]:
                    grid[i][j].wall = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_algorithm = "bfs"
                elif event.key == pygame.K_2:
                    selected_algorithm = "dfs"
                elif event.key == pygame.K_3:
                    selected_algorithm = "ucs"
                elif event.key == pygame.K_4:
                    set_random_costs()
                    selected_algorithm = "ucs_random"
                if selected_algorithm and start_box_set and target_box_set:
                    if selected_algorithm == "bfs":
                        bfs(start_box, target_box)
                    elif selected_algorithm == "dfs":
                        dfs(start_box, target_box)
                    elif selected_algorithm == "ucs":
                        ucs(start_box, target_box)
                    elif selected_algorithm == "ucs_random":
                        ucs(start_box, target_box, random_cost=True)
                    selected_algorithm = None

        draw_grid()

main()