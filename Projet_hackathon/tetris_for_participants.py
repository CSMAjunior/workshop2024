# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 23:41:58 2024

@author: GROLET
"""

import numpy as np
from matplotlib import pyplot as plt
plt.close('all')

#%% 
class state:
    # game state 
    # to be used in the decision algorithm
    # return the game state as seen by the 'player' (not all game info are given)
    def __init__(self, grid, b, list_actions):
        self.grid = grid  # H x L matrix
        self.block = b    # block
        self.list_actions = list_actions # list of available action for the current block

class action_gene:
    # game generalised action 
    def __init__(self, x, r):
        self.trans = x
        self.rot = r
    
class block:
    # define the different types of blocks
    def __init__(self, type):
        self.mask = []
        if type == 0: # 2x1 block
            self.type = 0   # block type in the game process
            self.value = 1  # value in grid for the block
            self.color = [255, 0, 0]
            self.rot = 2 # Number of possible rotations
            self.width = [ 1, 2]
            self.height =[ 2, 1]
            self.mask.append(np.array([[1, 0], [1, 0]]))      
            self.mask.append(np.array([[0, 0], [1, 1]]))      
        elif type == 1: # 2x2 block
            self.type = 1
            self.value = 2
            self.color = [0, 0, 255]
            self.rot = 1
            self.width = [ 1, 2]
            self.height =[ 2, 1]
            self.width = [2]
            self.height = [2]        
            self.mask.append(np.array([[1, 1], [1, 1]]))      
        elif type == 2: # S block
            self.type = 2
            self.value = 3
            self.color = [155, 50, 200]
            self.rot = 2
            self.width = [2, 3]
            self.height =[3, 2]        
            self.mask.append(np.array([[1, 0], [1, 1], [0, 1]]))      
            self.mask.append(np.array([[0, 1, 1], [1, 1, 0]]))      
        elif type == 3: # S-sym block
            self.type = 3
            self.value = 4
            self.color = [200, 150, 55]
            self.rot = 2
            self.width = [2, 3]
            self.height = [3, 2]        
            self.mask.append(np.array([[0, 1], [1, 1], [1, 0]]))      
            self.mask.append(np.array([[1, 1, 0], [0, 1, 1]]))      
        elif type == 4: # L block
            self.type = 4
            self.value = 5
            self.color = [55, 200, 200]
            self.rot = 4
            self.width = [3, 2, 3, 2]
            self.height =[2, 3, 2, 3]        
            self.mask.append(np.array([[1, 0, 0], [1, 1, 1]]))      
            self.mask.append(np.array([[0, 1], [0, 1], [ 1, 1]]))      
            self.mask.append(np.array([[1, 1, 1], [0, 0, 1]]))      
            self.mask.append(np.array([[1, 1], [1, 0], [ 1, 0]]))      
        elif type == 5: # L-sym block
            self.type = 5
            self.value = 6
            self.color = [50, 70, 150]
            self.rot = 4
            self.width = [3, 2, 3, 2]
            self.height =[2, 3, 2, 3]        
            self.mask.append(np.array([[0, 0, 1], [1, 1, 1]]))      
            self.mask.append(np.array([[1, 1], [0, 1], [ 0, 1]]))      
            self.mask.append(np.array([[1, 1, 1], [1, 0, 0]]))      
            self.mask.append(np.array([[1, 0], [1, 0], [ 1, 1]]))      
        elif type == 6: # 3x1 block
            self.type = 6
            self.value = 7
            self.color = [150, 30, 150]
            self.rot = 2
            self.width = [1, 3]
            self.height =[3, 1]        
            self.mask.append(np.array([[1, 0, 0], [1, 0, 0],[1, 0, 0]])) 
            self.mask.append(np.array([[0, 0, 0], [0, 0, 0],[1, 1, 1]]))      
        else: # -1 = error block
            self.type = -1
            self.value = -1
            self.color = [0, 0, 0]
            self.width = 1
            self.height = 1        
            self.mask = []     
            
    def print_block(self, rot=0):
        # plot the current block in a separate figure
        Nb = np.max((self.width[rot],self.height[rot]))
        Color_array_b = np.zeros((Nb, Nb , 3),dtype=np.uint8) + 255 #default white
        for i in range(self.width[rot]):
            for j in range(self.height[rot]):
                if self.mask[rot][-1-j,i] ==1:
                    Color_array_b[-1-j, i,:]  = self.color
        plt.imshow(Color_array_b, interpolation='nearest')
        self.print_current_block_lines(rot)
        plt.show()
        
    def print_current_block_lines(self,rot=0):
        # Nb = 3
        Nb = np.max((self.width[rot],self.height[rot]))
        x = np.linspace(0, Nb, Nb+1) - 0.5
        y = np.linspace(0, Nb, Nb+1) - 0.5
        for i in range(Nb):
            plt.plot(np.ones(Nb+1)*x[i], y, 'k')
        for i in range(Nb):
            plt.plot(x, np.ones(Nb+1)*y[i],'k')
                
class game:
    def __init__(self, L, H, fig=False,list_block = None):
        # grid size
        self.L = L
        self.H = H
        # initialise empty grid
        self.grid = np.zeros([H, L])
        # define block and action list
        Nbloc = 7
        self.Nbloc = Nbloc
        self.block_list = []
        self.list_block = list_block
        self.history_block = []
        self.actions = []      # actions[bloc_type][rot]
        for i in range(Nbloc):
            # create new block and append
            self.block_list.append(block(i))
            # define action list
            b_action = []
            for r in range(self.block_list[-1].rot): # action for each rotation state
                b_action.append([k for k in range(L-self.block_list[-1].width[r]+1)])         
            self.actions.append(b_action)
        # initialize initial current block at random
        if self.list_block is not None:
            self.current_bloc = self.list_block[0] # np.random.randint(Nbloc)
        else:
            self.current_bloc = np.random.randint(Nbloc)
        if fig:
            # define figures
            self.fig_grid = plt.figure()
            plt.subplot(1,2,1)
            plt.title('Game State')
#            self.fig_current_block = plt.figure()
            plt.subplot(1,2,2)
            plt.title('Current Block')
        
    def return_game_state(self):
        grid = self.grid
        block = self.block_list[self.current_bloc]
        list_actions = self.actions[self.current_bloc]
        s = state(grid, block, list_actions)
        return s

    def update_game_state(self, action_gene):
        # update the grid by positioning the current bloc in rotation state rot 
        # in the column indicated by the input variable 'action'
        rot = action_gene.rot
        trans = action_gene.trans        

        # retreive current block properties
        b = self.block_list[self.current_bloc]
        # find where to put the block
        y_max = self.find_max_y(b, action_gene)  
        print('block y-position : ' + str(y_max))
        if y_max < 0:
            game_over = True
        else:
            game_over = False
            # update the matrix  TODO change the loop to account for any block shape
            for k in range(b.width[rot]):
                x_scan = trans + k
                for l in range(b.height[rot]):
                    y_scan = y_max - l
                    if self.grid[y_scan, x_scan] == 0:
                        self.grid[y_scan, x_scan] = b.mask[rot][-1-l,k]*b.value
            # set a new current block at random (use custom random fction) 
            self.history_block.append(self.current_bloc)
            if self.list_block is not None and len(self.list_block) > len(self.history_block) :
                self.current_bloc = self.list_block[len(self.history_block)]
            elif len(self.list_block) == len(self.history_block):
                game_over = True
                print("You used all the blocks in the list")
            else:
                self.current_bloc = self.random_block(self.Nbloc)
            
        return game_over
    
    def random_block(self, N):
        vec = np.random.randint(np.ones(N)*N)
        idx = np.random.randint(N)
        return vec[idx]

    def step(self, current_state, ag):
        # evaluate the grid after taking the action 'action'
        # used to evaluate a reward between two states
        rot = ag.rot
        trans = ag.trans
        b = current_state.block
        grid = current_state.grid.copy()
        # find where to put the block
        y_max = self.find_max_y(b, ag)  
        # print('block y-position step: ' + str(y_max))
        if y_max < 0:
            game_over = True
        else:
            game_over = False
            # update the matrix  TODO change the loop to account for any block shape
            for k in range(b.width[rot]):
                x_scan = trans + k
                for l in range(b.height[rot]):
                    y_scan = y_max - l
                    if grid[y_scan, x_scan] == 0:
                        grid[y_scan, x_scan] = b.mask[rot][-1-l,k]*b.value
        new_state = state(grid, current_state.block, current_state.list_actions)
        return new_state, game_over
        
    def find_max_y(self, b, ag):
        # find max hight for block position
        # x is the starting offset in x direction
        # initialise to zero
        rot = ag.rot
        x = ag.trans
        ymax = self.H-1
        # find y position of the block acording to its shape
        y_max_list = np.ones(b.width[rot])*(self.H-1)
        for k in range(b.width[rot]): # loop over the block width
            x_scan = x + k  # column to be scanned
            for j in range(self.H): # scan top to bottom
                if (self.grid[j, x_scan] > 0): # if current scan pos is occupied
                    y_max_list[k]=j-1
                    break
        for k in range(b.width[rot]): # loop over the block width
            for m in range(b.height[rot]): # search if the block start at height 0
                if b.mask[rot][-1-m,k]==1:
                    y_max_list[k] = y_max_list[k] + m
                    break
        ymax = int(min(y_max_list))

        if ymax-b.height[rot]+1 < 0:
            return -1  # block already at the top will lead to game over    
        else:     
            return ymax # block can be put inside the grid

    def get_current_H_max(self):
        # find max hight for the current grid
        # initialise to zero
        ymax = self.H-1
        # loop over the grid width
        for k in range(self.L): # TODO change the loop to account for any block shape
            # x line to be scan (from the top)
            x_scan = k
            for j in range(0,self.H): # scan top to bottom
                if (self.grid[j, x_scan] > 0):
                    yc = j-1
                    if yc < ymax:
                        ymax = yc
                    break
        return ymax # max height for the current grid
       
        
    def display_all_block_all_config(self):
        Nb = len(self.block_list)
        # fund graph size
        r_max = 1
        for b in self.block_list:
            r = b.rot
            if r > r_max:
                r_max = r
        i=0
        plt.figure()
        for b in self.block_list:
            for r in range(b.rot):
                plt.subplot(r_max, Nb, Nb*r + (i+1))
                b.print_block(r)
                plt.ylabel('rot = ' + str(r))
                if r == 0:
                    plt.title('bloc number ' + str(b.type))                    
            i=i+1
        plt.show()
        return 1
      
    def print_grid_lines(self):
        # print black lines on the game grid 
        x = np.linspace(0, self.L, self.L+1) - 0.5
        y = np.linspace(0, self.H, self.H+1) - 0.5
        for i in range(self.L):
            plt.plot(np.ones(self.H+1)*x[i], y,'k')
        for i in range(self.H):
            plt.plot(x, np.ones(self.L+1)*y[i],'k')
        plt.show()
        
    def print_game_state(self, plot_inline=True):     
        # print the game state, i.e. the grid and the current block
        block_ind = [self.grid == i+1 for i in range(self.Nbloc)]
        #Create color array for grid, default white color
        Color_array = np.zeros((self.H,self.L,3),dtype=np.uint8)+255 #default white
        for i in range(self.Nbloc):
            Color_array[block_ind[i],:] = self.block_list[i].color         
        # plot
        if plot_inline:
            # plot grid
            plt.figure(self.fig_grid.number)
            plt.subplot(1,2,1)
            plt.imshow(Color_array, interpolation='nearest')
            self.print_grid_lines()
            # print current block to be placed
            plt.subplot(1,2,2)
            self.block_list[self.current_bloc].print_block()
        nb_trou = self.L*self.H - len(np.nonzero(self.grid)[0])
        taux_remplissage = 1-nb_trou/(self.L*self.H)
        plt.title("Nombre de trou : {} ; Nombre de bloc : {} ; Taux de remplissage : {}".format(nb_trou,len(self.history_block),taux_remplissage))
        return nb_trou, len(self.history_block), taux_remplissage

def set_game_from_file(file):
    with open(file) as f:
        f.readline()
        size = np.array(f.readline().split(',')).astype(np.int16)
        f.readline()
        list_block = np.array(f.readline().split(',')).astype(np.int16)
        return game(size[0], size[1], fig=True,list_block = list_block)

#%% Student work starts here



def decision_algo(game, current_state):
    # ...
    # ...
            
                
    #return action,game_over

# G = game(5, 5, fig=True,list_block = list_block_test)
G = set_game_from_file('game_4x4_0.txt')
# display block list
G.display_all_block_all_config()
# loop until game over
keep_playing = True
while keep_playing:
    s = G.return_game_state()   # get current game state
    a,go = decision_algo(G, s)     # choose an action
    if go == True:              # check for game over
        print('GAME OVER')
        break   
    G.update_game_state(a) # update the game


nb_trou, nb_bloc, taux_remplissage = G.print_game_state()


print("Nombre de trous : {}".format(nb_trou))
print("Taux de remplissage : {}".format(taux_remplissage))
