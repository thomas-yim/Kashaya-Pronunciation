import random
from dfConstructor import constructDF


specialIncrements = ["ʼ", "ʰ", "·"]
vowels = ['a','e','i','o','u']
sonorants = ['m', 'n', 'l', 'y', 'w']
sChars = ['s', 'sʼ', 'š']
consonants = ['b','c','d','f','g','j','k','p','q','r','s','t','ṭ','v','w','x','z', 'ʔ', 'h']
nonVowels = sonorants + sChars + consonants

def splitIntoSegments(entry):
    segments = []
    entry = entry.rstrip('\n')
    if entry[0] == "*":
        entry = entry[1:]
    for i in range(0, len(entry)):
        if i+1 < len(entry):
            
            if entry[i+1] in specialIncrements:
                
                segments.append(entry[i] + entry[i+1])
            elif entry[i] not in specialIncrements:
                segments.append(entry[i])
        elif entry[i] not in specialIncrements:
            segments.append(entry[i])
    return segments



def main():
    df = constructDF("Kashaya word list.txt")
    randIndex = random.randint(0,len(df['Entries']))
    entry = df.iloc[randIndex]['Entries']

    segments = splitIntoSegments(entry)
    
    
    lastVowelIndex = 0
    for j in range(0, len(segments)):
        if segments[j][0] in vowels:
            lastVowelIndex = j
    
    if segments[-1] != 'd':
        segments[lastVowelIndex] = segments[lastVowelIndex][0]
        
    print(segments)
    syllables = []
    lastUsedSegmentIndex = 0
    for k in range(len(segments)-1, -1, -1):
        if segments[k][0] in vowels:
            syllable = segments[k]
            if k > 0:
                if segments[k-1][0] in nonVowels:
                    if k < len(segments)-1 and k+1 != lastUsedSegmentIndex:
                        syllable = syllable + segments[k+1]
                    syllable = segments[k-1] + syllable
                    lastUsedSegmentIndex = k-1
            syllables.insert(0,syllable)
            
    print(syllables)
                    
if __name__ == '__main__':
    main()