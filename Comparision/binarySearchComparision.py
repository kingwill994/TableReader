import pandas as pd
import numpy as np

#### TO-DO ####
#tried built in pandas interpolation but couldn't get it to get values in relation to the altitude
#will build out method manually and test it next time
#extrapolation trigger needs to be rewritten to properly execute when relation is inverse to index progression
    #\-> if up > down do something; elif up < down do something :: where something is the actualy algorithm
#interpolation with radius

### PREPROCESSING
def directionFinder(upValue, downValue):
    #used to determine whether or not the value of the target lable is increasing or decreasing
    #returns a direction scalar which can be used to run the same algorithms just by modifying the up, down, and targetValue

    if upValue > downValue:
        direction = 1
    elif upValue < downValue:
        direction = -1
    else:
        print("There exists at least one peak")
    return direction

#####  PREDICTION FUNCTIONS  ########
def interp_builtIn(df, targetLabel, targetValue, up, down):
    df_shape = df.shape
    df_down = df.iloc[[down]]
    df_up = df.iloc[[up]]
    cols = (df.columns)
    df_find = pd.DataFrame([[np.nan]*df_shape[1]], columns = cols)
    df_find[targetLabel] = targetValue
    data = pd.concat([df_down, df_find, df_up])
    print(data)
    interp = data.interpolate(method = 'linear', limit_direction = 'forward', axis = 0)
    #not returning corresponding values in relation to targetLabel
    return interp.iloc[[1]]

def interp(df, targetLabel, targetValue, up, down):
    data = df.iloc[[down,up]]
    dataDict = data.to_dict('list')
    features = list(dataDict.keys())
    features.pop(features.index(targetLabel))

    x = targetValue
    x1 = up
    x2 = down
    stor = {} 
    for feat in features:
        y1, y2 = dataDict.get(feat)
        y = y1 + (x-x1) * (y2-y1)/(x2-x1)
        stor[feat] = [y]
    return pd.DataFrame.from_dict(stor)

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

    direction = directionFinder(upValue, downValue)
    print(direction)

    #transform targetValue, upValue, and downValue
    

    #extrapolation trigger needs to be rewritten to properly execute when relation is inverse to index progression
    if upValue < targetValue or downValue > targetValue:
        return extrapol(df, targetLabel, targetValue) 
    
    return recurBinSea(df, targetLabel, targetValue, up, down, ind, out)
    

def recurBinSea(df, targetLabel, targetValue, up, down, ind, out):
    #print(ind)
    if len(out) == 0:
        valueRow = df.iloc[[ind]]
        value = float(valueRow[targetLabel])
        if value > targetValue:
            up = ind
            print('up', up)
        elif value < targetValue:
            print('down', down)
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
            return df.iloc[[ind]]




#### ITERATIVE BINARY SEARCH ####
def iterBinSea(df, targetLabel, targetValue):
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
            print('up', up)
        elif value < targetValue:
            down = ind
            print('down', down)
        elif value == targetValue:
            out = [ind]
        
        indRange = abs(up-down)
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
    print(atm.columns)
    label = 'alt'
    target = 1200
    #data = iterBinSea(atm, label, target)
    data = find(atm, label, target)
    print(data)

main()