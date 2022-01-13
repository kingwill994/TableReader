import pandas as pd



#####  PREDICTION FUNCTIONS  ########
def interp(df, targetLabel, targetValue, up, down):
    print('interpolate')
    return 5

def extrapol(df, targetLabel, targetValue):
    return 0


##### RECURSIVR BINARY SEARCH #######
def find(df, targetLabel, targetValue):
    n = len(df) - 1
    up = n
    down = 0
    ind = int(round(n/2, 0))
    out = []

    # check if targetValue is outside of dataTable
    upRow = df.iloc[up]
    upValue = upRow[targetLabel]

    downRow = df.iloc[down]
    downValue = downRow[targetLabel]

    if upValue < targetValue or downValue > targetValue:
        return extrapol(df, targetLabel, targetValue) 
    
    return recurBinSea(df, targetLabel, targetValue, up, down, ind, out)


def recurBinSea(df, targetLabel, targetValue, up, down, ind, out):
    print(ind)
    if len(out) == 0:
        valueRow = df.iloc[[ind]]
        value = float(valueRow[targetLabel])
        if value > targetValue:
            up = ind
        elif value < targetValue:
            down = ind
        elif value == targetValue:
            out = [value]
        
        indRange = abs(up-down)
        ind = int(down + round(indRange/2, 0))

        if indRange == 1:
            out = [up,down]
        
        return recurBinSea(df, targetLabel, targetValue, up, down, ind, out)
    
    else:
        if len(out) == 2:
            return interp(df, targetLabel, targetValue, up, down)
        else:
            print(df.iloc[[ind]])
            return df.iloc[[ind]]




#### ITERATIVE BINARY SEARCH ####
def BinarySearch(df, targetLabel, targetValue):
    n = len(df) - 1
    up = n
    down = 0
    ind = (round(n/2,0))
    out = []

    # check if targetValue is outside of dataTable
    upRow = df.iloc[up]
    upValue = upRow[targetLabel]

    downRow = df.iloc[down]
    downValue = downRow[targetLabel]

    if upValue < targetValue or downValue > targetValue:
        return extrapol(df, targetLabel, targetValue,)

    #interpolation section
    while len(out) == 0:
        valueRow = df.iloc[[ind]]   #weird fix with double bracket but works -->requires float conversion
        #print(valueRow)
        value = float(valueRow[targetLabel])
        if value > targetValue:
            up = ind
        elif value < targetValue:
            down = ind
        elif value == targetValue:
            out = [ind]
        
        indRange = abs(up-down)
        print('up: ', up)
        print('down: ', down)
        print('diff: ', indRange)
        ind = int(down + round(indRange/2, 0))

        if indRange == 1:
            out = [up,down]

    if len(out) == 2:
        return interp(df, targetLabel, targetValue, up, down)
    else:
        return df.iloc[[ind]]   #same weird error 
    
    

def main():
    ### import data
    atm = pd.read_csv('atmProp_englishLabel.csv')
    label = 'alt'
    target = 1000

    #data = BinarySearch(atm, label, target)
    data = find(atm, label, target)
    #print(type(data))
    print(data)

main()
            
            
###### Preliminary testing of pd mechanics ######
#print(df)
#print(df['alt'])
#a = df.iloc[3]
#print(df.head())
#cols = df.columns
#print(type(cols))
#print(cols[1])
#print(a['alt'])
#print(df.iloc[3].shape)
#print(df.iloc[3,3])

#print(df.size)
#print(df.iloc[2])
#a = df.iloc[2]
#print(a['alt'])
#print((df.iloc[2])['alt'])

#a = len(df)
#print(a)
#print(df.iloc[a-1])

