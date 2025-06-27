import pygame

class Input(object):
    def __init__(self):
        # has user quit ?
        self.quit= False

        # lists to store keystates
        # down, up: discrete event, 1 iteration
        # pressed: continuous even betwee down and up
        self.keyDownList    = []
        self.keyPressedList = []
        self.keyUpList      = []

    def update(self):
        self.keyDownList    = []
        self.keyUpList      = []
        #iterate over inputs key and mouse
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keyName= pygame.key.name( event.key )
                self.keyDownList.append( keyName )
                self.keyPressedList.append( keyName )
            if event.type == pygame.KEYUP:
                keyName= pygame.key.name( event.key )
                self.keyPressedList.remove( keyName )
                self.keyUpList.append( keyName )
            if event.type == pygame.QUIT:
                self.quit= True

    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList
    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList
