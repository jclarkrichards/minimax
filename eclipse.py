import time
from random import randint
from gamestate import GameState
from minimax import Minimax
import numpy as np
#Winning lines
LINES = ((0,1,2), (1,2,3), (4,5,6), (5,6,7),
         (8,9,10), (9,10,11), (12,13,14), (13,14,15),
         (0,4,8), (4,8,12), (1,5,9), (5,9,13),
         (2,6,10), (6,10,14), (3,7,11), (7,11,15),
         (1,6,11), (0,5,10), (5,10,15), (4,9,14),
         (2,5,8), (3,6,9), (6,9,12), (7,10,13))

#==============================================================================
class EclipseState(GameState):
    def __init__(self, state, level=0, forceend=False):
        GameState.__init__(self, state, level)
        self.emptyVal = 0 #how empty spaces on the board are defined
        #Each piece has two sides
        self.sun = [1, -1]
        self.moon = [2, -2]
        self.numFlips = 0
        self.winScore = 100
        self.loseScore = -100
        self.invalid = False
        self.randomPaths = False
        self.checkEndState(forceend)
        
    def checkWin(self):
        '''To win all pieces must be the same and all adjacent spaces
        cannot be empty (locked)'''
        sunwin = 0
        moonwin = 0
        
        for win in LINES:
            for sun in self.sun:
                locked = self.checkLockedPieces(win, sun)
                if locked:
                    sunwin += 1
            for moon in self.moon:
                locked = self.checkLockedPieces(win, moon)
                if locked:
                    moonwin += 1
        return sunwin, moonwin

    def checkEndState(self, forceend=False):
        '''End state if no empty spaces or either player wins'''
        self.end = False
        indices = self.emptySpaces()
        if len(indices) == 0:
            self.end = True
        else: 
            self.getScore()
            sunwin, moonwin = self.checkWin()
            if sunwin or moonwin:
                self.end = True

        if forceend:
            self.end = True
        self.numFlips = self.totalNumFlipsForOpponent()

    def getChildren(self, end=False):
        '''Get all possible children of this state'''
        if self.sunIsParent():
            moonIndices = self.getPlayerIndices(self.moon)
            moonIndices = self.getFlippableIndices(moonIndices)
            self.createChildren(self.sun, moonIndices, end=end)
        else:
            sunIndices = self.getPlayerIndices(self.sun)
            sunIndices = self.getFlippableIndices(sunIndices)
            self.createChildren(self.moon, sunIndices, end=end)

        #self.removeDuplicateChildren()
        #self.sortChildren()
        self.pruneChildren()
        #self.evaluateChildren()
        #if len(self.children) > 0 and len(self.emptySpaces()) > 6:
        #    self.chooseRandomChild()

    def chooseRandomChild(self):
        '''Choose a random child and set as only child'''
        if len(self.children) > 0:
            index = randint(0, len(self.children) - 1)
            self.children = [self.children[index]]

    def createChildren(self, parent, indices, end=False):
        '''Actual work of creating the children'''
        if len(indices) > 0:
            for i in indices:
                flipindices = self.getAdjacentEmpty(i)
                for fi in flipindices:
                    empty = self.emptySpaces()
                    empty.remove(fi)
                    empty.append(i)
                    empty.sort()
                    for ei in empty:
                        for side in parent:
                            state = self.state[:]
                            state[fi] = state[i] * -1
                            state[i] = 0
                            state[ei] = side
                            
                            self.children.append(EclipseState(state, level=self.level+1, forceend=end))
        else:#No flippable pieces so just place own piece
            empty = self.emptySpaces()
            for ei in empty:
                for side in parent:
                    state = self.state[:]
                    state[ei] = side
                    self.children.append(EclipseState(state, level=self.level+1, forceend=end))

        
    def getScore(self):
        '''Getting score assumes we have reached a true end state'''
        sunwin, moonwin = self.checkWin()
        if sunwin == moonwin:
            #self.score = self.winScore - self.level * 5
            pass #No winners.  
        elif sunwin > moonwin:
            if self.sunIsRoot(self.level):
                self.score = self.winScore
            else:
                self.score = self.loseScore
        elif moonwin > sunwin:
            if self.sunIsRoot(self.level):
                self.score = self.loseScore
            else:
                self.score = self.winScore


    def checkLockedPieces(self, indices, val):
        '''Check if indices all match val and those indices are all locked'''
        if self.allPiecesMatch(indices, val):
            adjacents = self.getAdjacentIndices(indices)
            if 0 in [self.state[i] for i in adjacents]:
                return False
            return True
        return False

    def getAdjacentIndices(self, indices):
        '''Given one or more indices, get a list of adjacent indices not including
        the ones in the given list'''
        adjacents = []
        if len(indices) == 1:
            i = indices[0]
            if i-4 >= 0:
                adjacents.append(i-4)
            if i+4 < len(self.state):
                adjacents.append(i+4)
            if self.onSameRow(i+1, i):
                adjacents.append(i+1)
            if self.onSameRow(i-1, i):
                adjacents.append(i-1)
        else:
            for i in indices:
                adjacents += self.getAdjacentIndices([i])
        adjacents = list(set(adjacents))
        for i in indices:
            if i in adjacents:
                adjacents.remove(i)
        return adjacents

    def onSameRow(self, val1, val2):
        '''Two values are on the same row if their integer division is the same'''
        if val1/4 == val2/4:
            return True
        return False

    def sunIsRoot(self, level=0):
        '''Return True if sun is root, False if moon is root.
        Sun is root if even number of empty spaces on the board'''
        empty = self.emptySpaces()
        if self.isEven(len(empty)-level):
            return True
        return False

    def sunIsParent(self):
        '''Return True if sun is the parent, False if moon is the parent.
        Sun is the parent if even number of empty spaces on the board'''
        empty = self.emptySpaces()
        if self.isEven(len(empty)):
            return True
        return False

    def getPlayerIndices(self, values):
        '''Get indices of players pieces as specified by values'''
        indices = []
        for i in range(len(self.state)):
            for value in values:
                if self.state[i] == value:
                    indices.append(i)
        return indices

    def getFlippableIndices(self, indices):
        '''Return a subset of indices that are flippable'''
        flippables = []
        for i in indices:
            if self.anyAdjacentEmpty([i]):
                flippables.append(i)
        return flippables

    def getAdjacentEmpty(self, index):
        '''Get all adjacent empty indices of specified index'''
        result = []
        adjacent = self.getAdjacentIndices([index])
        empty = self.emptySpaces()
        for el in empty:
            if el in adjacent:
                result.append(el)
        return result

    def anyAdjacentEmpty(self, indices):
        '''Checks all indices and returns True if any adjacent spot is empty'''
        for i in indices:
            values = self.getAdjacentEmpty(i)
            if len(values) > 0:
                return True
        return False

    def rotate(self, state, rot):
        A = np.array(state).reshape(4,4)
        return list(np.rot90(A, rot).flatten())

    def removeDuplicateChildren(self):
        '''Remove children that are rotationally equivalent'''
        allstates = [child.state for child in self.children]
        temp = []
        for c in range(len(self.children)):
            indices = [c]
            for r in range(1, 4):
                cr = self.rotate(self.children[c].state, r)
                if cr in allstates:
                    indices.append(allstates.index(cr))
            temp.append(indices)
            
        junk = []
        for t in temp:
            t.sort()
            junk.append(t[0])
        indices = list(set(junk))
        newkids = []
        for i in range(len(self.children)):
            if i in junk:
                newkids.append(self.children[i])
        self.children = newkids
        #self.children = temp

    #-------------------------------------------------------------------
    #Below are optimization methods
    #-------------------------------------------------------------------
    def loseStateRoot(self):
        return self.end and self.score == self.loseScore and not self.isEven(self.level)
    
    def winStateRoot(self):
        return self.end and self.score == self.winScore and not self.isEven(self.level)

    def winStateOther(self):
        return self.end and self.score == self.loseScore and self.isEven(self.level)

    def loseStateOther(self):
        return self.end and self.score == self.winScore and self.isEven(self.level)

    def invalidState(self):
        if (self.score == self.winScore and self.isEven(self.level) or 
            self.score == self.loseScore and not self.isEven(self.level)):
            return True
        return False

    def pruneChildren(self):
        '''If any of the children are winning end states, then get rid of all the other children.
        Except if this child is on an even level because then it is invalid since the other
        player will never choose this state.'''
        #flips = [child.numFlips for child in self.children]
        #upperFlip = (min(flips) + max(flips)) / 2
        #temp = []
        #for child in self.children:
        #    if child.numFlips < upperFlip:
        #        temp.append(child)
        #if len(temp) > 0:
        #    self.children = temp

        temp = []

        for child in self.children:
            if not child.invalidState():
                temp.append(child)
            #if child.winStateRoot():
        #    if not child.loseStateRoot():
        #        temp.append(child)
        if len(temp) > 0:
            self.children = temp

        for child in self.children:
            if (child.winStateRoot() or child.winStateOther()):
                self.children = [child]
                break
            

    def sortChildren(self):
        '''Sort children based on numFlips.  Low to high.  Use bubble sort.'''
        issorted = False
        temp = 0
        while not issorted:
            issorted = True
            for i in range(len(self.children)-1):
                if self.children[i].numFlips > self.children[i+1].numFlips:
                    temp = self.children[i]
                    self.children[i] = self.children[i+1]
                    self.children[i+1] = temp
                    issorted = False
                

    def totalNumFlipsForOpponent(self):
        '''Get the total number of possible flips for a player.'''
        flips = 0
        if self.sunIsParent():
            indices = self.getPlayerIndices(self.moon)
        else:
            indices = self.getPlayerIndices(self.sun)
        for i in indices:
            empty = self.getAdjacentEmpty(i)
            flips += len(empty)
        return flips

    """
    def evaluateChildren(self):
        '''Evaluate children based on line scores'''
        if len(self.children) > 0:
            if self.sunIsRoot():
                for child in self.children:
                    for line in LINES:
                        for side in self.sun:
                            if child.allPiecesMatch(line, side):
                                if child.checkLockedPieces(line, side):
                                    child.prescore += 100
                                else:
                                    child.prescore += 10
                            else:
                                #if child.twoPiecesMatch(line, side):
                                if (child.state[line[0]] == child.state[line[1]] == side or
                                    child.state[line[0]] == child.state[line[2]] == side or
                                    child.state[line[1]] == child.state[line[2]] == side):
                                    child.prescore += 1
            else:
                for child in self.children:
                    val = 0
                    for line in LINES:
                        for side in self.moon:
                            if child.allPiecesMatch(line, side):
                                if child.checkLockedPieces(line, side):
                                    child.prescore += 100
                                else:
                                    child.prescore += 10
                            else:
                                if (child.state[line[0]] == child.state[line[1]] == side or
                                    child.state[line[0]] == child.state[line[2]] == side or
                                    child.state[line[1]] == child.state[line[2]] == side):
                                    child.prescore += 1
    """
             
    def setMaxLevel(self, maxLevel):
        '''Set the maximum level for minimax if this is a winning state.  
        The minimax object will call this method'''
        if self.winStateRoot():
        #if self.score == self.winScore and not self.isEven(self.level):
            print "set " + str(self.level - 2) + " as new level"
            print self
            print ""
            return self.level - 2
        return maxLevel


        #sunwin, moonwin = self.checkWin()
        #if ((self.sunIsRoot() and sunwin) or (not self.sunIsRoot() and moonwin)):
        #    print "set " + str(self.level - 1) + " as new level"
        #    return self.level - 1

    def __repr__(self):
        s = "%s %s %s %s\n%s %s %s %s\n%s %s %s %s\n%s %s %s %s\n" % tuple(self.state)
        return s
        
    


