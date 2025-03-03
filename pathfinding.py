import subprocess
import sys
import heapq
import random
import math

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
max_size = min(screen_width, screen_height) - 100
pygame.display.set_caption("Kare Maze")

reference_size = 950
reference_font_size = 19
reference_small_font_size = 14

font_size = int((max_size / reference_size) * reference_font_size)
small_font_size = int((max_size / reference_size) * reference_small_font_size)

font = pygame.font.SysFont("Calibri", font_size, bold=True)
small_font = pygame.font.SysFont("Calibri", small_font_size)

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

delay_speed = 1

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
        self.heuristic = float('inf')

    def draw(self, win, color):
        pygame.draw.rect(
            win,
            color,
            (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2),
        )
        if not self.wall:
            cost_text = small_font.render(str(self.cost), True, WHITE)
            text_rect = cost_text.get_rect(center=(self.x * box_width + box_width // 2,
                                                    self.y * box_height + box_height // 2))
            win.blit(cost_text, text_rect)

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def calculate_heuristic(self, target):
        self.heuristic = (abs(self.x - target.x) + abs(self.y - target.y))
        return self.heuristic

    def calculate_heuristic_euclidean(self, target):
        self.heuristic = math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)
        return self.heuristic

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

for j in range(rows):
    grid[0][j].wall = True

def bfs(start_box, target_box):
    queue.append(start_box)
    while queue:
        pygame.time.delay(delay_speed)
        current_box = queue.pop(0)
        current_box.visited = True
        for neighbour in current_box.neighbours:
            if not neighbour.queued and not neighbour.wall:
                neighbour.prior = current_box
                if neighbour == target_box:
                    return reconstruct_path(start_box, neighbour)
                else:
                    neighbour.queued = True
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

def ucs(start_box, target_box):
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
                new_cost = current_cost + neighbour.cost
                if neighbour not in costs or new_cost < costs[neighbour]:
                    costs[neighbour] = new_cost
                    neighbour.prior = current_box
                    heapq.heappush(priority_queue, (new_cost, neighbour))
                    neighbour.queued = True
        draw_grid()

def a_star(start_box, target_box):
    priority_queue = []
    start_box.heuristic = start_box.calculate_heuristic(target_box)
    heapq.heappush(priority_queue, (0, start_box))
    start_box.queued = True
    g_scores = {start_box: 0}

    while priority_queue:
        pygame.time.delay(delay_speed)
        current_f, current_box = heapq.heappop(priority_queue)
        current_box.visited = True

        if current_box == target_box:
            return reconstruct_path(start_box, current_box)

        for neighbour in current_box.neighbours:
            if not neighbour.wall:
                tentative_g = g_scores[current_box] + neighbour.cost
                if neighbour not in g_scores or tentative_g < g_scores[neighbour]:
                    g_scores[neighbour] = tentative_g
                    f_score = tentative_g + neighbour.calculate_heuristic(target_box)
                    neighbour.prior = current_box
                    heapq.heappush(priority_queue, (f_score, neighbour))
                    neighbour.queued = True
        draw_grid()

def a_star_euclidean(start_box, target_box):
    priority_queue = []
    start_box.heuristic = start_box.calculate_heuristic_euclidean(target_box)
    heapq.heappush(priority_queue, (0, start_box))
    start_box.queued = True
    g_scores = {start_box: 0}

    while priority_queue:
        pygame.time.delay(delay_speed)
        current_f, current_box = heapq.heappop(priority_queue)
        current_box.visited = True

        if current_box == target_box:
            return reconstruct_path(start_box, current_box)

        for neighbour in current_box.neighbours:
            if not neighbour.wall:
                tentative_g = g_scores[current_box] + neighbour.cost
                if neighbour not in g_scores or tentative_g < g_scores[neighbour]:
                    g_scores[neighbour] = tentative_g
                    f_score = tentative_g + neighbour.calculate_heuristic_euclidean(target_box)
                    neighbour.prior = current_box
                    heapq.heappush(priority_queue, (f_score, neighbour))
                    neighbour.queued = True
        draw_grid()

def greedy_search(start_box, target_box):
    priority_queue = []
    start_box.heuristic = start_box.calculate_heuristic(target_box)
    heapq.heappush(priority_queue, (start_box.heuristic, start_box))
    start_box.queued = True

    while priority_queue:
        pygame.time.delay(delay_speed)
        current_f, current_box = heapq.heappop(priority_queue)
        current_box.visited = True

        if current_box == target_box:
            return reconstruct_path(start_box, current_box)

        for neighbour in current_box.neighbours:
            if not neighbour.wall and not neighbour.visited:
                neighbour.heuristic = neighbour.calculate_heuristic(target_box)
                neighbour.prior = current_box
                heapq.heappush(priority_queue, (neighbour.heuristic, neighbour))
                neighbour.queued = True

        draw_grid()

def greedy_search_euclidean(start_box, target_box):
    priority_queue = []
    start_box.heuristic = start_box.calculate_heuristic_euclidean(target_box)
    heapq.heappush(priority_queue, (start_box.heuristic, start_box))
    start_box.queued = True

    while priority_queue:
        pygame.time.delay(delay_speed)
        current_f, current_box = heapq.heappop(priority_queue)
        current_box.visited = True

        if current_box == target_box:
            return reconstruct_path(start_box, current_box)

        for neighbour in current_box.neighbours:
            if not neighbour.wall and not neighbour.visited:
                neighbour.heuristic = neighbour.calculate_heuristic_euclidean(target_box)
                neighbour.prior = current_box
                heapq.heappush(priority_queue, (neighbour.heuristic, neighbour))
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

    top_instructions = "C: Reset Grid, Q: Quit, M: Random Maze"
    top_text_surface = font.render(top_instructions, True, (255, 255, 255))
    window.blit(top_text_surface, (0, 0))

    instructions = ["Sol Tık: Start, Sağ Tık: Goal, R: Random Cost, 1: BFS, 2: DFS, 3: UCS, 4: A* (M), 5: A* (E), 6: G (M), 7: G (E)"]
    for i, instruction in enumerate(instructions):
        text_surface = font.render(instruction, True, (255, 255, 255))
        window.blit(
            text_surface, (0, window_height - (len(instructions) - i) * (font_size))
        )
    pygame.display.flip()

def set_random_costs():
    for i in range(columns):
        for j in range(rows):
            if not grid[i][j].wall and not grid[i][j].start and not grid[i][j].target:
                grid[i][j].cost = random.randint(1, 9)

def reset_grid():
    global start_box_set, target_box_set, start_box, target_box, path, queue
    start_box_set = False
    target_box_set = False
    start_box = None
    target_box = None
    path.clear()
    queue.clear()

    for i in range(columns):
        for j in range(rows):

            if i == 0 or j == 0:
                continue
            grid[i][j].start = False
            grid[i][j].wall = False
            grid[i][j].target = False
            grid[i][j].queued = False
            grid[i][j].visited = False
            grid[i][j].prior = None
            grid[i][j].cost = 1
            grid[i][j].heuristic = float('inf')
    main()

def reset_grid_except_walls():
    global path, queue
    path.clear()
    queue.clear()

    for i in range(columns):
        for j in range(rows):
            grid[i][j].queued = False
            grid[i][j].visited = False
            grid[i][j].prior = None
            grid[i][j].heuristic = float('inf')

def generate_maze():

    for i in range(columns):
        for j in range(rows):
            grid[i][j].wall = True

    def visit(cell_x, cell_y):
        grid[cell_x][cell_y].wall = False
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cell_x + dx, cell_y + dy
            if 1 <= nx < columns - 1 and 1 <= ny < rows - 1 and grid[nx][ny].wall:

                grid[cell_x + dx // 2][cell_y + dy // 2].wall = False
                visit(nx, ny)

    start_x, start_y = 1, 1
    visit(start_x, start_y)
    draw_grid()

def main():
    start_box_set = False
    target_box_set = False
    target_box = None
    selected_algorithm = None
    is_removing = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = x // box_width
                j = y // box_height

                if 0 <= i < columns and 0 <= j < rows:
                    box = grid[i][j]

                    if event.button == 1:
                        if i == 0 or j == 0:
                            continue
                        if not start_box_set and not box.wall:
                            start_box = box
                            start_box.start = True
                            start_box.visited = True
                            start_box_set = True
                        else:
                            if box.wall:
                                is_removing = True
                                box.wall = False
                            else:
                                is_removing = False
                                if not box.start and not box.target:
                                    box.wall = True
                    elif event.button == 3:
                        if not target_box_set and not box.start and not box.wall:
                            target_box = box
                            target_box.target = True
                            target_box_set = True

            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                i = x // box_width
                j = y // box_height

                if 0 <= i < columns and 0 <= j < rows:
                    box = grid[i][j]

                    if i == 0 or j == 0:
                        continue
                    if event.buttons[0]:
                        if is_removing:
                            if box.wall:
                                box.wall = False
                        else:
                            if not box.wall and not box.start and not box.target:
                                box.wall = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_removing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    reset_grid()
                if event.key == pygame.K_r:
                    set_random_costs()
                elif event.key == pygame.K_m:
                    generate_maze()
                elif event.key in [pygame.K_1, pygame.K_KP1]:
                    selected_algorithm = "bfs"
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    selected_algorithm = "dfs"
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    selected_algorithm = "ucs"
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    selected_algorithm = "a_star"
                elif event.key in [pygame.K_5, pygame.K_KP5]:
                    selected_algorithm = "a_star_euclidean"
                elif event.key in [pygame.K_6, pygame.K_KP6]:
                    selected_algorithm = "greedy"
                elif event.key in [pygame.K_7, pygame.K_KP7]:
                    selected_algorithm = "greedy_euclidean"
                if selected_algorithm and start_box_set and target_box_set:
                    if selected_algorithm == "bfs":
                        reset_grid_except_walls()
                        bfs(start_box, target_box)
                    elif selected_algorithm == "dfs":
                        reset_grid_except_walls()
                        dfs(start_box, target_box)
                    elif selected_algorithm == "ucs":
                        reset_grid_except_walls()
                        ucs(start_box, target_box)
                    elif selected_algorithm == "a_star":
                        reset_grid_except_walls()
                        a_star(start_box, target_box)
                    elif selected_algorithm == "a_star_euclidean":
                        reset_grid_except_walls()
                        a_star_euclidean(start_box, target_box)
                    elif selected_algorithm == "greedy":
                        reset_grid_except_walls()
                        greedy_search(start_box, target_box)
                    elif selected_algorithm == "greedy_euclidean":
                        reset_grid_except_walls()
                        greedy_search_euclidean(start_box, target_box)
                    selected_algorithm = None

        draw_grid()

main()
