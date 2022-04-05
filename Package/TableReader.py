
import csv
import numpy

class TableReader:
    longestInstance = -1
    
    #--------Constructors------------
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = self.openFile()

    #-------------------User Print Out Methods-----------------
    def getFileName(self):
        print("Input file is ", self.fileName)

    def printHeader(self):
        for element in self.header:
            print(element)

    def printTable(self):
        return 0

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
    def findDirection(up, down):
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

    #-----------------------------Search Method 1-----------------------------------------------
    def binarySearch(self, targetFeat, targetValue):
        #binary search method where it finds the exact index or the upper and lower index
        #around the targetValue
        searchColumn = self.data.get(targetFeat)
        n = len(searchColumn) - 1
        up = n
        down = 0
        direction = self.findDirection(up, down)
        ind = (round(n/2, 0))
        out = []

        #transform up, down, and target value to direction scalar
        upValue = searchColumn[up] * direction
        downValue = searchColumn[down] *direction
        targetValue *= direction

        #check if target value is outside of table

        if upValue < targetValue or downValue > targetValue:
            return self.extrapol_M1(searchColumn, targetValue*direction, direction)

        #binary search to pass off to iterpolation methods
        while len(out) == 0:
            value = searchColumn[ind] * direction

            if value > targetValue:
                up = ind
            elif value < targetValue:
                down = ind
            elif value == targetValue:
                out.append(ind)
                
            indRange = abs(up-down)
            ind = down + round(indRange/2,0) * direction
            
            if indRange == 1:
                out.append(up)
                out.append(down)
            
        if len(out) == 2:
            return 0
        else:
            return 0

    #------------------------------Search Method #2-----------------------------------------
    def findValue(self, targetFeat, targetValue):
        #wrapper function to handle ascending and descending datasets
        #and interpolation and extrapolation functions
        #returns a list of all the values in the header
            #FIXME -- make a method for a return just a single value from the header

        searchColumn = self.data.get(targetFeat)
        up = len(searchColumn) - 1
        down = 0

        upValue = searchColumn[up]
        downValue = searchColumn[down]

        direction = self.findDirection(up, down)
        if direction == 1:
            if upValue < targetValue or downValue > targetValue:
                return self.extrapol_M2(searchColumn, targetValue)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.upBinarySearch(searchColumn, up, down, targetValue)

        elif direction == -1:
            if upValue > targetValue or downValue < targetValue:
                return self.extrapol_M2(searchColumn, targetValue)
                #maybe change the extrapol method to include direction to shorten the opeation

            index = self.downBinarySearch(searchColumn, up, down, targetValue)

        if len(index) == 2:
            return self.interp_M2()

    def upBinarySearch(self, column, up, down, target):
        #binary search if the up/right value is greater than the bottom/left value
            #ie: ascending order
        #returns index values found within the dataset --> exact or for interpolation
        n = up
        ind = round(n/2, 0)
        out = []
    
        while len(out) == 0:
            value = column[ind]
            
            if value > target:
                up = ind
            elif value < target:
                down = ind
            elif value == target:
                out.append(ind)
            
            indRange = abs(up - down)
            ind = down + round(ind/2, 0)

            if indRange == 1:
                out.append(up)
                out.append(down)
            
        return out
            
    def downBinarySearch(self, column, up, down, target):
        #for sorted list of descending order 
        #returns index values found within the dataset --> exact or for interpolation
        n = up
        ind = round(n/2, 0)
        out = []

        while len(out) == 0:
            value = column[ind]

            if value > target:
                down = ind
            elif value < target:
                up = ind
            elif value == target:
                out.append(ind)

            indRange = abs(up - down)
            ind = down - round(ind/2, 0)

            if indRange == 1:
                out.append(up)
                out.append(down)
        
        return out

    
    def findValueRadius(self, targetFeat, targetValue, radius):
        return 0
                 


        

    #Predict Methods 
    def extrapol_M1(self, column, target, direction):
        return 0

    def interp_M1(self, targetFeat, targetValue, indexes):
        return 0

    def extrapol_M2(self, columnm, target):
        return 0
    
    def interp_M2(self, targetFeat, targetValue, indexes):
        return 0

    def interp_M3(self, targetFeat, targetValue, indexes, radius):
        return 0
    
    def interpAll(self, baseFeat, baseValue, indexes):
        baseColumn = self.data.get(baseFeat)

        x = baseValue
        x1 = baseColumn[indexes[0]]
        x2 = baseColumn[indexes[1]]

        header = self.header.remove(baseFeat)
        out = {}

        for feat in header:
            targetColumn = self.data.get(feat)
            y1 = targetColumn[indexes[0]]
            y2 = targetColumn[indexes[1]]

            y = y1 + (x - x1) * (y2 - y1)/(x2 - x1)

            out[feat] = y
        
        return out            

    def interSingle(self, baseFeat, baseValue, indexes, targetFeat):
        baseColumn = self.data.get(baseFeat)
        targetColumn = self.data.get(targetFeat)

        x = baseValue
        x1 = baseColumn[indexes[0]]
        x2 = baseColumn[indexes[1]]
        y1 = targetColumn[indexes[0]]
        y2 = targetColumn[indexes[1]]

        y = y1 + (x - x1) * (y2 - y1)/(x2 - x1)
        return y

    def interpPolyAll(self, baseFeat, baseValue, indexes, radius):
        return 0
    
    def interpPolySingle(self, baseFeat, baseValue, indexes, targetFeat,radius):
        return 0

def main():
    atm = TableReader('atmProp_englishLabel.csv')
    atm.printHeader()
    print(atm.header)
    print(atm.data.get('temp'))
    print(atm.data)
    print(atm.longestInstance)


main()