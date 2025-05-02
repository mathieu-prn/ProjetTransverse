import json, pygame, config

def getrelativepos(pos):
    '''Returns the relative position to the field: (0,0) is the top left corner'''
    x,y=pos
    return x+80,y+55

def loadfile(file):
    '''Loads json files'''
    return json.load(open(file))

def get_font(size): # Returns a pygame font of size "size"
    return pygame.font.Font(config.FONT, size)


