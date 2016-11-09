from PyQt4 import uic, QtGui
from PyQt4.QtCore import *
import sys
if sys.version_info.major==2:
    import cPickle as pickle # pickle serializes python objects so they can be saved persistantly.  It converts a python object into a savable data structure
else:
    import pickle
import os, time
from ctypes import pointer
from os.path import expanduser


class Settings:
    ''' This class saves all the settings as you adjust them.  This way, when you close the program and reopen it, all your settings will automatically load as they were just after the last adjustement'''
    def __init__(self, index):
        self.folderName=expanduser("~")
        self.i=0
        self.index=int(index)
        a=dict()
        a['frequency']=0.0 #Hz
        a['radius']=.00 #in volts.  Max amplitude is 10 volts
        a['ellipticity']=1.00
        a['phase']=90.00
        a['x_shift']=.0
        a['y_shift']=-.0
        self.d=[a]
        
    def __getitem__(self, item):
        return self.d[self.i][item]
    
    def __setitem__(self,key,item):
        self.d[self.i][key]=item
        
    def save(self):
        '''save to a config file.'''
        topping = 'saving current settings to:'
        outFilename = QtGui.QFileDialog.getSaveFileName(None,topping,self.folderName,'*.*colibri')
        if outFilename:
            str1=str(outFilename)
            str2='.colibri'
            if str1.find(str2)<1:
                outFilename += '.colibri'
            self.refreshFolder(outFilename)
            filehandler = open(outFilename, 'wb')
            pickle.dump(self.d, filehandler)
            print (topping +' ' + outFilename)
        else:
            print('Warning. No file selected.')

    def load(self):
        '''load a config file'''
        topping = 'loading settings ' + str(self.index) + ' from folder:'
        importFilename = QtGui.QFileDialog.getOpenFileName(None,topping,self.folderName,'*.*colibri')
        if importFilename:
            self.refreshFolder(importFilename)
            filehandler = open(importFilename, 'rb')
            b = pickle.load(filehandler)
            for key in self.d[self.i]:
                try:
                    self.d[self.i][key]=float(b[0][key])
                except ValueError:
                    print('Error! %s values must pe a pure number' %(key))
                except:
                    print ('Warning! %s values are missing in loaded file' %(key))
            print (topping +' ' + importFilename)
        else:
            print('Warning. No file selected.')
     
    def refreshFolder(self, fileName):
        fileName=str(fileName)
        suffix='.'
        length=fileName.find(suffix)
        self.folderName=fileName[:length]

    def copy (self, origin):
        self.folderName=origin.folderName
        for key in self.d[self.i]:
            self.__setitem__(key,origin.__getitem__(key))
        
    def keys(self):
        return self.d[self.i].keys()

