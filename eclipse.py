from random import randint
from gamestate import GameState
from minimax import Minimax

#==============================================================================
class Eclipse(GameState):
    def __init__(self, state, level=0):
        GameState.__init__(self, state, level)
        self.emptyVal = 0
        self.sunSilver = 1
        self.sunGold = -1
        self.moonSilver = 2
        self.moonGold = -2
        self.sun = [self.sunSilver, self.sunGold]
        self.moon = [self.moonSilver, self.moonGold]

        self.lines = [[0,1,2],[1,2,3],[4,5,6],[5,6,7],
                      [8,9,10],[9,10,11],[12,13,14],[13,14,15],
                      [0,4,8],[4,8,12],[1,5,9],[5,9,13],
                      [2,6,10],[6,10,14],[3,7,11],[7,11,15],
                      [1,6,11],[0,5,10],[5,10,15],[4,9,14],
                      [2,5,8],[3,6,9],[6,9,12],[7,10,13]]
        
        self.checkEndState()
        
    def checkWin(self):
        '''To win all pieces must be the same and all adjacent spaces
        cannot be empty'''
        sunwin = 0
        moonwin = 0
        
        for win in self.lines:
            for sun in self.sun:
                locked = self.checkLockedPieces(win, sun)
                if locked:
                    sunwin += 1
            for moon in self.moon:
                locked = self.checkLockedPieces(win, moon)
                if locked:
                    moonwin += 1
        return sunwin, moonwin

    def checkEndState(self):
        '''End state if no empty spaces or either player wins'''
        self.end = False
        indices = self.emptySpaces()
        if len(indices) == 0:
            self.end = True
            
        sunwin, moonwin = self.checkWin()
        if sunwin or moonwin:
            self.end = True

    def getChildren(self):
        '''Get all possible children of this state'''
        if self.sunIsRoot():
            moonIndices = self.getPlayerIndices(self.moon)

            if self.anyAdjacentEmpty(moonIndices):
                for mi in moonIndices:
                    flipindices = self.getAdjacentEmpty(mi)
                    for fi in flipindices:
                        empty = self.emptySpaces()
                        empty.remove(fi)
                        empty.append(mi)
                        for ei in empty:
                            for side in self.sun:
                                state = self.state[:]
                                state[fi] = state[mi] * -1
                                state[mi] = 0
                                state[ei] = side
                                self.children.append(Eclipse(state, level=self.level+1))
            else:
                empty = self.emptySpaces()
                for ei in empty:
                    for side in self.sun:
                        state = self.state[:]
                        state[ei] = side
                        self.children.append(Eclipse(state, level=self.level+1))

        else:
            sunIndices = self.getPlayerIndices(self.sun)
            if self.anyAdjacentEmpty(sunIndices):
                for si in sunIndices:
                    flipindices = self.getAdjacentEmpty(si)
                    for fi in flipindices:
                        empty = self.emptySpaces()
                        empty.remove(fi)
                        empty.append(si)
                        for ei in empty:
                            for side in self.moon:
                                state = self.state[:]
                                state[fi] = state[si] * -1
                                state[si] = 0
                                state[ei] = side
                                self.children.append(Eclipse(state, level=self.level+1))
            else:
                empty = self.emptySpaces()
                for ei in empty:
                    for side in self.moon:
                        state = self.state[:]
                        state[ei] = side
                        self.children.append(Eclipse(state, level=self.level+1))


    def createNewState(self):
        pass

    def getScore(self):
        '''Getting score assumes we have reached a true end state'''
        sunwin, moonwin = self.checkWin()
        if sunwin > 0 and moonwin > 0:
            pass #TIE
        else:
            if self.sunIsRoot(self.level):
                if sunwin:
                    self.score = 1
                elif moonwin:
                    self.score = -1
            else: #Moon is root
                if moonwin:
                    self.score = 1
                elif sunwin:
                    self.score = -1

    def checkLockedPieces(self, indices, val):
        '''Check if indices all match val and those indices are all locked'''
        if self.allPiecesMatch(indices, val):
            adjacents = self.getAdjacentIndices(indices)
            empty = self.emptySpaces()
            for i in adjacents:
                if i in empty:
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

    def getNumChildren(self):
        '''For this state how many children can it have?'''
        empty = self.emptySpaces()
        numAdjacents = 0
        if self.sunIsRoot():
            moonIndices = self.getPlayerIndices(self.moon)
            for i in moonIndices:
                numAdjacents += len(self.getAdjacentEmpty(i))
        else:
            sunIndices = self.getPlayerIndices(self.sun)
            for i in sunIndices:
                numAdjacents += len(self.getAdjacentEmpty(i))

        if len(empty) == len(self.state):
            numAdjacents = 1
        return 2 * len(empty) * numAdjacents

    def sunIsRoot(self, level=0):
        '''Return True if sun is root, False if moon is root.
        Sun is root if even number of empty spaces on the board'''
        empty = self.emptySpaces()
        if self.isEven(len(empty)-level):
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

    def pruneChildren(self):
        '''Prune child if prescore is above 4.  Basic and simple, but not the best.'''
        if len(self.children) > 0:
            prescores = [c.prescore for c in self.children]
            #print len(prescores), len(self.children)
            #badkids = []
            for i in range(len(prescores)):
                #print i
                if prescores[i] > 100:
                    print self.level
                    print self.children[i].state
                    self.children = [self.children[i]]
                    break
                #if prescores[i] > 4:
                #    badkids.append(self.children[i])
                
            #for badkid in badkids:
            #    self.children.remove(badkid)

    def sortChildren(self):
        '''Sort children based on prescore.  highest to lowest.  Use bubble sort.'''
        sorted = False
        temp = 0
        while not sorted:
            sorted = True
            for i in range(len(self.children)-1):
                if self.children[i].prescore < self.children[i+1].prescore:
                    temp = self.children[i]
                    self.children[i] = self.children[i+1]
                    self.children[i+1] = temp
                    sorted = False
                

    #def evaluateChildren(self):
    #    '''Evaluate children based on number of flips other player can make'''
    #    if len(self.children) > 0:
    #        if self.sunIsRoot():
    #            for child in self.children:
    #                self.prescore = child.totalNumFlips(True)
    #        else:
    #            for child in self.children:
    #                self.prescore = child.totalNumFlips(False)

    def totalNumFlips(self, evalSun):
        '''Get the total number of possible flips for a player.  Set as prescore'''
        flips = 0
        if evalSun:
            indices = self.getPlayerIndices(self.sun)
        else:
            indices = self.getPlayerIndices(self.moon)
        for i in indices:
            empty = self.getAdjacentEmpty(i)
            flips += len(empty)
        return flips

    def evaluateChildren(self):
        '''Evaluate children based on line scores'''
        if len(self.children) > 0:
            if self.sunIsRoot():
                for child in self.children:
                    for line in self.lines:
                        for side in self.sun:
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
            else:
                for child in self.children:
                    val = 0
                    for line in self.lines:
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
                    
    def earlyMover(self):
        pass

    def setMaxLevel(self):
        sunwin, moonwin = self.checkWin()
        if ((self.sunIsRoot() and sunwin) or (not self.sunIsRoot() and moonwin)):
            return self.level - 1

    def __repr__(self):
        pass
    


        
board = [-1,0,-1,0,2,1,0,0,2,0,1,-2,0,-1,0,2]                                
#board = [-1,0,-1,-1,2,1,0,2,2,0,1,-2,-2,-1,0,2]                                
#board = [-1,0,0,0,1,-1,-1,2,1,-2,-2,2,-1,-2,1,2]                               
state = Eclipse(board)
minimax = Minimax()                                                         
minimax.minimax(state)
print minimax.num                                                                 
print state.state                                                              
print ""                                                                       
print state.bestChild.state
