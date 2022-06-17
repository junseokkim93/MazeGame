import random
import argparse
from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Move(Enum):
    UP = -1, 0
    LEFT = 0, -1
    DOWN = 1, 0
    RIGHT = 0, 1
  
class Maze:
    
    def __init__(self, size, save_animation=False):
        self.size = size
        self.lr = None
        self.lc = None
        self.cluster_dict = None
        self.wall_coord_list = None
        self.maze_history = []
        self.maze = self.generate(save_animation)
        self.solve_history = []
        
    def initialize_subplot(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 8))
        
    def maze_update(self, i):
        self.ax.imshow(self.maze_history[i])
        self.ax.set_title("Step {}".format(i), fontsize=10)
        self.ax.set_axis_off()
        
    def solve_update(self, i):
        self.ax.imshow(self.solve_history[i], cmap="inferno")
        self.ax.set_title("Step {}".format(i), fontsize=10)
        self.ax.set_axis_off()
        
    def initialize_maze(self):
        """initialize the maze filled with the wall"""
        n_r,n_c = self.size
        vmin = 50
        vmax = 255
        self.lr = n_r + n_r + 1
        self.lc = n_c + n_c + 1
        
        maze = np.zeros([self.lr, self.lc], dtype=np.int16)
        values = np.linspace(vmin, vmax, n_r * n_c, dtype=np.int16).reshape(n_c, n_r)
        k = 0
        
        for i in range(1,self.lr,2):
            for j in range(1,self.lc,2):
                maze[i][j] = values.flatten()[k]
                k+=1
        
        return maze
        
    def initialize_cluster(self):
        # example: {[1,1]:[[x1,x2,...], [y1,y2,...]], ...}
        ys = [y for y in range(1, self.lc, 2)]*3
        coords = [(x,y) for x in range(1, self.lr, 2) for y in range(1, self.lc, 2)]

        return {coord: [[coord[0]],[coord[1]]] for coord in coords}
   
    def ret_mv_direction(self, x, y):
        ret_set = set([direction for direction in Move])
        if x==1:
            ret_set.remove(Move.UP)
        if y==1:
            ret_set.remove(Move.LEFT)
        if x==len(self.maze)-2:
            ret_set.remove(Move.DOWN)
        if y==len(self.maze[0])-2:
            ret_set.remove(Move.RIGHT)    
        
        return ret_set
        
    @property    
    def single_value_left(self):
        values_2d_list = [[row[col] for col in range(1,self.lc,2)] for row in self.maze][1:-1:2]
        values_1d_list = [value for values_list in values_2d_list for value in values_list]
        values_set = set(values_1d_list)

        return len(values_set)==1
        
    def get_wall_coord_list(self):
        get_wall_coord_list = []
        for i in range(1,self.lr-1):
            for j in range(1,self.lc-1):
                if i%2 == 1 and j%2 == 0:
                    get_wall_coord_list.append((i,j))
                elif i%2 == 0 and j%2 == 1:
                    get_wall_coord_list.append((i,j))

        return get_wall_coord_list
        
    @staticmethod
    def get_coord_given_move(input_coord, *movable_directions):
        # print("input: {}, directions: {}".format(input_coord, movable_directions))
        # print([[coord1 + coord2 for coord1,coord2 in zip(input_coord,direction.value)] for direction in movable_directions])
        return [[coord1 + coord2 for coord1,coord2 in zip(
                    input_coord,direction.value)] for direction in movable_directions]
        
        
        
    def get_cluster_coords(self,coord):
        x,y = coord[0],coord[1]
        
        return self.cluster_dict.get((x,y))
        
    def update_cluster(self, affecting_coord, affected_coord, rand_wall_coord):
        affected_coord = tuple(affected_coord)
        affecting_coord = tuple(affecting_coord)
        
        cluster_coords = self.cluster_dict[affecting_coord] # [[x1,...], [y1,...]]

        xs = self.cluster_dict[affected_coord][0]
        ys = self.cluster_dict[affected_coord][1]
        for x in xs:
            cluster_coords[0].append(x)
        for y in ys:
            cluster_coords[1].append(y)

        cluster_coords[0].append(rand_wall_coord[0])
        cluster_coords[1].append(rand_wall_coord[1])
        
        for x,y in zip(cluster_coords[0], cluster_coords[1]):
            if [x,y] not in self.wall_coord_list and (x,y) != affecting_coord:    
                self.cluster_dict[(x,y)] = self.cluster_dict[affecting_coord]
        
    def merged_clusters(self, rand_wall_coord, *movable_directions):
    
        neighbor_coords = self.get_coord_given_move(rand_wall_coord, *movable_directions)
        affecting_coord = random.choice(neighbor_coords)

        if self.maze[neighbor_coords[0][0],
                    neighbor_coords[0][1]] != self.maze[neighbor_coords[1][0],
                                                        neighbor_coords[1][1]]:
            neighbor_coords.remove(affecting_coord)
            affected_coord = neighbor_coords.pop()
            cluster_coords = self.get_cluster_coords(affected_coord)
            self.maze[cluster_coords[0], cluster_coords[1]] = self.maze[affecting_coord[0],affecting_coord[1]]
            self.maze[rand_wall_coord] = self.maze[affecting_coord[0],affecting_coord[1]]
            
            self.update_cluster(affecting_coord, 
                                affected_coord, 
                                rand_wall_coord)
            return True
            
        return False
        
    def generate(self, save_animation):
        """geerate a maze using Kruskal's Algorithm"""
        n_r, n_c = self.size
        print("Generating a {}x{} maze...".format(n_r, n_c))
        self.maze = self.initialize_maze()
        self.cluster_dict = self.initialize_cluster()
        self.wall_coord_list = self.get_wall_coord_list()
        wall_coord_list = self.wall_coord_list.copy()
        count = 0
        while not self.single_value_left:
           
            rand_wall_coord = random.choice(wall_coord_list)
            movable_directions = self.ret_mv_direction(*rand_wall_coord)
            
            if (movable_directions == set([Move.UP, Move.DOWN, Move.RIGHT]) or
                movable_directions == set([Move.UP, Move.DOWN, Move.LEFT])):
                merged = self.merged_clusters(rand_wall_coord, Move.UP, Move.DOWN)
                
            elif (movable_directions == set([Move.LEFT, Move.RIGHT, Move.DOWN]) or 
                  movable_directions == set([Move.LEFT, Move.RIGHT, Move.UP])):
                merged = self.merged_clusters(rand_wall_coord, Move.LEFT, Move.RIGHT)
                
            else:
                neighbor_coords = self.get_coord_given_move(rand_wall_coord, Move.LEFT, Move.RIGHT)
                if self.maze[neighbor_coords[0][0],
                            neighbor_coords[0][1]] == self.maze[neighbor_coords[1][0],
                                                                neighbor_coords[1][1]] == 0:
                    merged = self.merged_clusters(rand_wall_coord, Move.UP, Move.DOWN)
                else:
                    merged = self.merged_clusters(rand_wall_coord, Move.LEFT, Move.RIGHT)
              
            if merged:
                wall_coord_list.remove(rand_wall_coord)

                if save_animation:
                    self.maze_history.append(self.maze.copy())
   
        if save_animation:
            self.initialize_subplot()
            anim = FuncAnimation(self.fig, 
                                self.maze_update, 
                                frames=range(len(self.maze_history)), 
                                interval=500)
            anim.save("maze_generation_{}x{}.gif".format(*self.size))
            
        print("Maze generation complete.")
        
        return self.maze
        
    def solve(self, algo:str, start_coord, goal_coord, save_animation=False):
        print("Start: {}, Goal: {}".format(start_coord, goal_coord))
        print("Solving generated maze using {}...".format(algo))
        self.maze = self.maze / np.max(self.maze) * 255 
        
        if algo=="DFS":
            solved = self.solve_with_DFS(start_coord, goal_coord, save_animation)
        elif algo=="BFS":
            solved = self.solve_with_BFS(start_coord, goal_coord, save_animation)
        elif algo=="A*":
            solved =self.solve_with_Astar(start_coord, goal_coord, save_animation)
        # return Bool to show success or fail?
        return solved
        
    def solve_with_BFS(self, start_coord, goal_coord, save_animation=False):
        pass
        
    def solve_with_DFS(self, start_coord, goal_coord, save_animation=False):
        to_visit_stack = [start_coord]
        visited = []
        self.solve_history = []
        maze = self.maze.copy()
        # absolute_wall = [[x,y] for x in range(2,self.lr-1,2) for y in range(2,self.lc-1,2)] # need to define the unchangeable walls
        walkable = [[x,y] for x,y in zip(self.maze.nonzero()[0], self.maze.nonzero()[1])]

        while to_visit_stack != []:
            coord_to_visit = to_visit_stack.pop()
            maze[coord_to_visit[0], coord_to_visit[1]] = 125
            self.solve_history.append(maze.copy())
            visited.append(coord_to_visit)

            if coord_to_visit == goal_coord:
                if save_animation:
                    self.initialize_subplot()
                    anim = FuncAnimation(self.fig, 
                                        self.solve_update, 
                                        frames=range(len(self.solve_history)), 
                                        interval=500)
                    anim.save("DFS_solution_{}x{}.gif".format(*self.size))
                return True
                
            movable_directions = self.ret_mv_direction(*coord_to_visit)
            neighbor_coords = self.get_coord_given_move(coord_to_visit, *movable_directions)
            neighbors = [neighbor for neighbor in neighbor_coords if (
                        neighbor in walkable and neighbor not in visited)]
                    
            for neighbor in neighbors:
                to_visit_stack.append(neighbor)

        return False       
        
    def solve_with_Astar(self, start_coord, goal_coord, save_animation=False):
        pass
            

def run(row,col, algo, save_gen_animation, save_sol_animation):

    # size = (args.row, args.col)\
    size = (row, col)
    amazing_maze = Maze(size, save_gen_animation)
    start_coord = [1,1]
    goal_coord = [amazing_maze.lr-2, amazing_maze.lc-2]

    solved = amazing_maze.solve(algo, start_coord, goal_coord, save_sol_animation)
    if solved:
        print("Finished solving a maze.")
    else:
        print("Maze could not be solved.")

# if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("row", help="row component of the maze size (row, col)",
                        # type=int)
    # parser.add_argument("col", help="column component of the maze size (row, col)",
                        # type=int)
    # parser.add_argument("-algo", "--search_algorithm", help="increase output verbosity",
                        # choices = ["DFS", "BFS", "A*"],
                        # default = "DFS",
                        # type=str)
    # args = parser.parse_args()
    
    # main()
