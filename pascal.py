import sys
args = sys.argv[1:5]

import numpy as np      # to use np arrays with PIL
from PIL import Image   # to generate images of fractals

# printing debug mode; VERBOSE is a Boolean
VERBOSE = True

# print if VERBOSE
def vpr(message):
    if VERBOSE:
        print("VPr:\t" + message + "\n")
    else:
        pass

# name the arguments so there is no confusion
# this revereses the order of the first two arguments
# new syntax: [modulus] [rowCount] [showTriangle*] [showZeroRows*]
# * optional; default to False
try:
    modulus = args[0]
except:
    modulus = input("No modulus provided. Enter a modulus: ")
try:
    rowCount = args[1]
except:
    rowCount = input("No row count provided. Enter a number of rows: ")
try:
    showTriangle = args[2]
except:
    showTriangle = False
    vpr("No argument given; not showing triangle in console.")
try:
    showZeroRows = args[3]
except:
    showZeroRows = False
    vpr("No argument given; not showing zero rows in console.")

def checkBool(inp, default=False):
    # if the input is already a boolean, use it
    if isinstance(inp, bool):
        return inp
    
    # otherwise, try to convert to integer
    try:
        inp = int(inp)
    except:
        # in case it's not a boolean or an integer,
        # use the default truth value
        inp = default

    # if the input is an integer, assign as follows:
    if inp == 0:
        inp = False
    
    elif inp == 1:
        inp = True
    # unless the integer doesn't make sense
    else:
        vpr(f"{inp} is not a boolean; using default value {default}")
        inp = default
    
    return inp

# sanitize inputs
# modulus
while (not isinstance(modulus, int) or modulus < 1):
    try:
        modulus = int(modulus)
        if modulus == 0:
            modulus = input(f"Error: modulus cannot be 0. Please enter a nonzero integer: ")
        elif modulus < 0:
            modulus = modulus * (-1)
            print(f"Given negative modulus; the modulus is now {modulus}")
    except:
        modulus = input(f"Error: bad modulus. {modulus} is not an integer. Please enter an integer: ")
vpr(f"The modulus is {modulus}")

# sanitize rowCount
while (not isinstance(rowCount, int) or rowCount < 1):
    try:
        rowCount = int(rowCount)
        if rowCount < 0:
            rowCount = rowCount * (-1)
            print(f"Given negative row count; the row count is now {rowCount}")
    except:
        rowCount = input(f"Error: bad row count. {rowCount} is not an integer. Please enter an integer: ")
vpr(f"The row count is {rowCount}")

# sanitize showTriangle (if given)
showTriangle = checkBool(showTriangle)
if showTriangle:
    vpr("Showing triangle in console.")
else:
    vpr("Not showing triangle in console.")

# sanitize showZeroRows (if given)
showZeroRows = checkBool(showZeroRows)
if showZeroRows:
    vpr("Showing zero rows in console.")
else:
    vpr("Not showing zero rows in console.")

# parameters are named differently than global variable names
# rc = local row count (global is rowCount)
# mod = modulus (global is modulus)
# PRINT = local version of VERBOSE
def pascal(rc, PRINT=True):
    # create pascal's triangle as a dictionary, where each key is the row number
    # and each value is the row digits stored as a list
    # so that we will always have at least {1:[1], 2:[1, 1], ...}
    triangle = {}
    triangle[1] = [1]
    triangle[2] = [1, 1]

    for row in range(3, rc+1):
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

def pascalMod(rc, mod, PRINT=True):
    # create pascal's triangle as a dictionary, where each key is the row number
    # and each value is the row digits stored as a list
    # so that we will always have at least {1:[1], 2:[1, 1], ...}
    triangle = {}
    triangle[1] = [1]
    triangle[2] = [1, 1]

    for row in range(3, rc+1):
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
                newValue = (triangle[row-1][digit-1] + triangle[row-1][digit])%mod
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

def pascalZeros(rc, mod, PRINT=True, TRI=False):
    # form the list of full rows
    noZeroRows = []
    # create the triangle to work from
    # using the arguments passed
    triangle = pascalMod(rc, mod, TRI)
    print("Input: {} rows, mod {}".format(rc, mod))
    
    for row in range(len(triangle)):
    # print(triangle[row+1])
        if not 0 in triangle[row+1]:
            noZeroRows.append(row+1)
            if PRINT:
                print("No 0 in row {}".format(row))
    
    return noZeroRows

# pascalZeros(int(args[0]), int(args[1]), int(args[2]), int(args[3]))

#### IMAGE EXPORT PART
def exportImage(rc, mod):

    bg = (255, 255, 255, 0)      # background color is white/transparent
    fg = (0, 0, 0, 255)          # foreground color is black

    # have an array for the image to be drawn from
    # numpy will convert this to an array of uint8 later
    imageArray = []

    # build a list of pixels from the strings that make up each row
    triangle = pascalMod(rc, mod, False)
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
    imageName = f"pMod{modulus}-{rowCount}r.png"

    imageArray = np.array(imageArray, dtype=np.uint8)
    triangleImage = Image.fromarray(imageArray)
    # box sampling works best because one pixel of source = one pixel of output
    triangleImage = triangleImage.resize((imageX, imageY), resample=Image.BOX)
    # change the colorspace to remove unnecessary data
    triangleImage = triangleImage.convert("LA")

    triangleImage.save(imageName)
    triangleImage.show()

exportImage(rowCount, modulus)
