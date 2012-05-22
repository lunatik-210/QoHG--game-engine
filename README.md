Last demonstration video: http://youtu.be/Pd6z6RKmlXk

Prerequirements:
----------
Already used:
* lxml (sudo easy_install lxml)
* PyGame lib
* numpy lib

Soon:
* PGU (PyGame Gui) lib

Interesting links:
----------
* Awesome GameEngine - based on PyGame (book as addition plus avaliable on site) http://www.aharrisbooks.net/pythonGame/
* stackless used in EVE online (simple thread lib) http://zope.stackless.com/
* Texturing sprites by using displacement map http://habrahabr.ru/post/117420/
* «diamond-square» to build fractal landscape http://habrahabr.ru/post/111538/
* Minecraft world generator creation http://habrahabr.ru/post/125621/
* A* search http://en.wikipedia.org/wiki/A*_search_algorithm
* Perling noise http://freespace.virgin.net/hugo.elias/models/m_perlin.htm

20.05.2012
----------
###Done:
* Added Textures Map class: removed all images files except one - textures.png, size converter is in the Texture class

24.04.2012
----------
###Done:
* Tryed Perling noise for map generation, but it turns out DemondSquare is better
* Added bioms: prairie, mountains, desert, swamp, taiga
* Monsters connected to their specific biom
* We've started work on TCP/IP protocol and there are already some great results
* And new Video =) (http://youtu.be/Pd6z6RKmlXk)

###Plans:
* Refactoring, again and again =(
* pythonGame, try to use it
* Do some menu
* Upgrdae tcp/ip protocol
* Merge our repositories

14.04.2012
----------
###Done:
* Added player to the map, and you may controll him!!! Cool =)
* I've done a lot of refactoring, now code more readable
* Changed folders
* Added new Video http://youtu.be/DfZdguZGq6w

###Plans:
* Optimize A* path search, player think about the path too much time
* Add fog
* Add multiplayer mode
* Think about GUI (PyGameGui - is a proper solution)
* Network, we need network ASAP

12.04.2012
----------
###Done:
* Implemented A* algorithm to be able move player around the map by optimal path
* Added small map to right top angle to be able to navigate, enjoy!! =)

###Plans:
* Connect all together (A*, Player movement)
* Tune map generation alghorintm to build cool mountains, forest etc
* Develop proper random starting point player generator/ Monsters generator
* Add FOG to the map >_>
* A lot of Refactoring have to be done, becouse the code now dont understandalbe =(

07.04.2012
----------

###Done:
* Added monster to the map, and made them to move stochastically (amazing -_-")
* Tried first sample about TCP in python
* Added viedo to YouTube http://youtu.be/jfgvRmdfA6w

###Plans:
* Made some AI about monsters
* Try to add a Single Player


04.04.2012
----------

###Done:
* Added debug information about current global/location on the screen (x,y)
* Developed hash map (see land class)

> I think we can develop small map later >_>

###Plans/Tasks:
* Start thinking about initial game engine (Player, Buildings, Textures)

> We shouldn't forget about multiplayer


01.04.2012
----------

###Done:

* Implemented diamond-square alghoritm for map generation
* Developed first visualizator based on PyGame engine
* Added very funny sprites (thanks sagod ~_~)
* Added first vision of game architecture (see docs folder)

###Plans/Tasks:

* Add debug information about current location on the screen (x,y)
* Develop small map
* Implement first version of class GameEngine with some hash map optimization

> Comment: After some thought i've decided implement hashing in separate class named Land
> and I'm amazed because it turns out that map hashing gives some performance and it now moves faster across the map

