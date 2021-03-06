#!/usr/bin/env python

########## System libs ##########
import random
import numpy
import sys
from copy import deepcopy
import os
from log import *
import argparse
#################################

########## PyGame ###############
import pygame
from pygame.locals import *
import sprites
from client import *

if not pygame.font: logging.warning('Warning, fonts disabled')
if not pygame.mixer: logging.warning('Warning, sound disabled')
#################################

########## Game logic ###########
from texture_manager import Texture, TexturesMap

from lands.Position import Position
import config
import engine
#################################

path = './configs'

items = config.load_items(path+'/items.xml')
bioms = config.load_bioms(path+'/bioms.xml', items)
network = config.load_network(path+'/network.xml')

class VirtualLand:
    def __init__(self, size, client):
        self.client = client
        self.size = size
        self.land = numpy.empty((self.size,self.size))
        self.land.fill(items['objects']['sky'])

    def value(self, pos):
        return self.land[pos.x][pos.y]

    def get_size(self):
        return self.size

    def update(self, displs, block_size):
        correct = lambda a: (a+1 if a % 2 else a)
        req = Request(0, '%d,%d,%d,%d' % (displs.x-block_size.x/2,
                                          displs.y-block_size.y/2,
                                          displs.x+correct(block_size.x)/2,
                                          displs.y+correct(block_size.y)/2))
        data = self.client.send_request(req.form_request(),
                                        waite_for_response=True, is_pickle=True)

        for x in range(block_size.x):
            for y in range(block_size.y):
                self.land[x+displs.x][y+displs.y] = data[block_size.y * x + y]

