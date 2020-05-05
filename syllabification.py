import random
from dfConstructor import constructDF


specialIncrements = ["ʼ", "ʰ", "·", "ʷ"]
vowels = ['a','e','i','o','u']
sonorants = ['m', 'n', 'l', 'y', 'w']
sChars = ['s', 'sʼ', 'š']
consonants = ['b','c','d','f','g','j','k','p','q','r',
              's','t','ṭ','v','w','x','z', 'ʔ', 'h']
nonVowels = sonorants + sChars + consonants

def splitIntoSegments(entry):
    segments = []
    #Get rid of the newline or the star character or a space at the end
    entry = entry.rstrip('\n')
    entry = entry.rstrip('*')
    if entry[-1] == " ":
        entry = entry[:-1]
    for i in range(0, len(entry)):
        if i+1 < len(entry):
            if entry[i+1] in specialIncrements:
                segments.append(entry[i] + entry[i+1])
            elif entry[i] not in specialIncrements:
                segments.append(entry[i])
        elif entry[i] not in specialIncrements:
            segments.append(entry[i])
    return segments

def syllabify(word):
    syllables = []
    segments = splitIntoSegments(word)
    #If the first segment is a h or ʔ, then it is deleted
    if segments[0] == "h" or segments[0] == "ʔ":
        if segments[1][0] not in vowels:
            segments = segments[1:]
    lastUsedSegmentIndex = len(segments)
    for k in range(len(segments)-1, -1, -1):
        if segments[k][0] in vowels:
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
        return[word]
    return syllables
    
def footStructure(syllables):
    structure = []
    for syllable in syllables:
        syllableStruct = ""
        letters = splitIntoSegments(syllable)
        for i in range(0,len(letters)):
            print(letters[i])
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

def main():
    df = constructDF("Kashaya word list.txt")
    randIndex = random.randint(0,len(df['Entries']))
    entry = df.iloc[randIndex]['Entries']
    #entry = "*pʰaʔsʼulh"
    entry = "*bo·catad"
    print(entry)

    segments = splitIntoSegments(entry)
    print(segments)
    
    syllables = syllabify(entry)
    print(syllables)
        
                    
    structure = footStructure(syllables)
    print(structure)
    if len(structure) > 1:
        if structure[0] == "CVV" and structure[1] == "CV":
            syllables[0] = syllables[0].rstrip("·")
            syllables[1] += "·"
            structure[0] = "CV"
            structure[1] = "CVV"
    print(syllables)
    print(structure)
if __name__ == '__main__':
    main()