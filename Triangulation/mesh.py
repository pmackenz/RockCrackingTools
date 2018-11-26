from numpy import array, dot, cross, arccos, rad2deg, deg2rad, sqrt, sin, cos, arccos, pi, linspace

from tricell import *
from line import *
from node import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#import matplotlib.tri as tri
#from matplotlib import cm

DPI = 150
#DPI = 300    # for high quality images

class Mesh(object):
    """
    :class: Mesh

    variables:
        self.points = []
        self.triangles = []
        self.nodes = []
        self.cells = []
        self.level = -1
        self.data  = {'deviator':[], 'mean':[]}
        self.sun   = None

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
        def getDirections(self)
        def getVertices(self, v)
        def getPolarVertices(self, v)
        def getTriangles(self)
        def getStereographicVertices(self, v)
        def getNodeAt(self,pos)
        def setSun(self, dir)
        def setData(self, data, data2)
        def setLabels(self, s1, s2)
        def createTestData(self, data)
        def createPolarPlot(self, filename='unknown.png', title='', units='')
        def create3DPlot(self, dir, filename='unknown.png', title='', units='')
        def createStereoPlot(self, filename='unknown.png', title='', units='')
        def createDoubleStereoPlot(self, filename='unknown.png', title='', units='')
    """

    def __init__(self):
        self. label1 = 'label 1'
        self. label2 = 'label 2'
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
        self.data = {'deviator':[], 'mean':[]}
        self.sun = None

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

    def getDirections(self):
        dirs = []
        for node in self.nodes:
            w = node.getPos()
            l = sqrt(dot(w,w))
            if (l>0.01):
                dirs.append(w/l)
        return dirs

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


    def getStereographicVertices(self):

        x = []
        y = []

        for node in self.nodes:
            pos = node.getPos()
            if pos[2] > -1.0:
                x.append(2.*pos[0]/(1.+pos[2]))
                y.append(2.*pos[1]/(1.+pos[2]))

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

    def setSun(self, dir):
        self.sun = dir

    def setData(self, data1, data2=[]):
        self.data['data1'] = data1
        self.data['data2'] = data2

    def setLabels(self, lbl1='label 1', lbl2='label 2'):
        self.label1 = lbl1
        self.label2 = lbl2

    def createTestData(self):
        # compute stress intensity for all nodes
        w = array([1., 3., 3.])
        w /= sqrt(dot(w, w))
        self.data['deviator'] = []
        for node in self.getNodes():
            # z.append(data.getF(node.getPos()))
            val = dot(w, node.getPos())
            if val < 0:
                val *= -1.
                self.data['deviator'].append(val)

    def createPolarPlot(self, filename='unknown.png', title='', units='', index=0):

        if index == 0:
            z = self.data['data1']
        elif index == 1:
            z = self.data['data2']
        else:
            print('no data set available for index={}'.format(index))
            raise

        # x, y      = mesh.getVertices([0.,0.,1.])
        x, y = self.getPolarVertices()
        triangles = self.getTriangles()

        # plot the triangularization
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')

        ax.set_axis_off()

        # plot contours
        contourLevels = linspace(0., 2.5, 26)  ## for stress
        ##contourLevels = linspace(0., 1.0, 21)   ## for deviatoric stress

        #tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('inferno'))
        #tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('YlOrRd'), levels=contourLevels)
        tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('gist_rainbow'), levels=contourLevels)
        cb = fig.colorbar(tcf)

        if (units):
            cb.set_label(units)

        # plot the triangulation
        ##ax.triplot(x, y, triangles, 'b-', lw=0.1)

        # plot polar axes
        ## circles
        an = linspace(0, 2 * pi, 100)
        for i in range(7):
            r = 90. * i / 6
            if (i % 2):
                ax.plot(r * cos(an), r * sin(an), '-', lw=0.33, color='grey')
            else:
                ax.plot(r * cos(an), r * sin(an), '-', lw=1.0, color='grey')

        ## radial lines
        for i in range(12):
            th = 2. * pi * i / 12.
            if (i % 3):
                ax.plot([0., 90. * sin(th)], [0., 90. * cos(th)], '-', lw=0.33, color='grey')
            else:
                ax.plot([0., 90. * sin(th)], [0., 90. * cos(th)], '-', lw=1.0, color='grey')

        ## labels
        for i in range(7):
            r = 90. * i / 6 + 0
            th = 2. * pi * (1.5 / 12.)
            label = "${:.0f}^\circ$".format(90 * i / 6)
            ax.text(r * sin(th), r * cos(th), label,
                    horizontalalignment='left', verticalalignment='bottom', fontsize=10)

        for i in range(12):
            r = 100.
            th = 2. * pi * (i / 12.)
            label = "${:.0f}^\circ$".format(360 * i / 12)
            if (i % 3 > 0):
                ax.text(r * sin(th), r * cos(th), label,
                        horizontalalignment='center', verticalalignment='center', fontsize=10)

        # plot the sun
        if (self.sun[2] >=0.0):
            r = rad2deg( arccos( self.sun[2]) )
            r2 = sqrt( self.sun[0]*self.sun[0] + self.sun[1]*self.sun[1] )
            if (r2 > 1e-12):
                x = r * self.sun[0]/r2
                y = r * self.sun[1]/r2
            else:
                x = 0.0
                y = 0.0

            ax.plot(x, y, 'o', lw=1.0, markersize=10., markeredgecolor='orange', markeredgewidth=1.,
                    markerfacecolor='yellow')

            print('Plotting sun at ', self.sun, '->', x, y)


        ax.set_xlabel('dip (degrees)')
        # ax.set_ylabel('Latitude (degrees)')
        ax.text(0., 92., 'N',
                horizontalalignment='center', verticalalignment='bottom', fontsize=14)
        ax.text(92., 0., 'E',
                horizontalalignment='left', verticalalignment='center', fontsize=14)
        ax.text(0., -92., 'S',
                horizontalalignment='center', verticalalignment='top', fontsize=14)
        ax.text(-92., 0., 'W',
                horizontalalignment='right', verticalalignment='center', fontsize=14)

        ## title
        if ( title ):
            ax.text(90., 95., title, horizontalalignment='center', verticalalignment='bottom', fontsize=14)

        ## export image file
        plt.savefig(filename, dpi=DPI)
        plt.close()


    def create3DPlot(self, filename='unknown.png', title='', units=''):

        # compute stress intensity for all nodes
        w = [1., 3., 3.]
        w /= sqrt(dot(w, w))
        z = []
        for node in self.getNodes():
            # z.append(data.getF(node.getPos()))
            val = dot(w, node.getPos())
            if val < 0:
                val *= -1.
            z.append(val)

        # get triangulation data for plotting
        x, y = self.getVertices([1., 1., 1.])
        triangles = self.getTriangles()

        # draw North axis

        # draw East axis

        # draw South axis

        # draw West axis

        # plot the triangularization
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')

        # plot contours
        tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('inferno'))
        fig.colorbar(tcf)

        if 0:
            ax.set_axis_off()

            # plot contours
            tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('inferno'))
            fig.colorbar(tcf)

            # plot the trianlulation
            ax.triplot(x, y, triangles, 'b-', lw=0.1)

            # plot polar axes
            ## circles
            an = np.linspace(0, 2 * np.pi, 100)
            for i in range(7):
                r = 90. * i / 6
                if (i % 2):
                    ax.plot(r * np.cos(an), r * np.sin(an), '-', lw=0.33, color='grey')
                else:
                    ax.plot(r * np.cos(an), r * np.sin(an), '-', lw=1.0, color='grey')

            ## radial lines
            for i in range(12):
                th = 2. * np.pi * i / 12.
                if (i % 3):
                    ax.plot([0., 90. * np.sin(th)], [0., 90. * np.cos(th)], '-', lw=0.33, color='grey')
                else:
                    ax.plot([0., 90. * np.sin(th)], [0., 90. * np.cos(th)], '-', lw=1.0, color='grey')

            ## labels
            # ax.set_xticks([-90.,-60.,-30.,0.,30.,60.,90.], minor=False)
            # ax.set_xticklabels(('90','60','30','0','30','60','90'))
            # ax.set_yticks([-90,-60,-30,0,30,60,90], minor=False)
            # ax.set_yticklabels(('90','60','30','0','30','60','90'))
            for i in range(7):
                r = 90. * i / 6 + 0
                th = 2. * np.pi * (1.5 / 12.)
                label = "${:.0f}^\circ$".format(90 * i / 6)
                ax.text(r * np.sin(th), r * np.cos(th), label,
                        horizontalalignment='left', verticalalignment='bottom', fontsize=10)

            for i in range(12):
                r = 100.
                th = 2. * np.pi * (i / 12.)
                label = "${:.0f}^\circ$".format(360 * i / 12)
                if (i % 3 > 0):
                    ax.text(r * np.sin(th), r * np.cos(th), label,
                            horizontalalignment='center', verticalalignment='center', fontsize=10)

            ax.set_xlabel('dip (degrees)')
            # ax.set_ylabel('Latitude (degrees)')
            ax.text(0., 92., 'N', horizontalalignment='center', verticalalignment='bottom', fontsize=14,
                    backgroundcolor=(1., 1., 1., .3))
            ax.text(92., 0., 'E', horizontalalignment='left', verticalalignment='center', fontsize=14,
                    backgroundcolor=(1., 1., 1., .3))
            ax.text(0., -92., 'S', horizontalalignment='center', verticalalignment='top', fontsize=14,
                    backgroundcolor=(1., 1., 1., .3))
            ax.text(-92., 0., 'W', horizontalalignment='right', verticalalignment='center', fontsize=14,
                    backgroundcolor=(1., 1., 1., .3))

            ## title
            if ( title ):
                ax.text(0., 95., title,
                        horizontalalignment='center', verticalalignment='bottom',
                        fontsize=16, backgroundcolor=(1., 1., 1., .3))

        plt.savefig(filename, dpi=DPI)
        plt.close()


    def createStereoPlot(self, filename='unknown.png', title='', units='', index=0):

        if index == 0:
            z = self.data['data1']
        elif index == 1:
            z = self.data['data2']
        else:
            print('no data set available for index={}'.format(index))
            raise

        # x, y      = mesh.getVertices([0.,0.,1.])
        x, y = self.getStereographicVertices()
        triangles = self.getTriangles()

        # plot the triangularization
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')

        ax.set_axis_off()

        # plot contours
        contourLevels = linspace(0., 2.5, 26)  ## for stress
        ##contourLevels = linspace(0., 1.0, 21)   ## for deviatoric stress

        #tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('inferno'))
        #tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('YlOrRd'), levels=contourLevels)
        tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('gist_rainbow'), levels=contourLevels)
        cb = fig.colorbar(tcf)

        if (units):
            cb.set_label(units)

        # plot the triangulation
        ##ax.triplot(x, y, triangles, 'b-', lw=0.1)

        ## meridians
        an = linspace(-pi/2, pi/2, 100)
        bn = linspace(-pi/2.*7./9., pi/2.*7./9., 80)
        phi = th = linspace(-pi/2, pi/2, 91)

        for i in range(91):
            if (i % 5):
                zz = 1 + cos(bn) * cos(th[i])
                ax.plot(-2 * cos(bn) * sin(th[i]) / zz, 2 * sin(bn) / zz, '-', lw=0.1, color='grey')
            else:
                zz = 1 + cos(an) * cos(th[i])
                ax.plot(-2 * cos(an) * sin(th[i]) / zz, 2 * sin(an) / zz, '-', lw=0.5, color='grey')

        ## latitudes lines
        for i in range(91):
            zz = 1 + cos(phi[i]) * cos(an)
            if (i % 5):
                if ( i > 10 and i < 81):
                    ax.plot(-2. * cos(phi[i]) * sin(an) / zz, 2. * sin(phi[i]) / zz, '-', lw=0.1, color='grey')
            else:
                ax.plot(-2. * cos(phi[i]) * sin(an) / zz, 2. * sin(phi[i]) / zz, '-', lw=0.5, color='grey')

        # plot the sun
        if (self.sun[2] >= 0.0):
            x = (2. * self.sun[0] / (1. + self.sun[2]))
            y = (2. * self.sun[1] / (1. + self.sun[2]))
            ax.plot(x,y,'o', lw=1.0, markersize=10., markeredgecolor='orange',
                    markeredgewidth=1., markerfacecolor='yellow')

            print('Plotting sun at ', self.sun, '->', x, y)

        ## labels
        for i in range(-2,3):
            phi = deg2rad(0.)
            th = pi * i / 6.
            label = "${:.0f}^\circ$".format(30 * i)
            zz = 1. + cos(phi) * cos(th)
            ax.text(-2. * cos(phi) * sin(th) / zz, 2. * sin(phi) / zz, label,
                    horizontalalignment='center', verticalalignment='center', fontsize=10)

        for i in range(12):
            phi = pi * i / 6.
            label = "${:.0f}^\circ$".format(30 * i)
            if (i % 3 > 0):
                ax.text( 2.2 * sin(phi), 2.2 * cos(phi), label,
                        horizontalalignment='center', verticalalignment='center', fontsize=10)

        ## label N, E, S, W:

        ax.set_xlabel('dip (degrees)')
        # ax.set_ylabel('Latitude (degrees)')
        ax.text(0., 2.05, 'N',
                horizontalalignment='center', verticalalignment='bottom', fontsize=14)
        ax.text(2.05, 0., 'E',
                horizontalalignment='left', verticalalignment='center', fontsize=14)
        ax.text(0., -2.05, 'S',
                horizontalalignment='center', verticalalignment='top', fontsize=14)
        ax.text(-2.05, 0., 'W',
                horizontalalignment='right', verticalalignment='center', fontsize=14)

        ## title
        if ( title ):
            ax.text(2., 2.3, title, horizontalalignment='center', verticalalignment='bottom', fontsize=14)

        ## export image file
        plt.savefig(filename, dpi=DPI)
        plt.close()


    def createDoubleStereoPlot(self, filename='unknown.png', title='', units=''):

        z1 = self.data['data1']
        z2 = self.data['data2']

        # x, y      = mesh.getVertices([0.,0.,1.])
        x, y = self.getStereographicVertices()
        triangles = self.getTriangles()

        # plot the triangularization
        #fig = plt.figure(figsize=[8.5, 3.5])
        fig = plt.figure(figsize=[7., 3.5])
        gs = GridSpec(1,7, figure=fig)
        ax1 = fig.add_subplot(gs[0,:3] )
        ax2 = fig.add_subplot(gs[0,3:] )
        #ax3 = fig.add_subplot(gs[0,6] )

        ax1.set_aspect('equal')
        ax1.set_axis_off()
        ax1.set_xlabel(self.label1)

        ax2.set_aspect('equal')
        ax2.set_axis_off()
        ax2.set_xlabel(self.label2)

        #ax3.set_aspect(10)
        #ax3.set_axis_off()


        # plot contours
        contourLevels = linspace(0., 2.5, 26)  ## for stress
        ##contourLevels = linspace(0., 1.0, 21)   ## for deviatoric stress

        tcf1 = ax1.tricontourf(x, y, triangles, z1, cmap=plt.get_cmap('gist_rainbow'), levels=contourLevels)
        tcf2 = ax2.tricontourf(x, y, triangles, z2, cmap=plt.get_cmap('gist_rainbow'), levels=contourLevels)

        cb = fig.colorbar(tcf1, ax=ax2)

        if (units):
            cb.set_label(units)

        for ax in [ax1, ax2]:

            # plot the triangulation
            ##ax.triplot(x, y, triangles, 'b-', lw=0.1)

            ## meridians
            an = linspace(-pi / 2, pi / 2, 100)
            bn = linspace(-pi / 2. * 7. / 9., pi / 2. * 7. / 9., 80)
            phi = th = linspace(-pi / 2, pi / 2, 91)

            for i in range(91):
                if (i % 5):
                    zz = 1 + cos(bn) * cos(th[i])
                    ax.plot(-2 * cos(bn) * sin(th[i]) / zz, 2 * sin(bn) / zz, '-', lw=0.1, color='grey')
                else:
                    zz = 1 + cos(an) * cos(th[i])
                    ax.plot(-2 * cos(an) * sin(th[i]) / zz, 2 * sin(an) / zz, '-', lw=0.5, color='grey')

            ## latitudes lines
            for i in range(91):
                zz = 1 + cos(phi[i]) * cos(an)
                if (i % 5):
                    if ( i > 10 and i < 81):
                        ax.plot(-2. * cos(phi[i]) * sin(an) / zz, 2. * sin(phi[i]) / zz, '-', lw=0.1, color='grey')
                else:
                    ax.plot(-2. * cos(phi[i]) * sin(an) / zz, 2. * sin(phi[i]) / zz, '-', lw=0.5, color='grey')

            # plot the sun
            if (self.sun[2] >= 0.0):
                x = (2. * self.sun[0] / (1. + self.sun[2]))
                y = (2. * self.sun[1] / (1. + self.sun[2]))
                ax.plot(x,y,'o', lw=1.0, markersize=10., markeredgecolor='orange',
                        markeredgewidth=1., markerfacecolor='yellow')

                print('Plotting sun at ', self.sun, '->', x, y)

            ## labels
            for i in range(-2,3):
                phi = deg2rad(0.)
                th = pi * i / 6.
                label = "${:.0f}^\circ$".format(30 * i)
                zz = 1. + cos(phi) * cos(th)
                ax.text(-2. * cos(phi) * sin(th) / zz, 2. * sin(phi) / zz, label,
                        horizontalalignment='center', verticalalignment='center', fontsize=9)

            for i in range(12):
                phi = pi * i / 6.
                label = "${:.0f}^\circ$".format(30 * i)
                if (i % 3 > 0):
                    ax.text( 2.2 * sin(phi), 2.2 * cos(phi), label,
                            horizontalalignment='center', verticalalignment='center', fontsize=9)

            ## label N, E, S, W:

            ax.set_xlabel('dip (degrees)')
            # ax.set_ylabel('Latitude (degrees)')
            ax.text(0., 2.05, 'N',
                    horizontalalignment='center', verticalalignment='bottom', fontsize=11)
            ax.text(2.05, 0., 'E',
                    horizontalalignment='left', verticalalignment='center', fontsize=11)
            ax.text(0., -2.05, 'S',
                    horizontalalignment='center', verticalalignment='top', fontsize=11)
            ax.text(-2.05, 0., 'W',
                    horizontalalignment='right', verticalalignment='center', fontsize=11)

        ## title
        if ( title ):
            ax1.text(2.3, 2.1, title, horizontalalignment='center', verticalalignment='bottom', fontsize=11)

            ax1.text(0., -2.4, self.label1,
                     horizontalalignment='center', verticalalignment='top', fontsize=11)
            ax2.text(0., -2.4, self.label2,
                     horizontalalignment='center', verticalalignment='top', fontsize=11)

        plt.subplots_adjust(left=0.05, bottom=0.15, top=0.85, right=0.95)

        ## export image file
        plt.savefig(filename, dpi=DPI)
        plt.close()


