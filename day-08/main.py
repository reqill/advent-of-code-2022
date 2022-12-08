from pathlib import Path    

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines

def checkIfTreeIsNotVisible(trees:str, xPos: int, yPos: int):
    currentTreeHeight = trees[xPos][yPos]
    isTopNotVisible = False
    isBottomNotVisible = False
    isRightNotVisible = False
    isLeftNotVisible = False
    x = xPos
    y = yPos
    
    while x < len(trees) - 1:
        x += 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            isRightNotVisible = True
        
    x = xPos
    
    while x > 0:
        x -= 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            isLeftNotVisible = True
        
    x = xPos
    
    while y < len(trees[x]) - 1:
        y += 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            isBottomNotVisible = True
    
    y = yPos
    
    while y > 0:
        y -= 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            isTopNotVisible = True
        
    return isTopNotVisible and isBottomNotVisible and isRightNotVisible and isLeftNotVisible

def countVisibleTrees(trees:str):
    count = 0
    
    for x in range(len(trees)):
        for y in range(len(trees[x])):
            if not checkIfTreeIsNotVisible(trees, x, y):
                count += 1
                
    return count

def scenicScoreForTree(trees:str, xPos: int, yPos: int):
    scoreTop = 0
    scoreBottom = 0
    scoreRight = 0
    scoreLeft = 0
    
    currentTreeHeight = trees[xPos][yPos]
    x = xPos
    y = yPos

    while x < len(trees) - 1:
        x += 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            scoreRight += 1
            break
        else:
            scoreRight += 1
        
    x = xPos
    
    while x > 0:
        x -= 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            scoreLeft += 1
            break
        else:
            scoreLeft += 1
        
    x = xPos
    
    while y < len(trees[x]) - 1:
        y += 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            scoreBottom += 1
            break
        else:
            scoreBottom += 1
    
    y = yPos
    
    while y > 0:
        y -= 1
        checkingTreeHeight = trees[x][y]
        if checkingTreeHeight >= currentTreeHeight:
            scoreTop += 1
            break
        else:
            scoreTop += 1
        
    return scoreTop * scoreBottom * scoreRight * scoreLeft
    
def scenicScoreForAllTrees(trees:str):
    scores = []
    
    for x in range(len(trees)):
        for y in range(len(trees[x])):
            scores.append(scenicScoreForTree(trees, x, y))
            
    return scores
    
def main():
    trees = linesFromFileToList("input.txt")
    visibleTrees = countVisibleTrees(trees)
    scenicScore = scenicScoreForAllTrees(trees)
    biggestScenicScore = max(scenicScore)
    print(visibleTrees)
    print(biggestScenicScore)
    
if __name__ == "__main__":
    main()