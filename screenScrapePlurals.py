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

def searchComponents(soup):
    parts = []
    for span in soup.find_all('span', {'class', 'complexformentryref'}):
        links = span.find_all('a')
        for link in links:
            parts.append(link.text)
    if len(parts) == 0:
        parts.append("Same")
    return parts


df = constructDF("Kashaya word list.txt")
entries = df['Entries']

with open('pluralComplexEntries.txt', 'r') as file:
    lines = file.readlines()
    allComponents = []
    for line in lines:
        allComponents.append(stripFinalSpaces(line))
print(len(allComponents))

"""
TODO: Go through each component
if 'same', pull from online and see if there is the word plural in the entry
if so go to the next link
pull the components from that and add them to the components of the plural entry
"""

pluralComponents = []
count = 0
for i in tqdm(range(5456, len(allComponents))):
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
                if nestedSpan.text == "Plural of" or nestedSpan.text == "Dialectal Variant of":
                    links = span.find_all('a')
                    link = links[0]
                    wordResponse = requests.get(link.get('href'))
                    soup = BeautifulSoup(wordResponse.text, "html.parser")
                    components = searchComponents(soup)
        if len(components) == 0:
            components.append("Same")
        parts = ""
        for component in components:
            parts = parts + component + " "
        allComponents[i] = stripFinalSpaces(parts)

with open("pluralComplexEntries.txt", 'w') as file:
    for components in allComponents:
        file.write(components)
        file.write("\n")

            
        