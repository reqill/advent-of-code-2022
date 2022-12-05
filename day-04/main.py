from pathlib import Path    

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines

def splitStringsInArrayToSubListsByComma(list:list):
    for i in range(len(list)):
        list[i] = list[i].split(",")
    return list

def splitDutyShiftToStartAndEndHours(list:list):
    for i in range(len(list)):
        for j in range(len(list[i])):
            list[i][j] =  list[i][j].split("-")
            for k in range(len(list[i][j])):
                list[i][j][k] = int(list[i][j][k]) 
    return list
        
def checkIfShiftIsIncludedInSecondShiftOfShiftPair(shiftPair: list):
    if shiftPair[0][0] >= shiftPair[1][0] and shiftPair[0][1] <= shiftPair[1][1] or shiftPair[0][0] <= shiftPair[1][0] and shiftPair[0][1] >= shiftPair[1][1]:
        return True
    return False

def checkIfShiftHaveAnyOverlappedHoursToTheirPair(shiftPair: list):
    shift_one_start = shiftPair[0][0]
    shift_one_end = shiftPair[0][1]
    shift_two_start = shiftPair[1][0]
    shift_two_end = shiftPair[1][1]
    
    if shift_one_start >= shift_two_start and shift_one_start <= shift_two_end or shift_one_end >= shift_two_start and shift_one_end <= shift_two_end or shift_two_start >= shift_one_start and shift_two_start <= shift_one_end or shift_two_end >= shift_one_start and shift_two_end <= shift_one_end:
        return True
    return False


def countOverlappingShiftsByWhole(shifts:list):
    count = 0
    for shiftPair in shifts:
        if checkIfShiftIsIncludedInSecondShiftOfShiftPair(shiftPair):
            count += 1
    return count

def countOverlappingShiftsByHour(shifts:list):
    count = 0
    for shiftPair in shifts:
        if checkIfShiftHaveAnyOverlappedHoursToTheirPair(shiftPair):
            count += 1
    return count

def main():
    dutyPairs = linesFromFileToList("input1.txt")
    dutyPairs = splitStringsInArrayToSubListsByComma(dutyPairs)
    dutyPairs = splitDutyShiftToStartAndEndHours(dutyPairs)
    overlappedShiftPairsByWhole = countOverlappingShiftsByWhole(dutyPairs)
    overlappingShiftPairsByHour = countOverlappingShiftsByHour(dutyPairs)
    print(overlappedShiftPairsByWhole)
    print(overlappingShiftPairsByHour)
    
if __name__ == "__main__":
    main()