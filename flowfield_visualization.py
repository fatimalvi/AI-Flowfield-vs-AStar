import pygame
from flowfield_implementation import FlowField
from random import randint

pygame.init()


#grid dict to store, goal, obstacles and free nodes
test_grid={}

#user will specify the grid size, they'll have 4 sizes to choose from
GRID_SIZE = int(input("choose a grid size from 8, 10, 12 or 14: "))


#the box size will remain 50 * 50 no matter what grid size, for better visualization
BOX_SIZE = 50

#if user enters a grid size other than the 4 given, ask user to enter size again until they enter a correct one
while GRID_SIZE not in [8, 10, 12, 14]:
    GRID_SIZE = int(input("enter a valid grid size: "))

obs_Num = int(input("Choose the number of obstacles: "))

#depending on the grid size, generate the screen size and number of obstacles
if(GRID_SIZE==8):
    screenh, screenw = 410, 800
    # obs_Num = 20

elif(GRID_SIZE==10):
    screenh, screenw = 510, 900
    # obs_Num = 20

elif(GRID_SIZE==12):
    screenh, screenw = 610, 1000
    # obs_Num = 17

else:
    screenh, screenw = 710, 1100
    # obs_Num = 24

#set up the pygame screen
screen = pygame.display.set_mode((screenw, screenh))

#generating random start coordinates for the first object
sx1=randint(0,GRID_SIZE-1)
sy1=randint(0,GRID_SIZE)

#generating random start coordinates for the second object
sx2=randint(0,GRID_SIZE-1)
while(sx2==sx1):
    sx2=randint(0,GRID_SIZE-1)

sy2=randint(0,GRID_SIZE-1)
while(sy2==sy1):
    sy2=randint(0,GRID_SIZE-1)

#generating coordinates for the goal node
ex=randint(0,GRID_SIZE-1)
while(ex==sx1 or ex==sx2):
    ex=randint(0,GRID_SIZE-1)

ey=randint(0,GRID_SIZE-1)
while(ey==sy1 or ey==sy2):
    ey=randint(0,GRID_SIZE-1)

#initializing the start node and goal node according to box size based on random number generated
start1_x, start1_y = BOX_SIZE*sx1, BOX_SIZE*sy1
start2_x, start2_y = BOX_SIZE*sx2, BOX_SIZE*sy2
goal_x, goal_y = BOX_SIZE*ex, BOX_SIZE*ey

pygame.display.set_caption("Flow Field Visualization")
icon = pygame.image.load("machine-learning.png")
pygame.display.set_icon(icon)

#will use this to get any user inputs
base_font=pygame.font.Font(None, 32)
grid_font=pygame.font.Font(None, 32)
user_text=""

#starts at 200, 200 and is 140 pixels wide and 32 pixels high
input_rect = pygame.Rect(200,200,140, 32)
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("gray15")
color = color_passive

vector_color=(255, 105, 180)
obstacle_color = (199, 21, 133)
bg_color = (230,230,250)
rect_color = (199, 21, 133)
text_color_g = (75, 0, 130)

active = False

#this obj will be a randomly generated object by player in one of the grid boxes which will follow the flowfield to goal
objimg1=pygame.image.load("happy.png")
objimg2=pygame.image.load("party.png")


#function for the objects
def obj_one(x,y):
    screen.blit(objimg1, (x, y))

def obj_two(x,y):
    screen.blit(objimg2, (x, y))

#will store all the obstacles here, they are randomly generated
obstacle_list=[]
for i in range(obs_Num):
    xcor=randint(0, GRID_SIZE-1)
    ycor=randint(0, GRID_SIZE-1)
    o_r=(xcor*BOX_SIZE, ycor*BOX_SIZE, BOX_SIZE, BOX_SIZE)

    #obstacles should never be equal to goal or start nodes
    while(o_r in obstacle_list or o_r==(goal_x, goal_y, BOX_SIZE, BOX_SIZE) or o_r==(start1_x, start1_y, BOX_SIZE, BOX_SIZE) or o_r==(start2_x, start2_y, BOX_SIZE, BOX_SIZE)):
        xcor=randint(0, GRID_SIZE-1)
        ycor=randint(0, GRID_SIZE-1)
        o_r=(xcor*BOX_SIZE, ycor*BOX_SIZE, BOX_SIZE, BOX_SIZE)
    obstacle_list.append(o_r)

