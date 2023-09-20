import pandas as pd


def createDictfromCSV(csvFileName):
    """
    Takes a csv file with no header and data beginning in the first column 
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

#create dictionaries for each of the CSV files
overridesDict = createDictfromCSV('overrides.csv')
mlbDict = createDictfromCSV('MLB_lines.csv')
ta1Dict = createDictfromCSV('TA1.csv')
imDict = createDictfromCSV('invoicemanagement_lines.csv')

#combine MLB, Invoice Managment, and TA 1.0 dictionaries into 1, 
#maintaining the most recent date for the student/term key
ta1_imDict = combineDicts(ta1Dict,imDict)
allLinesDict = combineDicts(ta1_imDict,mlbDict)

res = lateOverrideCheck(overridesDict,allLinesDict)

print(f"The number of late overrides is: {len(res[0])}")
print(f"The number of overrides without committed keys is: {len(res[1])}")
print("Here are the late overrides:")
print(res[0])

####
# Next steps:
# validate overridesNotFound list
# validate late override findings, comparing against Michelle's findings
# validate late override findings in MLB
# export findings to CSV file
# find a way to package the ta 1.0 and Invoice Managment data alongside this
# make this capable of being run in the command line (easier to refresh with file name agnostic)
# upload to github?
# take into account eligibility status on line item and on override to only include when mismatch 