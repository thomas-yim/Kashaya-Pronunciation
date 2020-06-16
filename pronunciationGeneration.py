#Thomas Yim 5/10/20
#Kashaya Pronunciation Generation

import random
import pandas as pd
from syllabification import splitIntoSegments, syllabify, findStructure, stripFinalSpaces, extrametricalityApplies
from absolutiveGeneration import createAbsolutive, generateAllAbsolutives
from dfConstructor import constructDF, findComponents
from specialLists import Config
from tqdm import tqdm

lists = Config()

vowels = lists.vowels
accentedVowels = lists.accentedVowels
def addSyllableMarker(syllable):
    stresses = {'a':'á', 'e':'é', 'i':'í', 'o':'ó', 'u':'ú'}
    syllable = list(syllable)
    for i in range(0, len(syllable)):
        if syllable[i] in vowels:
            syllable[i] = stresses[syllable[i]]
    return "".join(syllable)
             
    

def createPronunciation(entry):
    tone = None
    absolutive = createAbsolutive(entry)
    #These will be the segments, syllables, and structures of the absolutive form.
    segments = splitIntoSegments(absolutive)
    syllables = syllabify(segments)
    structure = findStructure(syllables)
    #We need this for calculating the effect of foot flipping and closed vowel shortening on stress
    #If the word ends in a /d/, a /u/ is added and stress is shifted
    entrySegments = splitIntoSegments(entry)
    entrySyllables = syllabify(entrySegments)
    entryStructure = findStructure(entrySyllables)
    """
    Note to self: account for extrametricality and outside stress marker for syllables > 2
    """
    if len(syllables) == 1:
        if extrametricalityApplies(entry):
            syllables[0] += "´"
        else:
            tone = 0
            #If the syllable has more than two letters
            if len(structure[0]) > 2:
                #If that letter has a long vowel in it, it is extrametrical so the stress symbol goes outside
                if entryStructure[0][0:3] == "CVV":
                    syllables[0] += "´"
                #Otherwise the syllable marker goes on the one syllable
                else:
                    syllables[0] = addSyllableMarker(syllables[0])
            else:
                syllables[0] = addSyllableMarker(syllables[0])
        pronunciation = "".join(syllables)
    elif len(syllables) == 2:
        extSyllables = []
        extStructure = []
        #This case is handling syllable extrametricality
        if extrametricalityApplies(entry):
            tone = 3
            extSyllables.append(syllables[0])
            extStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
            entryStructure = entryStructure[1:]
        
        if structure[0] == "CVV":
            tone = 4
            extSyllables.append(syllables[0])
            extStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
            entryStructure = entryStructure[1:]
        elif len(structure) == 2:
            if structure[0] == "CV" and structure[1] == "CVV":
                if entryStructure[0] == "CVV" and entryStructure[1] == "CV":
                    tone = 4
                    extSyllables.append(syllables[0])
                    extSyllables.append(syllables[1])
                    extStructure.append(structure[0])
                    extStructure.append(structure[1])
                    syllables = syllables[2:]
                    structure = structure[2:]
                    entryStructure = entryStructure[2:]
                    
        if len(structure) == 0:
            pronunciation = "".join(extSyllables) + "´"
        elif len(structure) == 1:
            if structure[0] == "CV" or (structure[0][0:3] == "CVC" and entryStructure[0][0:4] == "CVVC"):
                syllables[0] += "´"
            elif entryStructure[0] == "CVV":
                syllables[0] += "´"
            else:
                syllables[0] = addSyllableMarker(syllables[0])
            pronunciation = "".join(extSyllables + syllables)
        elif len(structure) == 2:
            tone = 0
            syl1Segs = splitIntoSegments(syllables[0])
            if structure[0] == "CV" or (structure[0][0:3] == "CVC" and entryStructure[0][0:4] == "CVVC"):
                syllables[1] = addSyllableMarker(syllables[1])
            elif structure[0] == "CVC" and (syl1Segs[2] == 'h'):
                syllables[1] = addSyllableMarker(syllables[1])
            else:
                syllables[0] = addSyllableMarker(syllables[0])
            pronunciation = "".join(extSyllables + syllables)
            
        """
        segmentsOfFirstSyllable = splitIntoSegments(syllables[0])
        if structure[0][0:3] == "CVC":
            if segmentsOfFirstSyllable[2] == 'ʔ' or segmentsOfFirstSyllable[2] == 'h':
                #If there was a second syllable to check from the entry (remember it can be different from absolutive structure)
                if len(entryStructure) > 1:
                    #If there was a long vowel, it is extrametrical and the stress symbol goes outside.
                    if entryStructure[1][0:3] == "CVV":
                        syllables[1] += "´"
                    else:
                        syllables[1] = addSyllableMarker(syllables[1])
                else:
                    syllables[1] = addSyllableMarker(syllables[1])
            else:
                syllables[0] = addSyllableMarker(syllables[0])
        else:
            if len(entryStructure) > 1:
                if entryStructure[1][0:3] == "CVV":
                    syllables[1] += "´"
                else:
                    syllables[1] = addSyllableMarker(syllables[1])
            else:
                syllables[1] = addSyllableMarker(syllables[1])
        pronunciation = "".join(syllables)
        """
    else:
        extSyllables = []
        extStructure = []
        #This case is handling syllable extrametricality
        if extrametricalityApplies(entry):
            tone = 3
            extSyllables.append(syllables[0])
            extStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
            entryStructure = entryStructure[1:]
        
        if structure[0] == "CVV":
            tone = 4
            extSyllables.append(syllables[0])
            extStructure.append(structure[0])
            syllables = syllables[1:]
            structure = structure[1:]
            entryStructure = entryStructure[1:]
        elif structure[0] == "CV" and structure[1] == "CVV":
            if entryStructure[0] == "CVV" and entryStructure[1] == "CV":
                tone = 4
                extSyllables.append(syllables[0])
                extSyllables.append(syllables[1])
                extStructure.append(structure[0])
                extStructure.append(structure[1])
                syllables = syllables[2:]
                structure = structure[2:]
                entryStructure = entryStructure[2:]
        
        if len(extStructure) == 0:
            tone = 0
        if len(structure) == 0:
            pronunciation == "".join(extSyllables) + "´"
            structure = extStructure
        else:
            syl1Segs = splitIntoSegments(syllables[0])
            if structure[0] == 'CV' or (structure[0][0:3] == "CVC" and entryStructure[0][0:4] == "CVVC"):
                if len(structure) > 1:
                    syllables[1] = addSyllableMarker(syllables[1])
                else:
                    syllables[0] += "´"
            elif structure[0] == 'CVC' and syl1Segs[2] == "h" and len(extSyllables) == 0:
                if len(structure) > 1:
                    syllables[1] = addSyllableMarker(syllables[1])
                else:
                    syllables[0] += "´"
            else:
                syllables[0] = addSyllableMarker(syllables[0])
            
            pronunciation = "".join(extSyllables + syllables)
            structure = extStructure + structure
    return pronunciation, tone