#generating our test grid here to apply flowfield on it
rect_grid = []
for i in range(GRID_SIZE):
    rect_row = []
    for j in range(GRID_SIZE):
        rect = pygame.Rect(i * BOX_SIZE, j * BOX_SIZE, BOX_SIZE, BOX_SIZE)
        rect_row.append(rect)
        if(tuple(rect) in obstacle_list):
            test_grid[tuple(rect)]="obstacle"
        else:
            test_grid[tuple(rect)]="free"
    rect_grid.append(rect_row)


#initializing our flow field here
x = FlowField(test_grid, (goal_x, goal_y, BOX_SIZE, BOX_SIZE), [(start1_x, start1_y, BOX_SIZE, BOX_SIZE), (start2_x, start2_y, BOX_SIZE, BOX_SIZE)], BOX_SIZE, GRID_SIZE, 2)

#generating cost field based on goal, obstacles and free node values
x.costfield()

#generating integration field to calculate cost for one node to reach another
x.integrationfield()

#selecting the best node to go to next
x.best_vectors()

#finding shortest path through the best nodes
follow = x.shortest_path()


#flags to deal with each stage of flowfield on the pygame window
running=True
flag_grid=True
flag_cost=False
flag_integ=False
flag_vec=False
flag_obj=False

#generates boxes for each stage
costF_rect = pygame.Rect((GRID_SIZE*BOX_SIZE)+100, 50, 200, 50)
integF_rect = pygame.Rect((GRID_SIZE*BOX_SIZE)+60, 150, 270, 50)
vec_rect = pygame.Rect((GRID_SIZE*BOX_SIZE)+90, 250, 225, 50)
obj_rect = pygame.Rect((GRID_SIZE*BOX_SIZE)+135, 350, 135, 50 )

#finding start nodes and their corresponding paths i.e the path of objects and storing them
for k,v in follow.items():
    vector_field1 = v
    #print("v: ",vector_field1)
    obj1 = k
    obj1x = obj1[0]
    obj1y = obj1[1]
del follow[obj1]
for k,v in follow.items():
    vector_field2 = v
    #print("v: ",vector_field1)
    obj2 = k
    obj2x = obj2[0]
    obj2y = obj2[1]

