stlisDict = {"122022_X469749late": "2023-03-01 19:36:28.464 +0000",
    "202302_X502842notlate": "2023-03-09 15:33:41.469 +0000",
    "202220B1_W00342018none": "2023-03-08 22:53:44.720 +0000"}
overridesDict = {"122022_X469749late": "2023-03-10 19:36:28.464 +0000", 
    "202302_X502842notlate": "2023-03-02 19:36:28.464 +0000"}



# lateOverrides = []
# #date of an override
# for k in overridesDict:
#     stliCommitDate = stlisDict[k]
#     overrideLogDate = overridesDict[k]
#     #print(f'Override logged for {k} on {overridesDict[k]}. STLI was committed on {stliCommitDate}.')
#     if overrideLogDate > stliCommitDate:
#         #print("found a late one!")
#         lateOverrides = lateOverrides + [k]

# print(lateOverrides)

def combineDicts(dict1, dict2):
    """
    Combines dictionaries together, maintaining the value where the date is the 
    most recent.
    """ 
    newDict = dict1 | dict2
    for k in newDict:
        if k in dict1 and k in dict2:
            if dict1[k] > dict2[k]:
                newDict[k] = dict1[k]
            else:
                newDict[k] = dict2[k]
    return newDict

res = combineDicts(stlisDict,overridesDict)
print(res)


#use the key from the override and access the date of the stli:

# res = "2023-03-10 19:36:28.464 +0000" > "2023-03-01 19:36:28.464 +0000"
# print(res)

### convert csv into one big dictionary: https://java2blog.com/convert-csv-to-dictionary-python/#Convert_CSV_to_Dictionary_in_Python


#list(allstlis.keys())[list(allstlis.values()).index(xxxxxx)]


