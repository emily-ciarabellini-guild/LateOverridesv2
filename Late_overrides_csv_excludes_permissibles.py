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


def lateOverrideCheck(overridesDict, linesDict):
    """
    Compares date of logged overrides to the date of the committed line item for the
    given term_studentID key. If the override is logged after the line item was 
    committed, the term_studentID key is added to the late override list. This function
    returns a list of the late override list and the overrides not found.
    """ 
    lateOverrideslist = []
    overridesNotFound = []

    for k in overridesDict:
        try:
            itemCommitDate = linesDict[k]
            overrideLogDate = overridesDict[k]
            if overrideLogDate > itemCommitDate:
                lateOverrideslist = lateOverrideslist + [k]
        except:
            overridesNotFound = overridesNotFound + [k]   
                #list of overrides where there is no committed line item for that override key
    return [lateOverrideslist,overridesNotFound]


def excludePermissables(permissables,overrides):
    """
    Takes two lists as parameters and returns a new version of the 2nd list that
    excludes items on the first list.
    """
    result = []
    for n in overrides:
        if [n] not in permissables:
            result.append(n)
    return result


def writeToCSV(list,filename):
    """
    Takes a list and a CSV file name as parameters and writes the contents of the 
    list to the csv file. File name is a string in quotes ''.
    """
    file = open(filename,'w',newline='')
    wrapper = csv.writer(file)
    wrapper.writerow(['results'])
    for i in list:
        wrapper.writerow([i])
    file.close()

#create dictionaries for each of the CSV files
overridesDict = createDictfromCSV('overrides.csv')
mlbDict = createDictfromCSV('MLB_lines.csv')
ta1Dict = createDictfromCSV('TA1.csv')
imDict = createDictfromCSV('invoicemanagement_lines.csv')

#create list for permissibles late overrides
file1 = open('permissables.csv')
permissables = list(csv.reader(file1))
file1.close()

#combine MLB, Invoice Managment, and TA 1.0 dictionaries into 1, 
#maintaining the most recent date for the student/term key
ta1_imDict = combineDicts(ta1Dict,imDict)
allLinesDict = combineDicts(ta1_imDict,mlbDict)

result = lateOverrideCheck(overridesDict,allLinesDict)
finalResult = excludePermissables(permissables,result[0])
writeToCSV(finalResult,'results.csv')

print(f"The number of late overrides is: {len(finalResult)}")


####
# Next steps:
# include full overrides table in results
# validate overridesNotFound list
# find a way to package the ta 1.0 and Invoice Managment data alongside this
# make this capable of being run in the command line (easier to refresh with file name agnostic)
# upload to github
# take into account payment status on MLB line items and exclude if to only include when not full paid ((but what about GAP?))