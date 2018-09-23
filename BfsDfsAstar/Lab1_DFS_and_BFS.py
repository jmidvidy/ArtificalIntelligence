# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:07:07 2018

@author: Jeremy Midvidy

EECS 348, Lab 1
Winter 2018
"""
import copy


##################################################

#----------- HELPER FUNCTIONS -------------------#

################################################## 

#small helper to find the correct path for BFS
#dont need this for DFS because it has a stack
def findPathForBFS(m, start_r, start_c, end_r, end_c, nodesList):
    #initialize useful variables
    e = [end_r, end_c]
    
    #create path for pathfinding
    path = []
    path.append(e)
    
    #start at end and find path back to top
    rnodes = nodesList[::-1]
    for i in range(1, len(rnodes)-1):
        row = rnodes[i]
        prevPoint = path[len(path) - 1]
        prev_r = prevPoint[0]
        prev_c = prevPoint[1]
        for point in row:
            r = point[0]
            c = point[1]
            
            #can't move diagnoally
            if r == prev_r and abs(c - prev_c) == 1:
                path.append(point)
            if c == prev_c and abs(r - prev_r) == 1:
                path.append(point)    
    return path

    #make sure this algorithm will work for all cases

##################################################

#----------- DEPTH FIRST SEARCH -----------------#

##################################################

def dfs(testmap):
    
    #initalize useful variables
    MAP_HEIGHT = len(testmap)
    MAP_WIDTH = len(testmap[0])
    m = copy.deepcopy(testmap) #not to mutate testmap
    
#    #want to split rows from String into list of chars
#    for i in range(0, MAP_HEIGHT):
#        m[i] = list(m[i])
    
    #find start location signaled by digit 2
    start_r, start_c = 0,0
    for r in range(0, MAP_HEIGHT):
        for c in range(0, MAP_WIDTH):
            if m[r][c] == 2:
                start_r, start_c = r , c
                break
    
    #start depth-first search
    searchTree = [] #keep track of position within tree
    optimalTree = [[]]
    found = [False]
    
    #recursive algorithm of DFS implementation
    #subfunction makes it easier to recurse without calling other elements
    def depthFirstSearch(r, c):
        
        #keeps track of locatin within tree
        searchTree.append([r,c])
        
        #if the start is the end goal, set loc = 5 and return
        if m[r][c] == 3:
            found[0] = True
            found.append([r,c])
            optimalTree[0] = copy.deepcopy(searchTree)
            return 
        if m[r][c] != 2: #else set this loc equal to 4, meaning visited, and do dfs
            m[r][c] = 4
            
        # ----------------- see if can do R, D, L, U in that order ----------------- #
        
        #if R is a 0 (can't be 1 or 4) and in range
        if c+1 < MAP_WIDTH and (m[r][c+1] == 0 or m[r][c+1] == 3):
            depthFirstSearch(r, c+1)
            if found[0]:
                return found[1]
                #added this within each call rather than next part
                #to avoid problems with tail recursion
        
        #can't R, go D
        #need to check if D is 0 and in range
        if r+1 < MAP_HEIGHT and (m[r+1][c] == 0 or m[r+1][c] == 3):
            depthFirstSearch(r+1, c)
            if found[0]:
                return found[1]
            
        #can't D, go L
        #need to check if L is 0 and in range
        if c > 0 and (m[r][c-1] == 0 or m[r][c-1] == 3):
            depthFirstSearch(r, c-1)
            if found[0]:
                return found[1]
            
        #cant L, go U
        #need to check if U is 0 and in range
        if r > 0 and (m[r-1][c] == 0 or m[r-1][c] == 3):
            depthFirstSearch(r-1 ,c)
            if found[0]:
                return found[1]
            
            
        # ------------------ if can't do any, go back up a branch, and do dfs along different leaf ------------ #        
        
        #get rid of current position on searchTree
        searchTree.pop() 
        
        #test to see if back at top node
        if (len(searchTree) == 0): 
            prev = [start_r, start_c]
        else:
            prev = searchTree[len(searchTree) - 1] #access previous leaf
            searchTree.pop() #new current will be added on next iteration
        
        #assign next coordinates to be last DFS parent on tree
        prev_r = prev[0]
        prev_c = prev[1]
        
        #must be a solution for these problems
        if(not found[0]):
            depthFirstSearch(prev_r, prev_c)  
        return
    
    #call dfs
    depthFirstSearch(start_r, start_c)   
    
    #fill in starting point with 5
    m[start_r][start_c] = 5

    #fill in the path with 5s
    path = optimalTree[0]
    for row in path:
        r = row[0]
        c = row[1]
        m[r][c] = 5
        
    return m
    

##################################################

#----------- BREADTH FIRST SEARCH ---------------#

##################################################


def bfs(testmap):
    
    #initalize useful variables
    MAP_HEIGHT = len(testmap)
    MAP_WIDTH = len(testmap[0])
    m = copy.deepcopy(testmap) #not to mutate testmap
    
    #want to split rows from String into list of chars
    for i in range(0, MAP_HEIGHT):
        m[i] = list(m[i])
    
    #find start location signaled by digit 2
    start_r, start_c = 0,0
    for r in range(0, MAP_HEIGHT):
        for c in range(0, MAP_WIDTH):
            if m[r][c] == 2:
                start_r, start_c = r , c
                break
    
    #keeps track of goal state
    found = [False]
    end = [[]]
    nodesList = [[start_r, start_c]]
    
    #recursive algorithm of BFS implementation
    #subfunction makes it easier to recurse without calling other elements
    def breathFirstSearch(nodes):
        
        nextNodes = []
        
        #check to see whether any of the nodes at the current level are the desired end node
        for node in nodes:
            r = node[0]
            c = node[1]
            
            #if the start is the end goal, return
            if m[r][c] == 3:
                found[0] = True
                end[0] = [r,c]
                break 
            if m[r][c] != 2 and not found[0]: #else set this loc equal to 4, meaning visited, and do bfs
                m[r][c] = 4
            
            
            # ----------------- for each node at this level, see if can do R, D, L, U ----------------- #
            # ---------------- if possible, add that coordinate to the next node list --------------- #
           
            # must be a solution in this case, so don't worry about no solution
            # again, included return statement in each if to avoid problems with tail recurison
            
            #if R is a 0 (can't be 1 or 4) and in range
            if c+1 < MAP_WIDTH and (m[r][c+1] == 0 or m[r][c+1] == 3):
                nextNodes.append([r, c+1])
                if found[0]:
                    return
    
            #can't R, go D
            #need to check if D is 0 and in range
            if r+1 < MAP_HEIGHT and (m[r+1][c] == 0 or m[r+1][c] == 3):
                nextNodes.append([r+1, c])
                if found[0]:
                    return
                
            #can't D, go L
            #need to check if L is 0 and in range
            if c > 0 and (m[r][c-1] == 0 or m[r][c-1] == 3):
                nextNodes.append([r, c-1])
                if found[0]:
                    return
                
            #cant L, go U
            #need to check if U is 0 and in range
            if r > 0 and (m[r-1][c] == 0 or m[r-1][c] == 3):
                nextNodes.append([r-1, c])
                if found[0]:
                    return


        #make recursive call
        if found[0]:
            return
        nodesList.append(nextNodes)
        breathFirstSearch(nextNodes)
        return
    
    #call the function
    breathFirstSearch([[start_r, start_c]])
    
    #call helper to back-propogate path in BFS
    path = findPathForBFS(m, start_r, start_c, end[0][0], end[0][1], nodesList)
    
    #convert path to 5s
    m[start_r][start_c] = 5
    for row in path:
        r = row[0]
        c = row[1]
        m[r][c] = 5  
    
    return m
