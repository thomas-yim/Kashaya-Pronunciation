#Thomas Yim 5/15/20
#Kashaya special lists. If changed here, it changes for all files.

increments = ["ʼ", "ʰ", "·", "ʷ"]
vowels = ['a','e','i','o','u']
sonorants = ['m', 'n', 'l', 'y', 'w']
sChars = ['s', 'sʼ', 'š']
consonants = ['b','c','d','f','g','j','k','p','q','r',
              's','t','ṭ','v','w','x','z', 'ʔ', 'h']
name="sortedLists"
prefixes = ['ba', 'bi', 'ca', 'cu', 'cʰi', 'da', 'du', 'di', 'ha', 'hi', 'li',
            'ma', 'mi', 'mu', 'pi', 'pʰa', 'pʰi', 'pʰu', 'qa', 'si', 'ša', 'šu']
suffixes = ['ad', 'mul', 'mad', 'aq', 'ala', 'ibic', 'hqa', 'ad', 'id','cid',
            'med']

class Config:
    def __init__(self):
        self.vowels = vowels
        self.sonorants = sonorants
        self.sChars = sChars
        self.consonants = consonants
        self.increments = increments
        self.suffixes = suffixes
        self.prefixes = prefixes
