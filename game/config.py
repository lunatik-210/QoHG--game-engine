##################################################
# Tcp setting
##################################################
HOST = 'localhost'
PORT = 29877   #our port from before
ADDR = (HOST, PORT)
BUFSIZE = 2048
##################################################

##################################################
# types of objects
##################################################
objects = {
    'water' : 0,
    'sand'  : 1,
    'grass' : 2,
    'log'   : 3,
    'stone' : 4,
    'tree'  : 5,
    'snow'  : 6,
}

monsters = {
    'wolf'  : 11,
    'pig'   : 12,
    'golem' : 13    
}

player_id = 10

##################################################
# colors for mini/demo map
# id - color
##################################################
colors = {
    objects['water']  : 'Blue',
    objects['sand']   : 'Yellow',
    objects['grass']  : 'Black',
    objects['log']    : 'Brown',
    objects['stone']  : 'Gray',
    objects['tree']   : 'Green',
    objects['snow']   : 'White',
    monsters['wolf']  : 'Black',
    monsters['pig']   : 'Black',
    monsters['golem'] : 'Black',
    player_id         : 'Black'
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
humidity = (((0.00, 0.50), bioms['prairie']   ),
            ((0.50, 0.65), bioms['mountains'] ),
            ((0.65, 0.80), bioms['taiga']     ),
            ((0.80, 0.90), bioms['swamp']     ),
            ((0.90, 1.00), bioms['desert']    ))

##################################################
# Determine hight map for every biom 
##################################################
taiga = { 'objects' : (((0.00, 0.58), objects['water'] ),
                       ((0.58, 0.60), objects['sand']  ),
                       ((0.60, 0.62), objects['grass'] ),
                       ((0.62, 0.64), objects['tree']  ),
                       ((0.64, 0.78), objects['grass'] ),
                       ((0.78, 0.80), objects['tree']  ),
                       ((0.80, 0.94), objects['grass'] ),
                       ((0.94, 1.00), objects['tree']  )),
         'monsters' : ((0.1, monsters['wolf']),
                       (0.1, monsters['pig']),
                       (0.8, objects['grass'])),
         'default'  : objects['grass']
}

prairie = { 'objects' : (((0.00, 0.58),  objects['water'] ),
                         ((0.58, 0.60),  objects['sand']  ),
                         ((0.60, 0.94),  objects['grass'] ),
                         ((0.94, 1.00),  objects['tree']  )),
          'monsters' : ((0.2, monsters['pig']),
                        (0.8, objects['grass'])),
          'default'  : objects['grass']
}

mountains = { 'objects' : (((0.00, 0.58),  objects['water'] ),
                           ((0.58, 0.60),  objects['sand']  ),
                           ((0.60, 0.70),  objects['grass'] ),
                           ((0.70, 0.73),  objects['stone'] ),
                           ((0.73, 0.80),  objects['grass'] ),
                           ((0.80, 0.85),  objects['stone'] ),
                           ((0.85, 0.88),  objects['snow']  ),
                           ((0.88, 0.91),  objects['tree']  ),
                           ((0.91, 0.97),  objects['snow']  ),
                           ((0.97, 1.00),  objects['stone'] )),
             'monsters' : ((0.2, monsters['golem']),
                           (0.8, objects['snow'])),
             'default'  : objects['snow']
}

desert = { 'objects' :  (((0.00, 0.58), objects['water'] ),
                         ((0.58, 0.59), objects['sand']  ),
                         ((0.59, 0.61), objects['grass'] ),
                         ((0.61, 1.00), objects['sand']  )),
           'monsters' : None,
           'default'  : objects['sand']
}        

swamp = { 'objects' : (((0.00, 0.56), objects['water'] ),
                       ((0.56, 0.58), objects['sand']  ),
                       ((0.58, 0.77), objects['grass'] ),
                       ((0.77, 0.79), objects['log']   ),
                       ((0.79, 0.82), objects['tree']  ),
                       ((0.82, 0.94), objects['grass'] ),
                       ((0.94, 0.97), objects['log']   ),
                       ((0.97, 0.98), objects['tree']  ),
                       ((0.98, 1.00), objects['log']   )),
         'monsters' : None,
         'default'  : objects['grass']
}      

##################################################
# Set hight map
##################################################
config = {
    'humidity' : humidity,
    bioms['prairie'] : prairie,
    bioms['mountains'] : mountains,
    bioms['desert'] : desert,
    bioms['swamp'] : swamp,
    bioms['taiga'] : taiga,
    'default' : objects['grass'],
    'monsters' : monsters,
    'objects' : objects,
    'bioms' : bioms
}

allowable_list = (objects['sand'],
                  objects['grass'],
                  objects['snow'])
