#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Conway's Game of Life (
https://zh.wikipedia.org/wiki/%E5%BA%B7%E5%A8%81%E7%94%9F%E5%91%BD%E6%B8%B8%E6%88%8F)
in Python

'''

import numpy as np
import matplotlib.pyplot as plt

from utils import fft_convolve2d
from utils import gen_gif


class World(object):
    '''
    The parent of other world.
    
    These method can be rewrite:
    init_status, update, display
    '''

    def __init__(self, size=(39,39), birth_rate=None):
        self.row = size[0]
        self.col = size[1]
        self.shape = size
        self.birth_rate = birth_rate
        self.init_status()
        
        self._next = self.status.copy()
        self.loop_count = 0


    def init_status(self):
        """
        initialize all celles status.
        """
        self.status = np.random.randint(2, size=self.shape)
        # self.status = np.zeros((self.row, self.col))

    def update(self):
        """
        update celles status.
        """
        self.calc_conv()
                    
        self._next[np.where((self.conv_matrix <  2) & (self.status == 1))] = 0
        self._next[np.where((self.conv_matrix >  3) & (self.status == 1))] = 0
        self._next[np.where((self.conv_matrix == 3) & (self.status == 0))] = 1

        if self.birth_rate:
            rand = np.random.rand(self.row, self.col)
            rand = np.where(rand < self.birth_rate, 1, 0)
            self._next = self._next | rand

        self.loop_count += 1
        self.status = self._next.copy()

    def display(self):
        """
        display all cell.
        """
        print("  " + "="*(self.col) + str(self.loop_count) + "="*(self.col))
        # print(self.status)
        for i in range(self.row):
            line = "|| "
            for j in range(self.col):
                if self.status[i,j]:
                    line += '# '
                else:
                    line += '  '
            line += "||"
            print(line)
        print("  " + "="*(self.col) + "="*len(str(self.loop_count)) + "="*(self.col))


    def calc_conv(self):
        m, n = self.shape
        k = np.zeros(self.shape)
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array(
            [[1,1,1],
             [1,0,1],
             [1,1,1]]) # convolve kernel
        conv = fft_convolve2d(self.status, k).round()
        self.conv_matrix = conv


    def neighbors(self, pos=(0, 0)):
        alive = self.status[pos[0], pos[1]]
        conv = self.conv_matrix
        num_alive_nb = conv[pos[0], pos[1]] - alive
        return num_alive_nb


    def run(self, limit=None, update=None,
             output=True, delay=0.01, display=True):
        """
        run the world.
        :limit: circle number limit
        :output: print current circle number and world population or not
        :delay: circle delay time 
        :display: display world status or not
        """
        c = 0
        while 1:
            c += 1
            if limit and c > limit: break
            if update:
                update()
            else:
                self.update()
            if display:
                self.display()
            if display and delay != 0:
                plt.pause(delay)
            if output:
                print("{}\t{}".format(c, self.population))
    
    @property
    def population(self):
        return self.status.sum()


class WorldGUI(World):
    ''' use matplotlib to display'''
    def __init__(self, size, birth_rate=None):
        super(WorldGUI, self).__init__(size, birth_rate)
        plt.figure()
        self._img_plot = plt.imshow(self.status, interpolation="nearest", cmap = plt.cm.gray)
        plt.show(block=False)

    def display(self):
        self._img_plot.set_data(self.status)
        plt.draw()


def make_a_movie(world, start=0, n=1000):
    """ 
    take a series of status of the world 
    just like make a little movie about this world :)
    """
    photos = []
    for i in range(start):
        world.update()
    for i in range(n):
        photos.append(world.status)
        world.update()
    return photos


if __name__ == '__main__':
    #w = WorldGUI((150, 150), birth_rate=0.0001)
    w = World((150, 150), birth_rate=0.0001)
    images = make_a_movie(w, start=1000, n=100)
    gif_path = "./tmp/conway.gif"
    gen_gif(images, gif_path)
    #w.run(display=False, delay=0)
    #w.run()
