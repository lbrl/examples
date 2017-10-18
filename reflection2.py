#! /usr/bin/env python

# from ROOT import RooFit as rf
import ROOT as r
import random
import math

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
    return [x, y]

def reflect(p, isPrint=False):
    beta = math.pi/4.
    px, py = p[0], p[1]
    pn = px*math.cos(beta) - py*math.sin(beta)
    pt = px*math.sin(beta) + py*math.cos(beta)
    kn = -pn
    kt = pt
    kx = kn*math.cos(-beta) - kt*math.sin(-beta)
    ky = kn*math.sin(-beta) + kt*math.cos(-beta)
    if isPrint:
        print '*'*40
        print 'px = {},  py = {},  |p| = {}'.format(px, py, (px**2+py**2)**.5)
        print 'pn = {},  pt = {},  |p\'| = {}'.format(pn, pt, (pn**2+pt**2)**.5)
        print 'kn = {},  kt = {},  |k\'| = {}'.format(kn, kt, (kn**2+kt**2)**.5)
        print 'kx = {},  ky = {},  |k| = {}'.format(kx, ky, (kx**2+ky**2)**.5)
        print '*'*40
    return [kx, ky]

def propogate(x, p, C, D):
    B = [x[0]+1., 0.]
    k = p[1] / p[0]
    B[1] = x[1] + k
    IP = line_intersection((x, B), (C, D))
    return [IP[0], IP[1]]

def get_intensity(x):
    f = r.TF1('f', 'gausn(0)', -60, 60)
    f.SetParameters(1, 1, 25)
    return f.Eval(x)

def main():
    n = 20
    d = 46.+68.
    D = 48.
    h = r.TH1D('h', 'h', n, 0, 120)
    c2 = r.TCanvas('c2', 'c2', 800, 800)
    c2.DrawFrame(0, -200, 300, 100)
    c2.SetGrid()
    line = r.TLine()
    line.SetLineColor(r.kBlack)
    line.SetLineStyle(1)
    line.SetLineWidth(3)
    # line.DrawLine(0, -60, 0, 60)
    line.DrawLine(50, -60, 50, 60)
    dx = 60*2**-.5
    line.DrawLine(120-dx, dx, 120+dx, -dx)
    line.DrawLine(120-D/2, -180, 120+D/2, -180)
    for i in xrange(n):
        x = (i+.5-n/2.)*D/n
        p = [x, d]
        x += 120.
        y = propogate([x, -180.], p, [120., 0], [140., -20.])
        k = reflect(p)
        # z = propogate(y, k, [0., -60.], [0., 60.])
        z = propogate(y, k, [50., -60.], [50., 60.])
        inten = get_intensity(z[1])
        h.SetBinContent(h.FindBin(z[1]), inten)
        ########################################
        line.SetLineColor(r.kBlue)
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        line.DrawLine(x, -180, y[0], y[1])
        line.SetLineColor(r.kRed)
        line.SetLineStyle(1)
        line.SetLineWidth(1)
        line.DrawLine(y[0], y[1], z[0], z[1])
    c2.Update()
    c1 = r.TCanvas('c1', 'c1', 800, 800)
    h.Draw()
    c1.Update()
    raw_input()


if __name__ == '__main__':
    main()