df = constructDF("Kashaya word list.txt")
entries = df['Entries']
pronunciations = df['Pronunciations']
generatedPronunciations = []
generatedTones = []
randIndex = 5595#random.randint(0,len(df['Entries']))

entry = df.iloc[randIndex]['Entries']
pronunciation, tone = createPronunciation(entry)
"""
if pronunciation != pronunciations[randIndex]:
    stressLoc = None
    if pronunciations[randIndex] != None:
        segments = splitIntoSegments(pronunciations[randIndex])
        syllables = syllabify(segments)
        for j in range(0, len(syllables)):
            for segment in splitIntoSegments(syllables[j]):
                if segment[0] in accentedVowels:
                    stressLoc = j + 1

        if stressLoc == 1 or stressLoc == 2:
            tone = stressLoc

print("Entry: " + entry)
print("Mine: " + pronunciation)
print("Listed: " + df['Pronunciations'][randIndex])
print("Tone: " + str(tone))
"""
generatedAbs = generateAllAbsolutives(entries)
for i in range(0, len(entries)):
    entry = entries[i]
    pronunciation, tone = createPronunciation(entry)
    if pronunciation != pronunciations[i]:
        stressLoc = None
        if pronunciations[i] != None:
            segments = splitIntoSegments(pronunciations[i])
            syllables = syllabify(segments)
            for j in range(0, len(syllables)):
                for segment in splitIntoSegments(syllables[j]):
                    if segment[0] in accentedVowels:
                        stressLoc = j + 1
            if stressLoc == 1 or stressLoc == 2:
                tone = stressLoc
    generatedPronunciations.append(pronunciation)
    generatedTones.append(tone)

df.insert(2, "Generated Pron", generatedPronunciations)
df.insert(5, "Generated Abs", generatedAbs)
df.insert(4, "Generated Tones", generatedTones)

with open("textFiles/" + "Pronunciation Errors.txt", "w") as errorFile:
    correct = 0
    total = 0
    for i in range(0, len(df['Entries'])):
        if df.iloc[i]['Pronunciations'] != None:
            pronunciation = df.iloc[i]['Pronunciations']
            generated = df.iloc[i]['Generated Pron']
            if pronunciation == generated:
                correct += 1
                total += 1
            else:
                if df.iloc[i]['Absolutives'] == df.iloc[i]['Generated Abs']:
                    total += 1
                    errorFile.write(
                            "Entry: " + df.iloc[i]['Entries'].rstrip("\n") +
                            " | Pronunciation: " + df.iloc[i]['Pronunciations'] +
                            " | Generated Pronunciation: " + df.iloc[i]['Generated Pron'] + "\n"
                        )
    errorFile.close()
print("Number Correct: " + str(correct) + ", Total: " + str(total) +
          ", Percent Correct: " + str(correct/total))
