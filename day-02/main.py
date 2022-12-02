from pathlib import Path  

def readLinesFromFile(path):
    lines = []
    with open(Path(__file__).parent/path, 'r') as file:
        lines = file.readlines()
    return lines

def splitAndCleanEnemyYou(rows):
    for i in range(len(rows)):
        rows[i] = (rows[i].strip("\n").split(" "))
    return rows
     
def haveWon(enemyPick, yourPick):
    if enemyPick == yourPick:
        return None
    elif enemyPick == "A" and yourPick == "Y":
        return True
    elif enemyPick == "A" and yourPick == "Z":
        return False
    elif enemyPick == "B" and yourPick == "X":
        return False
    elif enemyPick == "B" and yourPick == "Z":
        return True
    elif enemyPick == "C" and yourPick == "X":
        return True
    elif enemyPick == "C" and yourPick == "Y":
        return False
    else:
        return None
    
def changePickResultToPick(enemyPick, pickResult):
    if pickResult == "X":
        if enemyPick == "A":
            return "Z"
        elif enemyPick == "B":
            return "X"
        else:
            return "Y"
    elif pickResult == "Y":
        if enemyPick == "A":
            return "X"
        elif enemyPick == "B":
            return "Y"
        else:
            return "Z"
    else:
        if enemyPick == "A":
            return "Y"
        elif enemyPick == "B":
            return "Z"
        else:
            return "X"
    
def calculateScoreForRound(row):
    win = haveWon(row[0], row[1])
    pickScore = 1 if row[1] == "X" else 2 if row[1] == "Y" else 3
    winScore = 3 if win == None else 0 if win == False else 6
    return pickScore + winScore

def calculateScore(rows):
    score = 0
    for row in rows:
        score += calculateScoreForRound(row)
    return score

def changeSecondPickToSelectedOutcome(list):
    for i in range(len(list)):
        list[i][1] = changePickResultToPick(list[i][0], list[i][1])
    return list

def main():
    tacticSheet = readLinesFromFile('./input.txt')
    tacticSheet = splitAndCleanEnemyYou(tacticSheet)
    tacticSheet = changeSecondPickToSelectedOutcome(tacticSheet)
    score = calculateScore(tacticSheet)
    print(score)

if __name__ == "__main__":
    main()
