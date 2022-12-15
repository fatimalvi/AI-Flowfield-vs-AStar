from random import randint

GRID_SIZE=8
class FlowField:
    def __init__(self, grid, goal, start, grid_box_size, grid_size, objNum):
        self.start_pt = start                   # a list that stores the start state of object
        self.goal_pt = goal
        self.grid = grid
        self.cost_field = {}
        self.objNnum = objNum
        self.integration_field = {}
        self.vector_field = {}
        self.grid_box_size=grid_box_size
        self.grid_size=grid_size

    
    def costfield(self):
        """This function will assign costs to each node
        based on the node's value"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect=(i*self.grid_box_size, j*self.grid_box_size, self.grid_box_size, self.grid_box_size)  #our node is a pygame rectangle
                # print(rect)
                if self.grid[rect] == 'free':
                    #all free rectangles will have a cost of one
                    self.cost_field[rect] = 1      
                elif self.grid[rect] == 'obstacle':
                    #all obstacles will have a very high cost since they are impassable regions
                    self.cost_field[rect]=890
                #the goal always have 0 cost
                if rect == self.goal_pt:
                    self.cost_field[rect] = 0

    #generates cost to go from goal to another node
    def integrationfield(self):
        #gives keys so that if a neighbor doesnt exist we skip
        k=self.grid.keys()
        #assigning high integration values to all nodes except obstacle and goal initially
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect=(i*self.grid_box_size, j*self.grid_box_size, self.grid_box_size, self.grid_box_size)
                if(self.grid[rect]=="obstacle"):
                    continue
                elif(self.grid[rect]=="free"):
                    self.integration_field[rect]=999
                else:
                    self.integration_field[rect]=0

        #open list starting from goal node whose curr cost is 0 
        open=[(self.goal_pt, 0)]

        #until all nodes are dealt with
        while open:
            #the current cost of reaching node
            current_cost = open[0][1]
            current_position= open[0][0]
            s=self.grid_box_size

            #divide by box size for ease
            curr_x=int(current_position[0]//s)
            curr_y=int(current_position[1]//s)

            #check all the side by side and diagonal neighbours
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x, y = curr_x + i, curr_y + j
                    curr_rect = (x*self.grid_box_size, y*self.grid_box_size, self.grid_box_size, self.grid_box_size)
                    if(curr_rect in k):
                        if(self.grid[curr_rect]=="obstacle"):
                            continue
                        # print("in")
                        #if neighbors side by side, the cost is less
                        if (i, j) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                            e_cost = 5
                        else:
                            #ensuring that goal nodes cost is always 0
                            if(curr_rect!=self.goal_pt):
                                e_cost = 7
                            else:
                                e_cost = 0
                        #generating each neighbors cost keeps changing integration field values
                        neighbour_energy = self.cost_field[curr_rect]
                        neighbour_old_energy = self.integration_field[curr_rect]
                        neighbour_new_energy = current_cost + neighbour_energy + e_cost
                        if neighbour_new_energy < neighbour_old_energy:
                            self.integration_field[curr_rect]=neighbour_new_energy
                            open.append((curr_rect, neighbour_new_energy))
            del open[0]

    
    def best_vectors(self):
        """for each node it will check which neighbor has the lowest value
        and that neighbor will be the best neighbor"""
        rects=[]
        k=self.grid.keys()
        si=self.integration_field.keys()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x=i*self.grid_box_size
                y=j*self.grid_box_size
                # print("x: ",x)
                # print("y: ",y)
                rect=tuple((x,y,self.grid_box_size,self.grid_box_size))
                # print(rect)
                if(rect not in k):
                    continue
                if(self.grid[rect]=="obstacle"):
                    continue
                if rect == self.goal_pt:
                    self.vector_field[rect] = (None, None)
                    continue
                rects.append(rect)
        # print(rects)
        for rect in rects:
            # print("rect:", rect)
            #offset has values of all neighbors
            offset=[]
            curr_x=int(rect[0]//self.grid_box_size)
            curr_y=int(rect[1]//self.grid_box_size)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x, y = curr_x + i, curr_y + j
                    curr_rect = (x*self.grid_box_size, y*self.grid_box_size, self.grid_box_size, self.grid_box_size)
                    if(curr_rect in k):
                        if(self.grid[curr_rect]=="obstacle"):
                            continue
                        else:
                            offset.append(curr_rect)
            #print(offset)
            #neghbor has nodes and their costs stored in a dict
            neigh=[]
            for r in offset:
                neigh.append({"box":r, "cost": self.integration_field[r]})
            #sorts in ascending order to pick the lowest neighbour
            neigh=sorted(neigh, key=lambda d: d["cost"])
            # print("neigh: ",neigh)
            best_n=neigh[0]["box"]
            self.vector_field[rect]=best_n

    
    def shortest_path(self):
        """goes to each node key and gets their value generated 
        as the best neighbour value in previous function"""
        result={}
        for i in self.start_pt:
            temp=[]
            rect=i
            while rect!=(None, None):
                temp.append(rect)
                rect=self.vector_field[rect]
            result[i]=temp
        return result

        #code for a single start state
        # rect=self.start_pt
        # result=[]
        # while rect!=(None, None):
        #     result.append(rect)
        #     rect = self.vector_field[rect]
        # return result


# obstacle_list=[]
# for i in range(11):
#     xcor=randint(0, GRID_SIZE-1)
#     ycor=randint(0, GRID_SIZE-1)
#     o_r=(xcor*50, ycor*50, 50, 50)
#     while(o_r in obstacle_list or o_r==(350, 100, 50, 50) or o_r==(0, 0, 50, 50)):
#         xcor=randint(0, GRID_SIZE-1)
#         ycor=randint(0, GRID_SIZE-1)
#         o_r=(xcor*50, ycor*50, 50, 50)
#     obstacle_list.append(o_r)


# test_grid={}
# rect_grid = []
# for i in range(GRID_SIZE):
#     rect_row = []
#     for j in range(GRID_SIZE):
#         rect = (i * 50, j * 50, 50, 50)
#         rect_row.append(rect)
#         if(tuple(rect) in obstacle_list):
#             test_grid[tuple(rect)]="obstacle"
#         else:
#             test_grid[rect]="free"
#     rect_grid.append(rect_row)
# x = FlowField(test_grid, (350, 100, 50, 50), (0, 0, 50, 50), 50, 8, 2)
# x.costfield()
# x.integrationfield()
# x.best_vectors()
# print(x.vector_field)
# print(x.follow_vectors())