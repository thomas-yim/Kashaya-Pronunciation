#Thomas Yim 4/26/20
#Kashaya Syllabification, Segmentation, and Foot Structure Generation.

import random
from dfConstructor import constructDF, findComponents
from specialLists import Config

lists = Config()
specialIncrements = lists.increments
vowels = lists.vowels
sonorants = lists.sonorants
sChars = lists.sChars
consonants = lists.consonants
nonVowels = sonorants + sChars + consonants
accentedVowels = lists.accentedVowels

"""
This gets rid of the spaces following the last character in the world and the /n
"""
def stripFinalSpaces(entry):
    entry = entry.rstrip('\n')
    while entry[-1] == " ":
        entry = entry[:-1]
    return entry
        
"""
Since there are certain letters that have increments, this splits them and makes sure that
it is split at the real starts of letters.
"""
def splitIntoSegments(entry):
    segments = []
    #Get rid of the newline or the star character or a space at the end
    entry = entry.rstrip('*')
    entry = stripFinalSpaces(entry)
    for i in range(0, len(entry)):
        if i+1 < len(entry):
            if entry[i+1] in specialIncrements:
                segments.append(entry[i] + entry[i+1])
            elif entry[i] not in specialIncrements:
                segments.append(entry[i])
        elif entry[i] not in specialIncrements:
            segments.append(entry[i])
    return segments


"""
The way that this checks for syllables is as follows:
We assume that there is always an onset and that there is one onset
Accordingly, we start from the end and move left.
Once we get to a syllable we take the left consonant as the onset
And then the rest of the consonants to the right until the last onset is the coda
Then these are combined and appended to the array of syllables
"""
def syllabify(segments):
    syllables = []
    lastUsedSegmentIndex = len(segments)
    for k in range(len(segments)-1, -1, -1):
        if segments[k][0] in vowels or segments[k][0] in accentedVowels:
            vowel = segments[k]
            onset = ""
            coda = ""
            if k > 0:
                if segments[k-1][0] in nonVowels:
                    if k+1 != lastUsedSegmentIndex:
                        if k < len(segments)-1:
                            coda = "".join(segments[k+1:lastUsedSegmentIndex])
                    onset = segments[k-1]
                    lastUsedSegmentIndex = k-1
            syllables.insert(0,onset + vowel + coda)
    if len(syllables) == 0:
        return["".join(segments)]
    return syllables
    
"""
This builds the foot structure for the words
Usually CV CVV CVC
"""
def findStructure(syllables):
    structure = []
    for syllable in syllables:
        syllableStruct = ""
        letters = splitIntoSegments(syllable)
        for i in range(0,len(letters)):
            if letters[i][0] in nonVowels:
                syllableStruct += 'C'
            else:
                if len(letters[i]) == 2:
                    if letters[i][1] == "·":
                        syllableStruct += 'VV'
                    else:
                        syllableStruct += 'V'
                else:
                    syllableStruct += 'V'
        structure.append(syllableStruct)
    return structure

"""
This will return an array with all of the visible feet of the word/phrase
So, if a syllable is extrametrical, it won't be inclulded.
"""
def footStructure(startEntry, syllables):
    structure = findStructure(syllables)
    #We need this for calculating the effect of foot flipping and closed vowel shortening on stress
    #If the word ends in a /d/, a /u/ is added and stress is shifted
    entrySegments = splitIntoSegments(startEntry)
    entrySyllables = syllabify(entrySegments)
    entryStructure = findStructure(entrySyllables)
    if extrametricalityApplies(startEntry):
        syllables = syllables[1:]
        structure = structure[1:]
    if len(structure) > 0:
        if structure[0] == "CVV":
            syllables = syllables[1:]
            structure = structure[1:]
        elif len(structure) > 2:
            if structure[0] == "CV" and structure[1] == "CVV":
                if entryStructure[0] == "CVV" and entryStructure[1] == "CV":
                    syllables = syllables[2:]
                    structure = structure[2:]
    i = 0
    footStruct = []
    while i < len(structure):
        if structure[i] == "CV":
            if i < len(structure)-1:
                if structure[i+1] == "CV":
                    footStruct.append([syllables[i], syllables[i+1]])
                    i += 1
                else:
                    footStruct.append([syllables[i]])
            else:
                footStruct.append([syllables[i]])
        else:
            footStruct.append([syllables[i]])
        i += 1
    return footStruct

"""
This checks if extrametricality will apply. I pulled all the components for the words from the database
If there is a prefix (a component ending in a dash that doesn't have Ø)
then it will consider it an extrametrical syllable
Also, if the root (starting with a *) has two syllables, the first is extrametrical
Otherwise extrametricality does not apply here.
"""
def extrametricalityApplies(entry):
    components = findComponents(entry)
    segments = splitIntoSegments(entry)
    syllables = syllabify(segments) 
    if components[0][-1] == "-" and ("Ø" not in components[0]):
        return True
    
    elif components[0][0] == "*" or components[0][0] in nonVowels:
        compSegments = splitIntoSegments(components[0])
        compSyllables = syllabify(compSegments)
        if len(compSyllables) >= 2:
            return True
        else:
            return False
    #Need to confirm with buckley about this test
    elif components[0] == "Same":
        compSegments = splitIntoSegments(entry)
        compSyllables = syllabify(compSegments)
        if len(compSyllables) >= 2:
            return True
        else:
            return False
    else:
        return False

def main():
    df = constructDF("Kashaya word list.txt")
    randIndex = random.randint(0,len(df['Entries']))
    entry = df.iloc[randIndex]['Entries']
    #entry = "*pʰaʔsʼulh"
    #entry = "*bo·catad"
    #entry = "*bahcʰabacʰatadu"
    print(entry)

    segments = splitIntoSegments(entry)
    #print(segments)
    
    syllables = syllabify(segments)
    #print(syllables)
        
    structure = findStructure(syllables)
    print(structure)
                    
    footStruct = footStructure("*bahcʰabacʰatad", syllables)
    print(footStruct)
    if len(structure) > 1:
        if structure[0] == "CVV" and structure[1] == "CV":
            syllables[0] = syllables[0].rstrip("·")
            syllables[1] += "·"
            structure[0] = "CV"
            structure[1] = "CVV"
            
if __name__ == '__main__':
    main()