from pathlib import Path    

def linesFromFileToList(path:str):
    lines = []
    with open(Path(__file__).parent / 
              path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        
    return lines
    
def checkIfStringHasDuplicates(string:str):
    for i in range(len(string)):
        for j in range(i+1, len(string)):
            if string[i] == string[j]:
                return True
    return False
    
def getMarkerAndStartingPosition(line:str, markerLength:int = 4):
    marker = ""
    position = 0
    
    for i, letter in enumerate(line):
        hasDuplicates = checkIfStringHasDuplicates(marker)
        
        if len(marker) == markerLength and not hasDuplicates:
            position = i
            break
        
        elif len(marker) == markerLength and hasDuplicates:
            marker = marker[1:markerLength]
            
        marker += letter
    
    return [marker, position] 

def main():
    lines = linesFromFileToList("input1.txt")
    [startMarker, startPosition] = getMarkerAndStartingPosition(lines[0])
    [messageMarker, messagePosition] = getMarkerAndStartingPosition(lines[0], 14)
    
    print(startMarker, startPosition)
    print(messageMarker, messagePosition)
    
if __name__ == "__main__":
    main()