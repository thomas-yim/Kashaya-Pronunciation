#!/usr/bin/env python3

"""
This file will scrape the page to see if there is a prefix to determine extrimetricality
Note this version had a problem. If it was a plural, it did not go into the singular version
"""

# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from dfConstructor import constructDF
from tqdm import tqdm

df = constructDF("Kashaya word list.txt")
entries = df['Entries']
count = 0
allComponents = []
for i in tqdm(range(3918, 5598)):
    entry = entries[i]
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
        components.append("Same")
    else:
        count += 1
    allComponents.append(components)
print(count)
with open("complexEntries.txt", 'a') as file:
    for components in allComponents:
        for component in components:
            file.write(component + " ")
        file.write("\n")
        
    