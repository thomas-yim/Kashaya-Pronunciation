#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:34:48 2020

@author: thomas
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from dfConstructor import constructDF
from tqdm import tqdm
from dfConstructor import stripFinalSpaces, constructDF


df = constructDF("Kashaya word list.txt")
entries = df['Entries']

with open('textFiles/pluralComplexEntries.txt', 'r') as file:
    lines = file.readlines()
    allComponents = []
    for line in lines:
        allComponents.append(stripFinalSpaces(line))
print(len(allComponents))


pluralComponents = []
count = 0
for i in tqdm(range(0, len(allComponents))):
    if allComponents[i] == "Same":
        entry = entries[i]
        url = 'https://www.webonary.org/kashaya?s=' + entry + '&search=Search&key=&tax=-1&displayAdvancedSearchName=0'
        
        # Connect to the URL
        response = requests.get(url)
        
        components = []
        
        # Parse HTML and save to BeautifulSoup object
        soup = BeautifulSoup(response.text, "html.parser")
        for span in soup.find_all('span', {'class':'visiblevariantentryrefs'}):
            nestedSpans = span.find_all('span', {'class':'reversename'})
            for nestedSpan in nestedSpans:
                if nestedSpan.text[-2:] == "of":
                    links = span.find_all('a')
                    variant = links[0].text
                    components.append(variant)
        if len(components) == 0:
            components.append("Same")
        parts = ""
        for component in components:
            parts = parts + component + " "
        allComponents[i] = stripFinalSpaces(parts)

with open("textFiles/pluralOfCases.txt", 'w') as file:
    for components in allComponents:
        file.write(components)
        file.write("\n")

            
        