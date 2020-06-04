#Thomas Yim 5/10/20
#Kashaya Pronunciation Generation

import random
import pandas as pd
from syllabification import splitIntoSegments, syllabify, footStructure, stripFinalSpaces, extrametricalityApplies
from absolutiveGeneration import createAbsolutive, generateAllAbsolutives
from dfConstructor import constructDF, findComponents
from specialLists import Config
from tqdm import tqdm

lists = Config()

vowels = lists.vowels
def addSyllableMarker(syllable):
    stresses = {'a':'á', 'e':'é', 'i':'í', 'o':'ó', 'u':'ú'}
    syllable = list(syllable)
    for i in range(0, len(syllable)):
        if syllable[i] in vowels:
            syllable[i] = stresses[syllable[i]]
    return "".join(syllable)
            
    
    

def createPronunciation(entry):
    tone = 0
    absolutive = createAbsolutive(entry)
    segments = splitIntoSegments(absolutive)
    syllables = syllabify(segments)
    structure = footStructure(syllables)
    if len(syllables) == 1:
        syllables[0] = addSyllableMarker(syllables[0])
        pronunciation = "".join(syllables)
    elif len(syllables) == 2:
        segmentsOfFirstSyllable = splitIntoSegments(syllables[0])
        if structure[0][0:3] == "CVC":
            if segmentsOfFirstSyllable[2] == 'ʔ' or segmentsOfFirstSyllable[2] == 'h':
                syllables[1] = addSyllableMarker(syllables[1])
            else:
                syllables[0] = addSyllableMarker(syllables[0])
        else:
            syllables[1] = addSyllableMarker(syllables[1])
        pronunciation = "".join(syllables)
    else:
        prefix = ""
        firstStructure = []
        components = findComponents(entry)
        #This case is handling syllable extrametricality
        if extrametricalityApplies(entry):
            prefix = syllables[0]
            firstStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
        
                
        #Change this to a while loop? Also need to make sure syllables[2] is not out of bounds

        if structure[0] == 'CV':
            syllables[1] = addSyllableMarker(syllables[1])
        elif structure[0] == "CVV":
            if len(structure) > 2:
                if structure[1] == "CV":
                    syllables[2] = addSyllableMarker(syllables[2])
                else:
                    syllables[1] = addSyllableMarker(syllables[1])
            else:
                syllables[1] = addSyllableMarker(syllables[1])
        else:
            syllables[0] = addSyllableMarker(syllables[0])
        pronunciation = prefix + "".join(syllables)
        structure = firstStructure + structure
    return pronunciation, 0


df = constructDF("Kashaya word list.txt")
entries = df['Entries']
pronunciations = df['Pronunciations']
generatedPronunciations = []
generatedTones = []
randIndex = 287#random.randint(0,len(df['Entries']))
generatedAbs = generateAllAbsolutives(entries)
"""
entry = df.iloc[randIndex]['Entries']
print("Entry: " + entry)
print("Mine: " + createPronunciation(entry))
print("Listed: " + df['Pronunciations'][randIndex])
"""
for i in range(0, len(entries)):
    entry = entries[i]
    pronunciation, tone = createPronunciation(entry)
    generatedPronunciations.append(pronunciation)
    generatedTones.append(tone)

df.insert(2, "Generated Pron", generatedPronunciations)
df.insert(4, "Generated Abs", generatedAbs)

with open("Pronunciation Errors.txt", "w") as errorFile:
    correct = 0
    total = 0
    for i in tqdm(range(0, len(df['Entries']))):
        if df.iloc[i]['Pronunciations'] != None:
            pronunciation = df.iloc[i]['Pronunciations']
            generated = df.iloc[i]['Generated Pron']
            total += 1
            if pronunciation == generated:
                correct += 1
            elif df.iloc[i]['Entries'][0] == "*":
                if df.iloc[i]['Absolutives'] == df.iloc[i]['Generated Abs']:
                    errorFile.write(
                            "Entry: " + df.iloc[i]['Entries'].rstrip("\n") +
                            " | Pronunciation: " + df.iloc[i]['Pronunciations'] +
                            " | Generated Pronunciation: " + df.iloc[i]['Generated Pron'] + "\n"
                        )
                else:
                    correct += 1
    errorFile.close()
print("Number Correct: " + str(correct) + ", Total: " + str(total) +
          ", Percent Correct: " + str(correct/total))

