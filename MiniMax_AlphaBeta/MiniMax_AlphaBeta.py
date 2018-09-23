# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:53:56 2018

@author: Jeremy Midivdy, jam658

EECS 348, Winter 2018

Lab 2 :::: STUDENT_CODE.PY ::::
"""

import random
import Lab2_konane as kb   #### <-------------- make sure to change back
import copy


# class for individual player.  student and grader players should be identical except for:
#     - implementation of getMinimaxMove() and getAlphabetaMove(), and
#     - any helper functions and/or members implemented by student
class player:
    def __init__(self, b,s,depth,algo):
        self.b = b                  # board to be played for test
        self.s = s                  # save 'x' or 'o' designation
        self.depth = depth          # maximum depth for search (in number fo plies)
        self.algo = algo            # name of algorithm for player
        self.prior_move = 'L'       # helper variable for first/last deterministic player algo

    # should not be needed for autograder, but include to help development
    def makeFirstMove(self,r,c):
        self.b.firstMove(self.s,r,c)

    # returns list of available moves for player as list of [[x_from][y_from],[x_to][y_to]] items
    def getNextMoves(self):
        return(self.b.possibleNextMoves(self.s))

    # makes move specified by move expressed as [[x_from][y_from],[x_to][y_to]]
    def makeNextMove(self,move):
        self.b.nextMove(self.s,move)

    ######
    # next few methods get the next move for each of the available algorithms

    # get the first move of the list of available moves
    def getFirstMove(self):
        moves = self.b.possibleNextMoves(self.s)
        return moves[0]

    # alternative between taking the first and last available move
    def getFirstLastMove(self):
        moves = self.b.possibleNextMoves(self.s)
        if self.prior_move == 'L':
            move = moves[0]
            self.prior_move = 'F'
        else:
            move = moves[len(moves)-1]
            self.prior_move = 'L'
        return move

    # randomly choose one of the available moves
    def getRandomMove(self):
        moves = self.b.possibleNextMoves(self.s)
        selected = random.randint(0,len(moves)-1)
        return moves[selected]

    # ask a human player for a move
    def getHumanMove(self):
        print "Possible moves:" , self.b.possibleNextMoves(self.s)
        origin = self._promptForPoint("Choose a piece to move (in the format 'row column'): ")
        destination = self._promptForPoint("Choose a destination for (%s, %s) -> " % (origin[0], origin[1]))
        if (origin, destination) in self.b.possibleNextMoves(self.s):
            return (origin, destination)
        else:
            print "Invalid move.", (origin, destination)
            return self.getHumanMove()

    # help for prompting human player
    def _promptForPoint(self, prompt):
        raw = raw_input(prompt)
        (r, c) = raw.split()
        return (int(r), int(c))
    

    def opposite(self,s):
        if s == 'x':
            return 'o'
        else:
            return 'x'

    def heuristic(self, board, player):
        score = len(board.possibleNextMoves(self.s)) - len(board.possibleNextMoves(self.opposite(self.s))) + \
        int(board.state[0][0]==self.s) + \
        int(board.state[0][board.size-1]==self.s) + \
        int(board.state[board.size-1][0]==self.s) + \
        int(board.state[board.size-1][board.size-1]==self.s)
        #print "heuristic", board, player, score
        return score
    
    # member function called by test() which specifies move to be made for player's turn, with move
    # expressed as [[x_from][y_from],[x_to][y_to]]
    # if no moves available, return Python 'None' value
    def takeTurn(self):
        moves = self.b.possibleNextMoves(self.s)

        # return Python 'None' if no moves available
        if len(moves) == 0:
            return [True,None]

        if self.algo == 'First Move':  # select first avaliable move
            move = self.getFirstMove()

        if self.algo == 'First/Last Move':  # alternate first and last moves
            move = self.getFirstLastMove()

        if self.algo == 'Random':  # select random move Note: not determinisic, just used to exercise code
            move = self.getRandomMove()

        if self.algo == 'MiniMax':  # player must select best move based upon MiniMax algorithm
            move = self.getMinimaxMove()

        if self.algo == 'AlphaBeta':  # player must select best move based upon AlphaBeta algorithm
            move = self.getAlphaBetaMove()

        if self.algo == 'Human':
            move = self.getHumanMove()

        # makes move on board being used for evaluation
        self.makeNextMove(move)
        return [False,move]
    
    
    # ---------------------------------------------------------------- #
    # ---------------------------------------------------------------- #
    # ---------- MINIMAX AND ALPHA-BETA IMPLEMENTATION --------------- #
    # ---------------------------------------------------------------- #
    # ---------------------------------------------------------------- #

     # ------------------------------------------- #
     # ----------------- MINMAX ------------------ #
     # ------------------------------------------- #
     
    def getMinimaxMove(self):
               
        ##initialzie useful variables
        #keep track of Depth during recursion
        max_depth = self.depth #might have to change to *2 and take into account max moves
        
        # ------------------------------------------- #
        # ----------------- DECISION ---------------- #
        # ------------------------------------------- #
        
        def miniMax_Decision(board):
            
            #initialzie depth
            init_depth = 1
            init_side = self.s
            
            #compute possible moves from the initial state
            moves = board.possibleNextMoves(init_side)
                        
            #the game is already over?  <---- might have to change
            if len(moves) == 0:
                return #? game already over?
            
            #figure out next_side for recursive call
            next_side = 'x'
            if init_side == 'x':
                next_side = 'o'
            
            #compute the next possibe boards
            nextBoards = []
            for row in moves:
                c = copy.deepcopy(board)
                for i in range(1, len(row)): #multiple moves
                    c._makeJump(init_side, row[i-1], row[i])
                nextBoards.append(c)
            
            #get scores of next boards, starting recursion in minMax
            #init is always max, so init always calls min on the init boards
            #top = depth of 1, first min = depth 2
            scores = []
            for row in nextBoards:
                a = minValue(row, init_depth + 1, next_side)
                scores.append(a)
                
            #find max score after scores are tabulated with recursion
            maxScore = max(scores)
                    
            indexes = []
            #if more than one, choose first in list of moves provided by 
            #possibleNextMoves()
            for i in range(0, len(scores)):
                s = scores[i]
                if s == maxScore:
                    indexes.append(i)
            
            maxIndex = indexes[0]

            return moves[maxIndex]         
        
        # ------------------------------------------- #
        # ----------------- MAX --------------------- #
        # ------------------------------------------- #
        
        def maxValue(curr_board, curr_depth, curr_side):
            
            #get possible moves
            moves = curr_board.possibleNextMoves(curr_side)
            
            #figure out next_side for recursive call
            next_side = 'x'
            if curr_side == 'x':
                next_side = 'o'
            
            #test if terminal state
            if len(moves) == 0:
                return self.heuristic(curr_board, self)
            
            #construct boards after moves are made for each
            #possible move in moveslist
            nextBoards = []
            for row in moves:
                c = copy.deepcopy(curr_board)
                for i in range(1, len(row)): #multiple moves
                    c._makeJump(curr_side, row[i-1], row[i])
                nextBoards.append(c)            
            
            #if at max_depth, evaluate with hueristic and return
            #else, recurse through minValue
            scores = []
            for i in range(0, len(nextBoards)):
                if curr_depth >= max_depth:
                    a = self.heuristic(nextBoards[i], self)
                else:
                    a = minValue(nextBoards[i], curr_depth + 1, next_side)
                scores.append(a)
                
            #find max score after scores are tabulated with recursion
            maxScore = max(scores)
            
            return maxScore
                
        # ------------------------------------------- #
        # ----------------- MIN --------------------- #
        # ------------------------------------------- #
        
        def minValue(curr_board, curr_depth, curr_side):
            
            #get possible moves
            moves = curr_board.possibleNextMoves(curr_side)
            
            #figure out next_side for recursive call
            next_side = 'x'
            if curr_side == 'x':
                next_side = 'o'
            
            #test if terminal state
            if len(moves) == 0:
                return self.heuristic(curr_board, self)
            
            #construct boards after moves are made for each
            #possible move in moveslist
            nextBoards = []
            for row in moves:
                c = copy.deepcopy(curr_board)
                for i in range(1, len(row)): #multiple moves
                    c._makeJump(curr_side, row[i-1], row[i])
                nextBoards.append(c)            
            
            #if at max_depth, evaluate with hueristic and return
            #else, recurse through minValue
            scores = []
            
            for i in range(0, len(nextBoards)):
                if curr_depth >= max_depth:
                    a = self.heuristic(nextBoards[i], self)
                else:
                    a = maxValue(nextBoards[i], curr_depth + 1, next_side)
                scores.append(a)
                
            #find min score after scores are tabulated with recursion
            minScore = min(scores)
            
            return minScore
         
        #envoke miniMax algorithm
        return miniMax_Decision(self.b)


    # alphabeta algorithm to be completed by students
    # note: you may add parameters to this function call
    
     # -------------------------------------------------------------------------------- #
     # --------------------------- Alpha Beta ----------------------------------------- #
     # -------------------------------------------------------------------------------- #
     
    def getAlphaBetaMove(self):

        ##initialzie useful variables
        #keep track of Depth during recursion
        max_depth = self.depth #might have to change to *2 and take into account max moves
     
        # ------------------------------------------- #
        # ----------------- DECISION ---------------- #
        # ------------------------------------------- #
        
        def alpha_Beta_Search(board):
            
            #initialzie variables
            init_depth = 1
            init_side = self.s
            
            #initalize MAX and MIN for alpha and beta
            alpha = -10000 
            beta  =  10000
            
            #compute possible moves from the initial state
            moves = board.possibleNextMoves(init_side)
                        
            #the game is already over?  <---- might have to change
            if len(moves) == 0:
                return #? game already over?
            
            #figure out next_side for recursive call
            next_side = 'x'
            if init_side == 'x':
                next_side = 'o'
            
            #compute the next possibe boards
            nextBoards = []
            for row in moves:
                c = copy.deepcopy(board)
                if len(row) > 2:
                    for i in range(1, len(row)): #multiple moves
                        c._makeJump(init_side, row[i-1], row[i])
                else:
                    c._makeJump(init_side, row[0], row[1])
                nextBoards.append(c)
            
            #get scores of next boards, starting recursion in minMax
            #init is always max, so init always calls min on the init boards
            #top = depth of 1, first min = depth 2
            scores = []
            for row in nextBoards:
                scores.append(minValue(row, init_depth + 1, next_side, alpha, beta))
                
            maxScore = max(scores)
            
            #if more than one, choose first in list of moves provided by 
            #possibleNextMoves()
            for i in range(0, len(scores)):
                s = scores[i]
                if s == maxScore:
                    return moves[i]
        
        # ------------------------------------------- #
        # ----------------- MAX --------------------- #
        # ------------------------------------------- #
        
        def maxValue(curr_board, curr_depth, curr_side, alpha, beta):
            moves = curr_board.possibleNextMoves(curr_side)
            next_side = 'x'
            if curr_side == 'x':
                next_side = 'o'
            if len(moves) == 0:
                return self.heuristic(curr_board, self)
            nextBoards = []
            for row in moves:
                c = copy.deepcopy(curr_board)
                if len(row) > 2:
                    for i in range(1, len(row)): #multiple moves
                        c._makeJump(curr_side, row[i-1], row[i])
                else:
                    c._makeJump(curr_side, row[0], row[1])
                nextBoards.append(c)            
            scores = []                
            for i in range(0, len(nextBoards)):
                if curr_depth >= max_depth:
                    a = self.heuristic(nextBoards[i], self)
                else:
                    a = minValue(nextBoards[i], curr_depth + 1, next_side, alpha, beta)
                if a >= beta:
                    return a 
                alpha = max(a, alpha)
                scores.append(a)
            return max(scores)
                
        # ------------------------------------------- #
        # ----------------- MIN --------------------- #
        # ------------------------------------------- #
        
        def minValue(curr_board, curr_depth, curr_side, alpha, beta):
            moves = curr_board.possibleNextMoves(curr_side)
            next_side = 'x'
            if curr_side == 'x':
                next_side = 'o'
            if len(moves) == 0:
                return self.heuristic(curr_board, self)
            nextBoards = []
            for row in moves:
                c = copy.deepcopy(curr_board)
                if len(row) > 2:
                    for i in range(1, len(row)): 
                        c._makeJump(curr_side, row[i-1], row[i])
                else:
                    c._makeJump(curr_side, row[0], row[1])
                nextBoards.append(c)            
            scores = []
            for i in range(0, len(nextBoards)):
                if curr_depth >= max_depth:
                    a = self.heuristic(nextBoards[i], self)
                else:
                    a = maxValue(nextBoards[i], curr_depth + 1, next_side, alpha, beta)
                if a <= alpha:
                    return a 
                beta = min(beta, a)
                scores.append(a)
            return min(scores)
         
        #envoke alpha-beta algorithm
        return alpha_Beta_Search(self.b)
        
            
            
            
            
            

