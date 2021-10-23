from copy import deepcopy
import itertools
#-------------------------------------------------------------
#                   dis-similarity function
#       counts the empty intersections between rule1 and rule2            
def similarity(rule1,rule2,d):
    unions = []
    intersections = []
    indexes = []
    difference = 0
    for i in range( len(rule1) - 1 ):
        union = rule1[i] | rule2[i]
        intersection = rule1[i] & rule2[i]
        unions.append(union)
        intersections.append(intersection)
        if intersection == set():
            difference +=1
            indexes.append(i)
    if difference <= d:
#        print('The number of empty sets between',rule1,'and',rule2,'is',difference,'which is less equal than',d,'and therefore they can be grouped')
        return [True, unions, intersections, indexes]
    else:
        return [False, None, None, None]
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
#    check if all one-instance rules of a rule exist in the
#    original rules 
def allRules(rule, originalRules):
    expand = expandRule(rule)
    suma = 0
    for r in expand:
        if r in originalRules:
            suma+=1
    if suma == len(expand):
        return True
    else:
        return False
#------------------------------------------
#
#               Function
#    generalizationANDcontradictions
#             
#------------------------------------------------------------------
#    Quick and dirty draft without optimization                ----
#------------------------------------------------------------------
def generalizationANDcontradictions(rule,originalRules,otherRules,ratio):
    expanded = expandRule(rule)
    #print('rule', rule)
    #print('expanded', expanded)
    #print('original rules ', originalRules)
    #originalRulesCurrentCategory = []
    #[originalRulesCurrentCategory.append(x) for x in originalRules if x[-1]==rule[-1]]
    #print(originalRulesCurrentCategory)
    #originalRulesOtherCategories = []
    #[originalRulesOtherCategories.append(x) for x in originalRules if x[-1]!=rule[-1]]
    #print(originalRulesOtherCategories) 
    # C O N T R A D I C T I O N S
    for r1 in expanded:
        if r1!=None:  # I added this if and the one below for the d = 1,2. . . . test 
            temporalRule =r1[0:-1]
        for r2 in otherRules:
            if r2!= None: # I added this if
                if temporalRule == r2[0:-1]:
                    return False
    # G E N E R A L I Z A T I O N
    numberOfRulesInOriginalRules = 0
    for r1 in expanded:
        if r1 in originalRules:
            numberOfRulesInOriginalRules +=1
    if (numberOfRulesInOriginalRules/len(expanded)) >= ratio:
#        print('Enough rules in original rules, returning:',rule)
        return rule
    else:
        return False
#originalRules = [ [{1},{2},'a'],[{2},{2},'a'],[{2},{3},'a'],[{1},{3},'b'] ]
#print(generalizationANDcontradictions( [{1,2},{2,3},'a'], originalRules, ratio = 1/2))

#-------------------------------------------------------------
#   createRules for similarity "count empty intersections"
def create_rule(rule1, unions, originalRules, d, otherRules, ratio):
    rule = deepcopy(rule1)
    for i in range(len(rule1)-1):
        rule[i] = unions[i]

    if d == 1:
        all_rules = allRules(rule, originalRules)
        if all_rules:
 #           print(rule,'has been created')
            return rule
        else:
            return False
    if d >=2:
  #      print('d is >= 2')
        create = generalizationANDcontradictions(rule,originalRules,otherRules,ratio)
#        print('create',create)
        if create:
            return create
        else:
            return False

#--------------------------------------------------------------
#  True if a rule1 is subset of rule2, False otherwhise
def contained( rule1, rule2 ):
    #if rule1[-1] == rule2[-1]:
    equalParameters = 0
    for i in range( len(rule1) - 1 ):
        if rule1[i].issubset(rule2[i]):
            equalParameters +=1
    if equalParameters == len(rule1) - 1:
        return True
    else:
        return False

# T E S T S
#print(contained( [{1},{1},'A'],[{1},{1,2,3},'A']) )
#True
#print(  contained( [{2},{7},'D'],[{2,5},{7},'D']   )   )
#True

