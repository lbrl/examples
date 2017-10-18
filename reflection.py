#! /usr/bin/env python

# from ROOT import RooFit as rf
import ROOT as r
import random
import math

def get_point():
    fun = r.TF1('fun', 'gaus(0)', -60, 60)
    fun.SetParameters(1, 0, 15)
    y = fun.GetRandom()
    return [0., y]

def get_direction():
    alpha = math.pi*(random.random()-.5)
    # print 'alpha', alpha
    return [math.cos(alpha), math.sin(alpha)]

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
    # beta = 5.*math.pi/4.
    beta = math.pi/4.
    # beta = math.pi
    # n = [-1./2**.5, -1./2**.5]
    # t = [1./2**.5, -1./2**.5]
    # pn = p[0]*n[0] + p[1]*n[1]
    # pt = p[0]*t[0] + p[1]*t[1]
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

def propogate22(x, p):
    return propogate(x, p, [60., -120.], [180., -120.])
    B = [0., 0.]
    B[0] = 1.
    k = p[1] / p[0]
    B[1] = x[1] + k
    C = [60., -120.]
    D = [180., -120.]
    IP = line_intersection((x, B), (C, D))
    return [IP[0], IP[1]]

def propogate11(x, p):
    return propogate(x, p, [120., 0.], [140., -20.])
    B = [0., 0.]
    B[0] = 1.
    k = p[1] / p[0]
    B[1] = x[1] + k
    C = [120., 0.]
    D = [140., -20.]
    IP = line_intersection((x, B), (C, D))
    return [IP[0], IP[1]]

def main():
    isDrawRays = True
    isDrawRays = False
    D = 48.# Lens' diameter.
    csi = [50., -60., 50., 60.]
    dx = 60*2**-.5
    mirror = [120-dx, dx, 120+dx, -dx]
    lens = [120-D/2, -120., 120+D/2, -120.]
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    c1.DrawFrame(-50, -150, 250, 150)
    c1.SetGrid()
    # frame = r.TFrame(-1e3, -1e3, 1e3, 1e3)
    # frame.Draw()
    hx = r.TH1D('hx', 'hx', 100, -60, 60)
    hy_x = r.TH1D('hy_x', 'hy_x', 100, -60, 60)
    hz = r.TH1D('hz', 'hz', 100, -60, 60)
    line = r.TLine()
    line.SetLineColor(r.kBlack)
    line.SetLineStyle(1)
    line.SetLineWidth(3)
    line.DrawLine(csi[0], csi[1], csi[2], csi[3])
    line.DrawLine(mirror[0], mirror[1], mirror[2], mirror[3])
    line.DrawLine(lens[0], lens[1], lens[2], lens[3])
    for i in xrange(100000):
        x = get_point()
        p = get_direction()
        y = propogate11(x, p)
        if y[1] < min(mirror[1], mirror[3]):
            continue
        if y[1] > max(mirror[1], mirror[3]):
            continue
        k = reflect(p)
        z = propogate22(y, k)
        #############
        hx.Fill(x[1])
        hy_x.Fill(y[0]-120)
        hz.Fill(z[0]-120)
        #############
        if isDrawRays:
            line.SetLineColor(r.kRed)
            line.SetLineStyle(1)
            line.SetLineWidth(1)
            line.DrawLine(x[0], x[1], y[0], y[1])
            ####
            line.SetLineColor(r.kBlue)
            line.SetLineStyle(2)
            line.SetLineWidth(3)
            line.DrawLine(y[0], y[1], z[0], z[1])
            ####
            line.SetLineColor(r.kGreen+2)
            line.SetLineStyle(1)
            line.SetLineWidth(4)
            line.DrawLine(y[0], y[1], y[0]+10., y[1]+k[1]/k[0]*10.)
    c1.Update()
    c2 = r.TCanvas('c2', 'c2', 600, 600)
    hx.SetLineColor(r.kRed)
    hz.SetLineColor(r.kBlue)
    hx.Draw()
    hy_x.Draw('same')
    hz.Draw('same')
    print 'The number of photons reached the lens is %d.' % hz.Integral(hz.FindBin(-D/2), hz.FindBin(D/2))
    c2.Update()
    raw_input()


if __name__ == '__main__':
    # reflect( [1, 0], True )
    # reflect( [1, 1], True )
    # reflect( [0, 1], True )
    # reflect( [0.5504784896318798, 0.8348493471594767], True )
    main()
