.. _plotting:

========
Plotting
========

.. currentmodule:: rootpy.plotting

rootpy provides a more pythonic interface for histograms, graphs, canvases and
plotting styles.

Histograms
==========

rootpy simplifies ROOT's histogram class hierarchy into three classes:
``Hist``, ``Hist2D``, and ``Hist3D``. These classes dynamically inherit from
the corresponding ROOT histogram class depending on the value of the ``type``
keyword argument supplied to the constructor. The ROOT base class is always the
last class in the inheritance list. For example, to create a 2-dimensional
histogram with floating-point bin contents::

   >>> from rootpy.plotting import Hist2D
   >>> hist = Hist2D(10, 0, 1, 5, 0, 1, type='F')
   >>> hist.__class__.__bases__
   (<class 'rootpy.plotting.hist._Hist2D'>, <class 'ROOT.TH2F'>)

``type`` can be any of the type corresponding to the ROOT histogram classes:
``"C"``, ``"S"``, ``"I"``, ``"F"``, ``"D"`` (or lower case)::

   >>> hist = Hist2D(10, 0, 1, 5, 0, 1, type='C')
   >>> hist.__class__.__bases__
   (<class 'rootpy.plotting.hist._Hist2D'>, <class 'ROOT.TH2C'>)
   >>> hist = Hist2D(10, 0, 1, 5, 0, 1, type='D')
   >>> hist.__class__.__bases__
   (<class 'rootpy.plotting.hist._Hist2D'>, <class 'ROOT.TH2D'>)

If ``type`` is not specified the default is to use floating-point bins
(``"F"``).

Notice that the name or title of the histograms were not specified; In rootpy
names and titles are optional. ROOT will complain if you give two objects the
same name::

   >>> import ROOT
   >>> h1 = ROOT.TH1D("a name", "a title", 10, 0, 1)
   >>> h2 = ROOT.TH1D("a name", "a different title", 10, 0, 1)
   TROOT::Append:0: RuntimeWarning: Replacing existing TH1: a name (Potential memory leak).

With rootpy, if the ``name`` keyword argument is not specified in the
constructor, a universally unique identifier (UUID) will be used instead::

   >>> from rootpy.plotting import Hist
   >>> h = Hist(10, 0, 1)
   >>> h.GetName()
   '089163932f454725a9ab108437db9773'
   >>> h.GetTitle()
   ''

This ensures that all objects have unique names by default in rootpy and is
particularly helpful if naming isn't important in your application (since you
don't intend to write the objects in a file, for example). You can, however,
specify a ``name`` or ``title``::

   >>> from rootpy.plotting import Hist
   >>> h = Hist(10, 0, 1, name="some name", title="some title")
   >>> h.GetName()
   'some name'
   >>> h.GetTitle()
   'some title'

The arguments that specify the binning are consumed from left to right as either
three values for the number of bins, left bound, and right bound, or a list for
bins of variable width. Fixed and variable width bins may be mixed for 2D and 3D
histograms:

.. sourcecode:: python

   from rootpy.plotting import Hist, Hist2D, Hist3D
   # 1D histogram with fixed-width bins
   h1d = Hist(5, -2, 4)
   # variable-width bins
   h1d = Hist([-10, -3.2, 5.2, 35.])

   # 2D histogram with fixed-width bins; 10 along x and 5 along y
   h2d = Hist2D(10, 0, 1, 5, -2, 4)
   # 3 variable-width bins along x and 4 fixed-width bins along y
   h2d = Hist2D([10, 30, 100, 1000], 4, 10, 33.5)

   # 3D histogram with fixed-width bins
   h3d = Hist3D(100, 0, 1, 20, 5.8, 7.2, 1e4, -10, 1)
   # fixed-width bins along x and z and variable-width bins along y
   h3d = Hist3D(5, 0, 1, [-20, 5, 50, 1e3], 10, 0, 1)

Any additional keyword arguments are use to set style attributes of the
histogram, such as the line color, fill style, etc.