#----------------------------------------------------------------
#      Remove   redundant   rules
#----------------------------------------------------------------
#def deleteRedundant( rules ):#more eficient
#    nonRedundant = []
#    for i in range(0, len(rules)):
#        redundant = False
#        rule1 = rules[i]
#        for j in range( i+1, len(rules)):
#            rule2 = rules[j]
##            print('rule1 rule2',rule1, rule2)
#            if rule1 != None and rule2 != None and contained(rule1,rule2) == True:
#          #      print(rule1,'contained in', rule2)
#                redundant = True
#        if redundant == True:
#            rules[i] = None
#    [nonRedundant.append(r) for r in rules if r != None]
#    return nonRedundant
#   D  E  L  E  T  E    R  E  D  U  N  D  A  N  T    FUNCTION THAT COMPARES R1 WITH R2  AND R2 WITH R1
def deleteRedundant( rules ):#more eficient
    nonRedundant = []
    for i in range(0, len(rules)):
        rule1 = rules[i]
        for j in range( i+1, len(rules)):
            rule2 = rules[j]
            if rule1 != None and rule2 != None and contained(rule1,rule2) == True:
                rules[i] = None
            if rule2 != None and rule1 != None and contained(rule2,rule1) == True:
                rules[j] = None
    [nonRedundant.append(r) for r in rules if r != None]
    return nonRedundant
#-------------------------------------------------------------------------------------------------------
def search_patterns(rulesCurrentCategory, d, originalRules,otherRules,ratio):
    newRules = []
    for i in range( 0, len(rulesCurrentCategory) ):
        r1 = rulesCurrentCategory[i]
        for j in range(i+1, len(rulesCurrentCategory)):
            r2 = rulesCurrentCategory[j]
#            print('comparing',r1,r2)
            [pattern, unions, intersections, indexes] = similarity(r1, r2, d)
            if pattern:
                rule = create_rule(r1, unions, originalRules, d,otherRules,ratio)
                if rule!=False and rule not in newRules:
                    newRules.append(rule)
 #   print('previous rules',rulesCurrentCategory,'new created rules',newRules)
    [rulesCurrentCategory.append(r) for r in newRules]
  #  print('deleting redundant rules . . . . ')
    rules = deleteRedundant(rulesCurrentCategory)
    return rules

def iterate(rulesCurrentCategory,d,otherRules,ratio):
    originalRules = deepcopy(rulesCurrentCategory)
    extractedRules = []
    rules = search_patterns(rulesCurrentCategory, d, originalRules,otherRules,ratio)   #it'll need here rules other categories to compare with when d >= 2
#    print('rules in the first extraction : ', rules)
    while rules != extractedRules:
        extractedRules = deepcopy(rules)#is the deepcopy needed??
        rules = search_patterns(extractedRules, d, originalRules,otherRules,ratio)
#        print('rules extracted within the while : ', rules)
    return rules
#iterate([ [{2},{2},'A'], [{4},{2},'A'], [{2},{3},'A'] ], 1)


#-------------------------------------------------------
#   function that creates a dictionary containing    ---
#   for each category-key the respective rules       ---
#-------------------------------------------------------
def createCategoriesDict(Rules):
    dictionary_of_classes = dict()
    for rule in Rules:
        rule_class = rule[-1]
        if rule_class not in dictionary_of_classes:
            dictionary_of_classes[rule_class] = []
            dictionary_of_classes[rule_class].append(rule)
        else:
            dictionary_of_classes[rule_class].append(rule)
    return dictionary_of_classes
#-----------------------------------------------------------------------------
#    separates the rules of a specified category from the rest
def getCategory(key,dictionary_of_classes):
    rules_other_classes = []
    for key1 in dictionary_of_classes:
        if key1 != key:
            for r in dictionary_of_classes[key1]:
                rules_other_classes.append(r)
        else:
            rules_current_class = dictionary_of_classes[key]
    return [rules_current_class, rules_other_classes]
#-----------------------------------------------------------------------------
#    Main function that controls the process
def ruleExtraction(Rules,d,ratio):
    finalRules = [ ]
    categoriesDict = createCategoriesDict(Rules)
    for category in categoriesDict:
        [rulesCurrentCategory,otherRules] = getCategory(category,categoriesDict)
        rules = iterate(rulesCurrentCategory,d,otherRules,ratio)
        [finalRules.append(rule) for rule in rules]
    #print('Final set of rules : ')
    #print('-----------------------')
    #[print('rule',r) for r in finalRules]
    return finalRules

#Quick Tests
#d = 1
#ratio = 0.5
#Rules = [
#[{3}, {3}, {6}, 'a'],
#[{4}, {3}, {6}, 'a'],
#[{3}, {4}, {6}, 'a'],
#[{1}, {2}, {6}, 'a']
#]

#d = 2
#ratio = 0
#Rules = [
#[{1}, {4}, {6}, 'a'],
#[{2}, {5}, {6}, 'a'],
#[{3}, {6}, {6}, 'a']
#]
#print(ruleExtraction(Rules,d,ratio))












