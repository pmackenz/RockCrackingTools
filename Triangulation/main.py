import numpy as np

from createmesh import *

import matplotlib.pyplot as plt
#import matplotlib.tri as tri
#from matplotlib import cm


def main():
    # global settings
    Plot3D = False
    #Plot3D = True

    # create the master mesh
    mesh = createmesh(4)

    # read data file
    #
    #  this requires opening and parsing a MSC.marc output file
    #  Each output file has multiple increments in it.
    #  Only data from one single increment is to be used per plot.
    #

    # open file

    # search for a particular increment

    # parse data for that increment
    #data = ...

    # compute stress intensity for all nodes
    w = array([1.,3.,3.])
    w /= sqrt(dot(w,w))
    z = []
    for node in mesh.getNodes():
        #z.append(data.getF(node.getPos()))
        val = dot(w,node.getPos())
        if val<0:
            val *= -1.
        z.append(val)

    if Plot3D:
        # get triangulation data for plotting
        x, y      = mesh.getVertices([1.,1.,1.])
        triangles = mesh.getTriangles()

        # draw North axis

        # draw East axis

        # draw South axis

        # draw West axis

    else:
        #x, y      = mesh.getVertices([0.,0.,1.])
        x, y      = mesh.getPolarVertices()
        triangles = mesh.getTriangles()

    # plot the triangularization
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    if Plot3D:
        # plot contours
        tcf = ax.tricontourf(x, y, triangles, z, cmap=plt.get_cmap('inferno'))
        fig.colorbar(tcf)

    else:
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
            r = 90.*i/6
            if (i%2):
                ax.plot(r * np.cos(an), r * np.sin(an), '-', lw=0.33, color='grey')
            else:
                ax.plot(r * np.cos(an), r * np.sin(an), '-', lw=1.0, color='grey')

        ## radial lines
        for i in range(12):
            th = 2.*np.pi*i/12.
            if (i%3):
                ax.plot([0., 90.*np.sin(th)],[0., 90.*np.cos(th)], '-', lw=0.33, color='grey')
            else:
                ax.plot([0., 90.*np.sin(th)],[0., 90.*np.cos(th)], '-', lw=1.0, color='grey')

        ## labels
        for i in range(7):
            r = 90.*i/6 + 0
            th = 2.*np.pi*(1.5/12.)
            label = "${:.0f}^\circ$".format(90*i/6)
            ax.text(r*np.sin(th), r*np.cos(th), label,
                    horizontalalignment='left', verticalalignment='bottom', fontsize=10)

        for i in range(12):
            r = 100.
            th = 2.*np.pi*(i/12.)
            label = "${:.0f}^\circ$".format(360*i/12)
            if (i%3 > 0):
                ax.text(r*np.sin(th), r*np.cos(th), label,
                        horizontalalignment='center', verticalalignment='center', fontsize=10)



        ax.set_xlabel('dip (degrees)')
        #ax.set_ylabel('Latitude (degrees)')
        ax.text(0., 92., 'N', horizontalalignment='center', verticalalignment='bottom', fontsize=14, backgroundcolor=(1., 1., 1., .3))
        ax.text(92., 0., 'E', horizontalalignment='left', verticalalignment='center', fontsize=14, backgroundcolor=(1., 1., 1., .3))
        ax.text(0.,-92., 'S', horizontalalignment='center', verticalalignment='top', fontsize=14, backgroundcolor=(1., 1., 1., .3))
        ax.text(-92.,0., 'W', horizontalalignment='right', verticalalignment='center', fontsize=14, backgroundcolor=(1., 1., 1., .3))

        plt.savefig('demo.png')


if (__name__ == "__main__"):
    print("running main")
    main()