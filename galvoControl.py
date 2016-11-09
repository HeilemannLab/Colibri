from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from PyQt4.QtCore import pyqtSignal as Signal
import time
import colibriLib as clib
import numpy as np


print('National Instuments card successfully loaded.')

class GalvoDriver:
    '''
    
    '''
    finished_acquire_sig=Signal()
    def __init__(self, settings):
        self.guiSettings=clib.Settings(0)
        self.guiSettings.copy(settings)
        self.restSettings=clib.Settings(0)
        self.restSettings.copy(settings)
        self.operateSettings=clib.Settings(0)
        self.operateSettings.copy(settings)
        self.sample_rate=500000.0 # Maximum for the NI PCI-6229 is 833KHz.
        self.sampsPerPeriod=1.0 #dummy variable
        self.calculate()
        self.read = int32()
        self.stopped=True
        self.createTask()
        
    def startTask(self):
        self.analog_output.StartTask()
        self.stopped=False
    
    def stopTask(self):
        self.analog_output.StopTask()
        self.stopped=True
    
    def startStop(self, settings):
        if self.stopped:
            self.operateSettings.copy(self.guiSettings)
            self.startTask()
            #self.analog_output.StartTask()
            #self.stopped=False
            self.refresh(settings)
            #self.acquire()
            print('I am running')
        else:
            self.operateSettings.copy(self.restSettings)
            self.stopTask()
            #self.analog_output.StopTask()
            #self.stopped=True
            #self.refresh(settings)
            #self.stopAcquiring()
            print('i have stopped running')
            
    def refresh(self, settings):
        if self.stopped is False:
            self.updateGuiSettings(settings)
            self.operateSettings.copy(self.guiSettings)
            self.calculate()
            #self.analog_output.StopTask()
            self.stopTask()
            self.analog_output.CfgSampClkTiming("",self.sample_rate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.sampsPerPeriod)
            self.analog_output.WriteAnalogF64(self.sampsPerPeriod,0,-1,DAQmx_Val_GroupByChannel,self.data,byref(self.read),None) 
            #self.analog_output.StartTask()
            self.startTask()
        else:
            self.updateGuiSettings(settings)
        print (self.operateSettings['frequency'])
    
    def updateGuiSettings(self, settings):
        self.guiSettings.copy(settings)

    def calculate(self):
        print ('i am running')
        #sinwave,coswave,camera_ttl,blue_laser_ttl, green_laser_ttl=self.getSinCosTTL()
        sinwave,coswave=self.getSinCosTTL()
        self.data=np.concatenate((sinwave,coswave))
        self.sampsPerPeriod=len(sinwave)


    def getSinCosTTL(self):
        frequency = self.operateSettings['frequency']
        radius = self.operateSettings['radius']
        ellipticity = self.operateSettings['ellipticity']
        phase = self.operateSettings['phase']
        x_shift = self.operateSettings['x_shift']
        y_shift = self.operateSettings['y_shift']
        period = 0.005 # The period argument is only used when the value of the frequency is 0
        if frequency==0:
            t=np.arange(0,period,1.0/self.sample_rate)
            sinwave=radius*np.sin(np.zeros(len(t)))+x_shift/1000.0
            coswave=(ellipticity*radius*np.cos(np.zeros(len(t))+phase*(2*np.pi/360)))+(y_shift/1000.0)
        else:
            period=1/frequency
            t=np.arange(0.0,period,1.0/self.sample_rate )
            sinwave=radius*np.sin(frequency*(t*(2*np.pi)))+x_shift/1000.0
            coswave=(ellipticity*radius*np.cos(frequency*t*2*np.pi+phase*(2*np.pi/360)))+(y_shift/1000.0)
        return sinwave,coswave
     
    def createTask(self):
        self.analog_output = Task()
        self.analog_output.CreateAOVoltageChan("Dev1/ao0","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao2 is pin 57 and ground is 56
        self.analog_output.CreateAOVoltageChan("Dev1/ao1","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao3 is pin 25 and ground is 24
        """self.analog_output.CreateAOVoltageChan("Dev2/ao4","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao4 is pin 60 and ground is 59 What is this?"""
        """self.analog_output.CreateAOVoltageChan("Dev2/ao5","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao5 is pin 28 and ground is 29. This is blue laser"""
        """self.analog_output.CreateAOVoltageChan("Dev2/ao6","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao6 is pin 30 and ground is 31. This is green laser"""


                        #  CfgSampClkTiming(source, rate, activeEdge, sampleMode, sampsPerChan)
        print ('sample rate')
        print (self.sample_rate)
        self.analog_output.CfgSampClkTiming("",self.sample_rate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.sampsPerPeriod)
                        #  WriteAnalogF64(numSampsPerChan, autoStart, timeout, dataLayout, writeArray, sampsPerChanWritten, reserved)
        self.analog_output.WriteAnalogF64(self.sampsPerPeriod,0,-1,DAQmx_Val_GroupByChannel,self.data,byref(self.read),None) 
        #self.analog_output.StartTask()
        #self.stopped=False
        #self.acquiring=False
"""  
    def acquire(self):
        print('Acquiring')
        self.acquiring=True
        self.counter=0
        self.tic=time.time()

        #radius=self.settings.d[0]['radius']; alternate12=self.settings.d[0]['alternate12']; alternate123=self.settings.d[0]['alternate123']
        #self.settings['radius']=.6
        #self.settings['alternate12']=False
        #self.settings['alternate123']=False
        self.operateSettings.copy(self.restSettings)
        self.calculate()
        #self.settings['radius']=radius; self.settings['alternate12']=alternate12; self.settings['alternate123']=alternate123
        self.operateSettings.copy(self.guiSettings)
        if self.stopped is False:
            self.analog_output.StopTask()
        #self.EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(self.EveryNCallback_py)
        self.nSamples=int(self.sampsPerPeriod)
        #DAQmxRegisterEveryNSamplesEvent(self.analog_output.taskHandle,DAQmx_Val_Transferred_From_Buffer,self.nSamples,0,self.EveryNCallback,None)
        self.analog_output.CfgSampClkTiming("",self.sample_rate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.sampsPerPeriod)
        self.analog_output.WriteAnalogF64(self.sampsPerPeriod,0,-1,DAQmx_Val_GroupByChannel,self.data,byref(self.read),None)         
        self.analog_output.StartTask()
        self.stopped=False
       
    def stopAcquiring(self):
        #self.settings.d[0]['frequency']=0
        #self.settings.d[0]['radius']=.6
        #self.settings.d[0]['alternate12']=False
        #self.settings.d[0]['alternate123']=False
        print('stopped acquiring')
        self.analog_output.StopTask()
        self.calculate()
        self.createTask()
        self.startstop()
        self.acquiring=False
        self.finished_acquire_sig.emit()
"""