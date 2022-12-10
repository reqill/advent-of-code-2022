from pathlib import Path    

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines

def getIndex(value:int, list:list):
    for i in range(len(list)):
        if sum(list[:i]) == value:
            return i
    return -1

def printCrt(crt:list):
    for i in range(len(crt)):
        for j in range(len(crt[i])):
            print(crt[i][j], end=" ")
        print()

def main():
    instructions = linesFromFileToList("test.txt")
    futureActions = []
    cycleValues = []
    value = 1
    prevValue = 1
    cycleSchema=[]
    crt = [["."] * 40 for _ in range(6)]
    pixel = 0
    
    for i in range(len(instructions)):
        instructions[i] = instructions[i].split(" ")
        if len(instructions[i]) == 2:
            cycleSchema.append(2)
        else:
            cycleSchema.append(1)
    
    for i in range(sum(cycleSchema)-1):
        crt[i // 40 ][value] = "#"  
        
        if (i + 21) % 40 == 0:
            cycleValues.append(value * (i + 1))
   
        if len(instructions[getIndex(i, cycleSchema)]) == 2:
            futureActions.append([2, int(instructions[getIndex(i, cycleSchema)][1])])

        for j in range(len(futureActions)):
            futureActions[j][0] -= 1
                
        if len(futureActions) > 0 and futureActions[0][0] == 0:
            value += futureActions[0][1]
            futureActions = futureActions[1:]
    
    print(cycleValues)
    print(sum(cycleValues))
    print(sum(cycleSchema))
    printCrt(crt)

    
    
    
if __name__ == "__main__":
    main()