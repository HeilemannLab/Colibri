import colibriLib as clib

print ('no National Inatruments control card installed. Working in simulation mode!')

class GalvoDriver:
    '''
    
    '''
    #finished_acquire_sig=Signal()
    def __init__(self, settings):
        self.guiSettings=clib.Settings(0)
        self.guiSettings.copy(settings)
        self.restSettings=clib.Settings(0)
        self.restSettings.copy(settings)
        self.operateSettings=clib.Settings(0)
        self.operateSettings.copy(settings)
        self.sample_rate=1000000 # Maximum for the NI PCI-6733 is 1MHz.
        self.sampsPerPeriod=1 #dummy variable
        #self.calculate()
        #self.read = int32()
        #self.createTask()
        #self.hide()
        self.stopped=True
    
    def startStop(self, settings):
        if self.stopped:
            self.operateSettings.copy(settings)
            #self.analog_output.StartTask()
            self.stopped=False
            self.refresh(settings)
        else:
            self.operateSettings.copy(self.restSettings)
            #self.analog_output.StopTask()
            self.stopped=True
            self.refresh(settings)
            print('i have stopped running')
            
    def refresh(self, settings):
        if self.stopped is False:
            self.updateGuiSettings(settings)
            self.calculate()
            #self.analog_output.StopTask()
            #self.analog_output.CfgSampClkTiming("",self.sample_rate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.sampsPerPeriod)
            #self.analog_output.WriteAnalogF64(self.sampsPerPeriod,0,-1,DAQmx_Val_GroupByChannel,self.data,byref(self.read),None) 
            #self.analog_output.StartTask()
        else:
            self.updateGuiSettings(settings)
    
    def updateGuiSettings(self, settings):
        self.guiSettings.copy(settings)

    def calculate(self):
        print ('i am running')
        #sinwave,coswave,camera_ttl,blue_laser_ttl, green_laser_ttl=self.getSinCosTTL(self.operateSettings['frequency'],self.operateSettings['radius'],self.operateSettings['ellipticity'],self.operateSettings['phase'],self.operateSettings['x_shift'],self.operateSettings['y_shift'])
        #self.data=np.concatenate((sinwave,coswave,camera_ttl,blue_laser_ttl,green_laser_ttl))
        #self.sampsPerPeriod=len(sinwave)

'''
    def getSinCosTTL(self,frequency,radius,ellipticity,phase,x_shift,y_shift,blue_laser,green_laser,blue_laser_power,green_laser_power,period=.005):
        # The period argument is only used when the value of the frequency is 0
        if frequency==0:
            t=np.arange(0,period,1/self.sample_rate)
            sinwave=radius*np.sin(np.zeros(len(t)))+x_shift/1000
            coswave=(ellipticity*radius*np.cos(np.zeros(len(t))+phase*(2*np.pi/360)))+(y_shift/1000)
        else:
            period=1/frequency
            t=np.arange(0,period,1/self.sample_rate )
            sinwave=radius*np.sin(frequency*(t*(2*np.pi)))+x_shift/1000
            coswave=(ellipticity*radius*np.cos(frequency*t*2*np.pi+phase*(2*np.pi/360)))+(y_shift/1000)
            camera_ttl=np.zeros(len(t))
            camera_ttl[0]=5
        camera_ttl=np.zeros(len(t))
        camera_ttl[0]=5
        if blue_laser:
            blue_laser_ttl=blue_laser_power*np.ones(len(t))
            #a=len(t)
            #blue_laser_ttl[a/8:3*a/8]=blue_laser_power #right
            #blue_laser_ttl[3*a/8:5*a/8]=blue_laser_power #bottom
            #blue_laser_ttl[5*a/8:7*a/8]=blue_laser_power #left
            #blue_laser_ttl[:a/8]=blue_laser_power; blue_laser_ttl[7*a/8:]=blue_laser_power #top
            
        else:
            blue_laser_ttl=-.08*np.ones(len(t))
        if green_laser:
            green_laser_ttl=green_laser_power*np.ones(len(t)) #0V is on for green laser
        else:
            green_laser_ttl=-.08*np.ones(len(t)) #5V is off for green laser
        return sinwave,coswave,camera_ttl, blue_laser_ttl, green_laser_ttl
        
        
    def createTask(self):
        self.analog_output = Task()
        self.analog_output.CreateAOVoltageChan("Dev1/ao0","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao2 is pin 57 and ground is 56
        self.analog_output.CreateAOVoltageChan("Dev1/ao1","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao3 is pin 25 and ground is 24
        """self.analog_output.CreateAOVoltageChan("Dev2/ao4","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao4 is pin 60 and ground is 59"""
        """self.analog_output.CreateAOVoltageChan("Dev2/ao5","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao5 is pin 28 and ground is 29. This is blue laser"""
        """self.analog_output.CreateAOVoltageChan("Dev2/ao6","",-10.0,10.0,DAQmx_Val_Volts,None) #On the NI PCI-6733, ao6 is pin 30 and ground is 31. This is green laser"""


                        #  CfgSampClkTiming(source, rate, activeEdge, sampleMode, sampsPerChan)
        self.analog_output.CfgSampClkTiming("",self.sample_rate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.sampsPerPeriod)
                        #  WriteAnalogF64(numSampsPerChan, autoStart, timeout, dataLayout, writeArray, sampsPerChanWritten, reserved)
        self.analog_output.WriteAnalogF64(self.sampsPerPeriod,0,-1,DAQmx_Val_GroupByChannel,self.data,byref(self.read),None) 
        self.analog_output.StartTask()
        self.stopped=False
        self.acquiring=False
        '''
    