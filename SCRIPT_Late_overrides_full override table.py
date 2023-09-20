"""
Module with a functions to read CSV files containing logged overrides and 
committed line items (TA 1.0 line items, Invoice Management, and Member-level 
Billing student term line items (STLIs)), and then identify late-reported 
overrides, exlude a list of permissable exceptions, and finally  write the 
results to csv. Updating 6/17/23 to consume full override table instead of 
keys/dates only.

Author: Emily Ciarabellini
Date: 6/17/2023
"""


import pandas as pd
import csv


def createDictfromCSV(csvFileName):
    """
    Takes a csv file with data beginning in the first column 
    as an argument and returns a single dictionary.
    File name argument is formatted as a string with .csv. Example: 'overrides.csv'
    """ 
    csvDownload = pd.read_csv(csvFileName, header=None, index_col=0)
    dict1 = csvDownload.to_dict()
    return dict1[1]   #removes header '1', so dictionary is no longer nested


def combineDicts(dict1, dict2):
    """
    Combines two dictionaries where the values are dates. This function
    maintains the value where the date is the most recent for a given key 
    when there are duplicate keys across the two dictionaries. 
    """ 
    newDict = dict1 | dict2
    for k in newDict:
        if k in dict1 and k in dict2:
            if dict1[k] > dict2[k]:
                newDict[k] = dict1[k]
            else:
                newDict[k] = dict2[k]
    return newDict


def createListfromCSV(csvFileName):
    """
    Takes a csv file as an argument and returns a list.
    File name argument is formatted as a string with .csv. Example: 'overrides.csv'
    """ 
    file=open(csvFileName)
    new_list = list(csv.reader(file))
    return new_list


def lateOverrideCheck(overrides, linesDict):
    """
    Compares date of logged overrides to the date of the committed line item for the
    given term_studentID key. If the override is logged after the line item was 
    committed, the term_studentID key is added to the late override list. This function
    returns a list of the late override list and the overrides not found.
    """ 
    lateOverrideslist = []
    overridesNotFound = []

    for ovrd in overrides:
        if ovrd[0] in linesDict:
            if ovrd[5] > linesDict[ovrd[0]]:
                lateOverrideslist.append(ovrd)
        else:
            overridesNotFound.append(ovrd)
    return [lateOverrideslist,overridesNotFound]


def excludePermissables(permissables,overrides):
    """
    Takes one list (permissables) and one table (overrides) as parameters and 
    returns a new version of the overrides table that excludes items on the list. 
    Overrides contain the key in the first column that match the items in the 
    permissible list.
    """
    result = []
    for n in overrides:
        if [n[0]] not in permissables:
            result.append(n)
    return result


def writeToCSV(list,filename):
    """
    Takes a list and a CSV file name as parameters and writes the contents of the 
    list to the csv file. File name is a string in quotes ''.
    """
    file = open(filename,'w',newline='')
    wrapper = csv.writer(file)
    wrapper.writerow(['KEY', 'OVERRIDE_LOGGED_BY', 'AP_NAME', 'REASON', 'TUITION_ELIGIBLE', 'UPDATED_AT', 'STUDENT_EXTERNAL_ID', 'TERM_CODE', 'COMMENT', 'MP SEARCH URL'])
    for i in list:
        wrapper.writerow(i)
    file.close()

#create dictionaries/lists for each of the CSV files
overridesList = createListfromCSV('overrides.csv') 
permissables = createListfromCSV('Permissables.csv')
mlbDict = createDictfromCSV('MLB_lines.csv')
ta1Dict = createDictfromCSV('TA1.csv')
imDict = createDictfromCSV('invoicemanagement_lines.csv')


#combine MLB, Invoice Managment, and TA 1.0 dictionaries into 1, maintaining the
#  most recent date for the student/term key
ta1_imDict = combineDicts(ta1Dict,imDict)
allLinesDict = combineDicts(ta1_imDict,mlbDict)

result = lateOverrideCheck(overridesList,allLinesDict)
finalResult = excludePermissables(permissables,result[0])
writeToCSV(finalResult,'results.csv')
writeToCSV(result[1],'results_LIs_not_found.csv')
print(f"The number of late overrides is: {len(finalResult)-1}") #subtract 1 for header



####
# Next steps:
# validate overridesNotFound list
# find a way to package the ta 1.0 and Invoice Managment data alongside this
# make this capable of being run in the command line (easier to refresh with file name agnostic)
# upload to github
