from pathlib import Path    
from copy import deepcopy

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines

def splitCommand(command:str):
    for i in range(len(command)):
        command[i] = command[i].split(" ")
    return command

def moveH(direction: str, plane: list, Hx: int, Hy: int):
    if direction == "U":
        if Hy == 0:
            plane.insert(0, ["·" for _ in range(len(plane[0]))])
        else:
            Hy -= 1
            
    elif direction == "D":
        if Hy == len(plane) - 1:
            plane.append(["·" for _ in range(len(plane[0]))])
        Hy += 1
            
    elif direction == "R":
        if Hx == len(plane[0]) - 1:
            for i in range(len(plane)):
                plane[i].append("·")
        Hx += 1
            
    elif direction == "L":
        if Hx == 0:
            for i in range(len(plane)):
                plane[i].insert(0, "·")
        else:
            Hx -= 1
    
    return plane, Hx, Hy
    
def moveT(direction: str, Hx: int, Hy: int, Tx: int, Ty: int):
    disX, disY = distance(Hx, Hy, Tx, Ty)
    needToMove = True if disX > 1 or disY > 1 else False
    relativeDirection = direction
    
    if direction == "U":
        if needToMove and Tx == Hx:
            Ty -= 1
        elif needToMove and Tx == Hx - 1 or Tx == Hx - 2:
            Tx += 1
            Ty -= 1
            relativeDirection = "R"
        elif needToMove and Tx == Hx + 1 or Tx == Hx + 2:
            Tx -= 1
            Ty -= 1
            relativeDirection = "L"
            
    elif direction == "D":
        if needToMove and Tx == Hx:
            Ty += 1
        elif needToMove and Tx == Hx - 1 or Tx == Hx - 2:
            Tx += 1
            Ty += 1
            elativeDirection = "R"
        elif needToMove and Tx == Hx + 1 or Tx == Hx + 2:
            Tx -= 1
            Ty += 1
            relativeDirection = "L"
        
    elif direction == "R":
        if needToMove and Ty == Hy:
            Tx += 1
        elif needToMove and Ty == Hy - 1 or Ty == Hy - 2:
            Tx += 1
            Ty += 1
            relativeDirection = "D"
        elif needToMove and Ty == Hy + 1 or Ty == Hy + 2:
            Tx += 1
            Ty -= 1
            relativeDirection = "U"
            
    elif direction == "L":
        if needToMove and Ty == Hy:
            Tx -= 1
        elif needToMove and Ty == Hy - 1 or Ty == Hy - 2:
            Tx -= 1
            Ty += 1
            relativeDirection = "D"
        elif needToMove and Ty == Hy + 1 or Ty == Hy + 2:
            Tx -= 1
            Ty -= 1
            relativeDirection = "U"
            
    return Tx, Ty, relativeDirection

def distance(Hx: int, Hy: int, Tx: int, Ty: int):
    distanceX = abs(Hx - Tx)
    distanceY = abs(Hy - Ty)
    
    return distanceX, distanceY

def move(direction: str, plane: list, Hx: int, Hy: int, Tx: int, Ty: int, middleX: list, middleY: list):    
    plane[Ty][Tx] = "·"
    plane[Hy][Hx] = "·"
    
    plane, Hx, Hy = moveH(direction, plane, Hx, Hy)
    
    relativeDirection = direction
    
    startPosForMiddleX = Hx
    startPosForMiddleY = Hy
    
    for i in range(len(middleX)):
        startPosForMiddleX, startPosForMiddleY, relativeDirection= moveT(relativeDirection, startPosForMiddleX, startPosForMiddleY, middleX[i], middleY[i])
        middleX[i] = startPosForMiddleX
        middleY[i] = startPosForMiddleY

        
    
    Tx, Ty, relativeDirection = moveT(relativeDirection, startPosForMiddleX, startPosForMiddleY, Tx, Ty)

    plane[Ty][Tx] = "T"
    plane[Hy][Hx] = "H"
 
    return plane, Hx, Hy, Tx, Ty, middleX, middleY
        
def generateMovement(commands: list):
    size = 801
    plane = [["·" for _ in range(size)] for _ in range(size)]
    tracker = []
    plane[size//2][size//2] = "H"
    Hx = size//2
    Hy = size // 2
    middleX = [size//2 for _ in range(8)]
    middleY = [size//2 for _ in range(8)]
    Tx = size//2
    Ty = size // 2
    
    
    for command in commands:
        movement = command[0]
        steps = int(command[1])
        
        for _ in range(steps):
            plane, Hx, Hy, Tx, Ty, middleX, middleY = move(movement, plane, Hx, Hy, Tx, Ty, middleX, middleY)
            tracker.append([Tx, Ty])
            
        
    printPlaneWithTracker(plane, tracker, True, middleX, middleY)
    

            
def generateTracker(tracker: list, planeW: int, planeH: int):
    output = [["·" for _ in range(planeW)] for _ in range(planeH)]
    string = ""

    for i in range(len(tracker)):
        output[tracker[i][1]][tracker[i][0]] = "#"
        
    for i in range(len(output)):
        for j in range(len(output[i])):
            string += output[i][j]
        string += "\n"
    
    return output, string

def countChar(plane: list, char: str):
    count = 0
    for i in range(len(plane)):
        for j in range(len(plane[i])):
            if plane[i][j] == char:
                count += 1
    return count

def printPlaneWithTracker(plane: list, tracker: list, end: bool, middleX: list, middleY: list):    
    printPlane = plane.copy()
    times = (len(printPlane[0])) * 2 - 1
    whereTailHaveBeen, string = generateTracker(tracker, len(printPlane[0]), len(printPlane))

    # for i in range(len(printPlane)):
    #     for j in range(len(printPlane[i])):
    #         for x in range(len(middleX)):
    #             if i == middleY[x] and j == middleX[x]:
    #                 printPlane[i][j] = str(x+1)
    #             # elif printPlane[i][j] != "H" and printPlane[i][j] != "T":
    #             #     printPlane[i][j] = "·"

    # print("="*times, end="\n")
    # for i in range(len(printPlane)):
    #     for j in range(len(printPlane[i])):
    #         print(printPlane[i][j], end = " ")
    #     print()
    # print("="*times, end="\n")
    
    # for i in range(len(printPlane)):
    #     for j in range(len(printPlane[i])):
    #         print(whereTailHaveBeen[i][j], end = " ")
    #     print()
        
    # if(end):
    #     print("="*times, end="\n")

    
    with open(Path(__file__).parent / 'preview.txt', 'w', encoding="utf-8") as f:
        f.write(string)
        
    print(len(plane), len(plane[0]))
    print("T have been in", countChar(whereTailHaveBeen, "#"), "places")

def main():
    commands = splitCommand(linesFromFileToList("input.txt"))
    generateMovement(commands)
    
if __name__ == "__main__":
    main()