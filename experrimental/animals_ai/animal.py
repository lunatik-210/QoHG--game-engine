import sys
import random
import numpy
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def distance(a, b):
    return numpy.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

class Entity(object):
    def __init__(self, world, name, color):
        self.world = world
        self.name = name
        self.color = color
        self.x = int(0)
        self.y = int(0)

        self.brain = StateMachine()

    def process(self, time_passed):
        self.brain.think()

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 2)

class State(object):
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass

class StateExploring(State):
    def __init__(self, object):
        State.__init__(self, 'exploring')
        self.object = object

    def do_actions(self):
        generate_step = lambda : random.gauss(0.5, 1)*random.gauss(0.5, 1)
        self.object.x = int((self.object.x + generate_step() ) % self.object.world.height)
        self.object.y = int((self.object.y + generate_step() ) % self.object.world.width)        

    def check_conditions(self):
        for entity in self.object.world.entities:
            if 0 < distance(entity, self.object) < 20:
                return None
        return 'moving'

    def entry_actions(self):
        self.object.x = random.uniform(0, self.object.world.height)
        self.object.y = random.uniform(0, self.object.world.width)

class StateMoving(State):
    def __init__(self, object):
        State.__init__(self, 'moving')
        self.object = object
        self.neighbor = None

    def do_actions(self):
        if self.neighbor is None:
            return
        signx = self.neighbor.x - self.object.x
        signy = self.neighbor.y - self.object.y
        if signx > 0:
            self.object.x += 1
        else: self.object.x -= 1
        if signy > 0:
            self.object.x += 1
        else: self.object.x -= 1       

    def check_conditions(self):
        if self.neighbor is None:
            return 'exploring'

        if 0 <= distance(self.neighbor, self.object) < 10:
            return 'exploring'

        return None

    def entry_actions(self):
        for entity in self.object.world.entities:
            if 11 < distance(entity, self.object) < 70:
                self.neighbor = entity

class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
            print 'New state: ', new_state_name

    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()

class Animal(Entity):
    def __init__(self, world):
        Entity.__init__(self, world, 'Animal', (255,0,0))
        self.health = 100

        exploring_state = StateExploring(self)
        moving_state = StateMoving(self)

        self.brain.add_state(exploring_state)
        self.brain.add_state(moving_state)

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entities = []
        self.entity_id = 0

    def add_entity(self, entity):
        self.entities.append(entity)

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        for entity in self.entities:
            entity.process(time_passed_seconds)

    def render(self, surface):
        for entity in self.entities:
            entity.render(surface)

def run():
    pygame.init()
    width = 1024
    height = 768
    screen = pygame.display.set_mode((width, height))

    world = World(width, height)

    clock = pygame.time.Clock()

    for i in range(30):
        ent = Animal(world)
        ent.brain.set_state('exploring')
        world.add_entity(ent)

    while 1:
        time_passed = clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))
        world.process(time_passed)
        world.render(screen)

        pygame.display.update()         

if __name__ == "__main__":
    run()