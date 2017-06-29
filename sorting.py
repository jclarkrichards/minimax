def stacksort(items):
    stacks = []
    for item in items:
        if len(stacks) == 0:
            stack = [item]
            stacks.append(stack)
        else:
            added = False
            for stack in stacks:
                if item <= stack[-1]:
                    stack.append(item)
                    added = True
                    break
            if not added:
                stack = [item]
                stacks.append(stack)

    
    sorted = []
    for stack in stacks:
        stack.reverse()
        sorted += stack
        
    #for i in range(len(items)):
    #    for stack in stacks:
    #        if len(stack) > 0:
                
    return sorted


def bubble(items):
    sorted = False
    temp = 0
    while not sorted:
        sorted = True
        for i in range(len(items)-1):
            if items[i] > items[i+1]:
                temp = items[i]
                items[i] = items[i+1]
                items[i+1] = temp
                sorted = False

    return items
