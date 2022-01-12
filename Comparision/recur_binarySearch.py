import pandas as pd

### import data
df = pd.read_csv('atmProp_englishLabel.csv')
label = 'atm'
target = 1250

#####  PREDICTION FUNCTIONS  ########
def interp(df, targetLabel, targetValue, up, down):
    return 0

def extrapol(df, targetLabel, targetValue):
    return 0


##### RECURSIVR BINARY SEARCH #######
def find(df, targetLabel, targetValue):
    n = df.size
    up = n
    down = 0
    ind = round(n/2, 0)
    out = []

    # check if targetValue is outside of dataTable
    upRow = df.iloc[up]
    upValue = upRow[targetLabel]

    downRow = df.iloc[down]
    downValue = downRow[targetLabel]

    if upValue < targetValue or downValue > targetValue:
        extrapol(df, targetLabel, targetValue) 
    
    recurBinSea(df, targetLabel, targetValue, up, down, ind, out)


def recurBinSea(df, targetLabel, targetValue, up, down, ind, out):

    if len(out) == 0:
        valueRow = df.iloc[ind]
        value = valueRow[targetLabel]
        if value > targetValue:
            up = ind
        elif value < targetValue:
            down = ind
        elif value == targetValue:
            out = [value]
        
        indRange = abs(up-down)
        ind = down + round(indRange/2, 0)

        if indRange == 1:
            out = [up,down]
        
        recurBinSea(df, targetLabel, targetValue, up, down, ind, out)
    
    else:
        if len(out) == 2:
            interp(df, targetLabel, targetValue, up, down)
        else:
            return df.iloc[ind]




#### ITERATIVE BINARY SEARCH ####
def BinarySearch(df, targetLabel, targetValue):
    n = len(df) - 1
    up = n
    down = 0
    ind = round(n/2,0)
    out = []

    # check if targetValue is outside of dataTable
    upRow = df.iloc[up]
    upValue = upRow[targetLabel]

    downRow = df.iloc[down]
    downValue = downRow[targetLabel]

    if upValue < targetValue or downValue > targetValue:
        extrapol(df, targetLabel, targetValue,)

    #interpolation section
    while len(out) == 0:
        valueRow = df.iloc[ind]
        value = valueRow[targetLabel]
        if value > targetValue:
            up = ind
        elif value < targetValue:
            down = ind
        elif value == targetValue:
            out = [ind]
        
        indRange = abs(up-down)
        ind = down + round(indRange/2, 0)

        if indRange == 1:
            out = [up,down]

    if len(out) == 2:
        interp(df, targetLabel, targetValue, up, down)
    else:
        return df.iloc[ind]
    
    

    

            
            
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

a = len(df)
print(a)
print(df.iloc[a-1])

