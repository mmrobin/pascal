# this script is used to export numerical data
# as a file which can be read by reader.py

# we need to read the data because it is more computationally expensive
# to generate all of the rows than it is to read all the rows we already have
# and to begin generation from there
# (all of this is to save compute time)

import sys
import os
import random
import time

# just for testing
from pascalNew import pascalMod, vpr

# rc = row count
# mod = modulus
# ftxConvertData converts a triangle's fractal dictionary
# to the text block that gets saved in an ftx file
def ftxConvertData(rc, mod):
    text = ""
    # only need to import the triangle for testing purposes
    triangle = pascalMod(rc, mod, False)
    for rowNumber in triangle:
        currentRow = triangle[rowNumber]
        rowIndex = 0
        # vpr(f"Row {rowNumber} is {currentRow}")
        
        for value in currentRow:
            if rowIndex < rowNumber - 1:
                text = text + (str(value) + "k")
                rowIndex += 1
            else:
                text = text + (str(value) + "n")

    # vpr(text)
    return text

def ftxSave(rc, mod, data):
    # saveftx should receive a block of text from convert()
    # and save it as a file with the extension .ftx
    # ftx = fractal text export
    fileName = f"p{mod}r{rc}"
    try:
        fileObject = open(f"{fileName}.ftx", "x")
    
    except:
        print(f"File {fileName}.ftx already exists!")
        yn = input (f"Overwrite {fileName}.ftx? (Y/n): ")
        
        if yn in ["Y", "y", ""]:
            print(f"Overwriting {fileName}.ftx")
            os.system(f"rm {fileName}.ftx")
            fileObject = open(f"{fileName}.ftx", "x")
        
        elif yn in ["N", "n"]:
            print("No changes were made.")
            return 0
        
        else:
            print("Bad input. No changes were made.")
            return 0
   
    dataLen = len(data)
    vpr(f"Data is {dataLen} characters.")
    nlCount = dataLen // 60

    # insert a newline character every 60 characters
    breakCount = 0
    for i in range(0, nlCount + 1):
        breakCount += 1
        data = data[:60 * breakCount - 1 + (2 * breakCount)] + "\n" + data[60 * breakCount - 1 + (2 * breakCount):]
    data = data.strip()
    
    fileObject.write(data)

def ftxRead(data):
    # lineList is a container to hold each line from the data
    # represented as integers in lists
    lineList = []
    # split the data into lines using the line delimiter n
    dataLines = data.split("n")
    # remove empty string at end
    dataLines = dataLines[0:-1]
    for line in dataLines:
        # split each line by the value delimiter k
        line = line.split("k")
        # convert strings to ints so that each line is represented
        # as a list of integers
        valueList = [int(x) for x in line]
        # the lineList contains each of these rows stored
        # as lists of ints
        lineList.append(valueList)

    return lineList

def constructTriangle(lineList):
    # constructTriangle receives the dataLines list from read()
    # the construction is not done in the read() function because
    # separating them allows the (optional) integrity check
    triangle = {}
    rowNumber = 0
    for row in lineList:
        triangle[rowNumber] = row
        rowNumber += 1
    # return the triangle as a dictionary
    return triangle

startTime = time.time()

data = ftxConvertData(1000, 5)

# ftxSave(1000, 5, data)

ftxFile = open("p5r60.ftx", "r")
ftxFile = ftxFile.read()
ftxLines = ftxRead(ftxFile)
ftxDict = constructTriangle(ftxLines)

print(ftxDict)

runTime = time.time() - startTime
print(f"\nSaved triangle data in {runTime} seconds.")

# ftxPascal() reads a .ftx file and constructs a fractal from it
def ftxPascal(rowCount, triangle):
    trianglePrint = {}
    for rowNumber in range(len(triangle)):
        rowValues = triangle[rowNumber]
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

#ftxPascal(60, ftxDict)
