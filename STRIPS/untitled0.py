# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:41:29 2018

@author: Jeremy Midvidy
@author Ethan Park

EECS 371 Final Project
Update This with Comments and Nice Function Descriptions
"""

import numpy as np
import csv



"""
punk_score = [-4, 10,2,-11,-5]
jazz_score = [8, 8, 0, -3, 7]
classical_score = [-2, 12, 4, 4, 5]
rock_score = [-2, 12, 2,-6,0]
alternativerock_score = [-1, 7, -5, -6, -6]
reggae_score = [9,0,-6,-5,4]
ambient_score = [3,6,-6,-6,-2]
world_score = [3,9,-10,-2,1]
pop_score = [10,-8,-16,0,-9]
metal_score = [-9,11,9,-8,3]
hiphop_score = [14,2,-2,-5,2]
electronica_score = [9,4,-4,-5,-1]
religious_score = [6, -6, -12, 5, 1]
blues_score = [7, 9, -4, -3, 7]
country = [7, -9, -10, 1, 3]
soul = [13, -1, -13, -3, -1]
"""


#######################################################

# ---------------- HANDLE INPUT ----------------------#

#######################################################

#filename = sys.argv[1]
filename = "C:\Users\jmidv\Desktop\HHR.csv"


INPUT = []
with open(filename, 'r') as p:
    filenameReader = csv.reader(p, delimiter=" ")
    for row in filenameReader:
        INPUT.append(row[0].lower())
        

#######################################################

# ------------------- PROCESS ------------------------#

#######################################################

OUT = []
GENRE_SORES = {}
NUM_ELEMENTS = len(INPUT)


personalities = ["extraversion", "intuition", "thinking", "judging", "assertiveness"]

genres = ["punk", "jazz", "classical", "rock", "alternative rock", 
          "reggae", "ambient", "world", "pop", "metal", "hip-hop",
          "electronica", "religious", "blues", "country", "soul"]

personality_scores =  [[-4, 10,2,-11,-5], 
                        [8, 8, 0, -3, 7],
                        [-2, 12, 4, 4, 5],
                        [-2, 12, 2,-6,0],
                        [-1, 7, -5, -6, -6],
                        [9,0,-6,-5,4],
                        [3,6,-6,-6,-2],
                        [3,9,-10,-2,1],
                        [10,-8,-16,0,-9],
                        [-9,11,9,-8,3],
                        [14,2,-2,-5,2],
                        [9,4,-4,-5,-1],
                        [6, -6, -12, 5, 1],
                        [7, 9, -4, -3, 7],
                        [7, -9, -10, 1, 3],
                        [13, -1, -13, -3, -1]]



for row in personalities:
    OUT.append(0)
    
i = 0
for row in genres:
    GENRE_SORES[row] = personality_scores[i]
    i = i + 1
    
    
for row in INPUT:
    scores = GENRE_SORES[row]
    a = np.add(scores, OUT)
    b = np.ndarray.tolist(a)
    
    OUT = b
    
averages = []
for row in OUT:
    avg =  row / NUM_ELEMENTS
    averages.append(avg)
    
    

    

print(averages)
    




































    