class Main(engine.State):

    def init(self):
        """
        This is the Main Loop of the Game
        """
        # Create the Screen
        self.client = Client(network['addr'], False)

        # init lands
        self.demo_size = 100
        self.demo_land = self.client.send_request(
            Request(1, self.demo_size).form_request(),
            waite_for_response=True, is_pickle=True)

        self.land_size = int(self.client.send_request(Request(type=2).form_request(),
                             waite_for_response=True))

        self.land = VirtualLand(self.land_size, self.client)

        self.__set_view_mod(48)

        # Get random x,y starting location
        self.displs = Position(500, 500)
        ##################################

        # some local variables
        self.changes = True
        
        # speed.x = 1, speed.y = 1
        self.speed = Position(1, 1)
        self.mouse = Position(0, 0)

        ######################
        
        # init demo land surface 
        small_map_size = 200
        self.demo_land_surface = self.__create_demo_land_surface(small_map_size)
        ########################

        self.UPDATEMONSTERS = USEREVENT+1
        self.UPDATEPLAYER = USEREVENT+2

        # set User event to update Monsters
        pygame.time.set_timer(self.UPDATEMONSTERS, 600)
        pygame.time.set_timer(self.UPDATEPLAYER, 150)

    def paint(self):
        if self.changes:
            self.__redraw(self.displs)
            self.__draw_demo_land_surface(self.demo_land_surface, self.displs)
            self.changes = False

        if self.debug:
            self.__draw_debug_window(self.displs)

    def event(self, events):
        """Process single events"""
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == self.UPDATEMONSTERS:
                correct = lambda a: (a+1 if a % 2 else a)
                req = Request(3, '%d,%d,%d,%d' % (self.displs.x-self.block_size.x/2,
                                                  self.displs.y-self.block_size.y/2,
                                                  self.displs.x+correct(self.block_size.x)/2,
                                                  self.displs.y+correct(self.block_size.y)/2))
                self.client.send_request(req.form_request())
                self.changes = True
                pass
            elif event.type == self.UPDATEPLAYER:
                #self.land.move_player()
                #changes = True
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == K_1:
                    self.__set_view_mod(64)
                    self.changes = True
                elif event.key == K_2:
                    self.__set_view_mod(48)
                    self.changes = True        
                elif event.key == K_3:
                    self.__set_view_mod(32)
                    self.changes = True    
                elif event.key == K_ESCAPE:
                    return engine.Quit(self.game, self.debug)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    #destination = Position(
                    #    int(event.pos[0]/self.texture_size+displs.x),
                    #    int(event.pos[1]/self.texture_size+displs.y))
                    #self.land.add_path_to_player(destination)
                    pass

        # Process continuous events
        key = pygame.key.get_pressed()
        if key[K_RIGHT] or key[K_d]:
            self.displs.x += self.speed.x
            self.displs.x %= self.land_size
            self.changes = True
        if key[K_LEFT] or key[K_a]:
            self.displs.x -= self.speed.x
            self.displs.x %= self.land_size
            self.changes = True
        if key[K_UP] or key[K_w]:
            self.displs.y -= self.speed.y
            self.displs.y %= self.land_size
            self.changes = True
        if key[K_DOWN] or key[K_s]:
            self.displs.y += self.speed.y
            self.displs.y %= self.land_size
            self.changes = True

    def __draw_debug_window(self, displs):
        values = { 'x': displs.x, 'y': displs.y }
        font = pygame.font.Font(None, 30)
        text = font.render("Center: x = %(x)d y = %(y)d" % values, True,
                            (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0,0))

        pos = pygame.mouse.get_pos()
        values = { 'x': pos[0]/self.texture_size+displs.x-self.block_size.x/2,
                   'y': pos[1]/self.texture_size+displs.y-self.block_size.y/2 }
        font = pygame.font.Font(None, 30)
        text = font.render("Mouse:   x = %(x)d y = %(y)d" % values, True,
                            (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0, 20))    

        font = pygame.font.Font(None, 30)
        text = font.render("Mode: %d (1-3 to switch)" % self.texture_size,
                            True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (0, 40))

    def __set_view_mod(self, bit):
        width, height = self.screen.get_size()
        self.texture_size = bit
        self.block_size = Position(width/self.texture_size,
                                   height/self.texture_size)
        self.__load_resources()

    def __load_resources(self):
        self.textures_map = TexturesMap('textures.png', self.texture_size).get_map()

    def __redraw(self, displs):
        """
        Get necessary image block and
        redraw matrix of LandscapeBlocks' sprites
        """
        self.land.update(displs, self.block_size)

        for x in range(self.block_size.x):
            for y in range(self.block_size.y):
                val = self.land.value((Position(x,y) + displs) % 
                                           self.land.get_size())
                #val = data[self.block_size.y * x + y]
                lb = sprites.LandscapeBlock(self.screen,
                                            x*self.texture_size,
                                            y*self.texture_size,
                                            self.texture_size,
                                            self.texture_size,
                                            self.textures_map[val])
                lb.draw(self.screen)

    def __draw_demo_land_surface(self, surface, displs):
        surface_size = surface.get_width()
        b_surface = pygame.Surface((surface_size, surface_size))
        b_surface.blit(surface, (0, 0))
        
        # draw rectangle to show you current location
        get_local_pos = lambda global_pos, surface_size: global_pos / (self.land_size/surface_size)
        dp = get_local_pos(displs, surface_size)
        # move window to central
        dp -= self.block_size / 2
        lines = [(dp-self.block_size / 2).value(),
                 (dp + Position(self.block_size.x/2, -self.block_size.y/2)).value(),
                 (dp+self.block_size / 2).value(),
                 (dp + Position(-self.block_size.x/2, self.block_size.y/2)).value()]
        pygame.draw.lines(b_surface, (255, 0, 0), True, lines, 2)
        #############################################

        self.screen.blit(b_surface, (self.screen.get_size()[0]-surface_size-20, 20)) 

    def __create_demo_land_surface(self, size):
        demo = self.demo_land
        s = self.demo_size
        border = 2
        ds = size / s
        map = pygame.Surface((size, size))
        # just fill the surface
        #for x in range(border, s-border):
        #    for y in range(border, s-border):
        for x in range(border, s-border):
            for y in range(border, s-border):
                color = pygame.Color(items['colors'][self.demo_land[x][y]])
                pygame.draw.rect(map, color, pygame.Rect(x*ds, y*ds, ds, ds))
        return map


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-f", "--fullscreen", action="store_true", help="turn on full screen mode")
    parser.add_argument("-d", "--debug", action="store_true", help="turn on debug mode")
    args = parser.parse_args()

    game = engine.Game()
    game.set_full_screen(args.fullscreen)
    game.run(Main(game, args.debug))
