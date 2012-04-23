#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Импортируем библиотеку Math
import math
#Импортируем один из пакетов Matplotlib
import pylab
#Импортируем пакет со вспомогательными функциями
from matplotlib import mlab

#Рисуем график функции y = sin(x)
def func (x):
    """
    sin (x)
    """
    return 0.5*math.sin (3.14*x)

def noise(x, y):
    n = x + y * 57
    x = (x<<13) ^ x
    return ( 1.0 - ( (x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

def lin_interpolate(a, b, x):
    return  a*(1-x) + b*x

def cos_interpolate(a, b, x):
    ft = x * 3.1415927
    f = (1 - math.cos(ft)) * .5
    return  a*(1-f) + b*f

def smooth_noise1(x, y):
	corners = ( noise(x-1, y-1)+noise(x+1, y-1)+noise(x-1, y+1)+noise(x+1, y+1) ) / 16
	sides   = ( noise(x-1, y)  +noise(x+1, y)  +noise(x, y-1)  +noise(x, y+1) ) /  8
	center  =  noise(x, y) / 4
	return corners + sides + center

def interpolated_noise_2d(x, y, interpolate):
	integer_X    = int(x)
	fractional_X = x - integer_X
	integer_Y    = int(y)
	fractional_Y = y - integer_Y
	v1 = smooth_noise1(integer_X,     integer_Y)
	v2 = smooth_noise1(integer_X + 1, integer_Y)
	v3 = smooth_noise1(integer_X,     integer_Y + 1)
	v4 = smooth_noise1(integer_X + 1, integer_Y + 1)
	i1 = interpolate(v1 , v2 , fractional_X)
	i2 = interpolate(v3 , v4 , fractional_X)
	return interpolate(i1 , i2 , fractional_Y)

octaves = 6
persistence = 0.2

def perling_noise_2d(x, y):
	total = 0.0
	for i in range(octaves):
		total += interpolated_noise_2d(x * (2**i), y * (2**i), cos_interpolate) * persistence**i
	return total

#Указываем X наименьее и наибольшее
xmin = -40.0
xmax = 40.0

# Шаг между точками
dx = 1

#Создадим список координат по оси 
#X на отрезке [-xmin; xmax], включая концы
xlist = mlab.frange (xmin, xmax, dx)

print xlist

# Вычислим значение функции в заданных точках
ylist = [perling_noise_2d (int(x), int(x)) for x in xlist]

#Нарисуем одномерный график
pylab.plot (xlist, ylist)

#Покажем окно с нарисованным графиком
pylab.show()