#board = [-1,0,-1,-1,0,1,0,2,2,0,1,-2,-2,-1,0,2]        
#board = [0,0,-1,0,2,1,1,0,2,-1,0,0,2,-1,0,2]                                
#board = [-1,0,-1,0,2,1,0,0,2,0,1,-2,0,-1,0,2]                                
#board = [0,1,-1,-1,0,1,-2,2,2,0,1,-2,-2,-1,0,2]                                
#board = [1,0,0,-1,2,-1,0,2,0,0,1,-2,-2,-1,0,2]                                
#board = [-1,0,0,0,1,-1,-1,2,1,-2,-2,2,-1,-2,1,2]
#board = [1,-2,0,0,-1,2,0,0,0,-1,0,0,0,0,0,0]
#board = [-1,2,2,0,0,-1,0,0,0,0,0,0,0,0,0,0]
board = [-2,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#board = [2,-1,2,1,0,1,-1,0,2,2,1,2,0,-1,2,0]
#Run Thru, I start

#board = [1,2,1,1,
#         -2,-2,2,-1,
#         -2,-1,0,2,
#         0,0,0,1]

state = EclipseState(board)

#print len(state.children)
#for i in range(len(state.children)):
#    print state.children[i].score 
minimax = Minimax()               
start = time.time()                                          
minimax.minimax(state)
end = time.time()

"""
state.getChildren()
win = False
wins = [0]*len(state.children)
for i in range(5000):
    print i
#while not win:
    index = randint(0, len(state.children)-1)
    win = minimax.randomPath(state.children[index])
    if win:
        wins[index] += 1
end = time.time()
bestIndex = wins.index(max(wins))
print wins
print ""
print bestIndex
print ""
print state.children[bestIndex]
print ""
print win

"""
print "Elapsed Time = " + str(end-start)
print minimax.num                                                                 
print state                                                              
print ""
print state.bestChild

