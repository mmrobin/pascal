def pascal(rowCount, PRINT=True):
    # create pascal's triangle as a dictionary, where each key is the row number
    # and each value is the row digits stored as a list
    # so that we will always have at least {1:[1], 2:[1, 1], ...}
    triangle = {}
    triangle[1] = [1]
    triangle[2] = [1, 1]

    for row in range(3, rowCount+1):
        rowLength = row             # easier to understand this way
        rowValues = [1]             # create a list to hold the row values
        
        for digit in range(rowLength - 2):
            rowValues.append(0)     # make a row of zeros
        rowValues.append(1)

        # print(rowValues)

        for digit in range(rowLength):
            if rowValues[digit] == 1:   # the only digits that hold a 1 at this point are the ends
                pass                    # don't change them
            else:
                # triangle: the triangle dictionary
                # row-1: the previous (above) row
                # digit and digit-1: the two numbers overhead
                newValue = triangle[row-1][digit-1] + triangle[row-1][digit]
                rowValues[digit] = newValue 
            #print(digit)

        triangle[row] = rowValues

    # print(triangle)
    if PRINT:
        for rowNumber in range(len(triangle)):
            rowValues = triangle[rowNumber+1]
            rowString = ""
            for value in rowValues:
                rowString = rowString + str(value) + " "
            rowString = rowString.center(rowCount*2)
            print(rowString)
    
    return triangle

import sys
args = sys.argv[1:5]

def pascalMod(rowCount, n, PRINT=True):
    # create pascal's triangle as a dictionary, where each key is the row number
    # and each value is the row digits stored as a list
    # so that we will always have at least {1:[1], 2:[1, 1], ...}
    triangle = {}
    triangle[1] = [1]
    triangle[2] = [1, 1]

    for row in range(3, rowCount+1):
        rowLength = row             # easier to understand this way
        rowValues = [1]             # create a list to hold the row values
        
        for digit in range(rowLength - 2):
            rowValues.append(0)     # make a row of zeros
        rowValues.append(1)

        # print(rowValues)

        for digit in range(rowLength):
            if rowValues[digit] == 1:   # the only digits that hold a 1 at this point are the ends
                pass                    # don't change them
            else:
                # triangle: the triangle dictionary
                # row-1: the previous (above) row
                # digit and digit-1: the two numbers overhead
                newValue = (triangle[row-1][digit-1] + triangle[row-1][digit])%n
                rowValues[digit] = newValue 
            #print(digit)

        triangle[row] = rowValues

    # print(triangle)
    if PRINT:
        trianglePrint = {}
        for rowNumber in range(len(triangle)):
            rowValues = triangle[rowNumber+1]
            rowString = ""
            for value in rowValues:
                if value != 0:
                    value = "\u2588\u2588"
                else:
                    value = "  "
                rowString = rowString + str(value)
            trianglePrint[rowNumber+1] = rowString

        centering = len(trianglePrint[rowCount])
        for row in trianglePrint:
            printRow = trianglePrint[row].center(centering * 2)
            print(printRow + str(row))
    
    return triangle

# pascalMod(36, 2)

def pascalZeros(rowCount, n, PRINT=True, TRI=False):
    noZeroRows = []
    triangle = pascalMod(rowCount, n, TRI)
    print("Input: {} rows, mod {}".format(int(args[0]), int(args[1])))
    for row in range(len(triangle)):
    # print(triangle[row+1])
        if not 0 in triangle[row+1]:
            noZeroRows.append(row+1)
            if PRINT:
                print("No 0 in row {}".format(row+1))
    return noZeroRows

pascalZeros(int(args[0]), int(args[1]), int(args[2]), int(args[3]))