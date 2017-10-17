#! /usr/bin/env python

# from ROOT import RooFit as rf
import ROOT as r
import random
import math

def get_point():
    fun = r.TF1('fun', 'gaus(0)', -10, 10)
    fun.SetParameters(1, 0, 1.5)
    x = f.GetRandom()
    return x

def get_direction(x):
    alpha = math.pi*random.random()
    return [math.cos(aplha), math.sin(alpha)]

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def propogate1(x, p):
    B = [0., 0.]
    B[0] = 1.e3 + x[0]
    k = p[1] / p[0]
    B[1] = x[1] + k*(C-x[0])
    C = [40., 40.]
    D = [120., -40.]
    IP = line_intersection((x, B), (C, D))
    return [IP[0], IP[1]]

def reflect(p):
    n = [-1./2**.5, -1./2**.5]
    t = [1./2**.5, -1./2**.5]
    pn = p[0]*n[0] + p[1]*n[1]
    pt = p[0]*t[0] + p[1]*t[1]
    kx = pn*n[0] + pt*t[0]
    ky = pn*n[1] + pt*t[1]
    return [kx, ky]

def propogate2(x, p):
    B = [0., 0.]
    B[0] = 1.e3 + x[0]
    k = p[1] / p[0]
    B[1] = x[1] + k*(C-x[0])
    C = [40., 40.]
    D = [120., -40.]
    IP = line_intersection((x, B), (C, D))
    return [IP[0], IP[1]]

def main():
    x = get_point()
    p = get_direction()
    y = propogate(x, p)
    k = reflect(p)
    z = catch(k)


if __name__ == '__main__':
    main()
