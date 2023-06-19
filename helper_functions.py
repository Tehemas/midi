from tkinter import W
from urllib import response
import requests
import os
from bs4 import BeautifulSoup
import pygame

def getMidiInfo():
    output = dict()

    url = "https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies"
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('div', attrs = {'class':'table-responsive'})
        tbody = data.find('tbody')
        for x in tbody.find_all('tr'):
            output.update({x.find_all('td')[0].text:x.find_all('td')[3].text})

    return output


print(getMidiInfo())