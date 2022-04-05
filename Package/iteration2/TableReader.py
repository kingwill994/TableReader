
import csv
import numpy as np
from numpy.linalg import inv
import math

class TableReader:
    longestInstance = -1
    
    #--------Constructors------------
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = self.openFile()

    #---------------Public Methods for finding values-------------------------------
    def findValue(self, baseFeat, baseValue, targetFeat):
        #Returns single numerical single value
        #arguments are the data category and the desired data value that you want to find a corresponding value for another data category

        searchColumn = self.data.get(baseFeat)
        up = len(searchColumn) - 1
        down = 0

        upValue = searchColumn[up]
        downValue = searchColumn[down]

        direction = self.findDirection(upValue, downValue)
        if direction == 1:
            if upValue < baseValue or downValue > baseValue:
                return self.extrapSingle(searchColumn, baseFeat, baseValue, targetFeat)
                
            index = self.upBinarySearch(searchColumn, up, down, baseValue)

        elif direction == -1:
            if upValue > baseValue or downValue < baseValue:
                return self.extrapSingle(searchColumn, baseFeat, baseValue, targetFeat)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.downBinarySearch(searchColumn, up, down, baseValue)
        print("index ",index)
        if len(index) == 2:
            return self.interpSingle(baseFeat, baseValue, index, targetFeat)
        elif len(index) == 1:
            return self.getSingle(targetFeat, index)            
        else:
            print("Error -- findValue Method")
            return -1
        
    def findAllValues(self, baseFeat, baseValue):
        #returns a dictionary
        searchColumn = self.data.get(baseFeat)
        up = len(searchColumn) - 1
        down = 0

        upValue = searchColumn[up]
        downValue = searchColumn[down]

        direction = self.findDirection(upValue, downValue)
        if direction == 1:
            if upValue < baseValue or downValue > baseValue:
                return self.extrapAll(searchColumn, baseFeat, baseValue)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.upBinarySearch(searchColumn, up, down, baseValue)

        elif direction == -1:
            if upValue > baseValue or downValue < baseValue:
                return self.extrapAll(searchColumn, baseFeat, baseValue)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.downBinarySearch(searchColumn, up, down, baseValue)

        if len(index) == 2:
            return self.interpAll(baseFeat, baseValue, index)
        elif len(index) == 1:
            return self.getAll(index)
        else:
            print("Error -- findAllValues Method")
            return -1
        
        
    def findValueRadius(self, baseFeat, baseValue, targetFeat, radius):
        #returns single numerical value
        searchColumn = self.data.get(baseFeat)
        up = len(searchColumn) - 1
        down = 0

        upValue = searchColumn[up]
        downValue = searchColumn[down]

        direction = self.findDirection(upValue, downValue)
        if direction == 1:
            if upValue < baseValue or downValue > baseValue:
                return self.extrapSingle(searchColumn, baseFeat, baseValue, targetFeat)
                
            index = self.upBinarySearch(searchColumn, up, down, baseValue)

        elif direction == -1:
            if upValue > baseValue or downValue < baseValue:
                return self.extrapSingle(searchColumn, baseFeat, baseValue, targetFeat)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.downBinarySearch(searchColumn, up, down, baseValue)

        if len(index) == 2:
            return self.interpPolySingle(baseFeat, baseValue, index, targetFeat, radius)
        elif len(index) == 1:
            return self.getSingle(targetFeat, index)            
        else:
            print("Error -- findValueRadius Method")
            return -1

    def findAllValuesRadius(self, baseFeat, baseValue, radius):
        #returns a dictionary of all corresponding value to the base value
        #1. performs binary search to find initial index range
        #2. using the radius, gets adjacent data values 
        searchColumn = self.data.get(baseFeat)
        up = len(searchColumn) - 1
        down = 0

        upValue = searchColumn[up]
        downValue = searchColumn[down]

        direction = self.findDirection(upValue, downValue)
        if direction == 1:
            if upValue < baseValue or downValue > baseValue:
                return self.extrapSingle(searchColumn, baseFeat, baseValue)
                
            index = self.upBinarySearch(searchColumn, up, down, baseValue)

        elif direction == -1:
            if upValue > baseValue or downValue < baseValue:
                return self.extrapSingle(searchColumn, baseFeat, baseValue)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.downBinarySearch(searchColumn, up, down, baseValue)
        
        if len(index) == 2:
            return self.interpPolyAll(baseFeat, baseValue, index, radius)
        elif len(index) == 1:
            return self.getAll(index)
        else:
            print("Error -- findValueRadius Method")
            return -1
        

    #-------------------User Print Out Methods-----------------
    #These methods would also be public to the user since it conveys information about the held data set
    def printFileName(self):
        print("Input file is ", self.fileName)

    def printHeader(self):
        for element in self.header:
            print(element)

    def printTable(self):
        return 0

    def help(self):
        print("HELP")

    #-------------------------------------------PRIVATE METHODS--------------------------------------------
    #-------------------File Handling Methods------------------
    def cleanString(self, str):
        newStr = ''
        for letter in str:
            value = ord(letter)
            if (value > 47 and value < 58) or (value > 65 and value < 91) or (value > 96 and value < 123):
                newStr += letter
        return newStr
    
    def cleanNumber(self, numStr):
        return float(numStr)
    
    def str2Double(self, numStr):
        whole = 0
        decimal = 0

        numList = numStr.split('.')
        if numList[0][0] == '-':
            scaling = -1
            numList[0] = numList[0].replace('-','')
        else:
            scaling = 1
        
        whole = float(numList[0])

        if len(numList) == 2:
            decimal = float(numList[1]) / (10 ** len(numList[1]))
        num = (whole + decimal) * scaling
        return num

    def openFile(self):
        file = open(self.fileName)
        csvreader = csv.reader(file)
        
        #header getter and setter
        header = []
        tempHeader = next(csvreader)
        for element in tempHeader:
            if len(element) > self.longestInstance:
                self.longestInstance = len(element)
            header.append(self.cleanString(element))
        self.header = header
        self.printHeader()
        
        #get rest of data
        row = []
        for element in csvreader:
            tempRow = []
            for num in element:
                if len(num) > self.longestInstance:
                    self.longestInstance = len(num)
                tempRow.append(self.cleanNumber(num))
            row.append(tempRow)
        
        #build dictionary to access features
        tableDict = {}
        for i in range(len(header)):
            tableDict[header[i]] = []
            for j in range(len(row)):
                tableDict[header[i]].append(row[j][i])

        file.close()

        return tableDict

    #-------------------Helper Methods for Search and Output-----------------
    def findDirection(self, up, down):
        if up > down:
            direction = 1
        elif up < down:
            direction = -1
        else:
            print("WARNING: There is at least one peak")
            print("Implying there is two instances equal to the targetValue")
            print("Please select a narrower range")
            direction = 1 #FIXME --done to prevent crashing the program

        return direction 

    #------------------------------Modified Binary Search Algorithms-----------------------------------------
    def upBinarySearch(self, column, up, down, target):
        #binary search if the up/right value is greater than the bottom/left value
            #ie: ascending order
        #returns index values found within the dataset --> exact or for interpolation

        # addition made to code in order to handle the alt = 7000 case 
        n = up
        ind = int(round(n/2, 0))
        out = []
        
        count = 0
        while len(out) == 0:
            value = column[ind]
            """
            print("count: ", count)
            print("old index ", ind)
            print("value ", value)
            """
            if value > target:
                up = ind
            elif value < target:
                down = ind
            elif value == target:
                out.append(ind)

            indRange = abs(up - down)
            ind = int(down + (up - down) // 2)
            """    
            print("new index ", ind)
            print("range ",indRange)
            print("range add", round(ind/2, 0))
            print("up ", up)
            print("down", down)
            print()
            """
            count += 1
            upValue = column[up]
            downValue = column[down]
            if indRange == 1 and (downValue < target and upValue > target):
                out.append(down)
                out.append(up)
            
            if count == 16:
                break
        #print(value)
        #print(out)
        return out
            
    def downBinarySearch(self, column, up, down, target):
        #for sorted list of descending order 
        #returns index values found within the dataset --> exact or for interpolation
        n = up
        ind = int(round(n/2, 0))
        out = []

        while len(out) == 0:
            value = column[ind]

            if value > target:
                #tempInd = ind
                #ind = int(down + math.ceil(down + ind/2))
                down = ind
            elif value < target:
                up = ind
            elif value == target:
                out.append(ind)

            indRange = abs(up - down)
            #ind = int(down + round(ind/2, 0))
            ind = int(down + (up - down) //2 )

            if indRange == 1:
                out.append(down)
                out.append(up)

        return out
    
    #Basic Get Methods for index size of 1
    def getAll(self, index):
        #returns dictionary
        out = {}

        for feat in self.header:
            column = self.data.get(feat)
            out[feat] = column[index[0]]

        return out
    
    def getSingle(self, targetFeat, index):
        #returns a numerical value
        targetColumn = self.data.get(targetFeat)
        return targetColumn[index[0]]
    
    def getAll(self, index):
        #return a dictionary 
        out = {}
        for element in self.header:
            column = self.data.get(element)
            out[element] = column[index[0]]
        return out


    #------------------------Prediction Methods------------------------
    def extrapAll(self, column, baseFeat, baseValue):
        print("Work on extrapAll Method")
        return 0
    
    def extrapSingle(self, column, baseFeat, baseValue, targetFeat):
        print("Work on extrapSingle Method")
    
    def interpAll(self, baseFeat, baseValue, indexes):
        baseColumn = self.data.get(baseFeat)

        x = baseValue
        x1 = baseColumn[indexes[0]]
        x2 = baseColumn[indexes[1]]

        out = {}
        out[baseFeat] = baseValue

        for feat in self.header:
            if feat == baseFeat:
                out[feat] = baseValue
            else:
                targetColumn = self.data.get(feat)
                y1 = targetColumn[indexes[0]]
                y2 = targetColumn[indexes[1]]

                y = y1 + (x - x1) * (y2 - y1)/(x2 - x1)

                out[feat] = round(y, 10)
        
        return out            

    def interpSingle(self, baseFeat, baseValue, indexes, targetFeat):
        baseColumn = self.data.get(baseFeat)
        targetColumn = self.data.get(targetFeat)

        x = baseValue
        x1 = baseColumn[indexes[0]]
        x2 = baseColumn[indexes[1]]
        y1 = targetColumn[indexes[0]]
        y2 = targetColumn[indexes[1]]

        y = y1 + (x - x1) * (y2 - y1)/(x2 - x1)
        return round(y, 10)

    def getRadialIndex(self, baseFeat, indexes, radius):
        ind = indexes[0]   #should only by two elements in indexes
        maxInd = len(self.data.get(baseFeat)) - 1
        
        #getting index range
        newIndexes = []
        for i in range((-radius +1), (radius+1)):
            newInd = ind + i
            if(newInd < 0 or newInd > maxInd):
                #if requested index is out of bounds, dont append to newIndexes
                print("Warning -- interpPolySinge Method -- Index Out of Bounds -- Index Skipped")
                continue
            newIndexes.append(newInd)
        return newIndexes      0287

    def interpPolyAll(self, baseFeat, baseValue, indexes, radius):
        #returns a dictionary
        #uses Polynomial Z Method to find coefficients
        newIndexes = self.getRadialIndex(baseFeat, indexes , radius)

        #One Time Operation
        #building independent and dependent arrays
        n = len(newIndexes)
        x = np.zeros(n)
        xColumn = self.data.get(baseFeat)

        for i in range(n):
            x[i] = xColumn[i]
        
        #building of A matrix
        A = np.zeros((n, n))

        for row in range(n):
            for col in range(n):
                #FIXME -- to reduce complexity maybe switch the order of the if and else
                if row == 0 and col == 0:
                    A[0,0] = n
                else:
                    A[row, col] = sum(np.power(x, col+row))

        #Repeat operation for each header 
        header = self.header
        out = {}
        for element in header:
            if element == baseFeat:
                out[baseFeat] = baseValue
            else:
                print(element)
                y = np.zeros(n)
                yColumn = self.data.get(element)
                b = np.zeros((n,1))

                #build dependent array
                for j in range(n):
                    y[j] = yColumn[j]
                
                for row in range(n):
                    b[row,0] = sum(np.multiply(y, np.power(x, row)))

                coefs = np.matmul(inv(A), b)

                #calculating out dependent value from coefficients
                yOut = 0
                for i in range(len(coefs)):
                    yOut += coefs[i][0] * baseValue ** i
                print("here", coefs[0][0])
                out[element] = round(yOut, 10)
        return out
    
    def interpPolySingle(self, baseFeat, baseValue, indexes, targetFeat, radius):
        #returns a numerical value
        newIndexes = self.getRadialIndex(baseFeat, indexes, radius)

        #building independent and dependent arrays
        n = len(newIndexes)
        x = np.zeros(n)
        xColumn = self.data.get(baseFeat)
        y = np.zeros(n)
        yColumn = self.data.get(targetFeat)

        for i in range(n):
            x[i] = xColumn[newIndexes[i]]
            y[i] = yColumn[newIndexes[i]]
        
        #Build A and b matrices
        A = np.zeros((n,n))
        b = np.zeros((n,1))

        for row in range(n):
            for col in range(n):
                #FIXME -- to reduce complexity maybe switch the order of the if and else
                if row == 0 and col == 0:
                    A[0,0] = n
                else:
                    A[row, col] = sum(np.power(x, col+row))
            b[row, 0] = sum(np.multiply(y, np.power(x, row)))
            
        coefs = np.matmul(inv(A), b)

        """
        print("indexes\n", newIndexes, "\n")
        print("A\n", A, "\n")
        print("b\n", b, "\n")
        print("coefficients\n", coefs, "\n")
        """
        
        #calculating out dependent value from coefficients
        yOut = 0
        for i in range(len(coefs)):
            yOut += coefs[i][0] * baseValue ** i

        return round(yOut, 10)

def main():
    atm = TableReader('atmProp_englishLabel.csv')
    print("\n-----------------------Test 1-----------------------")
    print(atm.findValue('alt', 1000, 'temp'))
    print()
    print(atm.findAllValues('alt', 1000))

    print("\n-----------------------Test 2-----------------------")
    print(atm.findValue('alt', 1250, 'temp'))
    print()
    print(atm.findAllValues('alt', 1250))
    
    print("\n-----------------------Test 3-----------------------")
    print(atm.findValue('temp', 515.1, 'alt'))
    print()
    print(atm.findAllValues('temp', 515.1))
    
    print("\n-----------------------Test 4-----------------------")
    print(atm.findValue('temp', 514.2, 'alt'))
    print()
    print(atm.findAllValues('temp', 514.2))
    
    print("\n-----------------------Test 5-----------------------")
    print(atm.findValue('alt', 7500, 'temp'))
    print()
    print(atm.findValueRadius('alt', 10637 , 'temp', 1))

    print("\n-----------------------Test 6-----------------------")
    print(atm.findValue('alt', 10637, 'temp'))
    
    print(atm.findValueRadius('alt', 10637 , 'temp', 3))
    print(atm.findAllValuesRadius('alt', 10637 , 3))
    print(atm.findAllValues('alt', 10637))

    print('end')



    atm.printFileName()
    

main()