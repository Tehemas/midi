from tkinter import W
import pygame
import random
import pygame.locals

# Static values for the staff and note classes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STAFF_LENGTH = 250
STAFF_SPACING = 12

# dictionary of all midi notes where each key has a tuple value 
# containing the note name, octave and the relative y positivon on the staff and
# if the note is sharp or flat
notes = {
    55: ('G', -3, False),
    56: ('G#', -3, True),
    57: ('A', -2, False),
    58: ('A#', -2, True),
    59: ('B', -1, False),
    60: ('C', 0, False),
    61: ('C#', 0, True),
    62: ('D', 1, False),
    63: ('D#', 1, True),
    64: ('E', 2, False),
    65: ('F', 3, False),
    66: ('F#', 3, True),
    67: ('G', 4, False),
    68: ('G#', 4, True),
    69: ('A', 5, False),
    70: ('A#', 5, True),
    71: ('B', 6, False),
    72: ('C', 7, False),
    73: ('C#', 7, True),
    74: ('D', 8, False),
    75: ('D#', 8, True),
    76: ('E', 9, False),
    77: ('F', 10, False),
    78: ('F#', 10, True),
    79: ('G', 11, False),
    80: ('G#', 11, True),
    81: ('A', 12, False),
    82: ('A#', 12, True),
    83: ('B', 13, False),
    84: ('C', 14, False),
}

class Note(pygame.sprite.Sprite):
    def __init__(self,
                 x,
                 y, 
                 image_file='Resources/images/half-note-cropped.png', 
                 note_value=60,
                 ):
        super().__init__()

        self.img_offset = 28
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if notes[note_value][2] == True:
            self.sharp = True
        else:
            self.sharp = False
        # Note value will always increment with a half-step and will include sharps and flats
        self.note_value = note_value
        self.flipped = False
        self.adjusted = False


    def update(self):
        print(self)

    def flip(self):
        self.image = pygame.transform.flip(self.image,True, False)
        self.flipped = True

    #def __eq__(self, other):
    #    if not isinstance(other, Note):
    #        return NotImplemented
    #    return self.note_value == other.note_value
 

    def __str__(self):
        return f"pos.x: {self.rect.x} pos.y: {self.rect.y} note_value: {self.note_value}"


class Staff():
    def __init__(self, x, y, scr: pygame.surface.Surface, clef='treble'):
        self.x = x + 45
        self.y = y
        self.l1 = (scr, BLACK, (x, y), (x + STAFF_LENGTH, y))
        self.l2 = (scr, BLACK, (x, y + STAFF_SPACING), (x + STAFF_LENGTH, y + STAFF_SPACING))
        self.l3 = (scr, BLACK, (x, y + STAFF_SPACING * 2), (x + STAFF_LENGTH, y + STAFF_SPACING * 2))
        self.l4 = (scr, BLACK, (x, y + STAFF_SPACING * 3), (x + STAFF_LENGTH, y + STAFF_SPACING * 3))
        self.l5 = (scr, BLACK, (x, y + STAFF_SPACING * 4), (x + STAFF_LENGTH, y + STAFF_SPACING * 4))
        self.surface = scr
        self.notes = pygame.sprite.Group()
        #if clef == 'treble':
        #    self.clef_image = pygame.image.load('Resources/treble_clef.png')
        #else:
        #    self.clef_image = pygame.image.load('Resources/bass_clef.png')


    def draw(self):
        pygame.draw.line(self.surface, BLACK, self.l1[2], self.l1[3])
        pygame.draw.line(self.surface, BLACK, self.l2[2], self.l2[3])
        pygame.draw.line(self.surface, BLACK, self.l3[2], self.l3[3])
        pygame.draw.line(self.surface, BLACK, self.l4[2], self.l4[3])
        pygame.draw.line(self.surface, BLACK, self.l5[2], self.l5[3])
        self.notes.draw(self.surface)

    
    def update(self):
        pass 

    def add_note(self, n):
        self.calculate_pos(n) 
        self.notes.add(n)

    # function to remove_note from the notes collection, takes a parameter n that is a pygame.Sprite object
    def remove_note(self, note_value):
        for x in self.notes.sprites():
            if x.note_value == note_value:
                self.notes.remove(x)


    def calculate_pos(self, new_note: Note):
        new_note.rect.x = self.x + new_note.rect.x

        for existing in self.notes.sprites():
            # existing note is lower than new note and existing note is not flipped
            if existing.note_value == new_note.note_value-1 and existing.adjusted == False:
                if notes[existing.note_value][2] == True:
                    new_note.rect.x = new_note.rect.x + 13
                    new_note.flip()
                    break
                elif notes[existing.note_value][2] == False and notes[new_note.note_value][2] == False:
                    new_note.rect.x = new_note.rect.x + 13
                    new_note.flip()
                    break
                else:
                    break
            elif existing.note_value == new_note.note_value-2 and existing.adjusted == False:
                new_note.rect.x = new_note.rect.x + 13
                new_note.flip()
                break
            elif existing.note_value == new_note.note_value+1 and existing.adjusted == False:
                new_note.rect.x = new_note.rect.x + 13
                new_note.flip()
                break



            elif existing.note_value == new_note.note_value-1 and notes[existing.note_value-1][2] == True:
                new_note.rect.x = new_note.rect.x + 13
                new_note.flip()
                break
            elif existing.note_value == new_note.note_value-2 and notes[existing.note_value-1][2] == True:
                new_note.rect.x = new_note.rect.x + 13
                new_note.flip()
                break
            elif existing.note_value == new_note.note_value+1 and notes[new_note.note_value+1][2] == False:
                existing.rect.x = existing.rect.x + 13
                existing.flip()
                break
            elif existing.note_value == new_note.note_value+2:
                existing.rect.x = existing.rect.x + 13
                existing.image = pygame.transform.flip(new_note.image,True, False)
                break

               
        # set y position for note based on the staff y position, the size of the note image
        # since position is based on top left and adding all the staff spacings to get middle c placement
        new_note.rect.y = self.y - new_note.img_offset + (5 * STAFF_SPACING) - ((notes[new_note.note_value][1] * STAFF_SPACING)) / 2


    def __str__(self):
        return f"pos.x: {self.x} pos.y: {self.y}"


#pygame.init()
#wh = (255,255,255)
#w, h = 640, 240
#screen = pygame.display.set_mode((w, h))
#
#clock = pygame.time.Clock()
#
#a = Note(0,0)
#
#s = Staff(screen.get_size()[0]/2, screen.get_size()[1]/2, screen)
#s.add_note(a)
#
#while True:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            pygame.quit()
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_LEFT:
#                s.notes.empty()
#                s.add_note(Note(0,0,note_value=random.randint(60,70)))
#                
#    screen.fill(wh)
#    s.draw()
#    pygame.display.flip()
#    pygame.display.update()
#    clock.tick(10) 
