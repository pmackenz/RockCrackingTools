from numpy import array, dot, cross, arccos, rad2deg

from tricell import *
from line import *
from node import *



class Mesh(object):
    """
    :class: Mesh

    variables:
        self.points = []
        self.triangles = []
        self.nodes = []
        self.cells = []
        self.level = -1
        self.data  = []

    methods:
        def __init__(self)
        def __str__(self)
        def __repr__(self)
        def createmesh(self, targetlevel=1)
        def clearAll(self)
        def clearGrid(self)
        def addPoint(self, node)
        def addNode(self, node)
        def addTriangle(self, nodeIDs)
        def addCell(self, cell)
        def initGrid(self)
        def refine(self)
        def refineCell(self, cell)
        def getNodes(self)
        def getVertices(self, v)
        def getPolarVertices(self, v)
        def getTriangles(self)
        def getNodeAt(self,pos)
        def setData(self, data)
        def createPolarPlot(self,filename)
        def create3DPlot(self,filename)
        def createStereoPlot(self,filename)
    """

    def __init__(self):
        self.clearAll()

    def __str__(self):
        s = "Mesh(\n"
        for node in self.points:
            s += "    " + node
        for cell in self.triangles:
            s += "    " + cell
        s += "    )"
        return s

    def __repr__(self):
        return 'Mesh(nds={},tri={})'.format(self.points, self.triangles)

    def clearAll(self):
        self.clearGrid()
        self.points = []
        self.triangles = []
        self.data = []

    def clearGrid(self):
        self.nodes = []
        self.cells = []
        self.level = -1

    def addPoint(self, node):
        self.points.append(node)

    def addNode(self, node):
        # check id node already stored
        hasNode = False
        for existingNode in self.nodes:
            if (existingNode.getID() == node.getID()):
                hasNode = True
                break;
        # add the node if it does not exist in our list
        if ( not hasNode):
            self.nodes.append(node)

    def addLine(self, line):
        self.lines.append(line)

    def addTriangle(self, nodeIDs):
        self.triangles.append(nodeIDs)

    def addCell(self, cell):
        self.cells.append(cell)

    def initGrid(self):
        # convert master triangles to identical mesh

        # generate nodes
        self.nodes = self.points

        # generate triangles
        self.cells = []
        for tri in self.triangles:
            self.cells.append(TriCell(tri))

    def refine(self):
        #refine the mesh by one level
        existingCells = self.cells[:]
        self.cells = []

        for cell in existingCells:
            self.refineCell(cell)

        # remove duplicate lines


        # remove duplicate nodes


        # once done, increase the level index
        self.level += 1

    def refineCell(self, cell):
        # refine a single cell

        nodes = cell.getNodes()
        edges = cell.getEdges()

        # get mid-edge nodes
        nd1 = nodes[0]
        nd2 = nodes[1]
        nd3 = nodes[2]
        nd4 = self.getNodeAt( edges[0].getMiddleNodePos() )
        nd5 = self.getNodeAt( edges[1].getMiddleNodePos() )
        nd6 = self.getNodeAt( edges[2].getMiddleNodePos() )

        self.addNode(nd4)
        self.addNode(nd5)
        self.addNode(nd6)

        # create new cells as TriCell objects
        self.cells.append( TriCell((nd1, nd4, nd6)) )
        self.cells.append( TriCell((nd4, nd2, nd5)) )
        self.cells.append( TriCell((nd6, nd5, nd3)) )
        self.cells.append( TriCell((nd5, nd6, nd4)) )

    def getNodes(self):
        return self.nodes

    def getVertices(self, v):
        w = v / sqrt(dot(v, v))

        # find north
        north = array([0., 0., 1.])
        north -= dot(north, w)

        # if v is pointing straight up/down
        if (dot(north, north) < 1.e-10):
            north = array([-1., 0., 0.])
        else:
            north /= sqrt(dot(north, north))

        # find east
        east = cross(north, w)

        x = []
        y = []

        for node in self.nodes:
            pos = node.getPos()
            pos -= dot(w, pos) * w
            x.append(dot(pos, east))
            y.append(dot(pos, north))

        return x, y


    def getPolarVertices(self):

        # define up
        w = array([0.,0.,1.0])

        # define north
        north = array([-1., 0., 0.])

        # find east
        east = cross(north, w)

        x = []
        y = []

        for node in self.nodes:
            pos = node.getPos()
            rxy = sqrt(pos[0]*pos[0] + pos[1]*pos[1])
            theta = rad2deg( arccos(dot(pos,w)) )
            if rxy > 1.0e-12:
                x.append(pos[0]*theta/rxy)
                y.append(pos[1]*theta/rxy)
            else:
                x.append(pos[0])
                y.append(pos[1])

        return x, y

    def getTriangles(self):
        triangles = []
        for tri in self.cells:
            nodes = tri.getNodes()
            triangles.append([nodes[k].getID() for k in range(3)])
        return triangles

    def getNodeAt(self, pos):

        # assume we don't have this node
        haveNodeAtPos = False

        for node in self.nodes:
            d = node.getPos() - pos
            dist2 = dot(d,d)
            if (dist2 < 1e-12):
                # node is at the target position
                nd = node
                haveNodeAtPos = True
                break

        if (not haveNodeAtPos):
            # create a node if none found
            nd = Node()
            nd.setPos(pos)

        return nd

    def createmesh(self, targetlevel=1):
        # create the master mesh
        self.clearGrid()

        nd1 = self.getNodeAt(array([1., 0., 0.]))
        nd2 = self.getNodeAt(array([0., 1., 0.]))
        nd3 = self.getNodeAt(array([-1., 0., 0.]))
        nd4 = self.getNodeAt(array([0., -1., 0.]))
        nd5 = self.getNodeAt(array([0., 0., 1.]))

        self.addPoint(nd1)
        self.addPoint(nd2)
        self.addPoint(nd3)
        self.addPoint(nd4)
        self.addPoint(nd5)

        self.addTriangle([nd1, nd2, nd5])
        self.addTriangle([nd2, nd3, nd5])
        self.addTriangle([nd3, nd4, nd5])
        self.addTriangle([nd4, nd1, nd5])

        # create the grid
        self.initGrid()  # level 0
        theLevel = 0

        while theLevel < targetlevel:
            self.refine()
            theLevel += 1

    def setData(self, data):
        self.data = data

    def createPolarPlot(self, filename):
        pass

    def create3DPlot(self, filename):
        pass

    def createStereoPlot(self, filename):
        pass
