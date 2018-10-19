from numpy import array

class Node(object):
    """
    classdoc Node()

    variables:
       self.id
       self.x     ... position of the node
       self.lines ... list of attached lines

    methods:
        def __init__(self, pos=array([0.,0.]))
        def __str__(self)
        def __repr__(self)
        def getID(self)
        def setPos(self, x)
        def getPos(self)
        def getX(self)
        def getY(self)
        def attach(self, line)
        def connectedToLine(self,line)
    """

    MAX_NODE_ID = -1  # class variable

    def __init__(self, pos=array([0.,0., 0.])):
        Node.MAX_NODE_ID += 1

        self.id = Node.MAX_NODE_ID
        self.x  = pos
        self.lines = []

    def __str__(self):
        return "Node({})".format(self.x)

    def __repr__(self):
        return "Node({})".format(self.x)

    def getID(self):
        return self.id

    def setPos(self, x):
        self.x = array(x)

    def getPos(self):
        return self.x

    def getX(self):
        return self.x[0]

    def getY(self):
        return self.x[1]

    def attach(self, line):
        if ( not line in self.lines):
            self.lines.append(line)

    def connectedToLine(self,line):
        return (line in self.lines)

