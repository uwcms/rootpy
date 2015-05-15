#!/usr/bin/env python
"""
===================================
Fill a histogram with a NumPy array
===================================

This example demonstrates how a 1D, 2D, or 3D ROOT histogram can be efficiently
filled with a NumPy array.
"""
print __doc__
from rootpy.interactive import wait
from rootpy.plotting import Canvas, Hist, Hist2D, Hist3D
from rootpy.plotting.style import set_style
import numpy as np

set_style('ATLAS')

c1 = Canvas()
a = Hist(1000, -5, 5)
a.fill_array(np.random.randn(1000000))
a.Draw('hist')

c2 = Canvas()
c2.SetRightMargin(0.1)
b = Hist2D(100, -5, 5, 100, -5, 5)
b.fill_array(np.random.randn(1000000, 2))
b.Draw('LEGO20')

c3 = Canvas()
c3.SetRightMargin(0.1)
c = Hist3D(10, -5, 5, 10, -5, 5, 10, -5, 5)
c.markersize = .3
c.fill_array(np.random.randn(10000, 3))
c.Draw('SCAT')
wait(True)
