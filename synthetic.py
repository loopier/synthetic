import pandas as pd
import sys
import itertools
import csv
from ruler import ruleExtraction
#==============================================================================================
#
#
#
#
#----------------------------------------------------------------------------------------------
#  usage:  pad_to_data d ratio
#----------------------------------------------------------------------------------------------
# path_to_data = sys.argv[1]
# d = sys.argv[2]
# ratio = sys.argv[3]

# PARAMETERS TO CONFIGURE
starting_column = 0
#selected_class = "positive"

def rulerData(path_to_data, skiped_rows):
    negative = []
    positive = []
    skiped_rows = int(skiped_rows)

    data = pd.read_csv(path_to_data, header=skiped_rows, delim_whitespace=False)
    dimensions = data.shape
    print('data dimensions : ',dimensions)
    for i in range(dimensions[0]):
        point = []
        for j in range(starting_column, dimensions[1] - 1):
            element = data.iloc[i,j]
            element = float(element)
            point.append(set([element]))
        point.append( data.iloc[ i, dimensions[1] - 1 ] )
        if True:
        #if point[-1] == selected_class:
            positive.append(point)
        else:
            negative.append(point)
    return negative, positive
#setData = rulerData(path_to_data, skiped_rows)

#-------------------------------------------------------------
#    expand r int its one-instance rules

def expandRule(rule):
    rules = []
    sets = rule[0:-1]
    #print('sets', sets)
    combinations = itertools.product(*sets)
    for i in combinations:
        temp_rule = []
        combination = i
        #print(combination,type(combination))
        for j in combination:
            _set = set()
            _set.add(j)
            temp_rule.append(_set)
        
        temp_rule.append(rule[-1]) # Append category
        rules.append(temp_rule)
#    print(rules)
    return rules
#print(expandRule([{1,2,3},{2,3},'A']))
#-------------------------------------------------------------

def asList(r):
    temp_list = []
    for i in r:
        if type(i) == set:
           for unique in i:
               temp_list.append(unique)
        else:
            temp_list.append(i)
    return temp_list

#-------------------------------------------------------------

def syntheticOversampling(path_to_data,d,ratio):
    synthetic = []
    oversampled_data = []
    d = int(d)
    ratio = float(ratio)
    negative, positive = rulerData(path_to_data, 0)
    #print(positive,negative) 
    #positive = positive[0:40]
    rules = ruleExtraction(positive,d,ratio)
    #print(rules)
    print('number of original Rules :',len(positive),'number of extracted rules: ',len(rules) )
    for r in rules:
        expanded = expandRule(r)
        [synthetic.append(rule) for rule in expanded]
    print('synthetic',len(synthetic))
    for n in negative:
        oversampled_data.append( asList(n) )
    for s in synthetic:
        oversampled_data.append( asList(s) )
    print('oversampled data ::', len(oversampled_data))
    print(oversampled_data[0:10])

    with open('training-RULER.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in oversampled_data:
            writer.writerow(row)

    return oversampled_data

# syntheticOversampling(path_to_data,d,ratio)


