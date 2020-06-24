#Thomas Yim 6/3/20
#Convert the txt file to a json where the components can be referenced by the key of the entry

from dfConstructor import constructDF
import json
from syllabification import stripFinalSpaces

#the reason this is a variable is because I initially ran one without searching through plurals.
filename = 'textFiles/' + 'pluralComplexEntries'


with open(filename + '.txt', 'r') as file:
    dictionary = {}
    df = constructDF('Kashaya word list.txt')
    entries = df['Entries']
    lines = file.readlines()
    print(len(lines))
    size = -1
    count = 1
    for i in range(0, len(lines)):
        newSize = len(dictionary)
        #This will be added in the format entry:components
        dictionary[stripFinalSpaces(entries[i].rstrip('\n'))] = stripFinalSpaces(lines[i].rstrip('\n'))
        if newSize == size:
            count += 1
            print(entries[i-1])
        size=newSize
        
print(len(dictionary))

#This will add the dictionary to a json file.
with open(filename + '.json', 'w') as jsonFile:
    json.dump(dictionary, jsonFile)