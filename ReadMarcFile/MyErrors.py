'''
Created on Mar 31, 2016

@author: pmackenz
'''

class DataIntegrityError(Exception):
    '''
    classdocs
    '''

    def __init__(self, msg=""):
        '''
        Constructor
        '''
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)
    
        