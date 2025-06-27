import pygame
import sys

from core.input import Input

class Base(object):
    def __init__(self, screenSize=[512,512], titlebartext='Graphics Window'):
        self.kwargs={}
        for kwarg in sys.argv[1:]:
            k,v=kwarg.split('=')
            self.kwargs[k]=float(v)
        print(f'self.kwargs= {self.kwargs}')

        # initialize all pygame modules
        pygame.init()
        # indicate rendering details
        displayFlags= pygame.DOUBLEBUF | pygame.OPENGL
        # init buffers to perfomr antialiasing
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLEBUFFERS, 1 )
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLESAMPLES, 4 )
        # use a core OpenGL profile for cross-platofrm compatability
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE )
        # create and display the window
        self.screen= pygame.display.set_mode( screenSize, displayFlags )
        # Set text that displays in title bar
        pygame.display.set_caption(titlebartext)

        self.running= True

        self.clock= pygame.time.Clock()

        self.input = Input()

        self.time= 0

    def initialize(self):
        pass

    def update(self):
        pass

    def run(self):
        ## STARTUP ##
        self.initialize()

        while self.running:
            ## process input ##
            self.input.update()
            if self.input.quit:
                self.running= False
            
            # secs since iteration of run loop
            self.deltaTime= self.clock.get_time() / 1000
            # increment time app has been running
            self.time += self.deltaTime

            ## update ##
            self.update()

            ## render ##
            # disp img on screen
            pygame.display.flip()

            # pause if necessary for 60 fps
            self.clock.tick(60)

        ## shutdown ##
        pygame.quit()
        sys.exit()

