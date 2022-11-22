from algorithms import *
from animation_api import *
import random
import math
import pickle
import time
import numpy as np
import json
import matplotlib.pyplot as plt


# def CreateSyntheticCircleDataset(n):
#     # Creates a synthetic dataset of n points where all the points lie on the circle
#     # This dataset will NOT be output sensitive
#     S = []
#     for i in range(n):
#         x = -1+2*random.random()
#         y = -1+2*random.random()
#         mag = math.sqrt(x**2 + y**2)
#         S.append(Point(x/mag, y/mag))
#     return S


def CreateCircleDataset(n, h):
    # Creates a synthetic dataset of n points where h points lie on the circle and n-h inside the circle
    # This dataset will be output sensitive if h<<n
    # This dataset will NOT be output sensitive if h=n
    S = []
    scale = math.sqrt(1)
    for i in range(h):
        x = -1+2*random.random()
        y = -1+2*random.random()
        mag = math.sqrt(x**2 + y**2)
        S.append(Point(x*scale/mag, y*scale/mag))
    for i in range(n-h):
        r = 0.99*math.sqrt(random.random())
        angle = random.random()
        x = r*math.cos(2*math.pi*angle)
        y = r*math.sin(2*math.pi*angle)
        S.append(Point(x, y))

    return S

def btbDataset():
    # Real Dataset 1: This dataset contains the locations of the farms where bovine tuberculosis was detected along with the
    # years in which it was detected and the "spoligotype" of the tuberculosis
    S = []
    S9, S12, S15, S20 = [], [], [], []
    with open("btb.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        eval('S'+L[2][i]['spoligotype']+'.append(Point(L[0][i],L[1][i]))')

    (fig, ax) = new_plot()
    plot_points(S9, ax, c="g", wait=0, label = 'spoligotype: 9')
    plot_points(S12, ax, c="b", wait=0, label = 'spoligotype: 12')
    plot_points(S15, ax, c="r", wait=0, label = 'spoligotype: 15')
    plot_points(S20, ax, c="k", wait=0, label = 'spoligotype: 20')
    plt.title("Bovine Tuberculosis Dataset")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.legend(loc="upper left")
    plt.show()

    return S9+S12+S15+S20



def beiDataset():
    # Real Dataset 2: Location of 3605 trees in a tropical rain-forest
    S = []
    with open("bei.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        S.append(Point(L[0][i],L[1][i]))

    (fig, ax) = new_plot()
    plot_points(S, ax, c="g", wait=0)
    plt.title("Beilschmiedia data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()

    return S


def mucosaDataset():
    # Real Dataset 3: Location of two types of cells in the gastric mucosa of a rat
    SECL, Sother = [], []
    with open("mucosa.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        eval('S'+L[2][i]+'.append(Point(L[0][i],L[1][i]))')

    (fig, ax) = new_plot()
    plot_points(SECL, ax, c="g", wait=0, label = 'ECL')
    plot_points(Sother, ax, c="b", wait=0, label='other')
    plt.title("Mucosa data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.legend()
    plt.show()

    return SECL+Sother


def gorillaDataset():
    # Real Dataset 3: Location of nesting sites of Gorillas in National park in Cameron
    S = []
    with open("gorillas.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        S.append(Point(L[0][i], L[1][i]))

    (fig, ax) = new_plot()
    plot_points(S, ax, c="g", wait=0)

    plt.title("Gorilla data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()

    return S



def nbfiresDataset():
    # Real Dataset 3: Records of forest fires provided by New Brunsvick Department of Natural Resources of the fires between 1987
    #                   and 2003
    S = []
    with open("nbfires.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        S.append(Point(L[0][i], L[1][i]))

    (fig, ax) = new_plot()
    plot_points(S, ax, c="g", wait=0)

    plt.title("NBfires data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()

    return S


def saveDataset(filename, data):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle)


def loadDataset(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data


def CalculateAvgTime(whichAlgorithm, n, h, max_iter):
    # whichAlgorithm is a list of name of algorithm functions which we want to do time analysis for
    # h: number of points on the the circle of radius 1
    # n-h: number of points strictly inside the circle of radius 1
    # max_iter: number of iterations to average over

    T = np.zeros((len(whichAlgorithm), max_iter))

    for i in range(max_iter):
        S = CreateCircleDataset(n, h)
        # S = btbDataset()
        # S = beiDataset()
        # S = mucosaDataset()
        print('iter = ', i)
        for j in range(len(whichAlgorithm)):
            start = time.time()
            eval(whichAlgorithm[j]+'(S)')
            end = time.time()
            T[j, i] = end-start

    return np.mean(T, axis=1)


if __name__ == '__main__':

    # whichAlgorithm = ['divideConquer_unsorted', 'jarvis', 'andrew', 'quickhull', 'chan']
    # T = CalculateAvgTime(whichAlgorithm, 1000, 3, 1)
    # print(T)



    # Example of using save and load functionality
    # S = CreateCircleDataset(10000,100)
    # saveDataset('myData', S)
    # SS = loadDataset('myData')
    # scttr(SS)


    # S = mucosaDataset()
    S = nbfiresDataset()





