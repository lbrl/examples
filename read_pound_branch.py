#! /usr/bin/env python

import ROOT as r
# import os
# import sys
# import glob
# import math
# import numpy as np
# import array


def main():
    #
    Fin = r.TFile('/home/vvorob/public/tuples/fccedm/dkspipi.root')
    tin = Fin.Get('events')
    #
    for i in xrange(3):
        tin.GetEntry(i)
        print tin.allGenParticles[0].core.pdgId
        for vert in getattr(tin, 'allGenParticles#0'):
            print vert.index
    Fin.Close()

if __name__ == '__main__':
    main()
