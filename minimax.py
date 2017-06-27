from gamestate import TicTacToeState


def minimax(parent, level=0):
    parent.level = level
    if parent.end:
        parent.getScore()
        #print parent.score
        #return parent
    else:
        parent.getChildren()
        #print len(parent.children)
        for child in parent.children:
            minimax(child, level=level+1)
        parent.getScoreFromChildren()


def printTree(parent):
    print parent.level, parent.score, len(parent.children)
    for child in parent.children:
        printTree(child)



root = TicTacToeState([1,-1,0,0,1,-1,1,-1,-1])
minimax(root)
print root
#print "STATUS"
#printTree(root)
#print ""
#print ""
print ""
print ""
print "Best child"
print root.bestChild

    
