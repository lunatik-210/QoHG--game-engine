import sys
import random
import numpy
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Animal:
	def __init__(self, x, y):
		self.health = 100
		self.hunger = 10
		self.age    = 0
		self.age_limit = [0, 10]
		self.speed_movement = 5
		self.observe_area = 5
		self.x = x
		self.y = y


class Gui:
    def __init__(self, count = 40, width=1024, height=768):
        # Initialize PyGame
        self.height, self.width = height, width
    	self.screen = pygame.display.set_mode((width, height))
    	self.animals = []
    	for i in range(count):
    		self.animals.append(Animal(random.uniform(0, self.height), random.uniform(0, self.width)))
    
    def main_loop(self):
        clock = pygame.time.Clock()

        while 1:
            clock.tick(10)
            
            """Process single events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.screen.fill((0,0,0))

            for anymal in self.animals:
            	pygame.draw.circle(self.screen, (255,0,0), (anymal.x, anymal.y), 2)
            	anymal.x = (anymal.x + random.gauss(0.5, 1)*random.gauss(0.5, 1) ) % self.height
            	anymal.y = (anymal.y + random.gauss(0.5, 1)*random.gauss(0.5, 1) ) % self.width

        	pygame.display.update()            

if __name__ == "__main__":
    MainWindow = Gui()
    MainWindow.main_loop()