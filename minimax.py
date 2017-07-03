#from gamestate import TicTacToeState, Eclipse

def minimax(parent):
    if parent.end:
        parent.getScore()
    else:
        parent.getChildren()
        if len(parent.children) > 0:
            for child in parent.children:
                minimax(child)
            parent.getScoreFromChildren()
            #parent.maxLevel = parent.bestChild.maxLevel


"""If maxLevel is None, then full depth is searched.  Otherwise the depth will never go below maxLevel"""
class Minimax(object):
    def __init__(self):
        self.maxLevel = None
        self.num = 0

    def minimax(self, parent):
        self.num += 1
        if self.num % 10000:
            print self.num
        if parent.end:
            parent.getScore()
            self.maxLevel = parent.setMaxLevel()
        else:
            if self.maxLevel is not None:
                if parent.level < self.maxLevel:
                    parent.getChildren()
            else:
                parent.getChildren()

            if len(parent.children) > 0:
                for child in parent.children:
                    self.minimax(child)
                parent.getScoreFromChildren()



























def minimaxOpt(parent, level=0):
    #print level
    parent.level = level
    if parent.end:
        parent.getScore()
    else:
        parent.getChildren()
        #parent.evaluateChildren()
        #parent.sortChildren()
        #parent.pruneChildren()
        #if level < 2:
        #    print "children = " + str(len(parent.children))
        #    print [c.prescore for c in parent.children]
        #print ""
        #if len(parent.children) == 0:
        #    print parent.state

        #for i in range(len(parent.children)/2):
        #    minimax(parent.children[i], level=level+1)
        if len(parent.children) > 0:
            for child in parent.children:
                minimax(child, level=level+1)
            parent.getScoreFromChildren()


def printTree(parent):
    print parent.level, parent.score, len(parent.children)
    for child in parent.children:
        printTree(child)

#board = [-1,0,-1,-1,2,1,0,2,2,0,1,-2,-2,-1,0,2]
#board = [-1,0,0,0,1,-1,-1,2,1,-2,-2,2,-1,-2,1,2]
#state = Eclipse(board)
#minimax(state)
#print state.state
#print ""
#print state.bestChild.state

