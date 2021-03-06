#!/usr/bin/env python

########## System libs ##########
import random
import sys
from copy import deepcopy
from log import *
#################################

########## PyGame ###############
import pygame
from pygame.locals import *
import sprites

if not pygame.font: logging.warning('Warning, fonts disabled')
if not pygame.mixer: logging.warning('Warning, sound disabled')
#################################

########## Game logic ###########
import lands.generators.Map as MapGenerator

from texture_manager import Texture, TexturesMap
from lands.Land import Land
from lands.DemoLand import DemoLand
from lands.Position import Position
import config

#################################

path = './configs'

items = config.load_items(path+'/items.xml')
bioms = config.load_bioms(path+'/bioms.xml', items)

class Main:
    """
    The Main Class - This class handles the main 
    initialization and creating of the Game.
    """
    
    def __init__(self, land, size=(1024, 768), debug=False):
        # Initialize PyGame
        pygame.init()

        # init lands
        self.land = land
        self.demo_land = DemoLand(land, 100)

        # Create the Screen
        self.screen = pygame.display.set_mode(size)
        self.width, self.height = size
        self.debug = debug

    def set_full_screen(self, fullscreen_option):
        modes = pygame.display.list_modes(32)
        if modes and fullscreen_option:
            self.screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 32)
        self.width, self.height = modes[0]

    def main_loop(self):
        """
        This is the Main Loop of the Game
        """
        self.set_view_mod(48)

        # Get random x,y starting location
        displs = self.land.init_player()
        displs -= Position(10, 10)
        ##################################

        # some local variables
        changes = True
        
        # speed.x = 1, speed.y = 1
        speed = Position(1, 1)

        mouse = Position(0, 0)

        ######################
        
        # init demo land surface 
        small_map_size = 200
        demo_land_surface = self.create_demo_land_surface(small_map_size)
        ########################

        clock = pygame.time.Clock()

        # set User event to update Monsters
        pygame.time.set_timer(USEREVENT+1, 600)
        pygame.time.set_timer(USEREVENT+2, 150)
        while 1:
            # Make sure game doesn't run at more than 60 frames per second
            clock.tick(60)
            
            # Process single events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == USEREVENT+1:
                    self.land.update(displs, (displs+self.block_size) % self.land.get_size())
                    changes = True
                    pass
                elif event.type == USEREVENT+2:
                    self.land.move_player()
                    changes = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        self.set_view_mod(64)
                        changes = True
                    elif event.key == K_2:
                        self.set_view_mod(48)
                        changes = True        
                    elif event.key == K_3:
                        self.set_view_mod(32)
                        changes = True    
                    elif event.key == K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        destination = Position(int(event.pos[0]/self.texture_size+displs.x),
                                               int(event.pos[1]/self.texture_size+displs.y))
                        self.land.add_path_to_player(destination)

            # Process continuous events
            key = pygame.key.get_pressed()
            if key[K_RIGHT] or key[K_d]:
                displs.x += speed.x
                displs.x %= self.land.get_size()
                changes = True
            elif key[K_LEFT] or key[K_a]:
                displs.x -= speed.x
                displs.x %= self.land.get_size()
                changes = True
            elif key[K_UP] or key[K_w]:
                displs.y -= speed.y
                displs.y %= self.land.get_size()
                changes = True
            elif key[K_DOWN] or key[K_s]:
                displs.y += speed.y
                displs.y %= self.land.get_size()
                changes = True

            if changes:
                self.redraw(displs)
                self.draw_demo_land_surface(demo_land_surface, displs)
                changes = False

            if self.debug:
                self.draw_debug_window(displs)
                
            pygame.display.update()

    def draw_debug_window(self, displs):
        values = { 'x' : displs.x, 'y' : displs.y }
        font = pygame.font.Font(None, 30)
        text = font.render("Global: x = %(x)d y = %(y)d" % values, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0,0))

        pos = pygame.mouse.get_pos()
        values = { 'x' : pos[0] / self.texture_size + displs.x,
                   'y' : pos[1] / self.texture_size + displs.y }
        font = pygame.font.Font(None, 30)
        text = font.render("Local:   x = %(x)d y = %(y)d" % values, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0, 20))    

        font = pygame.font.Font(None, 30)
        text = font.render("Mode: %d (1-3 to switch)" % self.texture_size, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0, 40))

    def set_view_mod(self, bit):
        self.texture_size = bit
        self.block_size = Position(self.width / self.texture_size, 
                                   self.height / self.texture_size)
        self.load_resources()

    def load_resources(self):
        self.textures_map = TexturesMap('textures.png', self.texture_size).get_map()

    def redraw(self, displs):
        """
        Get necessary image block and
        redraw matrix of LandscapeBlocks' sprites
        """
        for x in range(self.block_size.x):
            for y in range(self.block_size.y):
                val = self.land.value((Position(x,y) + displs) % self.land.get_size())
                lb = sprites.LandscapeBlock(self.screen,
                                            x*self.texture_size,
                                            y*self.texture_size,
                                            self.texture_size,
                                            self.texture_size,
                                            self.textures_map[val])
                lb.draw(self.screen)

    def draw_demo_land_surface(self, surface, displs):
        surface_size = surface.get_width()
        b_surface = pygame.Surface((surface_size, surface_size))
        b_surface.blit(surface, (0, 0))
        
        # draw rectangle to show you current location
        dp = self.demo_land.get_local_pos(displs, surface_size)
        # move window to central
        dp -= self.block_size / 2
        lines = [dp.value(), 
                 (dp + Position(0, self.block_size.y)).value(),
                 (dp + self.block_size).value(),
                 (dp + Position(self.block_size.x, 0)).value()]
        pygame.draw.lines(b_surface, (255, 0, 0), True, lines, 2)
        #############################################

        self.screen.blit(b_surface, (self.width-surface_size-20, 20)) 


    def create_demo_land_surface(self, size):
        demo = self.demo_land.get_demo()
        s = self.demo_land.get_size()
        border = 2
        ds = size / s
        map = pygame.Surface((size, size))
        # just fill the surface
        for x in range(border, s-border):
            for y in range(border, s-border):
                color = pygame.Color(items['colors'][demo[x][y]])
                pygame.draw.rect(map, color, pygame.Rect(x*ds, y*ds, ds, ds))
        return map


##################################################
# define constants
##################################################
# the approximate size of the map you want (should be large than size of main screen)
# I will try to think how to fix it later
size = 2000
# (change view) roughness, more biggest value will give more filled map
roughness = 20.0
# (change map ) you can think about seed as map number or id
land_id = 1233215
##################################################

def start(fullscreen_option=True, debug_option=False):
    # init map generator
    map_generator = MapGenerator.DiamondSquare(size, roughness, land_id, True)

    # init land
    land = Land(map_generator)

    # create window
    MainWindow = Main(land, (1024, 768), debug_option)
    MainWindow.set_full_screen(fullscreen_option)

    # starting the main loop / game
    MainWindow.main_loop()

if __name__ == "__main__":
    # command line flags:
    #   [-f] fullscreen mode on
    #   [-w] window mode on
    #   [-d] debug mode on

    fullscreen_option = True
    debug_option = True # Actually False as default, but who cares

    argv = sys.argv
    for arg in argv:
        if arg == "-d":
            debug_option = True
        elif arg == "-f":
            fullscreen_option = True
        elif arg == "-w":
            fullscreen_option = False

    start(fullscreen_option, debug_option)