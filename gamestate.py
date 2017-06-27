from random import randint

class GameState(object):
    def __init__(self, state):
        self.state = state #represents this state 
        #parent, children, and bestChild  are of type GameState
        self.parent = None
        self.children = []
        self.bestChild = None
        self.level = 0 #level this state was created on
        self.score = 0 
        
    def getScoreFromChildren(self):
        '''Ask children for scores and choose'''
        scores = [child.score for child in self.children]
        #print scores
        if self.level % 2: #level is odd
            self.score = min(scores)
        else: #level is even
            self.score = max(scores)
        
        #More than one child has the same best score
        if scores.count(self.score) > 1:
            #levels = [child.level for child in self.children]
            #print levels
            levels = []
            for child in self.children:
                if child.bestChild is not None:
                    levels.append(child.bestChild.level)
                else:
                    levels.append(child.level)
            print levels
            level = min(levels)
            if levels.count(level) > 1:
                num = levels.count(level)
                indices = []
                for i in range(len(self.children)):
                    if self.children[i].score == self.score:
                        indices.append(i)
                index = randint(0, len(indices)-1)
                #print scores, levels
                self.bestChild = self.children[indices[index]]
            else:
                #print scores, levels
                index = levels.index(level)
                self.bestChild = self.children[index]
        else:
            index = scores.index(self.score)
            self.bestChild = self.children[index]


class TicTacToeState(GameState):
    def __init__(self, state):
        GameState.__init__(self, state)
        #state is a list with entries:  1=X, 0=O, -1=Empty space
        self.checkEndState()
        
    def checkWin(self):
        '''Check if either X or O wins'''
        wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],
                [1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        xwin = 0
        owin = 0
        for win in wins:            
            if self.state[win[0]] == self.state[win[1]] == self.state[win[2]] == 1:
                xwin += 1
            elif self.state[win[0]] == self.state[win[1]] == self.state[win[2]] == 0:
                owin += 1
        return xwin, owin

    def getScore(self):
        '''If level is even, O is root.'''
        xwin, owin = self.checkWin()
        
        if xwin == owin == 0 or xwin == owin:
            pass #TIE
        else:
            empty = 0
            for i in range(len(self.state)):
                if self.state[i] == -1:
                    empty += 1
            if (empty + self.level) % 2: #odd so X is root
                #print "X is root"
                if xwin:
                    self.score = 1
                else:
                    self.score = -1
            else: #Even so O is root
                #print "O is root"
                if owin:
                    self.score = 1
                else:
                    self.score = -1

    def getChildren(self):
        '''Create next states based on current state'''
        indices = []
        for i in range(len(self.state)):
            if self.state[i] == -1:
                indices.append(i)
        if len(indices) % 2: #odd number of spaces, place an X
            for index in indices:
                state = self.state[:]
                state[index] = 1
                self.children.append(TicTacToeState(state))
        else: #even number of spaces, place an O
            for index in indices:
                state = self.state[:]
                state[index] = 0
                self.children.append(TicTacToeState(state))
        
    def checkEndState(self):
        '''This is an endstate if there are no more empty spaces'''
        self.end = False
        indices = []
        for i in range(len(self.state)):
            if self.state[i] == -1:
                indices.append(i)
        if len(indices) == 0:
            self.end = True
            
        #Also an end state if either X or O wins
        xwin, owin = self.checkWin()
        if xwin or owin:
            self.end = True

        
    def __repr__(self):
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

    
