import sys
import pygame
import time
white = (255, 255, 255) 
black = (0,0,0) 

class GUI():
    font = None
    text = None

    def __init__(self):
        self.BASEY = 500
        self.line = 0
        self.fsz = 15
 
        pygame.init()

        # create the display surface object 
        # of specific dimension..e(X, Y). 
        self.display_surface = pygame.display.set_mode((1200, 700 )) 
        
        # set the pygame window name 
        pygame.display.set_caption('Eddy Night Out')
        
        # create a font object. 
        # 1st parameter is the font file 
        # which is present in pygame. 
        # 2nd parameter is size of the font 
        self.font = pygame.font.Font('freesansbold.ttf', self.fsz) 
        
        # create a text suface object, 
        # on which text is drawn on it. 
        #self.text = self.font.render('GeeksForGeeks', True, black) 
        
        self.line = 1    
        # create a rectangular object for the 
        # self.text surface object 

        self.addtext("'-----------'")
        self.display_surface.fill(white)

        pygame.display.update()
    
    def addImage(self, index):
        img = pygame.image.load("node{}.jpg".format(index))
        self.display_surface.blit(pygame.transform.scale(img, (1200, 400)), (0,0))

    def refresh(self):
        pygame.display.flip()

    def clear(self):
        self.display_surface.fill(white)
        self.line = 0

    def addtext(self, strrr):
        self.text = self.font.render(strrr, True, black)
        self.display_surface.blit(self.text, (10, self.BASEY+(self.fsz)*self.line))
        self.line = self.line + 1