#until user doesnt quit
while running:
    #set bg color
    screen.fill(bg_color)

    #check for all events like mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if costF_rect.collidepoint(event.pos):
                if flag_integ==True:
                    flag_integ=False
                if flag_vec==True:
                    flag_vec=False
                flag_cost = True
            if ((integF_rect.collidepoint(event.pos) and flag_cost==True) or (integF_rect.collidepoint(event.pos) and flag_vec==True)):
                if flag_vec == True:
                    flag_vec = False
                flag_cost=False
                flag_integ=True
            if vec_rect.collidepoint(event.pos) and flag_integ == True:
                flag_integ=False
                flag_vec=True
            if obj_rect.collidepoint(event.pos) and flag_vec==True:
                flag_obj=True

        if event.type == pygame.KEYDOWN:
            if active==True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    #generate main grid with obstacles here
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if(flag_cost==True or flag_integ==True or flag_vec==True):
                pygame.draw.rect(screen, rect_color, rect_grid[i][j], 1)
                if(test_grid[tuple(rect_grid[i][j])]=="obstacle"):
                    pygame.draw.rect(screen, obstacle_color, rect_grid[i][j])
            else:
                pygame.draw.rect(screen, rect_color, rect_grid[i][j], 1)

    #GENERATING COST FIELD
    pygame.draw.rect(screen, (106,90,205), costF_rect)
    cost_box_text = base_font.render("generate cost field", True, (0, 0, 0))
    screen.blit(cost_box_text, (costF_rect.x+2, costF_rect.y+11))
    if(flag_cost == True):
        for i in x.integration_field:
            if(i==x.goal_pt):
                text_surface = grid_font.render(str(x.cost_field[i]), True, (0, 0, 255))
            else:
                text_surface = grid_font.render(str(x.cost_field[i]), True, text_color_g)
            screen.blit(text_surface, (i[0]+5, i[1]+5))

    #GENERATING INTEGRATION FIELD
    pygame.draw.rect(screen, (123,104,238), integF_rect)
    integ_box_text = base_font.render("generate integration field", True, (0, 0, 0))
    screen.blit(integ_box_text, (integF_rect.x+2, integF_rect.y+11))
    if(flag_integ == True):
        for i in x.integration_field:
            if(i==x.goal_pt):
                text_surface = grid_font.render(str(x.integration_field[i]), True, (0, 0, 255))
            else:
                text_surface = grid_font.render(str(x.integration_field[i]), True, text_color_g)
            screen.blit(text_surface, (i[0]+5, i[1]+5))
        #     if flag_grid==True:
        #         pygame.time.wait(25)
        #         pygame.display.update()
        # flag_grid=False

    #GENERATING VECTOR FIELD
    pygame.draw.rect(screen, (147,112,219), vec_rect)
    vector_box_text = base_font.render("generate vector field", True, (0, 0, 0))
    screen.blit(vector_box_text, (vec_rect.x+2, vec_rect.y+11))
    if(flag_vec==True):
        h=BOX_SIZE//2
        b=BOX_SIZE
        for i in x.vector_field:
            e=x.vector_field[i]
            if e==(None, None):
                continue
            #print(e)
            s_x=int(i[0])
            s_y=int(i[1])

            e_x=int(e[0])
            e_y=int(e[1])
            if(e_x > s_x and e_y > s_y):
                pygame.draw.line(screen, vector_color, (s_x, s_y), (e_x, e_y), 4)
            elif(s_x == e_x and e_y > s_y):
                pygame.draw.line(screen, vector_color, (s_x+h, s_y), (e_x+h, e_y), 4)
            elif(s_x > e_x and s_y < e_y):
                pygame.draw.line(screen, vector_color, (s_x+b, s_y), (e_x+b, e_y), 4)
            elif(s_x < e_x and s_y == e_y):
                pygame.draw.line(screen, vector_color, (s_x, s_y+h), (e_x, e_y+h), 4)
            elif(s_x > e_x and s_y == e_y):
                pygame.draw.line(screen, vector_color, (s_x+b, s_y+h), (e_x+b, e_y+h), 4)
            elif(e_x > s_x and e_y < s_y):
                pygame.draw.line(screen, vector_color, (s_x, s_y+b), (e_x, e_y+b), 4)
            elif(e_x<s_x and e_y < s_y):
                pygame.draw.line(screen, vector_color, (s_x+b, s_y+b), (e_x+b, e_y+b), 4)
            else:
                pygame.draw.line(screen, vector_color, (s_x+h, s_y+b), (e_x+h, e_y+b), 4)
            
            if flag_grid==True:
                pygame.time.wait(25)
                pygame.display.update()
        flag_grid=False


    #GENERATING OBJECT
    pygame.draw.rect(screen, (72,61,139), obj_rect)
    obj_box_text = base_font.render("move object", True, (0, 0, 0))
    screen.blit(obj_box_text, (obj_rect.x+2, obj_rect.y+11))
    if(flag_obj==True and len(vector_field1)>0):
        # if(objx==start_x and objy==start_y):
        #     obj(objx+10, objy+10)
        if(len(vector_field1)>0):
            obj_one(obj1x+10, obj1y+10)
            obj1x=vector_field1[0][0]
            obj1y=vector_field1[0][1]
            del vector_field1[0]
            # print("x: ",objx)
            # print("y: ", objy)
            if (len(vector_field2)==0):
                pygame.time.wait(500)
                pygame.display.update()
    
    if(flag_obj==True and len(vector_field2)>0):
        # if(objx==start_x and objy==start_y):
        #     obj(objx+10, objy+10)
        if(len(vector_field2)>0):
            obj_two(obj2x+10, obj2y+10)
            obj2x=vector_field2[0][0]
            obj2y=vector_field2[0][1]
            del vector_field2[0]
            # print("x: ",objx)
            # print("y: ", objy)
            pygame.time.wait(500)
            pygame.display.update()
    if (obj2x==goal_x and obj2y==goal_y):
        obj_two(obj2x+10, obj2y+10)
    if (obj1x==goal_x and obj1y==goal_y):
        obj_one(obj1x+10, obj1y+10)

    
    pygame.display.update()