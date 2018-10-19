'''
Created on May 22, 2017

@author: pmackenz
updated and extended by Smit Kamal: Tue May 30
updated by pmackenz: Wed May 31 18:27:23 PDT 2017
'''

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


all_skin_depth = 0.1610

tasks = [
    {'outfile':"../data/ws15cm.csv",  'diameter':0.15,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws20cm.csv",  'diameter':0.20,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws25cm.csv",  'diameter':0.25,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws30cm.csv",  'diameter':0.30,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws40cm.csv",  'diameter':0.40,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws50cm.csv",  'diameter':0.50,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws63cm.csv",  'diameter':0.625, 'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws75cm.csv",  'diameter':0.75,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws88cm.csv",  'diameter':0.875, 'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws100cm.csv", 'diameter':1.00,  'skindepth':all_skin_depth, 'startAtInc':48, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws125cm.csv", 'diameter':1.25,  'skindepth':all_skin_depth, 'startAtInc':84, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws150cm.csv", 'diameter':1.50,  'skindepth':all_skin_depth, 'startAtInc':84, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws200cm.csv", 'diameter':2.00,  'skindepth':all_skin_depth, 'startAtInc':168, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws300cm.csv", 'diameter':3.00,  'skindepth':all_skin_depth, 'startAtInc':252, 'endAtInc':9999, 'dTime':0.25},
    {'outfile':"../data/ws500cm.csv", 'diameter':5.00,  'skindepth':all_skin_depth, 'startAtInc':336, 'endAtInc':9999, 'dTime':0.25}
    ]


class PlotData(object):
    '''
    classdocs
    
    variables:
        self.filename  = filename
        self.headerline
        self.headers self.nSegments
        self.INCidx = 0
        self.POSidx = 2
        self.POFidx = 3
        self.LIMITSidx  = []
        self.Bidx       = []
        self.POSidx     = []
        self.POFidx     = []
        self.CoreBidx   = []
        self.CorePOSidx = []
        self.CorePOFidx = []
        self.data = {}
        
        self.POF     = []
        self.POF1    = []
        self.POF2    = []
        self.POF3    = []
        self.POFcore = []
    
    methods:
        def __init__(self, filename)
        def parseFile(self)
        def POFplot(self, filename='default.pdf')
        def getTime(self)
        def getPOF(self)
        def getPOF1(self)
        def getPOF2(self)
        def getPOF3(self)
        def getPOFcore(self)
        def maxPOF(self)
        def maxPOF1(self)
        def maxPOF2(self)
        def maxPOF3(self)
        def maxPOFcore(self)
        def flagStatus(self)
        def POF_R(self,series,filename='default2.pdf')
        def POF_time(self,series,filename='POF_time.pdf')
        def POE_time_layer(self, series, title, filename='POF_time.pdf')
        def has_POF(self)
        def has_POF1(self)
        def has_POF2(self)
        def has_POF3(self)
        def has_POFcore(self)
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        
        self.filename  = filename
        try:
            self.file = open(filename, 'r')
            self.file_open = True
        except:
            print('cannot open file {}'.format(filename))
            self.file_open = False
            return
        
        # sample header line:
        # Inc,nSegments,POS,POF,R1,R2,R3,B1,B2,B3,POS1,POS2,POS3,POF1,POF2,POF3,

        self.headerline = self.file.readline().rstrip()
        self.headers = self.headerline.split(',')
        
        anotherline = self.file.readline().rstrip()
        vals = anotherline.split(',')
        
        self.nSegments = int(vals[1])
        self.INCidx = 0
        self.allPOSidx = 2
        self.allPOFidx = 3
        self.LIMITSidx = [ i+4 for i in range(self.nSegments) ]
        self.Bidx   = [ self.LIMITSidx[-1]+1+i for i in range(self.nSegments) ]
        self.POSidx = [ self.Bidx[-1]+1+i      for i in range(self.nSegments) ]
        self.POFidx = [ self.POSidx[-1]+1+i    for i in range(self.nSegments) ]
        if self.nSegments > 3:
            self.CoreBidx   = self.Bidx[3:]
            self.CorePOSidx = self.POSidx[3:]
            self.CorePOFidx = self.POFidx[3:]
        else:
            self.CoreBidx   = []
            self.CorePOSidx = []
            self.CorePOFidx = []
        
        self.data = {'INC':[],'TIME':[],'POF':[],'POF1':[],'POF2':[],'POF3':[],'POFCORE':[]}
        
        self.POF     = []
        self.POF1    = []
        self.POF2    = []
        self.POF3    = []
        self.POFcore = []
        
        self.file.close()
        try:
            self.file = open(filename, 'r')
            self.file_open = True
        except:
            print('cannot open file',filename)
            self.file_open = False
            
        self.headerline = self.file.readline().rstrip()
        self.headers = self.headerline.split(',')
        
        
    def parseFile(self, startInc=0, endInc=99999, deltaTime=1.0):
        if not self.file_open:
            return
        
        for line in self.file:
            vals = [ float(item) for item in line.rstrip('\n,').split(',') ]
            
            if vals[self.INCidx] < startInc:
                continue
            
            if vals[self.INCidx] > endInc:
                continue
            
            time = deltaTime*(vals[self.INCidx] - startInc)
            self.data['TIME'].append(time)
            self.data['INC'].append(vals[self.INCidx])
            B_total=sum([vals[i] for i in self.Bidx])
            POF=vals[self.allPOFidx]
            if POF < B_total:
                POF = B_total*(1.0 - B_total/2.0*(1.0 - B_total/3.0*(1.0 - B_total/4.0)))
            self.data['POF'].append(POF)
            POF1 = vals[self.POFidx[0]]
            B1   = vals[self.Bidx[0]]
            if POF1 < B1:
                POF1 = B1*(1.0 - B1/2.0*(1.0 - B1/3.0*(1.0 - B1/4.0)))
            self.data['POF1'].append(POF1)
            if self.nSegments > 1:
                POF2 = vals[self.POFidx[1]]
                B2   = vals[self.Bidx[1]]
                if POF2 < B2:
                    POF2 = B2*(1.0 - B2/2.0*(1.0 - B2/3.0*(1.0 - B2/4.0)))
                self.data['POF2'].append(POF2)
            if self.nSegments > 2:
                POF3 = vals[self.POFidx[2]]
                B3   = vals[self.Bidx[2]]
                if POF3 < B3:
                    POF3 = B3*(1.0 - B3/2.0*(1.0 - B3/3.0*(1.0 - B3/4.0)))
                self.data['POF3'].append(POF3)
            if self.nSegments > 2:
                CoreB = sum([vals[i] for i in self.CoreBidx])
                POFcore = 1.0 - np.exp(-CoreB)
                if CoreB > POFcore:
                    POFcore = CoreB*(1.0 - CoreB/2.0*(1.0 - CoreB/3.0*(1.0 - CoreB/4.0)))
                self.data['POFCORE'].append(CoreB)
    
    def POFplot(self, filename='default.pdf', titlestring=""):
        if not self.file_open:
            return
    
        if not titlestring:
            titlestring = "Probabibility of Event (POE) for boulder {}".format(filename[:-4])
            
        self.time = np.array(self.data['TIME'])
        self.POF  = np.array(self.data['POF'])
        self.POF1 = np.array(self.data['POF1'])
        self.POF2 = np.array(self.data['POF2'])
        self.POF3 = np.array(self.data['POF3'])
        self.POFC = np.array(self.data['POFCORE'])
        
        dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
        
        plt.semilogy(self.time, self.POF, '--r', linewidth=2, label="POE boulder")
        plt.hold(True)
        if self.has_POF1():
            plt.semilogy(self.time, self.POF1, '-b', linewidth=3, label="POE 1st skin")
        if self.has_POF2():
            plt.semilogy(self.time, self.POF2, '-y', linewidth=3, label="POE 2nd skin")
        if self.has_POF3():
            plt.semilogy(self.time, self.POF3, '-m', linewidth=3, label="POE 3rd skin")
        if self.has_POFcore():
            plt.semilogy(self.time, self.POFC, '-g', linewidth=3, label="POE core")
        plt.hold(False)
        
        plt.xlim(0., 24.)
        plt.ylim(1.e-15, 1.e-2)
        plt.xticks([0,6,12,18,24],["0:00","6:00","12:00","18:00","24:00"])
        plt.title(titlestring)
        plt.legend(loc='best')
        plt.grid(True,which='major',axis='both')
        plt.grid(True,which='minor',axis='y')
        
        plt.savefig(filename)
     
    def getTime(self):
        return np.array(self.data['TIME']) 
       
    def getPOF(self):
        return np.array(self.data['POF'])
    
    def getPOF1(self):
        return np.array(self.data['POF1'])
    
    def getPOF2(self):
        return np.array(self.data['POF2'])
    
    def getPOF3(self):
        return np.array(self.data['POF3'])
    
    def getPOFcore(self):
        return np.array(self.data['POFCORE'])
    
    def maxPOF(self):
        return max(self.data['POF'])
    
    def maxPOF1(self):
        return max(self.data['POF1'])
    
    def maxPOF2(self):
        return max(self.data['POF2'])
    
    def maxPOF3(self):
        return max(self.data['POF3'])
    
    def maxPOFcore(self):
        return max(self.data['POFCORE'])
    
    def flagStatus(self):
        return self.flag
  
    def POF_R(self, data, filename='default2.pdf'):
        titlestring = "maximum Probability of Event (POE) within one diurnal cycle"
        if data.has_key('POE') and max(data['POE']['POF']) >= 1e-20:
            line = data['POE']
            plt.semilogy(line['diameter'],line['POF'], '--r', linewidth=3, label="POE boulder")
            plt.hold(True)
        
        if data.has_key('POE1') and max(data['POE1']['POF']) >= 1e-20:
            line = data['POE1']
            plt.semilogy(line['diameter'],line['POF'], '-b', linewidth=3, label="POE 1st skin layer")
            plt.hold(True)
        
        if data.has_key('POE2') and max(data['POE2']['POF']) >= 1e-20:
            line = data['POE2']
            plt.semilogy(line['diameter'],line['POF'], '-y', linewidth=3, label="POE 2nd skin layer")
            plt.hold(True) 
        
        if data.has_key('POE3') and max(data['POE3']['POF']) >= 1e-20:
            line = data['POE3']
            plt.semilogy(line['diameter'],line['POF'], '-m', linewidth=3, label="POE 3rd skin layer")
            plt.hold(True) 
        
        if data.has_key('POEC') and max(data['POEC']['POF']) >= 1e-20:
            line = data['POEC']
            plt.semilogy(line['diameter'],line['POF'], '-g', linewidth=3, label="POE core")
            plt.hold(True) 
            
        plt.xlabel('Diameter of the boulder (m)')
        plt.ylabel('Max Probability of Event (POE)')
        plt.ylim(1.e-15, 1.e-2)
        plt.title(titlestring) 
        plt.grid(True,which='major',axis='both')
        plt.grid(True,which='minor',axis='y')
        plt.legend(loc='best',labelspacing=0)
        plt.hold(False)   
        plt.savefig(filename) 
    
    def POF_time(self, series, title, filename='POE_default.pdf'):
        count = 0
        num_plots = len(series)
        #colormap = plt.cm.gist_ncar
        #plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))
        for line in series:
            lbl = "{:.3f} m".format(line['diameter'])
            plt.semilogy(line['time'],line['POF'], linewidth=2, label=lbl)
            plt.hold(True)
            count += 1
        titlestring = "Probability of Event (POE) for the entire boulder"
        #colormap = plt.cm.gist_ncar
        #plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))
        plt.xlim(0., 24.)
        plt.ylim(1.e-15, 1.e-2)
        plt.xlabel('Time (hours)')
        plt.ylabel('Probability of Event (POE)')
        plt.legend(loc='best',labelspacing=0, fontsize=12,ncol=2)
        plt.xticks([0,6,12,18,24],["0:00","6:00","12:00","18:00","24:00"])
        plt.grid(True,which='major',axis='both')
        plt.grid(True,which='minor',axis='y')  
        plt.title(titlestring) 
        plt.hold(False)
        plt.savefig(filename) 
        
    def POE_time_layer(self, series, titlestring, filename='POE1_time.pdf'):
        
        for line in series:
            if max(line['POF']) < 1.0e-20:
                continue
            lbl = "{:.3f} m".format(line['diameter'])
            plt.semilogy(line['time'],line['POF'],linewidth=2, label=lbl)
            plt.hold(True)
            
        plt.xlim(0., 24.)
        plt.ylim(1.e-15, 1.e-2)
        plt.xlabel('Time (hours)')
        plt.ylabel('Probability of Event (POE)')
        plt.legend(loc='best',labelspacing=0, fontsize=12,ncol=2)
        plt.xticks([0,6,12,18,24],["0:00","6:00","12:00","18:00","24:00"])
        plt.grid(True,which='major',axis='both')
        plt.grid(True,which='minor',axis='y')  
        plt.title(titlestring) 
        plt.hold(False)
        plt.savefig(filename) 
            
    def has_POF(self):
        if len(self.POF) > 0 and len(self.POF) == len(self.time):
            return True
        else:
            return False
        
    def has_POF1(self):
        if len(self.POF1) > 0 and len(self.POF1) == len(self.time):
            return True
        else:
            return False
        
    def has_POF2(self):
        if len(self.POF2) > 0 and len(self.POF2) == len(self.time):
            return True
        else:
            return False

    def has_POF3(self):
        if len(self.POF3) > 0 and len(self.POF3) == len(self.time):
            return True
        else:
            return False
            
    def has_POFcore(self):
        if len(self.POFC) > 0 and len(self.POFC) == len(self.time):  
            return True
        else:
            return False  
       
        
if __name__ == "__main__":
    
    d_matrix  = []
    d1_matrix = []
    d2_matrix = []
    d3_matrix = []
    dcore_matrix = []
    
    POF_t     = []
    POF1_t    = []
    POF2_t    = []
    POF3_t    = []
    POFcore_t = []
    
    maxPOF_mat     = []
    maxPOF1_mat    = []
    maxPOF2_mat    = []
    maxPOF3_mat    = []
    maxPOFcore_mat = []
    
    for task in tasks:
        datafile   = task['outfile']
        plotfile   = "{}_POF.pdf".format(datafile[:-4])
        diameter   = datafile[:-4].split('/')
        title      = "Probability of Event (POE) for {} cm diameter boulder".format(diameter[-1][2:-2])
        diameter   = task['diameter']
        skin_depth = task['skindepth']
        fromInc    = task['startAtInc']
        toInc      = task['endAtInc']
        dTime      = task['dTime']
        
        # create plot for a single boulder
        plot = PlotData(datafile)
        plot.parseFile(fromInc, toInc, dTime)
        plot.POFplot(plotfile, title)\
        
        # now collect information for all boulders
        if plot.has_POF():
            maxPOF_mat.append(plot.maxPOF())
            d_matrix.append(diameter)
            POF_t.append({'diameter':diameter, 'time':plot.getTime(),'POF':plot.getPOF()})
        
        if plot.has_POF1():
            maxPOF1_mat.append(plot.maxPOF1())
            d1_matrix.append(diameter)
            POF1_t.append({'diameter':diameter, 'time':plot.getTime(),'POF':plot.getPOF1()})

        if plot.has_POF2():
            maxPOF2_mat.append(plot.maxPOF2())
            d2_matrix.append(diameter)
            POF2_t.append({'diameter':diameter, 'time':plot.getTime(),'POF':plot.getPOF2()})

        if plot.has_POF3():
            maxPOF3_mat.append(plot.maxPOF3())
            d3_matrix.append(diameter)
            POF3_t.append({'diameter':diameter, 'time':plot.getTime(),'POF':plot.getPOF3()})

        if plot.has_POFcore():
            maxPOFcore_mat.append(plot.maxPOFcore())
            dcore_matrix.append(diameter)
            POFcore_t.append({'diameter':diameter, 'time':plot.getTime(),'POF':plot.getPOFcore()})

        
    POF_data={'POE': {'diameter':d_matrix,    'POF':maxPOF_mat},
              'POE1':{'diameter':d1_matrix,   'POF':maxPOF1_mat},
              'POE2':{'diameter':d2_matrix,   'POF':maxPOF2_mat},
              'POE3':{'diameter':d3_matrix,   'POF':maxPOF3_mat},
              'POEC':{'diameter':dcore_matrix,'POF':maxPOFcore_mat}}
    
    plot.POF_R(POF_data,'../data/POE_over_R.pdf')
    plot.POF_time(POF_t, '../data/POEcomparison.pdf') 
    plot.POE_time_layer(POF1_t,"Probability of Event (POE) within the 1st skin layer",'../data/POE1comparison.pdf') 
    plot.POE_time_layer(POF2_t,"Probability of Event (POE) within the 2nd skin layer",'../data/POE2comparison.pdf') 
    plot.POE_time_layer(POF3_t,"Probability of Event (POE) within the 3rd skin layer",'../data/POE3comparison.pdf') 
    plot.POE_time_layer(POFcore_t,"Probability of Event (POE) within the core",'../data/POEcoreComparison.pdf')  
    

