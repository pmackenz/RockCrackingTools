from numpy import array, dot
from scipy import sqrt
from node import *

class DataError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Line(object):
    """
    classdoc Line()

    variables:
       self.id    ... unique integer id
       self.nodes ... list of attached nodes

    methods:
        def __init__(self)
        def __str__(self)
        def __repr__(self)
        def setNode1(self, node)
        def setNode2(self, node)
        def setNodes(self, node1, node2)
        def getMiddleNodePos(self)
    """

    METHOD = 0

    MAX_LINE_ID = -1    # class variable

    def __init__(self, node1=None, node2=None):
        Line.MAX_LINE_ID += 1
        self.id = Line.MAX_LINE_ID
        self.node1 = node1
        self.node2 = node2
        self.nodeM = None   # invalidate center node

    def __str__(self):
        return "Line(id={}, nodes=({},{}))".format(self.id, self.node1, self.node2)

    def __repr__(self):
        return "Line(id={}, nodes=({},{}))".format(self.id, self.node1, self.node2)

    def setNode1(self, node):
        self.node1 = node
        self.nodeM = None   # invalidate center node

    def setNode2(self, node):
        self.node2 = node
        self.nodeM = None   # invalidate center node

    def setNodes(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.nodeM = None   # invalidate center node

    def getMiddleNodePos(self):
        if (not self.nodeM):
            # create middle point node
            if (self.node1 and self.node2):
                # place node at center of straight line from node 1 to node 2
                XM = 0.5 * (self.node1.getPos() + self.node2.getPos())

                if (Line.METHOD == 0):
                    # project node onto unit sphere
                    normXM = sqrt(dot(XM, XM))
                    XM /= normXM
                else:
                    # project node onto unit sphere while preserving z
                    normXM = sqrt(dot(XM[:2], XM[:2]))
                    TargetNormXM = sqrt(1.0 - XM[2]*XM[2])
                    XM[0] *= TargetNormXM/normXM
                    XM[1] *= TargetNormXM/normXM

            else:
                msg = "Line {} has undefined nodes".format(self.id)
                raise DataError(msg)

        return XM

    
