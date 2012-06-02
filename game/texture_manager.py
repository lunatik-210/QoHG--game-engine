import pygame
import os

import config

path = './configs'
items = config.load_items(path+'/items.xml')

class Texture:
    """
    TODO: add documentation
    """
    def __init__(self, file_or_size, x=0, y=0, alpha=False):
        if isinstance(file_or_size, int):
            if alpha:
                self.image = pygame.Surface((file_or_size, file_or_size), flags=pygame.SRCALPHA)
            else:
                self.image = pygame.Surface((file_or_size, file_or_size), flags=pygame.HWSURFACE)
        else:
            if alpha:
                self.image = pygame.image.load(os.path.join("./resources/images/", file_or_size)).convert_alpha()
            else:
                self.image = pygame.image.load(os.path.join("./resources/images/", file_or_size)).convert()

    def copy(self, image, pos=(0, 0)):
        self.image.blit(image, (0, 0), pos)

    def scale(self, size):
         self.image = pygame.transform.scale(self.image, (size, size))

    def draw(self, parent, pos):
        if self.image is not None:
            parent.blit(self.image, pos)


class TexturesMap:
    """
    TODO: add documentation
    """
    max_in_raw, max_in_col = 8, 2
    objects = ['water', 'sand', 'grass', 'swamp', 'stone', 'tree', 'snow', 'sky']
    monsters = ['wolf', 'pig', 'golem', 'player']

    def __init__(self, file, texture_size):
        image = pygame.image.load(os.path.join("./resources/images/", file))
        size = image.get_rect().width / self.max_in_raw # 64px
        self.textures_map = {}

        for i in range(self.max_in_col):
            for j in range(self.max_in_raw):
                texture = Texture(size, alpha=i) # there is trick with i = 0 or 1
                texture.copy(image, (j*size, i*size, size, size))
                if texture_size != size:
                    texture.scale(texture_size)
                if i == 0:
                    try:
                        self.textures_map[items['objects'][self.objects[j]]] = texture
                    except IndexError:
                        break
                elif i == 1:
                    try:
                        self.textures_map[items['monsters'][self.monsters[j]]] = texture
                    except IndexError:
                        break

    def get_map(self):
        return self.textures_map

    def get_texture(self, value):
        return self.textures_map[value]

    def draw(self, parent, value, pos):
        self.textures_map[value].draw(parent, pos)