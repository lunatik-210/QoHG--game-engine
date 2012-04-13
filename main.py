#!/usr/bin/env python

import random
import sprites
import sys
import MapGenerator

from land import Land
from land import DemoLand
from land import Position
from copy import deepcopy

from pathsearch import a_star_path_search as get_path

import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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

    def set_full_screen(self):
        modes = pygame.display.list_modes(32)
        if modes:
            pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 32)
        self.width, self.height = modes[0]

    def main_loop(self):
        """
        This is the Main Loop of the Game
        """
        self.set_view_mod(48)

        # Get random x,y starting location
        lsize = self.land.get_size() >> 2
        displs_x = abs(int(random.gauss(lsize, lsize)))
        displs_y = abs(int(random.gauss(lsize, lsize)))

        self.land.set_value(displs_x, displs_y, player_id)
        ##################################

        # some local variables
        changes = True
        
        speed_x = 1
        speed_y = 1

        mouse_x = 0
        mouse_y = 0
        ######################
        
        # init demo land surface 
        small_map_size = 200
        demo_land_surface = self.create_demo_land_surface(small_map_size)
        ########################

        clock = pygame.time.Clock()

        # set User event to update Monsters
        pygame.time.set_timer(USEREVENT+1, 700)
        while 1:
            # Make sure game doesn't run at more than 60 frames per second
            clock.tick(30)
            
            """Process single events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == USEREVENT+1:
                    self.land.update( displs_x, displs_y, 
                                     (displs_x+self.block_size_x) % self.land.get_size(), 
                                     (displs_y+self.block_size_y) % self.land.get_size() )
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
                    if event.button == 1:
                        mouse_x = int(event.pos[0]/self.texture_size + displs_x)
                        mouse_y = int(event.pos[1]/self.texture_size + displs_y)
                    if event.button == 3:
                        dx = int(event.pos[0]/self.texture_size + displs_x)
                        dy = int(event.pos[1]/self.texture_size + displs_y)
                        # now you may see debug information about the path
                        print get_path(Position(mouse_x, mouse_y), Position(dx, dy), self.land.get_land(), 2)


            """Process continuous events"""
            key = pygame.key.get_pressed()
            if key[K_RIGHT] or key[K_d]:
                displs_x += speed_x
                displs_x %= self.land.get_size()
                changes = True
            elif key[K_LEFT] or key[K_a]:
                displs_x -= speed_x
                displs_x %= self.land.get_size()
                changes = True
            elif key[K_UP] or key[K_w]:
                displs_y -= speed_y
                displs_y %= self.land.get_size()
                changes = True
            elif key[K_DOWN] or key[K_s]:
                displs_y += speed_y
                displs_y %= self.land.get_size()
                changes = True

            if changes:
                self.redraw(displs_x, displs_y)
                self.draw_demo_land_surface(demo_land_surface, displs_x, displs_y)
                changes = False

            if self.debug:
                self.draw_debug_window(displs_x, displs_y)
                
            pygame.display.update()


    def draw_debug_window(self, displs_x, displs_y):
        values = { 'x' : displs_x, 'y' : displs_y }
        font = pygame.font.Font(None, 30)
        text = font.render("Global: x = %(x)d y = %(y)d" % values, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0,0))

        pos = pygame.mouse.get_pos()
        values = { 'x' : pos[0]/self.texture_size + displs_x, 'y' : pos[1]/self.texture_size + displs_y }
        font = pygame.font.Font(None, 30)
        text = font.render("Local:   x = %(x)d y = %(y)d" % values, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0,20))    

        font = pygame.font.Font(None, 30)
        text = font.render("Mode: %d (1-3 to switch)" % self.texture_size, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0, 40))

    def set_view_mod(self, bit):
        self.texture_size = bit
        self.block_size_x = self.width / self.texture_size
        self.block_size_y = self.height / self.texture_size
        self.load_resources()

    def load_resources(self):
        suffix = "_"
        img_sand  = self.load_image("sand%s%d.png"  % (suffix, self.texture_size))
        img_tree  = self.load_image("tree%s%d.png"  % (suffix, self.texture_size))
        img_grass = self.load_image("grass%s%d.png" % (suffix, self.texture_size))
        img_log   = self.load_image("log%s%d.png"   % (suffix, self.texture_size))
        img_stone = self.load_image("stone%s%d.png" % (suffix, self.texture_size))
        img_water = self.load_image("water%s%d.png" % (suffix, self.texture_size))

        img_wolf = self.load_image("wolf%s%dr.png"   % (suffix, self.texture_size))
        img_pig = self.load_image("pig%dr.png" % self.texture_size)
        img_player = self.load_image("player%d.png" % self.texture_size)
        
        self.img_blocks = { heights['water'][1] : img_water,
                            heights['sand'][1]  : img_sand,
                            heights['grass'][1] : img_grass,
                            heights['log'][1]   : img_log,
                            heights['stone'][1] : img_stone,
                            heights['tree'][1]  : img_tree,
                            monsters['wolf'][0] : img_wolf,
                            monsters['pig'][0]  : img_pig,
                            player_id : img_player }
                
    def load_image(self, name):
        img_resources = "./images/"
        return pygame.image.load(img_resources + name).convert()

    def redraw(self, displs_x, displs_y):
        """
        Get necessary image block and
        redraw matrix of LandscapeBlocks' sprites
        """
        for x in range(self.block_size_x):
            for y in range(self.block_size_y):
                val = self.land.value((x+displs_x)%self.land.get_size(), (y+displs_y)%self.land.get_size())
                lb = sprites.LandscapeBlock(self.screen,
                                            x*self.texture_size,
                                            y*self.texture_size,
                                            self.texture_size,
                                            self.texture_size,
                                            self.img_blocks[val])
                lb.draw(self.screen)

    def draw_demo_land_surface(self, surface, displs_x, displs_y):
        surface_size = surface.get_width()
        b_surface = pygame.Surface((surface_size, surface_size))
        b_surface.blit(surface,(0,0))
        
        # draw rectangle to show you current location
        dp = self.demo_land.get_local_pos(Position(displs_x,displs_y), surface_size)
        # move window to central
        dp -= Position(self.block_size_x/2, self.block_size_y/2)
        lines = [(0+dp.x,0+dp.y), 
                 (0+dp.x,self.block_size_y+dp.y), 
                 (self.block_size_x+dp.x,self.block_size_y+dp.y), 
                 (self.block_size_x+dp.x,0+dp.y)]
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
                pygame.draw.rect(map, color, pygame.Rect(x * ds, y * ds, ds, ds))
        return map

if __name__ == "__main__":
    # the approximate size of the map you want (should be large than size of main screen)
    # I will try to think how to fix it later
    size = 1000
    # (change view) roughness, more biggest value will give more filled map
    roughness = 15.0
    # (change map ) you can think about seed as map number or id
    land_id = 1231123213123
    
    # water, sand, grass    
    #land_heights = [0, 0.55, 0.60, 1]

    # log, stone, tree
    #objects_heights = [0.948, 0.949,  0.95, 1]

    # water, sand, grass, log, stone, tree
    heights = {
        'water' : [[0, 0.58],     0],
        'sand'  : [[0.58, 0.60],  1],
        'grass' : [[0.60, 0.948], 2],
        'log'   : [[0.948, 0.949],3],
        'stone' : [[0.949,  0.95],4],
        'tree'  : [[0.95, 1],     5],
    }
    colors = {
        0 : 'Blue',
        1 : 'Yellow',
        2 : 'Black',
        3 : 'Brown',
        4 : 'Gray',
        5 : 'Green',
        10: 'Black',
        11 : 'Black',
        12 : 'Black',
    }
    # [monster_id, probability]
    # wolf, pig
    monsters = { 
        'wolf' : [11, 0.2],
        'pig'  : [12, 0.2]
    }

    player_id = 10

    # grass area
    grass_area = [0.8, 0.9]

    map_generator = MapGenerator.DiamondSquare(size, roughness, land_id, True)

    land = Land(heights, monsters, grass_area, map_generator)

    MainWindow = Main(land, 1024, 768, True)
    MainWindow.set_full_screen()
    MainWindow.main_loop()
