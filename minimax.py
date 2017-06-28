from gamestate import TicTacToeState, Eclipse

def minimax(parent, level=0):
    print level
    parent.level = level
    if parent.end:
        parent.getScore()
    else:
        parent.getChildren()
        print "children = " + str(len(parent.children))
        if len(parent.children) == 0:
            print parent.state
        for child in parent.children:
            minimax(child, level=level+1)
        parent.getScoreFromChildren()


def printTree(parent):
    print parent.level, parent.score, len(parent.children)
    for child in parent.children:
        printTree(child)


board = [-1,0,1,0,1,-1,0,2,1,-2,-2,0,-1,0,2,2]
state = Eclipse(board)
minimax(state)
print state.state
print ""
print state.bestChild.state

"""
XPlayer = True #Human player
xturn = True
gameover = False
state = TicTacToeState([-1,-1,-1,-1,-1,-1,-1,-1,-1])

print state
while not gameover:
    if xturn:
        if XPlayer:
            i = int(raw_input("Enter an X at location: (0-8)  "))
            state.state[i] = 1
            state = TicTacToeState(state.state)
        else:
            pass
    else:
        minimax(state)
        state = state.bestChild

    if state.end:
        gameover = True
    else:
        xturn = not xturn
    print state
    print ""

print "GAME OVER"
print state
"""            
    
