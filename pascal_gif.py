import sys
args = sys.argv[1:5]

import numpy as np      # to use np arrays with PIL
from PIL import Image   # to generate images of fractals

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
            print(printRow + str(row-1))
    
    return triangle

def pascalZeros(rowCount, n, PRINT=True, TRI=False):
    noZeroRows = []
    triangle = pascalMod(rowCount, n, TRI)
    print("Input: {} rows, mod {}".format(int(args[0]), int(args[1])))
    for row in range(len(triangle)):
    # print(triangle[row+1])
        if not 0 in triangle[row+1]:
            noZeroRows.append(row+1)
            if PRINT:
                print("No 0 in row {}".format(row))
    return noZeroRows

# pascalZeros(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
def image(rowCount, n):
    rowCount = int(rowCount)
    n = int(n)
    
    #### IMAGE EXPORT PART
    bg = (255, 255, 255, 0)    # background color is white
    fg = (0, 0, 0, 255)          # foreground color is black

    # have an array for the image to be drawn from
    # numpy will convert this to an array of uint8 later
    imageArray = []

    # build a list of pixels from the strings that make up each row
    triangle = pascalMod(rowCount, n, False)
    # print(triangle[3])  # returns [1, 0, 1] for 32 rows mod 2 (the information is accurate)

    # find how many rows there are (y dimension of the array)
    maxRow = len(triangle)
    # print(f"The bottom row is {maxRow - 1}, which contains {triangle[maxRow]} as values")

    imageDict = {}
    # loop to put these all in one array
    for row in triangle:
        currentRow = []
        # print(triangle[row])
        for char in triangle[row]:
            if char == 0:
                # add two bg spaces to the array
                # textbook inelegant hack
                currentRow.insert(0, bg)
                currentRow.insert(0, bg)
            elif char != 0:
                # add two fg spaces to the array
                currentRow.insert(0, fg)
                currentRow.insert(0, fg)
        # save the row information to the dictionary
        imageDict[row] = currentRow

    # after the triangle information has been added to the dictionary
    #### print(imageDict[maxRow])

    # add appropriate white space
    # get the length of the entire image (this is the length of maxRow before padding)
    maxLen = len(imageDict[maxRow]) # this should be twice the number of rows

    for row in imageDict:
        # print(f"This is the current list: {imageDict[row]}")
        currentRow = imageDict[row]
        currentLen = len(currentRow)
        
        # calculate padding; we want to center the rows under each other
        # by making each block 2 pixels wide and staggering by 1 each time
        # padding is how much data we need minus how much we have
        targetLen = maxLen - currentLen
        padding = int(targetLen / 2)
        
        # split the padding between the front and back to keep the rows centered
        # in the image
        for i in range(0, padding):
            currentRow.insert(0, bg)
            currentRow.insert(len(currentRow), bg)

        # print(f"Now the list looks like this: {currentRow}\n")
        
    # double each row from the dictionary when building the array 
    # this causes the triangle to be made up of 2x2 blocks, not 2x1 planks
    for row in imageDict:
        currentRow = imageDict[row]
        # appending each row twice achieves a doubling effect
        # an inelegant hack, but quite unbreakable
        imageArray.append(currentRow)
        imageArray.append(currentRow)

    # calculate appropriate dimensions for the image
    imageX = maxLen
    imageY = 2 * int(rowCount)

    # name the file
    imageName = f"pMod{n}-{rowCount}r.png"

    imageArray = np.array(imageArray, dtype=np.uint8)
    triangleImage = Image.fromarray(imageArray)
    # box sampling works best because one pixel of source = one pixel of output
    triangleImage = triangleImage.resize((imageX, imageY), resample=Image.BOX)
    # change the colorspace to remove unnecessary data
    # triangleImage = triangleImage.convert("LA")

    # triangleImage.save(imageName)
    return triangleImage

# image(args[0], args[1])

frames = []
for i in range(2, 13):
    currentFrame = image(args[0], i)
    frames.append(currentFrame)

frames[0].save("test_gif.gif", save_all=True, append_images=frames[1:], optimize=False, duration=1000, loop=0)
