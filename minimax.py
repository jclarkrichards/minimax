"""If maxLevel is None, then full depth is searched.  Otherwise the depth will never go below maxLevel"""
class Minimax(object):
    def __init__(self):
        self.maxLevel = None
        self.num = 0

    def minimax(self, parent):
        #print "LEVEL "+ str(parent.level)
        self.num += 1
        if parent.end:
            parent.getScore()
            self.maxLevel = parent.setMaxLevel(self.maxLevel)
        else:
            if self.maxLevel is not None:
                if parent.level < self.maxLevel:
                    parent.getChildren()
            else:
                parent.getChildren()
            #parent.getChildren()
            
            #if parent.level != 0:
            #    parent.chooseRandomChild()

            if len(parent.children) > 0:
                for i, child in enumerate(parent.children):
                    #print "CHILD "+str(i)
                    self.minimax(child)
                parent.getScoreFromChildren()

                if parent.level == 0:
                    print len(parent.children)
                    print [child.invalid for child in parent.children]
                #    print [child.numFlips for child in parent.children]



















