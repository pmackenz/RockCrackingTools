'''
Created on Feb 11, 2015

@author: pmackenz
'''

class Element(object):
    '''
    classdocs
    '''

    def __init__(self, ID, nodes):
        '''
        Constructor
        '''
        self.ID = ID
        self.nodes = nodes
        
    def __str__(self):
        txt = "element "+self.ID+"\n"
        for nd in self.nodes:
            txt += "  node "+nd['ID']+": "+nd['pos']+"\n"
        return txt
        