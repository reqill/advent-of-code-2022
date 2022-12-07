from pathlib import Path    

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines

def getNumberOfStacks(stacks:list):
    indicatorRow = stacks[-1]
    indicatorRow = indicatorRow.split(" ")  
    
    for _ in range(indicatorRow.count("")):
        indicatorRow.remove("")
    
    numberOfColumns = int(indicatorRow[-1])
    
    return numberOfColumns

def arrangeByStacks(stacks:list, stackGap:int=1, stackWidth:int=3):
    numberOfStacks = getNumberOfStacks(stacks)
    stacks = stacks[:-1]
    displacement = stackGap + stackWidth
    emptyStackIndicator = " "*stackWidth #"[" + " "*(stackWidth-2) + "]"
    maxStackHeight = len(stacks)
    arrangedStacks = [[None for _ in range(numberOfStacks)] for _ in range(maxStackHeight)]

    for itemNumber in range(maxStackHeight):
        for stackNumber in range(numberOfStacks):
            curr = stacks[itemNumber][(stackNumber*displacement):(stackNumber*displacement+stackWidth)]
            item = curr if not curr == " "*stackWidth else emptyStackIndicator
            arrangedStacks[itemNumber][stackNumber] = item
    
    fixedStacks = [[] for _ in range(numberOfStacks)]
    
    for stack in arrangedStacks:
        for i in range(len(stack)):
            fixedStacks[i].insert(0, stack[i])
    
    return fixedStacks

def printStacks(title:str, stacksInput:list):
    print()
    print(title, end="\n\n")
    
    stacks = stacksInput.copy()
    
    for i in range(len(stacks)):
        stacks[i] = stacks[i][::-1]
    
    for i in range(len(stacks[0])):
        for stack in stacks:
            print(f"{stack[i]}", end=" ")
        print()
        
    for _ in range(len(stacks)):
        print("___", end=" ")
    print()
    
    for i in range(len(stacks)):
        print(f" {i+1} ", end=" ")
    print()
    
def extractIntructionData(instruction:str):
    instruction = instruction.split(" ")
    
    for _ in range(instruction.count("")):
        instruction.remove("")
        
    instruction.remove("move")
    instruction.remove("from")
    instruction.remove("to")
    
    for i in range(len(instruction)):
        instruction[i] = int(instruction[i])
    
    return instruction

def getNumberOfItemsInStack(stack: list):
    count = 0
    
    for item in stack:
        if not item == " "*3:
            count += 1
    
    return count

def sortStacksByInstructions(stacks:list, instructions:list):
    for instruction in instructions:
        [numberOfItemsToMove, stackToTakeItemsFrom, stackToPlaceItemsTo] = extractIntructionData(instruction)
        tsIDX = stackToTakeItemsFrom-1
        psIDX = stackToPlaceItemsTo-1
        
        numberOfItemsInStackToPlaceItemsTo = getNumberOfItemsInStack(stacks[psIDX])
        numberOfFreeSpotsInStackToPlaceItemsTo = len(stacks[psIDX]) - numberOfItemsInStackToPlaceItemsTo
        numberOfItemsInStackToTakeItemsFrom = getNumberOfItemsInStack(stacks[tsIDX])
        
        takenItems = []
        if numberOfItemsInStackToTakeItemsFrom <= numberOfItemsToMove:
            takenItems = stacks[tsIDX][:numberOfItemsInStackToTakeItemsFrom]
        elif numberOfItemsInStackToTakeItemsFrom > numberOfItemsToMove:
            takenItems = stacks[tsIDX][(numberOfItemsInStackToTakeItemsFrom-numberOfItemsToMove):numberOfItemsInStackToTakeItemsFrom]
        for i in range(numberOfItemsToMove):
            stacks[tsIDX][numberOfItemsInStackToTakeItemsFrom-numberOfItemsToMove + i] = " "*3
                
        # takenItems.reverse()
            
        if len(takenItems) > 0:
            rowsToAdd = numberOfItemsToMove - numberOfFreeSpotsInStackToPlaceItemsTo
            if rowsToAdd > 0:
                for i in range(len(stacks)):
                    for _ in range(rowsToAdd):
                        stacks[i].append(" "*3)
            for i in range(len(takenItems)):
                stacks[psIDX][numberOfItemsInStackToPlaceItemsTo + i] = takenItems[i]
        # printStacks(f"Stacks during operation ({instruction}):", removeEmptyRows(stacks))
    return removeEmptyRows(stacks)

def removeEmptyRows(stacks:list):
    maxHeight = 0
    
    for stack in stacks:
        currStackHeight = getNumberOfItemsInStack(stack)
        if currStackHeight > maxHeight:
            maxHeight = currStackHeight
    
    for i in range(len(stacks)):
        stacks[i] = stacks[i][:maxHeight]
    
    return stacks
        
def getStackTopValues(stacks:list):
    values = []
    
    for stack in stacks:
        numberOfItems = getNumberOfItemsInStack(stack)
        values.append(stack[numberOfItems-1])  
        
    return values

def main():
    stacks1 = linesFromFileToList("stack1.txt")
    intructions1 = linesFromFileToList("instructions1.txt")
    
    arrangedStacks = arrangeByStacks(stacks1)
    printStacks("Stacks before operation:", arrangedStacks)
    
    sortedStacks = sortStacksByInstructions(arrangedStacks, intructions1)
    printStacks("Stacks after operation:", sortedStacks)
    
    # join all items from list to string removing [ ]
    topValues = getStackTopValues(sortedStacks)
    topValues = "".join(topValues)
    topValues = topValues.replace("[", "")
    topValues = topValues.replace("]", "")
    print(f"Top values of stacks: {topValues}")
    
if __name__ == "__main__":
    main()