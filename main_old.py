from tkinter import W
import mido
import sys
import os
import pygame
import helper_functions
import pygame_menu

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
    global text
    global textRect
    print(message)
    if message.type == 'note_on':
        text = font.render(str(mididict[str(message.note)]), True, black, white)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)


display_surface = pygame.display.set_mode((X, Y)) 
pygame.display.set_caption('Note Flashcard')

clock = pygame.time.Clock()

staff = pygame.image.load(os.path.abspath(os.curdir) + '\Resources\images\staff.png')
note = pygame.image.load(os.path.abspath(os.curdir) + '\Resources\images\half-note.png')
note = pygame.image.load(os.path.abspath(os.curdir) + '\Resources\images\half-note-cropped.png')

print(staff.get_height())
print(staff.get_size())

menu = pygame_menu.Menu('Device selector', 400, 300, theme=pygame_menu.themes.THEME_BLUE)


for pos, devices in enumerate(mido.get_input_names()):
    menu.add.button(devices, setmididevice, devices)

menu.add.button('close', setmididevice, 'test')
menu.mainloop(display_surface)


font = pygame.font.Font('freesansbold.ttf', 48)
text = font.render('', True, black, white)
text_notex = font.render(str(notex), True, black, white)
text_notey = font.render(str(notey), True, black, white)
textRect = text.get_rect()
textRect.center = (X // 2, Y // 2)


while True:  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                notex -= 1
                text_notex = font.render(str(notex), True, black, white)
            if event.key == pygame.K_RIGHT:
                notex += 1
                text_notex = font.render(str(notex), True, black, white)
            if event.key == pygame.K_UP:
                notey -= 1
                text_notey = font.render(str(notey), True, black, white)
            if event.key == pygame.K_DOWN:
                notey += 1
                text_notey = font.render(str(notey), True, black, white)
            if event.key == pygame.K_1:
                if menu.is_enabled == False:
                    menu.enable()

    mx, my = pygame.mouse.get_pos()
    notex = mx
    notey = my 
    text_notex = font.render(str(notex), True, black, white)
    text_notey = font.render(str(notey), True, black, white)

    
    display_surface.fill(white)
    display_surface.blit(staff,(0,100))
    display_surface.blit(note,(notex,notey))
    display_surface.blit(text, textRect)    
    display_surface.blit(text_notex, (0,0))
    display_surface.blit(text_notey, (100,0))

    pygame.draw.line(display_surface, black, (60, 80), (200,80))

    pygame.display.update()
    clock.tick(60)