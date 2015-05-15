.. _install

.. include:: references.txt

===================
Installing `rootpy`
===================

Requirements
------------

* Python 2.6 or 2.7 (Python 3 is currently not supported, but see
  `this issue <https://github.com/rootpy/rootpy/issues/35>`_ for progress)

* `setuptools`_ 0.7 or newer

* `ROOT`_ 5.28+ with `PyROOT`_ enabled

The following dependencies are optional:

* `NumPy`_ and `root_numpy`_ for speed
* `matplotlib`_ for plotting
* `PyTables`_ for HDF5 IO in rootpy.root2hdf5
* `readline <http://docs.python.org/library/readline.html>`_ and
  `termcolor <http://pypi.python.org/pypi/termcolor>`_ for roosh

rootpy is developed and tested on Linux and Mac.

..
   NumPy: which min version? List all places required in rootpy.
   matplotlib: which min version? List all places required in rootpy.

Getting the Latest Source
-------------------------

Clone the repository with git::

    git clone git://github.com/rootpy/rootpy.git

or checkout with svn::

    svn checkout https://github.com/rootpy/rootpy/trunk rootpy

Manual Installation
-------------------

If you have obtained a copy of `rootpy` yourself use the ``setup.py``
script to install.

To install in your `home directory
<http://www.python.org/dev/peps/pep-0370/>`_::

    python setup.py install --user

To install system-wide (requires root privileges)::

    sudo python setup.py install

To install optional requirements (`matplotlib`_, `NumPy`_, etc.)::

    pip install -U -r requirements/[roosh|array|...].txt

Automatic Installation
----------------------

To install a `released version <http://pypi.python.org/pypi/rootpy/>`_ of
`rootpy` use `pip <http://pypi.python.org/pypi/pip>`_.

.. note:: This will install the latest version of rootpy on PyPI which may be
   lacking many new unreleased features.

To install in your `home directory
<http://www.python.org/dev/peps/pep-0370/>`_::

    pip install --user rootpy

To install system-wide (requires root privileges)::

    sudo pip install rootpy

To install optional requirements (`matplotlib`_, `NumPy`_, etc.)::

    pip install --user rootpy[array,matplotlib,...]

This requires
`pip version 1.1 <http://www.pip-installer.org/en/latest/news.html#id3>`_
or later.

Post-Installation
-----------------

If you installed `rootpy` into your home directory with the `--user` option
above, add ``${HOME}/.local/bin`` to your ``${PATH}`` if it is not there
already (put this in your .bashrc)::

   export PATH=${HOME}/.local/bin${PATH:+:$PATH}

