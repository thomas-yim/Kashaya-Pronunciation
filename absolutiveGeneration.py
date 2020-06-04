#Thomas Yim 4/26/20
#Kashaya Absolutive form generation

import pandas as pd
from dfConstructor import constructDF, findComponents
from syllabification import splitIntoSegments, syllabify, footStructure, stripFinalSpaces, extrametricalityApplies
from specialLists import Config

lists = Config()
    
specialIncrements = lists.increments
vowels = lists.vowels
sonorants = lists.sonorants
sChars = lists.sChars
consonants = lists.consonants
nonVowels = sonorants + sChars + consonants



def footFlipping(startEntry, syllables, structure):
    #This is the process of "Foot Flipping"
    if len(structure) > 2:
        if extrametricalityApplies(startEntry):
            if structure[1] == "CVV" and structure[2] == "CV":
                syllables[1] = syllables[1].rstrip("·")
                syllables[2] += "·"
                structure[1] = "CV"
                structure[2] = "CVV"
        elif structure[0] == "CVV" and structure[1] == "CV":
            syllables[0] = syllables[0].rstrip("·")
            syllables[1] += "·"
            structure[0] = "CV"
            structure[1] = "CVV"
    return syllables, structure
        

def createAbsolutive(entry):
    """
    This code looks for the last vowel and if it doesn't end with /d/,
    it shortens the long vowel
    """
    startEntry = entry
    if entry[0] == "*":
        segments = splitIntoSegments(entry)
        #If the first segment is a h or ʔ, then it is deleted
        if segments[0] == "h" or segments[0] == "ʔ":
            if segments[1][0] not in vowels:
                segments = segments[1:]
        syllables = syllabify(segments)
        finalSyllable = syllables[-1]
        #If the final letter is not d and the final vowel is long, shorten it.
        if finalSyllable[-1] != 'd':
            #This iterates backwards through the last syllable in the word
            for i in range(len(finalSyllable)-1, -1, -1):
                #If the current letter is a vowel
                if finalSyllable[i] in vowels:
                    #If it is not the last character in the string
                    if i < len(finalSyllable)-1:
                        #If the final vowel is a long one
                        if finalSyllable[i+1] == "·":
                            #This deletes that long vowel dot
                            finalSyllable = finalSyllable[:i+1] + finalSyllable[i+2:]
                            syllables[-1] = finalSyllable
        
                            
        
        #Entry has now been modified. Needs to be after initial foot flipping
        entry = "".join(syllables)
        segments = splitIntoSegments(entry)
        
            
        #This gets the final letter without its special increment
        final = segments[-1][0]
        #If the final segment is a d, add a 'u'
        if final == 'd':
            segments.append('u')
            syllables = syllabify(segments)
            structure = footStructure(syllables)
            #Must be at least three to see if the third to last is CV and
            #The second to last is CV
            if len(structure) > 3:
                if structure[-2] == "CV" and structure[-3] == "CV":
                    syllables[-2] += "·"
                    segments = splitIntoSegments("".join(syllables))
                elif structure[-2] == "CV" and structure[-3] == "CVV":
                    syllables[-3] = syllables[-3].rstrip("·")
                    syllables[-2] += "·"
                    structure[-3] = "CV"
                    structure[-2] = "CVV"
        #If the final segment is a sonorant, add a glottal stop
        elif final in sonorants:
            segments.append('ʔ')
        #If it is a 's' segment, then don't do anything
        elif final in sChars:
            pass
        #If the final segment is a consonant, butnon 's' character or not a sonorant
        #it becomes a glottal stop
        elif final in nonVowels:
            segments[-1] = 'ʔ'
        #If it is a short vowel, add a w
        elif segments[-1] in vowels:
            segments.append('w')
        
        
        syllables = syllabify(segments)
        structure = footStructure(syllables)
        #This is the process of "Foot Flipping"
        syllables, structure = footFlipping(startEntry, syllables, structure)
    else:
        """
        It reaches this point if it is not a bound stem.
        If a non-bound stem has a word initial h or ʔ that is not the onset
        to the syllable, delete it.
        """
        if (entry[0] == "h" or entry[0] == "ʔ") and entry[1] not in vowels:
            entry = entry[1:]
        segments = splitIntoSegments(entry)
        final = segments[-1][0]
        
        if final in sChars:
            pass
        elif final in sonorants:
            pass
        elif final in nonVowels:
            segments[-1] = 'ʔ'

        syllables = syllabify(segments)
        structure = footStructure(syllables)

    #This handles closed vowel shortening. A CVVC turns into a CVC
    for i in range(0, len(syllables)):
        if structure[i] == "CVVC" or structure[i] == "CVVCC":
            syllableSegments = splitIntoSegments(syllables[i])
            syllableSegments[1] = syllableSegments[1][0]
            syllables[i] = "".join(syllableSegments)

    absolutive = "".join(syllables)
    return absolutive
  
def generateAllAbsolutives(entries):
    generatedAbs = []
    
    for entry in entries:
        absolutive = createAbsolutive(entry)
        generatedAbs.append(stripFinalSpaces(absolutive))
    return generatedAbs

def main():
    #See dfConstructor.py for how I handled missing entries
    df = constructDF("Kashaya word list.txt")
    entries = df['Entries']
    #I am pulling this list to compare against my generated ones
    absolutives = df['Absolutives']
    
    generatedAbs = generateAllAbsolutives(entries)
        
    df.insert(4, "Generated Abs", generatedAbs)
    with open("Bound Stem Errors.txt", "w") as errorFile:
        correct = 0
        total = 0
        notBoundErrors = 0
        notBoundTotal = 0
        for i in range(0, len(df['Entries'])):
            if df.iloc[i]['Absolutives'] != None:
                if df.iloc[i]['Entries'][0] == "*":
                    notBoundTotal += 1
                absolutive = df.iloc[i]['Absolutives']
                generated = df.iloc[i]['Generated Abs']
                total += 1
                if absolutive == generated:
                    correct += 1
                elif df.iloc[i]['Entries'][0] == "*":
                    notBoundErrors += 1
                    errorFile.write(
                            "Entry: " + df.iloc[i]['Entries'].rstrip("\n") +
                            " | Absolutive: " + df.iloc[i]['Absolutives'] +
                            " | Generated Absolutive: " + df.iloc[i]['Generated Abs'] + "\n"
                        )
        errorFile.close()
    print(notBoundErrors)
    print(notBoundTotal)
    print("Number Correct: " + str(correct) + ", Total: " + str(total) + ", Percent Correct: " + str(correct/total))
                
if __name__ == "__main__":
    main()