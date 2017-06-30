from random import randint
from gamestate import GameState
from minimax import minimax, Minimax

#==============================================================================
class TicTacToe(GameState):
    def __init__(self, state, level=0):
        GameState.__init__(self, state, level)
        #state is a list with entries:  1=X, 0=O, -1=Empty space
        self.checkEndState()
        
    def xIsRoot(self):
        '''Return True if X is root, False if O is root'''
        empty = self.emptySpaces()
        if self.isEven(len(empty) + self.level):
            return False
        return True

    def checkWin(self):
        '''Check if either X or O wins'''
        wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],
                [1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        xwin = 0
        owin = 0
        for win in wins:
            if self.allPiecesMatch(win, 1):
                xwin += 1
            elif self.allPiecesMatch(win, 0):
                owin += 1
        return xwin, owin

    def getScore(self):
        '''If level is even, O is root.'''
        xwin, owin = self.checkWin()
        
        if xwin == owin == 0 or xwin == owin:
            pass #TIE
        else:
            if self.xIsRoot():
                if xwin:
                    self.score = 1
                else:
                    self.score = -1
            else:
                if owin:
                    self.score = 1
                else:
                    self.score = -1


    def getChildren(self):
        '''Create next states based on current state.  The number of children
        is the same as the number of empty spaces'''
        indices = self.emptySpaces()

        if self.isEven(len(indices)): #Even spaces, place an O
            piece = 0
        else: #odd number of spaces, place an X
            piece = 1

        for index in indices:
            state = self.state[:]
            state[index] = piece
            self.children.append(TicTacToe(state, level=self.level+1))
            
        self.evaluateChildren()
            
    def checkEndState(self):
        '''This is an endstate if there are no more empty spaces'''
        self.end = False
        indices = self.emptySpaces()
        if len(indices) == 0:
            self.end = True
            
        #Also an end state if either X or O wins
        xwin, owin = self.checkWin()
        if xwin or owin:
            self.end = True
                   

    def __repr__(self):
        '''How do we want to represent this object?'''
        XO = []
        for i in range(len(self.state)):
            if self.state[i] == 1:
                XO.append('X')
            elif self.state[i] == 0:
                XO.append('O')
            else:
                XO.append(' ')
        XO = tuple(XO)
        s = "%s|%s|%s\n- - -\n%s|%s|%s\n- - -\n%s|%s|%s" % XO
        return s

    def evaluateChildren(self):
        '''Check if any children are end states'''
        bestKids = []
        for i, child in enumerate(self.children):
            if child.end:
                xwin, owin = child.checkWin()
                if self.xIsRoot() and xwin:
                    bestKids.append(child)
                elif not self.xIsRoot() and owin:
                    bestKids.append(child)
        if len(bestKids) > 0:
            self.children = bestKids

    def setMaxLevel(self):
        xwin, owin = self.checkWin()
        if ((self.xIsRoot() and xwin) or (not self.xIsRoot() and owin)):
            return self.level - 1
            
#==============================================================================

XPlayer = True #Human player 
OPlayer = False                                                   
xturn = True                                                                    
gameover = False                                                                
state = TicTacToe([-1,-1,-1,-1,-1,-1,-1,-1,-1])                            
#state = TicTacToe([0,-1,0,1,1,-1,1,0,-1])
print state                         
while not gameover:                                                             
    if xturn:                                                                   
        if XPlayer:                                                             
            i = int(raw_input("Enter an X at location: (0-8)  "))               
            state.state[i] = 1                                                  
            state = TicTacToe(state.state)                                 
        else:                    
            minimax = Minimax()
            minimax.minimax(state)
            state = state.bestChild
            print "minimax called "+str(minimax.num) + " times"
            print minimax.maxLevel
    else:                          
        if OPlayer:
            i = int(raw_input("Enter an O at location: (0-8)  "))               
            state.state[i] = 0                                                  
            state = TicTacToe(state.state)                                 
        else:
            minimax = Minimax()
            minimax.minimax(state)                                                          
            state = state.bestChild                                                 
            print "minimax called "+str(minimax.num) + " times"
            print minimax.maxLevel
            
    if state.end:                                                               
        gameover = True                                                         
    else:                                                                       
        xturn = not xturn                                                       
    print state                                                                 
    print ""                                                                    
                                                                                
print "GAME OVER"                                                               


