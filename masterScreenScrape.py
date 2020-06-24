import requests
import urllib.request
import time
import json
from bs4 import BeautifulSoup
from dfConstructor import constructDF
from tqdm import tqdm
from dfConstructor import stripFinalSpaces, constructDF

"""
This file runs the functionality of the other screen scrapers
"""

def searchComponents(soup):
    parts = []
    for span in soup.find_all('span', {'class', 'complexformentryref'}):
        links = span.find_all('a')
        for link in links:
            parts.append(link.text)
    if len(parts) == 0:
        parts.append("Same")
    return parts

print("This program will scrape the website and either append or replace the components")

runType = input("Is this an append or replacement run: ")

if runType.lower() == "append":
    print("The input file should be in the format of the Kashaya word list.txt file")
    filename = input("What is the name of the file with the new entries? ")
    df = constructDF(filename)
    entries = list(df['Entries'])
    with open("textFiles/pluralComplexEntries.json") as componentFile:
        components = json.load(componentFile)
        componentFile.close()
    currentEntries = list(components.keys())
    newEntries = []
    allComponents = []
    for i in range(0, len(entries)):
        if entries[i] not in currentEntries:
            newEntries.append(entries[i])
    for entry in newEntries:
        entry = entry.rstrip("\n")
        print(entry)
        # Set the URL you want to webscrape from
        url = 'https://www.webonary.org/kashaya?s=' + entry + '&search=Search&key=&tax=-1&displayAdvancedSearchName=0'
        
        # Connect to the URL
        response = requests.get(url)
        
        # Parse HTML and save to BeautifulSoup object
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all('a'):
    
            if link.text == entry:
                url = link.get('href')
        wordResponse = requests.get(url)
        soup = BeautifulSoup(wordResponse.text, "html.parser")
        """
        for link in soup.find_all('a'):
            if link.text == "Advanced Search":
                break
            if foundComponentLinks:
                print(link.text)
            if link.text == "Contact Us":
                foundComponentLinks = True
        """
        components = []
        for span in soup.find_all('span', {'class', 'complexformentryref'}):
            links = span.find_all('a')
            for link in links:
                components.append(link.text)
        if len(components) == 0:
            for span in soup.find_all('span', {'class':'visiblevariantentryrefs'}):
                nestedSpans = span.find_all('span', {'class':'reversename'})
                for nestedSpan in nestedSpans:
                    if nestedSpan.text[-2:] == "of":
                        links = span.find_all('a')
                        link = links[0]
                        wordResponse = requests.get(link.get('href'))
                        deepSoup = BeautifulSoup(wordResponse.text, "html.parser")
                        components = searchComponents(deepSoup)
                        if len(components) == 0:
                            if len(links) > 0:
                                variant = links[0].text
                                components.append(variant)
            if len(components) == 0:
                components.append(link.text)
            parts = ""
            for component in components:
                parts = parts + component + " "
            allComponents[i] = stripFinalSpaces(parts)
        allComponents.append(components)

elif runType.lower() == "replace":
    print("The input file should be in the format of the Kashaya word list.txt file")
    filename = input("What is the name of the file with the new entries? ")
    df = constructDF(filename)
    entries = list(df['Entries'])
    with open('textFiles/pluralComplexEntries.txt', 'r') as file:
        lines = file.readlines()
        allComponents = []
        for line in lines:
            allComponents.append(stripFinalSpaces(line))
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
                    if nestedSpan.text[-2:] == "Plural of":
                        links = span.find_all('a')
                        wordResponse = requests.get(link.get('href'))
                        soup = BeautifulSoup(wordResponse.text, "html.parser")
                        components = searchComponents(soup)
                        if len(components) == 0:
                            if len(links) > 0:
                                variant = links[0].text
                                components.append(variant)
            if len(components) == 0:
                components.append("Same")
            parts = ""
            for component in components:
                parts = parts + component + " "
            allComponents[i] = stripFinalSpaces(parts)

with open("textFiles/pluralComplexEntries.txt", 'a') as file:
    for components in allComponents:
        for component in components:
            file.write(component + " ")
        file.write("\n")
        