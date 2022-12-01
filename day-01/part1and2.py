from pathlib import Path    

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()
    return lines

def groupAndSumBetweenEmpty(lines: list):
    elvesCalories = [None] * len(lines)
    elfIdx = 0
    
    for line in lines:
        if line == "\n":
            elfIdx += 1
            continue
        else:
            line.strip("\n") 
            if elvesCalories[elfIdx] == None:
                elvesCalories[elfIdx] = 0
            try:
                elvesCalories[elfIdx] += int(line)
            except ValueError:
                continue
            
    return elvesCalories

def findMaxValueIndex(list:list):
    index = 0
    
    for i in range(len(list)):
        currMax = list[index]
        currItem = list[i]
        
        if currItem != None and currItem > currMax:
            index = i
            
    return index
    
def main():
    lines = linesFromFileToList('./input.txt')
    elvesCalories = groupAndSumBetweenEmpty(lines)

    elvesCalories = [x for x in elvesCalories if x != None]
    
    elfWIthMostCalories = findMaxValueIndex(elvesCalories)

    print("Elf with most calories is elf number "+str(elfWIthMostCalories+1)+" with total of "  + str(elvesCalories[elfWIthMostCalories]) + " calories")

    elvesCalories.sort()
    elvesCalories.reverse()
    
    print(sum(elvesCalories[0:3]))
    
    

    
    
    
if __name__ == "__main__":
    main()