#Thomas Yim 4/26/20
#Database construction based a text file

import pandas as pd

def constructDF(filename):
    #ARRAYS TO BE ADDED TO PANDAS DATAFRAME
    entries = []
    
    pronunciation = []
    currentPronunciation = None
    
    absolutive = []
    currentAbsolutive = None
    
    grammaticalInfo = []
    currentInfo = None
    
    tones = []
    currentTone = None
    
    gloss = []
    currentGloss = None
    
    """
    Note if a current value has a None value, then it is missing in the txt file
    
    This is how it works:
    When it finds the first entry, it adds it.
    It then continues through and when it finds a pronunciation, absolutive, etc.
    it will change its current value to whatever follows it
    The reason they are default set to none and reset to none at the start
    of every new entry is that all words don't have all other information as well
    
    There are sometimes also dashes where there is no value so it check for that
    """
    
    with open(filename, 'r') as wordList:
        for line in wordList.readlines():
            #Every time it comes across an entry:
            if (line[:len("Entry")] == "Entry"):
                entries.append(line[len("Entry: "):])
                if (len(entries) != 1):
                    pronunciation.append(currentPronunciation)
                    tones.append(currentTone)
                    absolutive.append(currentAbsolutive)
                    grammaticalInfo.append(currentInfo)
                    gloss.append(currentGloss)
                    currentPronunciation = None
                    currentTone = None
                    currentAbsolutive = None
                    currentInfo = None
                    currentGloss = None
            elif (line[:len("Tone")] == "Tone"):
                if line[len("Tone: "):len("Tone: ")+1] != "-":
                    currentTone = line[len("Tone: "):]
            elif (line[:len("Absolutive")] == "Absolutive"):
                if line[len("Absolutive: "):len("Absolutive: ")+1] != "-":
                    currentAbsolutive = line[len("Absolutive: "):]
            elif (line[:len("Grammatical")] == "Grammatical"):
                if line[len("Grammatical Info: "):len("Grammatical Info: ")+1] != "-":
                    currentInfo = line[len("Grammatical Info: "):]
            elif (line[:len("Gloss")] == "Gloss"):
                if line[len("Gloss: "):len("Gloss: ")+1] != "-":
                    currentGloss = line[len("Gloss: "):]
            elif (line[:len("Pronunciation")] == "Pronunciation"):
                if line[len("Pronunciation: "):len("Pronunciation: ")+1] != "-":
                    currentPronunciation = line[len("Pronunciation: "):]
        pronunciation.append(currentPronunciation)
        tones.append(currentTone)
        absolutive.append(currentAbsolutive)
        grammaticalInfo.append(currentInfo)
        gloss.append(currentGloss)
    
    data = {"Entries":entries, "Pronunciations":pronunciation, "Tones": tones,
            "Absolutives": absolutive, "Grammatical Info": grammaticalInfo, "Gloss": gloss}
    columns = ["Entries", "Pronunciations", "Tones", "Absolutives", "Grammatical Info", "Gloss"]
    df = pd.DataFrame(data, columns=columns)
    return df