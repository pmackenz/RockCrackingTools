from numpy import array
import numpy as np

from mesh import *
from tricell import *
from line import *
from node import *

import matplotlib.pyplot as plt
import matplotlib.tri as tri


def createmesh(targetlevel=1):
    # create the master mesh
    mesh = Mesh()
    mesh.createmesh(targetlevel)
    return mesh
