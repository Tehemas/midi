import random
from tkinter import W
import mido
import sys
import os
import pygame
import helper_functions
import pygame_menu
import note

mididict = helper_functions.getMidiInfo()

pygame.init()
 
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

notex = 100
notey = 100
 
X = 1024
Y = 768

display_surface = pygame.display.set_mode((X, Y)) 
pygame.display.set_caption('Note Flashcard')

active_notes = []

staff = note.Staff(X/2,Y/2, display_surface)

staff.add_note(note.Note(0,0,note_value=random.randint(55,84)))

def setmididevice(dev):
    global port
    try:
        port = mido.open_input(str(dev))
        port.callback = print_message
    except Exception as e:
        print(e) 
    print('Port Created')
    menu.disable()

def print_message(message):
    global staff
    global active_notes
    print(message) 

    if message.type == 'note_on':
       #staff.add_note(note.Note(0,0,note_value=int(message.note))) 
       active_notes.append(message.note)

    if message.type == 'note_off':
        #staff.remove_note(int(message.note))
        #staff.update_adjacent_notes(int(message.note))
        for note in active_notes:
            if message.note == note:
                active_notes.remove(note)

    staff_notes = [note.note_value for note in staff.notes.sprites()]
    staff_notes.sort()
    active_notes.sort()
    
    if staff_notes == active_notes:
        print("GOOD JOB!")
        staff.remove_all()
        staff.add_random_note(60,80)  
        staff.add_random_note(60,80)  

clock = pygame.time.Clock()

menu = pygame_menu.Menu('Device selector', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

for pos, devices in enumerate(mido.get_input_names()):
    menu.add.button(devices, setmididevice, devices)

menu.add.button('close', setmididevice, 'test')
menu.mainloop(display_surface)

while True:  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if menu.is_enabled == False:
                    menu.enable()

    display_surface.fill(white)
    staff.draw()
    pygame.display.update()
    clock.tick(60)