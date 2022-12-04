from pathlib import Path    

values = {}
for i in range(1, 27):
    values[chr(i + 96)] = i
for i in range(1, 27):
    values[chr(i + 64)] = i + 26


def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines

def splitIntoCompartments(compartmentPairs: list):
    compartments = []
    for pair in compartmentPairs:
        compartments.append([pair[0:len(pair)//2], pair[len(pair)//2:]])

    return compartments
        
def chackWhichLetterIsCommonInCompartmentPair(compartmentPair: list):
    for letter in compartmentPair[0]:
        for letter2 in compartmentPair[1]:
            if letter == letter2:
                return letter
                
def chackWhichLetterIsCommonInCompartmentTrio(compartmentPair: list):
    for letter in compartmentPair[0]:
        for letter2 in compartmentPair[1]:
            for letter3 in compartmentPair[2]:
                if letter == letter2 == letter3:
                    return letter


def listOfLettersCommonIsTrios(compartments: list):
    commonItems = []
    for compartmentPair in compartments:
        commonItems.append(chackWhichLetterIsCommonInCompartmentTrio(compartmentPair))
    return commonItems                

def listOfLettersCommonInPairs(compartments: list):
    commonItems = []
    for compartmentPair in compartments:
        commonItems.append(chackWhichLetterIsCommonInCompartmentPair(compartmentPair))
    return commonItems
    
def sumScoreForCommonLetters(commonItems: list):
    sum = 0
    for item in commonItems:
        sum += values[item]
    return sum

def splitIntoGroupsOfThree(lines: list):
    groups = []
    for i in range(0, len(lines), 3):
        groups.append([lines[i], lines[i+1], lines[i+2]])
    return groups

def main():
    comparments = linesFromFileToList("input1.txt")
    comparments = splitIntoCompartments(comparments)
    commonItems = listOfLettersCommonInPairs(comparments)
    priorityScore = sumScoreForCommonLetters(commonItems)
    print(priorityScore)
    
    allElves = linesFromFileToList("input2.txt")
    groups = splitIntoGroupsOfThree(allElves)
    badges = listOfLettersCommonIsTrios(groups)
    priorityBadgeScore = sumScoreForCommonLetters(badges)
    print(priorityBadgeScore)
    
    
if __name__ == "__main__":
    main()