from numpy import array

from line import *

class TriCell(object):
    """
    classdoc TriCell

    variables:
        self.id = MAX_CELL_ID
        self.nodes = nodes
        self.edges = []

    methods:
        def __init__(self, nodes)
        def __str__(self)
        def __repr__(self)
        def getNodes(self)
        def getEdges(self)
        def getPos(self, x1,x2,x3)
        def getPath(self)

    """

    MAX_CELL_ID = -1    # class variable

    def __init__(self, nodes):
        TriCell.MAX_CELL_ID += 1
        self.id = TriCell.MAX_CELL_ID
        self.nodes = nodes

        edge1 = Line()
        edge1.setNodes(nodes[0],nodes[1])

        edge2 = Line()
        edge2.setNodes(nodes[1],nodes[2])

        edge3 = Line()
        edge3.setNodes(nodes[2],nodes[0])

        self.edges = [edge1, edge2, edge3]

    def __str__(self):
        return "TriCell(nodes={})".format(self.nodes)

    def __repr__(self):
        return "TriCell(nodes={})".format(self.nodes)

    def getNodes(self):
        return self.nodes

    def getEdges(self):
        return self.edges

    def getPos(self, x1,x2,x3):
        # check if coordinates are valid
        if (abs(1.0 - x1 - x2 - x3) > 1.0e-14):
            raise AssertionError("sum of triangular coordinates must be 1.0")

        if (len(self.nodes) == 3):
            x  = x1 * self.nodes[0].getPos()
            x += x2 * self.nodes[1].getPos()
            x += x3 * self.nodes[2].getPos()
        else:
            raise AssertionError("TriCell needs 3 nodes")

        return x

    def getPath(self):
        if (len(self.nodes) != 0):
            raise AssertionError("TriCell needs 3 nodes")

        x = []
        y = []

        for node in self.nodes:
            x.append(node.getX())
            y.append(node.getY())

        x.append(self.nodes[0].getX())
        y.append(self.nodes[0].getY())

        return (array(x), array(y))

