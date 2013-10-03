# -*- coding: utf-8 -*-
#
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
Scientific Python startup script

Requires NumPy, SciPy and Matplotlib
"""

# Need a temporary print function that is Python version agnostic.
import sys

def exec_print(string="", end_space=False):
    if sys.version[0] == '2':
        if end_space:
            exec("print '" + string + "',")
        else:
            exec("print '" + string + "'")
    else:
        if end_space:
            exec("print('" + string + "', end=' ')")
        else:
            exec("print('" + string + "')")

has_numpy = True
has_scipy = True
has_matplotlib = True

#==============================================================================
# Pollute the namespace but also provide MATLAB-like experience
#==============================================================================
try:
    from pylab import *  #analysis:ignore
    # Enable Matplotlib's interactive mode:
    ion()
except ImportError:
    pass

# Import modules following official guidelines:
try:
    import numpy as np
except ImportError:
    has_numpy = False

try:
    import scipy as sp
except ImportError:
    has_scipy = False

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt  #analysis:ignore
except ImportError:
    has_matplotlib = False

#==============================================================================
# Print what modules have been imported
#==============================================================================
imports = ""
if has_numpy:
    imports += "Imported NumPy %s" % np.__version__
if has_scipy:
    imports += ", SciPy %s" % sp.__version__
if has_matplotlib:
    imports += ", Matplotlib %s" % mpl.__version__

exec_print("")
if imports:
    exec_print(imports)

import os
if os.environ.get('QT_API') != 'pyside':
    try:
        import guiqwt
        import guiqwt.pyplot as plt_
        import guidata
        plt_.ion()
        exec_print("+ guidata %s, guiqwt %s" % (guidata.__version__,
                                           guiqwt.__version__))
    except ImportError:
        exec_print()

#==============================================================================
# Add help about the "scientific" command
#==============================================================================
def setscientific():
    """Set 'scientific' in __builtin__"""
    infos = ""
    
    if has_numpy:
        infos += """
This is a standard Python interpreter with preloaded tools for scientific 
computing and visualization. It tries to import the following modules:

>>> import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)"""

    if has_scipy:
        infos += """
>>> import scipy as sp  # SciPy (signal and image processing library)"""

    if has_matplotlib:
        infos += """
>>> import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
>>> import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
>>> from pylab import *              # Matplotlib's pylab interface
>>> ion()                            # Turned on Matplotlib's interactive mode"""
    
    try:
        import guiqwt  #analysis:ignore
        infos += """
>>> import guidata  # GUI generation for easy dataset editing and display

>>> import guiqwt                 # Efficient 2D data-plotting features
>>> import guiqwt.pyplot as plt_  # guiqwt's pyplot: MATLAB-like syntax
>>> plt_.ion()                    # Turned on guiqwt's interactive mode"""
    except ImportError:
        pass
    
    if has_numpy:
        infos += "\n"

    infos += """
Within Spyder, this interpreter also provides:
    * special commands (e.g. %ls, %pwd, %clear)
    * system commands, i.e. all commands starting with '!' are subprocessed
      (e.g. !dir on Windows or !ls on Linux, and so on)
"""
    try:
        # Python 2
        import __builtin__ as builtins
    except ImportError:
        # Python 3
        import builtins
    from site import _Printer
    builtins.scientific = _Printer("scientific", infos)


setscientific()
exec_print('Type "scientific" for more details.')

#==============================================================================
# Delete temp vars
#==============================================================================
del setscientific, has_numpy, has_scipy, has_matplotlib, imports, exec_print
