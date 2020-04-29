#Thomas Yim 4/26/20
#Kashaya Absolutive form generation

import pandas as pd
from dfConstructor import constructDF
from syllabification import splitIntoSegments

#ARRAY GROUPINGS OF CHARACTERS
sonorants = ['m', 'n', 'l', 'y', 'w']
sChars = ['s', 'sʼ', 'š']
consonants = ['b','c','d','f','g','j','k','p','q','r','t','ṭ','v','x','z', 'ʔ', 'h']
specialIncrements = ["'", "ʰ"]
vowels = ['a','e','i','o','u']
nonVowels = sonorants + sChars + consonants

def main():
    df = constructDF("Kashaya word list.txt")
    entries = df['Entries']
    absolutives = df['Absolutives']
    generatedAbs = []
    
        
    for entry in entries:
        segments = splitIntoSegments(entry)
        
        #If the first segment is a h or ʔ, then it is deleted
        if segments[0] == "h" or segments[0] == "ʔ":
            segments = segments[1:]
            
        final = segments[-1]
        #If the final segment is a d, add a 'u'
        if final == 'd':
            segments.append('u')
        #If the final segment is a sonorant, add a glottal stop
        elif final in sonorants:
            segments.append('ʔ')
        #If the final segment is a consonant, butnon 's' character or not a sonorant
        #it becomes a glottal stop
        elif final in nonVowels:
            segments[-1] = 'ʔ'
        #If it is a 's' segment, then don't do anything
        elif final in sChars:
            pass
        #If it is a short vowel, add a w
        elif final in vowels:
            segments.append('w')
        generatedAbs.append("".join(segments) + "\n")
        
        
    df.insert(4, "Generated Abs", generatedAbs)
        
    count = 0
    for i in range(len(df['Entries'])):
        if (df.iloc[i]['Absolutives'] != None):
            if "·" in df.iloc[i]['Entries']:
                count += 1
            
if __name__ == "__main__":
    main()