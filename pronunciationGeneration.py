#Thomas Yim 5/10/20
#Kashaya Pronunciation Generation

import random
import pandas as pd
from syllabification import splitIntoSegments, syllabify, footStructure, stripFinalSpaces
from absolutiveGeneration import createAbsolutive, generateAllAbsolutives
from dfConstructor import constructDF
from specialLists import Config

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
    absolutive = createAbsolutive(entry)
    syllables = syllabify(splitIntoSegments(absolutive))
    structure = footStructure(syllables)
    if len(syllables) == 1:
        syllables[0] = addSyllableMarker(syllables[0])
        pronunciation = "".join(syllables)
    elif len(syllables) == 2:
        if structure[0] == "CVC":
            if syllables[0][2] == 'ʔ' or syllables[0][2] == 'h':
                syllables[1] = addSyllableMarker(syllables[1])
            else:
                syllables[0] = addSyllableMarker(syllables[0])
        else:
            syllables[1] = addSyllableMarker(syllables[1])
        pronunciation = "".join(syllables)
    else:
        prefix = ""
        firstStructure = []
        #This case is handling syllable extrametricality
        if syllables[0] in lists.prefixes:
            prefix = syllables[0]
            firstStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
        elif len(syllables[0]) > 2 and (syllables[0][2] == 'ʔ' or syllables[0][2] == 'h'):
            prefix = syllables[0]
            firstStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
        if structure[0] == 'CV':
            syllables[1] = addSyllableMarker(syllables[1])
        elif structure[0] == "CVV":
            syllables[1] = addSyllableMarker(syllables[1])
        else:
            syllables[0] = addSyllableMarker(syllables[0])
        pronunciation = prefix + "".join(syllables)
        structure = firstStructure + structure
    return pronunciation

def main():
    df = constructDF("Kashaya word list.txt")
    entries = df['Entries']
    pronunciations = df['Pronunciations']
    generatedPronunciations = []
    randIndex = random.randint(0,len(df['Entries']))
    generatedAbs = generateAllAbsolutives(entries)
    #entry = df.iloc[randIndex]['Entries']
    for entry in entries:
        pronunciation = createPronunciation(entry)
        generatedPronunciations.append(stripFinalSpaces(pronunciation))
    
    df.insert(6, "Generated Pron", generatedPronunciations)
    df.insert(4, "Generated Abs", generatedAbs)
    with open("Pronunciation Errors.txt", "w") as errorFile:
        correct = 0
        total = 0
        for i in range(0, len(df['Entries'])):
            if df.iloc[i]['Pronunciations'] != None:
                pronunciation = df.iloc[i]['Pronunciations']
                generated = df.iloc[i]['Generated Pron']
                total += 1
                if pronunciation == generated:
                    correct += 1
                elif df.iloc[i]['Entries'][0] == "*":
                    if df.iloc[i]['Absolutives'] == df.iloc[i]['Generated Abs'] and pronunciation[-1] != "´":
                        errorFile.write(
                                "Entry: " + df.iloc[i]['Entries'].rstrip("\n") +
                                " | Pronunciation: " + df.iloc[i]['Pronunciations'] +
                                " | Generated Pronunciation: " + df.iloc[i]['Generated Pron'] + "\n"
                            )
        errorFile.close()
    print("Number Correct: " + str(correct) + ", Total: " + str(total) +
              ", Percent Correct: " + str(correct/total))
    
if __name__ == "__main__":
    main()
"""
    if structure[1] == "CVC":
        structure[2] = addSyllableMarker(syllables[2])
    elif structure[0] == "CVC" and structure[1] == "CVV":
        structure[1] = addSyllableMarker(syllables[1])
    elif structure[1] == "CV":
        structure[2] = addSyllableMarker(syllables[2])
    elif structure[0] == "CV" and structure[1] == "CVV":
        structure[2] = addSyllableMarker(syllables[2])
    elif structure[1] == "CVV":
        structure[1] = addSyllableMarker(syllables[1])
"""