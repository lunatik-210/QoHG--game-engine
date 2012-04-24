#!/usr/bin/env python

########## System libs ##########
import random
import sys
from copy import deepcopy
#################################

######### PyGame ################
import pygame
from pygame.locals import *
import sprites

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
#################################

######### Game logic ############
import lands.generators.Map as MapGenerator

from lands.Land import Land
from lands.DemoLand import DemoLand
from lands.Position import Position

#from pathsearch import a_star_path_search as get_path
#################################


class Main:
    """
    The Main Class - This class handles the main 
    initialization and creating of the Game.
    """
    
    def __init__(self, land, width=1024, height=768, debug=False):
        # Initialize PyGame
        pygame.init()

        # init lands
        self.land = land
        self.demo_land = DemoLand(land, 100)

        # Create the Screen
        self.screen = pygame.display.set_mode((width, height))
        self.width, self.height = width, height
        self.debug = debug

    def set_full_screen(self, fullscreen_option):
        modes = pygame.display.list_modes(32)
        if modes and fullscreen_option:
            pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 32)
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
            
            """Process single events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == USEREVENT+1:
                    self.land.update(displs, (displs+self.block_size) % self.land.get_size())
                    changes = True
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

            """Process continuous events"""
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
        suffix = "_"
        img_sand  = self.load_image("sand%s%d.png"  % ('__', self.texture_size))
        img_tree  = self.load_image("tree%s%d.png"  % (suffix, self.texture_size))
        img_grass = self.load_image("grass%s%d.png" % ('__',self.texture_size))
        img_log   = self.load_image("log%s%d.png"   % (suffix, self.texture_size))
        img_stone = self.load_image("stone%s%d.png" % (suffix, self.texture_size))
        img_water = self.load_image("water%s%d.png" % ('__',self.texture_size))

        img_wolf   = self.load_image("wolf%s%dr.png" % (suffix, self.texture_size))
        img_pig    = self.load_image_with_alpha("pig%s%dr.png"  % ('', self.texture_size))
        img_player = self.load_image_with_alpha("player%s%d.png" % (suffix, self.texture_size))
        
        self.img_blocks = { objects['water']    : img_water,
                            objects['sand']     : img_sand,
                            objects['grass']    : img_grass,
                            objects['log']      : img_log,
                            objects['stone']    : img_stone,
                            objects['tree']     : img_tree,
                            monsters['wolf'][0] : img_wolf,
                            monsters['pig'][0]  : img_pig,
                            player_id : img_player }
                
    def load_image(self, name):
        img_resources = "./resources/images/"
        return pygame.image.load(img_resources + name).convert()

    def load_image_with_alpha(self, name):
        img_resources = "./resources/images/"
        return pygame.image.load(img_resources + name).convert_alpha()

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
                                            self.img_blocks[val])
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
                color = pygame.Color(colors[demo[x][y]])
                pygame.draw.rect(map, color, pygame.Rect(x*ds, y*ds, ds, ds))
        return map


##################################################
# types of objects
##################################################
objects = {
    'water' : 0,
    'sand'  : 1,
    'grass' : 2,
    'log'   : 3,
    'stone' : 4,
    'tree'  : 5
}

monsters = { 
    'wolf' :  [11, 0.2],
    'pig'  :  [12, 0.3],
    'grass' : [2,  0.5]
}

grass_area = [0.8, 0.81]

player_id = 10

##################################################
# colors for mini/demo map
# id - color
##################################################
colors = {
    objects['water']    : 'Blue',
    objects['sand']     : 'Yellow',
    objects['grass']    : 'Black',
    objects['log']      : 'Brown',
    objects['stone']    : 'Gray',
    objects['tree']     : 'Green',
    monsters['wolf'][0] : 'Black',
    monsters['pig'][0]  : 'Black',
    player_id           : 'Black',
}

#################################################
# types of bioms (areas)
##################################################
bioms = {
    'prairie'   : 0,
    'mountains' : 1,
    'desert'    : 2,
    'swamp'     : 3,
    'taiga'     : 4
}

##################################################
# determine hight map for bioms
##################################################
humidity = (((0.0, 0.50),  bioms['prairie']   ),
            ((0.50, 0.65), bioms['mountains'] ),
            ((0.65, 0.80), bioms['taiga']     ),
            ((0.80, 0.90), bioms['swamp']     ),
            ((0.90, 1.0),  bioms['desert']    ))

##################################################
# Determine hight map for every biom 
##################################################
taiga = (((0.00, 0.58), objects['water'] ),
         ((0.58, 0.60), objects['sand']  ),
         ((0.60, 0.62), objects['grass'] ),
         ((0.62, 0.64), objects['tree']  ),
         ((0.64, 0.78), objects['grass'] ),
         ((0.78, 0.80), objects['tree']  ),
         ((0.80, 0.94), objects['grass'] ),
         ((0.94, 1.00), objects['tree']  ))

prairie = (((0.00, 0.58),  objects['water'] ),
           ((0.58, 0.60),  objects['sand']  ),
           ((0.60, 0.94),  objects['grass'] ),
           ((0.94, 1.00),  objects['tree']  ))

mountains = (((0.00, 0.58),  objects['water'] ),
             ((0.58, 0.60),  objects['sand']  ),
             ((0.60, 0.70),  objects['grass'] ),
             ((0.70, 0.73),  objects['stone'] ),
             ((0.73, 0.80),  objects['grass'] ),
             ((0.80, 0.85),  objects['stone'] ),
             ((0.85, 0.88),  objects['grass'] ),
             ((0.88, 0.91),  objects['tree'] ),
             ((0.91, 0.97),  objects['grass'] ),
             ((0.97, 1.00),  objects['stone'] ))

desert = (((0.00, 0.58), objects['water'] ),
          ((0.58, 0.59), objects['sand']  ),
          ((0.59, 0.61), objects['grass'] ),
          ((0.64, 1.00), objects['sand']  ))

swamp = (((0.00, 0.56), objects['water'] ),
         ((0.56, 0.58), objects['sand']  ),
         ((0.58, 0.77), objects['grass'] ),
         ((0.77, 0.79), objects['log']   ),
         ((0.79, 0.82), objects['tree']  ),
         ((0.82, 0.94), objects['grass'] ),
         ((0.94, 0.97), objects['log']   ),
         ((0.97, 0.98), objects['tree']  ),
         ((0.98, 1.0),  objects['log']   ))

##################################################
# Set hight map
##################################################
heights = {
    'humidity' : humidity,
    bioms['prairie'] : prairie,
    bioms['mountains'] : mountains,
    bioms['desert'] : desert,
    bioms['swamp'] : swamp,
    bioms['taiga'] : taiga,
    'default' : objects['grass']
}

##################################################
# define constants
##################################################
# the approximate size of the map you want (should be large than size of main screen)
# I will try to think how to fix it later
size = 1000
# (change view) roughness, more biggest value will give more filled map
roughness = 20.0
# (change map ) you can think about seed as map number or id
land_id = 1233213
##################################################

def start(fullscreen_option=True, debug_option=False):
    # init map generator
    map_generator = MapGenerator.DiamondSquare(size, roughness, land_id, True)

    # init land
    land = Land(heights, monsters, player_id, grass_area, map_generator)

    # create window
    MainWindow = Main(land, 1024, 768, debug_option)
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