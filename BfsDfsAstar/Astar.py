# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:40:20 2018

@author: Jeremy Midvidy

EECS 348, Lab 1 - Part Two
Winter 2018
"""

##################################################

#----------- A-star IMPLEMENTATION --------------#

##################################################

def a_star_search (dis_map, time_map, start, end):
    
    #initialize useful variables
    scores = {}
    
    g = time_map
    h = dis_map
    
    OPEN = {start : 100}
    CLOSED = set() 
    dist_dict = {}
    firstIter = 0
    
    curr = start
        
    while (5 != 2):        
        # ------- choose next curr out options in OPEN with lowest F-score --------------#
        
        if firstIter == 0:
            curr = start
            firstIter = 10
            
        else:
            #find lowest f-score in the dictionary of {{OPEN KEY: F-SCORE}}
            minScore = 1000
            for key in OPEN:
                if OPEN[key] < minScore:
                    minScore = OPEN[key]
            
            #go through the OPEN dict and add keys with lowest f-score to the list
            keys_With_Lowest_F_Score = []
            for key in OPEN:
                if OPEN[key] == minScore:
                  keys_With_Lowest_F_Score.append(key)
                  
            #if there is more than one with the same F-score, proritize alphabetically
            #else, the first element of the list is now the curr
            if len(keys_With_Lowest_F_Score) > 1:
                s = sorted(keys_With_Lowest_F_Score)
                curr = s[0]
            else:
                curr = keys_With_Lowest_F_Score[0]   
        
        #if we get curr to become end, path found        
        if curr == end:
            break
                
        # --------------------- now that curr is chosen ---------------------------------- #
        # -------- compute F-score for each neighbor and store it in currScores ---------- #   
        
        currScores = {}
        
        #only consider neighbors with actual connections
        g_dict_unclean = g[curr]
        neighbours = {}
        for key in g_dict_unclean:
            if  g_dict_unclean[key] != None:
                neighbours[key] = g_dict_unclean[key]
        
        for node in neighbours: 
            #g(x)
            g_val = neighbours[node] 
            if curr in dist_dict:
                g_val = g_val + dist_dict[curr]
            
            #h(x)
            h_dict = h[node]
            h_val = h_dict[end]
        
            #f(x) = g(x) + h(v)
            f_val = g_val + h_val
            
            #add to current scores dictionary
            currScores[node] = f_val
            
        #add currnt explored neighbours to total list for output
        scores[curr] = currScores
                
        #update OPEN and CLOSED sets 
        for key in currScores:
            elem = currScores[key]
            if key in CLOSED:
                continue
            else:
                #add key and corresponding f-score to dictionary
                OPEN[key] = elem 
                
                #update distance key for further calculation
                dist_dict[key] = elem - h[key][end]          
                    
        del OPEN[curr]
        CLOSED.add(curr)

    return scores
