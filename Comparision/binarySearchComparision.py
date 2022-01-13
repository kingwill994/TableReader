import pandas as pd
import numpy as np

#### TO-DO ####
#tried built in pandas interpolation but couldn't get it to get values in relation to the altitude
#will build out method manually and test it next time

#####  PREDICTION FUNCTIONS  ########
def interp(df, targetLabel, targetValue, up, down):
    df_shape = df.shape
    df_down = df.iloc[[down]]
    df_up = df.iloc[[up]]
    cols = (df.columns)
    df_find = pd.DataFrame([[np.nan]*df_shape[1]], columns = cols)
    df_find[targetLabel] = targetValue
    data = pd.concat([df_down, df_find, df_up])
    print(data)
    interp = data.interpolate(method = 'linear', limit_direction = 'forward', axis = 0)
    print(interp)

    return 0
    """
    data_shape = data.shape

    for i in range(data_shape[1]):
        temp = data.iloc[:,i]
        
        print(type(temp))
        print(temp)
        print(data.iloc[:,i])
    
    print(data)
    #print(type(data))
    return 5
    """

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
        elif value < targetValue:
            down = ind
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
    label = 'alt'
    target = 1250

    data = iterBinSea(atm, label, target)
    #data = find(atm, label, target)
    #print(data)

main()