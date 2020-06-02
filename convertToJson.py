#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:30:01 2020

@author: thomas
"""
from dfConstructor import constructDF
import json
from syllabification import stripFinalSpaces

filename = 'pluralComplexEntries'

with open(filename + '.txt', 'r') as file:
    dictionary = {}
    df = constructDF('Kashaya word list.txt')
    entries = df['Entries']
    lines = file.readlines()
    print(len(lines))
    size = -1
    count = 1
    for i in range(0, len(lines)):
        newSize = len(dictionary)
        dictionary[stripFinalSpaces(entries[i].rstrip('\n'))] = stripFinalSpaces(lines[i].rstrip('\n'))
        if newSize == size:
            count += 1
            print(entries[i-1])
        size=newSize
        
print(len(dictionary))
with open(filename + '.json', 'w') as jsonFile:
    json.dump(dictionary, jsonFile)