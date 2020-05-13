#Thomas Yim 4/26/20
#Kashaya Absolutive form generation

import pandas as pd
from dfConstructor import constructDF
from syllabification import splitIntoSegments, syllabify, footStructure, stripFinalSpaces

#ARRAY GROUPINGS OF CHARACTERS
specialIncrements = ["ʼ", "ʰ", "·", "ʷ"]
vowels = ['a','e','i','o','u']
sonorants = ['m', 'n', 'ŋ', 'l', 'y', 'w']
sChars = ['s', 'sʼ', 'š']
consonants = ['b','c','d','f','g','j','k','p','q','r',
              's','t','ṭ','v','w','x','z', 'ʔ', 'h']
nonVowels = sonorants + sChars + consonants

#See dfConstructor.py for how I handled missing entries
df = constructDF("Kashaya word list.txt")
entries = df['Entries']
#I am pulling this list to compare against my generated ones
absolutives = df['Absolutives']
generatedAbs = []


for entry in entries: 
    """
    This code looks for the last vowel and if it doesn't end with /d/,
    it shortens the long vowel
    """
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
    
                        

    structure = footStructure(syllables)
    #This is the process of "Foot Flipping"
    if len(structure) > 2:
        if structure[0] == "CVV" and structure[1] == "CV":
            syllables[0] = syllables[0].rstrip("·")
            syllables[1] += "·"
            structure[0] = "CV"
            structure[1] = "CVV"
    
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
        if len(structure) > 3:
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
    
    entry = "".join(segments)
        
    generatedAbs.append(stripFinalSpaces(entry))
    
    
df.insert(4, "Generated Abs", generatedAbs)
with open("Absolutive Errors.txt", "w") as errorFile:
    correct = 0
    total = 0
    for i in range(0, len(df['Entries'])):
        if df.iloc[i]['Absolutives'] != None:
            absolutive = df.iloc[i]['Absolutives']
            generated = df.iloc[i]['Generated Abs']
            total += 1
            if absolutive == generated:
                correct += 1
            else:
                errorFile.write(
                        "Entry: " + df.iloc[i]['Entries'].rstrip("\n") +
                        " | Absolutive: " + df.iloc[i]['Absolutives'] +
                        " | Generated Absolutive: " + df.iloc[i]['Generated Abs'] + "\n"
                    )
    errorFile.close()
print("Number Correct: " + str(correct) + ", Total: " + str(total) + ", Percent Correct: " + str(correct/total))
            
#if __name__ == "__main__":
    #main()