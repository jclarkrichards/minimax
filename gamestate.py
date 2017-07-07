from random import randint

class GameState(object):
    def __init__(self, state, level):
        self.state = state #represents this state 
        #children and bestChild  are of type GameState
        self.children = []
        self.bestChild = None
        self.level = level #level this state was created on
        self.score = 0
        self.prescore = 0 #an initial score, not a final one
        self.emptyVal = -1 #how empty spaces on the board are defined

    def isEven(self, value):
        '''Checks whether value is odd or even.  False if odd'''
        if value % 2:
            return False
        return True

    def getBestChildLevel(self, children):
        '''Get the levels children were created.  We want to win fast.'''
        levels = []
        for child in children:
            if child.bestChild is not None:
                levels.append(child.bestChild.level)
            else:
                levels.append(child.level)
        return levels
        
                
    def getScoreFromChildren(self):
        '''Ask children for scores and choose the best child'''
        scores = [child.score for child in self.children]
        #print scores
        if self.isEven(self.level): #level is even
            self.score = max(scores)
        else: #level is even
            self.score = min(scores)
        
        #More than one child has the same best score
        if scores.count(self.score) > 1:
            #Only use the children with best scores
            children = self.filterChildrenByScore(self.score)
            levels = self.getBestChildLevel(children)
            level = min(levels)
            #If more than one child with best score was created on same level
            if levels.count(level) > 1:
                num = levels.count(level)
                indices = []
                for i in range(len(levels)):
                    if levels[i] == level:
                        indices.append(i)
                index = randint(0, len(indices)-1)
                #print scores, levels
                self.bestChild = children[indices[index]]
            else:
                #print scores, levels
                index = levels.index(level)
                self.bestChild = children[index]
        else:
            index = scores.index(self.score)
            self.bestChild = self.children[index]

    def filterChildrenByScore(self, score):
        children = []
        for child in self.children:
            if child.score == score:
                children.append(child)
        return children

    def emptySpaces(self):
        '''Get indices of empty spaces'''
        indices = []
        for i in range(len(self.state)):
            if self.state[i] == self.emptyVal:
                indices.append(i)
        return indices

    
    def allPiecesMatch(self, i, val):
        '''Check if all pieces at the indices match the val and are not an empty space'''
        if self.state[i[0]] == self.state[i[1]] == self.state[i[2]] == val != self.emptyVal:
            return True
        return False

    def twoPiecesMatch(self, i, val):
        pass

    


        
