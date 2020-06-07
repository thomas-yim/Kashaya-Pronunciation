#Thomas Yim 4/26/20
#Kashaya Absolutive form generation

import pandas as pd
from dfConstructor import constructDF, findComponents
from syllabification import splitIntoSegments, syllabify, footStructure, stripFinalSpaces, extrametricalityApplies
from specialLists import Config
from tqdm import tqdm

lists = Config()
    
specialIncrements = lists.increments
vowels = lists.vowels
sonorants = lists.sonorants
sChars = lists.sChars
consonants = lists.consonants
nonVowels = sonorants + sChars + consonants


"""
This completes the process of foot flipping.
Foot Flipping only occurs when there is a CVV CV syllable pattern
For this to occur, the CVV has to be at the left edge of the visible domain
So, if there is extrametricality, the second syllable can be CVV and the third CV
If this happens, (CVV, CV) -> (CV,CVV)
"""
def footFlipping(startEntry, syllables, structure):
    #If there are more than 2 syllables
    if len(structure) > 2:
        #If the first syllable is extrametrical, there must be more than 3 syllables so the CV is not final
        if extrametricalityApplies(startEntry) and len(structure) > 3:
            if structure[1] == "CVV" and structure[2] == "CV":
                #These four lines move the heavy syllable marker to the other syllable
                syllables[1] = syllables[1].rstrip("·")
                syllables[2] += "·"
                structure[1] = "CV"
                structure[2] = "CVV"
        elif structure[0] == "CVV" and structure[1] == "CV":
            syllables[0] = syllables[0].rstrip("·")
            syllables[1] += "·"
            structure[0] = "CV"
            structure[1] = "CVV"
    #Return the modified syllables and structure
    return syllables, structure
        

def createAbsolutive(entry):
    #We need this because entry will be modified as it transitions to the absolutive
    startEntry = entry
    
    """
    The * is present when it is a bound stem. This receives all of the absolutive rules
    """
    if entry[0] == "*":
        segments = splitIntoSegments(entry)
        #If the first segment is a h or ʔ and is not the onset, then it is deleted
        if segments[0] == "h" or segments[0] == "ʔ":
            #If the second character is not a vowel, it is not part of the onset.
            if segments[1][0] not in vowels:
                segments = segments[1:]
        syllables = syllabify(segments)
        finalSyllable = syllables[-1]
        """
        This code looks for the last vowel and if it doesn't end with /d/,
        it shortens the final long vowel
        """
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
        
                            
        
        #Entry has now been modified.
        entry = "".join(syllables)
        segments = splitIntoSegments(entry)
        
            
        #This gets the final letter without its special increment if it had it
        final = segments[-1][0]
        #If the final segment is a d, add a 'u'
        if final == 'd':
            segments.append('u')
            #Note that the foot structure (and possibly stress) will change with the added u.
            #This is because the syllables are shifted over.
            syllables = syllabify(segments)
            structure = footStructure(syllables)
            #Must be at least three to see if the third to last is CV and
            #The second to last is CV
            if len(structure) > 3:
                if startEntry == "*bahqʰayad":
                    print(structure)
                #If the second and third to last syllables are light, lengthen it 
                #Note for self... Check for extrametricality
                if structure[-2] == "CV" and structure[-3] == "CV":
                    syllables[-2] += "·"
                    segments = splitIntoSegments("".join(syllables))

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
        if startEntry == "*bahqʰayad":
            print(syllables)
        structure = footStructure(syllables)
        
        #This is the process of "Foot Flipping"
        syllables, structure = footFlipping(startEntry, syllables, structure)
    else:
        """
        It reaches this point if it is not a bound stem.
        There is an absolutive-like form that only has debuccalization, initial increment deletion,
        and closed syllable shortening.
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
                if df.iloc[i]['Entries'][0] == "d":
                    notBoundTotal += 1
                absolutive = df.iloc[i]['Absolutives']
                generated = df.iloc[i]['Generated Abs']
                total += 1
                if absolutive == generated:
                    correct += 1
                elif df.iloc[i]['Entries'][-1] == "d":
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