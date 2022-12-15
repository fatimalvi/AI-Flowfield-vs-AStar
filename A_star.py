import pygame
import random

random.seed(0)

grid_size = int(input("choose a grid size from 8, 10, 12 or 14: "))

while grid_size != 12 and grid_size != 8 and grid_size != 14 and grid_size != 10:
    grid_size = int(input("Please choose a grid size from 8, 10, 12 or 14: "))

enemies = int(input("Choose the number of obstacles: "))

start = (0, 0)
goal = (5, 5)
#grid_size = 8
#enemies = 20

if grid_size == 12:
    width = 650
    height = 650
    button_location = (625, 10, 10, 10)

if grid_size == 14:
    width = 750
    height = 750
    button_location = (725, 10, 10, 10)

if grid_size == 10:
    width = 550
    height = 550
    button_location = (525, 10, 10, 10)

if grid_size == 8:
    width = 450
    height = 450
    button_location = (425, 10, 10, 10)




def initialise_cost_grid(size):

    cost = []
    all_enemies = []

    for i in range(size):
        temp_list = []
        for j in range(size):
            random_num = random.randint(1, 10)
            temp_list.append(random_num)
        
        cost.append(temp_list)

    for f in range(enemies):
        ran_x = random.randint(1, grid_size - 2)
        ran_y = random.randint(1, grid_size - 2)

        node = (ran_x, ran_y)
        if node != goal:
            cost[ran_x][ran_y] = 200
            all_enemies.append((ran_x, ran_y))


    return cost, all_enemies

def find_cost_(cost, node):

    return cost[node[0]][node[1]]

def heuristic(node, goal):

    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
 
    h = (dx + dy) + (1 - 2 * 1) * min(dx, dy)

    #distance = abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    return h

def getNeighbours(Grid, node):
    neighbours = []

    x, y = node
    row, col = len(Grid), len(Grid[0])

    # check all 8 possible neighbours
    if x > 0:
        neighbours.append((x-1, y))
        if y > 0:
            neighbours.append((x-1, y-1))
        if y < col - 1:
            neighbours.append((x-1, y+1))
    if x < row - 1:
        neighbours.append((x+1, y))
        if y > 0:
            neighbours.append((x+1, y-1))
        if y < col - 1:
            neighbours.append((x+1, y+1))
    if y > 0:
        neighbours.append((x, y-1))
    if y < col - 1:
        neighbours.append((x, y+1))

    return neighbours

#Initialize Pygame
pygame.init()

#Set the width and heigh of screen
#width = 650
#height = 650
screen = pygame.display.set_mode((width, height))
#screen2 = pygame.display.set_mode((width, height))
#Set title of window
pygame.display.set_caption("A Star Algorithm Visualization")

#Define the Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (143,188,143)
purple = (75,57,75)
actual_yellow = (255,217,102)
blue = (159,197,232)
obstacle_color = (199, 21, 133)
bg_color = (230,230,250)
rect_color = (199, 21, 133)
vector_color=(255, 105, 180)
rect_color_2 = (194,180,226)
#Font 
font_name = pygame.font.match_font("arial")
font = pygame.font.Font(font_name, 25)

screen.fill(bg_color)

Grid, all_Enemies = initialise_cost_grid(grid_size)


for row in range(grid_size):
    for column in range(grid_size):
        
        x_pos = row * 50
        y_pos = column * 50
        
        grid_num = Grid[row][column]

        if grid_num != 200:
            font = pygame.font.Font(None, 25)
            text = font.render(str(grid_num), 1, purple)
            screen.blit(text, (38 + column * 50, 42 + row * 50))
        else:
            rect = pygame.Rect(11 + y_pos, 11 + x_pos, 48, 48)
            screen.fill(obstacle_color, rect)

        

        square = pygame.Rect(10 + x_pos, 10 + y_pos, 50, 50)

        pygame.draw.rect(screen, rect_color, square, 1)

        pygame.display.update()

#button = pygame.Rect(625, 10, 10, 10)
button = pygame.Rect(button_location[0], button_location[1], button_location[2], button_location[3])
pygame.draw.rect(screen, purple, button, 1)
screen.fill(purple, button_location)
#screen.fill(purple, (625, 10, 10, 10))
#update the display
pygame.display.flip()

flag = 0
#Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if button.collidepoint(mouse_pos) and mouse_pressed[0] == 1:

        if flag == 0:

            open_nodes = [(0, start)]

            # Create a dictionary to store the costs of nodes that have been visited
            visited = {}
            visited[start] = 0

            # Create a dictionary to store the paths to nodes that have been visited
            paths = {}
            paths[start] = [start]

            # Create a flag to indicate if the goal has been found
            found = False

            # Loop until the open nodes list is empty or the goal is found
            while open_nodes and not found:
                # Sort the open nodes list in ascending order of cost
                open_nodes.sort()

                # Get the node with the lowest cost
                node = open_nodes.pop(0)[1]

                center = (34 + 50 * node[1], 34 + 50 * node[0])
                radius = 10
                pygame.draw.circle(screen, rect_color_2, center, radius)
                pygame.time.wait(300)
                pygame.display.update()

                # Check if the node is the goal
                if node == goal:
                    # Set the found flag to True
                    found = True
                    flag = 1

                else:
                    # Get the neighbors of the current node
                    neighbors = getNeighbours(Grid, node)

                    center = (34 + 50 * node[1], 34 + 50 * node[0])
                    radius = 10
                    pygame.draw.circle(screen, blue, center, radius)

                    pygame.display.update()
                    circles = []
                    # Loop over the neighbors
                    for neighbor in neighbors:
                        # Calculate the cost of reaching the neighbor
                        cost = find_cost_(Grid, neighbor) + visited[node]

                        i_ = neighbor
                        
                        center = (34 + 50 * i_[1] - 12, 34 + 50 * i_[0] - 12)

                        if neighbor not in all_Enemies:
                            circles.append(center)
                            radius = 5
                            pygame.draw.circle(screen, purple, center, radius)
                            #pygame.display.update()
                            pygame.time.wait(200)
                            pygame.display.update()
                        

                        # If the neighbor has not been visited, or if the cost of reaching
                        # the neighbor through the current node is lower than the previously
                        # recorded

                                # recorded cost of reaching the neighbor, add the neighbor to the
                        # open nodes list and update the cost and path for the neighbor
                        if neighbor not in visited or cost < visited[neighbor]:
                            visited[neighbor] = cost
                            priority = cost + heuristic(neighbor, goal)
                            open_nodes.append((priority, neighbor))
                            paths[neighbor] = paths[node] + [neighbor]

                    pygame.time.wait(200)

                    for one in circles:
                        center = one
                        radius = 5
                        pygame.draw.circle(screen, bg_color, center, radius)
                        pygame.time.wait(200)

                    #center = (34 + 50 * node[0] - 12, 34 + 50 * node[1] - 12)
                    center = (34 + 50 * node[1], 34 + 50 * node[0])
                    radius = 10
                    pygame.draw.circle(screen, rect_color_2, center, radius)

                    pygame.display.update()

            # Return the path to the goal, if it was found, or an empty list otherwise
        print(paths.get(goal, []))
        u = paths.get(goal, [])

        for uu in u:

            center = (34 + 50 * uu[1], 34 + 50 * uu[0])
            radius = 10
            pygame.draw.circle(screen, vector_color, center, radius)
            pygame.time.wait(300)
            pygame.display.update()
        


#Close the window and quit
pygame.quit()
