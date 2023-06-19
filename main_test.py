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

staff = note.Staff(X/2,Y/2, display_surface)

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
    print(message) 

    if message.type == 'note_on':
       staff.add_note(note.Note(0,0,note_value=int(message.note))) 

    if message.type == 'note_off':
        staff.remove_note(int(message.note))


clock = pygame.time.Clock()

# 
staff.add_note(note.Note(0,0,note_value=60))
staff.add_note(note.Note(0,0,note_value=61))

staff.add_note(note.Note(0,0,note_value=64))
staff.add_note(note.Note(0,0,note_value=65))


#menu = pygame_menu.Menu('Device selector', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
#
#for pos, devices in enumerate(mido.get_input_names()):
#    menu.add.button(devices, setmididevice, devices)
#
#menu.add.button('close', setmididevice, 'test')
#menu.mainloop(display_surface)

while True:  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_1:
        #        if menu.is_enabled == False:
        #            menu.enable()

    display_surface.fill(white)
    staff.draw()
    pygame.display.update()
    clock.tick(60)