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
    
    
    with open(filename, 'r') as wordList:
        for line in wordList.readlines():
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
                currentTone = line[len("Tone: "):]
            elif (line[:len("Absolutive")] == "Absolutive"):
                currentAbsolutive = line[len("Absolutive: "):]
            elif (line[:len("Grammatical")] == "Grammatical"):
                currentInfo = line[len("Grammatical Info: "):]
            elif (line[:len("Gloss")] == "Gloss"):
                currentGloss = line[len("Gloss: "):]
            elif (line[:len("Pronunciation")] == "Pronunciation"):
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