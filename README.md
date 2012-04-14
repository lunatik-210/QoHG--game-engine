Interesting links:
----------
* Текстурирование спрайтов с помощью (dis)placement map http://habrahabr.ru/post/117420/
* Алгоритм «diamond-square» для построения фрактальных ландшафтов http://habrahabr.ru/post/111538/
* Создание генератора мира для minecraft http://habrahabr.ru/post/125621/
* A* search http://en.wikipedia.org/wiki/A*_search_algorithm
* Perling noise http://freespace.virgin.net/hugo.elias/models/m_perlin.htm

14.04.2012
----------
###Done:
* Added player to the map, and you may controll him!!! Cool =)
* I've done a lot of refactoring, now code more readable
* Changed folders

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