Slicing
-------

Histogram ``__getitem__`` and ``__setitem__`` methods support slicing by global
bin index or along each axis separately.

Access contents and errors::

   >>> from rootpy.plotting import Hist
   >>> a = Hist(10, 0, 1)
   >>> a[1].value = 2
   >>> a[1].value
   2.0
   >>> a[1].error = 2
   >>> a[1].error
   2.0

``__setitem__`` with a slice and a single value just repeats that value over
the sliced view::

   >>> from rootpy.plotting import Hist3D
   >>> a = Hist3D(10, 0, 1, 10, 0, 1, 10, 0, 1)
   >>> a[:,:,5] = a[40] # set with a BinProxy
   >>> a[:,:,:] = (2, 4) # set content and error with a 2-tuple
   >>> a[:,:,:] = 2 # only set the content

If a single index is requested then a ``BinProxy`` is returned::

   >>> from rootpy.plotting import Hist3D
   >>> a = Hist3D(10, 0, 1, 10, 0, 1, 10, 0, 1)
   >>> a[3,4,8]
   BinProxy(Hist3D('5a8e7fbe8ff54be6be18709220b3da31'), 1203)
   >>> a[3,4,8].value
   1.0
   >>> a[3,6,8].value
   5.0
   >>> a[3,6,8].error
   2.23606797749979
   >>> a[0,5,6].overflow
   True
   >>> a[1,5,6].overflow
   False

If a slice is requested, then a ``HistIndexView`` or ``Hist[2D|3D]View`` is
returned::

   >>> a[:]
   HistIndexView(Hist3D('5a8e7fbe8ff54be6be18709220b3da31'), idx=[start=None, stop=None, step=None])
   >>> a[:,:,:]
   Hist3DView(Hist3D('5a8e7fbe8ff54be6be18709220b3da31'), x=[start=None, stop=None, step=None], y=[start=None, stop=None, step=None], z=[start=None, stop=None, step=None])
   >>> a[:,:,2:5]
   Hist3DView(Hist3D('5a8e7fbe8ff54be6be18709220b3da31'), x=[start=None, stop=None, step=None], y=[start=None, stop=None, step=None], z=[start=2, stop=5, step=None])
   >>> a[:,:,::-1]
   Hist3DView(Hist3D('5a8e7fbe8ff54be6be18709220b3da31'), x=[start=None, stop=None, step=None], y=[start=None, stop=None, step=None], z=[start=None, stop=None, step=-1])

You may iterate over the BinProxies in these views.
You can then construct a new histogram using a view of another. The step member
of a slice translates to a rebinning along the associated axis::

   >>> b = Hist3D(a[3:5,::2,:])
   >>> list(b.xedges())
   [0.2, 0.30000000000000004, 0.4]
   >>> list(b.yedges())
   [0.0, 0.2, 0.4, 0.6000000000000001, 0.8, 1.0]
   >>> list(b.zedges())
   [0.0, 0.1, 0.2, 0.30000000000000004, 0.4, 0.5, 0.6000000000000001, 0.7000000000000001, 0.8, 0.9, 1.0]

For example, to reverse the bin contents and errors::

	>>> from rootpy.plotting import Hist
	>>> a = Hist(10, 0, 1)
	>>> a.FillRandom('gaus')
	>>> a.Draw()
	>>> a[:] = a.Clone(shallow=True)[::-1]
	>>> a.Draw()


Plotting Style
==============

.. warning:: The following documentation is still under construction.

All plottable ROOT classes that are subclassed in rootpy have additional
features that allow styling in new ways:

* style attributes can be accessed or set using properties::

      hist.fillstyle = 'solid'
      color = hist.linecolor

* if matplotlib is installed colors can also be set using hex, RGB tuples, or
  SVG names::

      hist.fillcolor = (32, 178, 170)
      hist.linecolor = '#87cefa'
      hist.markercolor = 'salmon'

* all colors (line, fill, and markers) can be set with one line::

      hist.color = 'red'

