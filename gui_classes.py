##############################################################################
####   GRAPHICAL USER INTERFACE ##############################################
##############################################################################
import math
import matplotlib.pyplot as plt

class SliderBox:
    '''SliderLabel is a widget containing a QSlider and a QSpinBox (or QDoubleSpinBox if decimals are required)
    The QSlider and SpinBox are connected so that a change in one causes the other to change. 
    '''
    #changeSignal=Signal(int)
    def __init__(self,minValue,maxValue,factor): #decimals specifies the resolution of the slider.  0 means only integers,  1 means the tens place, etc.
        self.minValue=minValue
        self.maxValue=maxValue
        self.boxValue=0
        self.sliderValue=0
        self.factor=float(factor)
    
    def checkValue(self, value):
        i=1;
        if value<self.minValue:
            i-=1
        if value>self.maxValue:
            i-=1
        return i
    
    def changeSliderValue(self, sValue):
        value=sValue*self.factor
        if self.checkValue(value)<1:
            print ('Error value out of bounds.')
        else:
            self.boxValue=float(value)
            self.sliderValue=float(sValue)
        return [self.boxValue, self.sliderValue]
        
    def changeBoxValue(self, value):
        if self.checkValue(value)<1:
            print ('Error value out of bounds.')
        else:
            self.boxValue=float(value)
            self.sliderValue=value/self.factor
        return [self.boxValue, self.sliderValue]
        
class BFP:
    ''' This class visualizes the illumination of the back focal plane. '''
    def __init__(self):
        self.radius=0.0
        self.ellipticity=0.0
        self.phase=0.0
        self.xShift=0.0
        self.yShift=0.0
        self.steps=360
        self.phi=[]
        self.x=[]
        self.y=[]
        self.initAngle()
        
    def setValues(self, r, e, p, dx, dy):
        self.radius=float(r)
        self.ellipticity=float(e)
        self.phase=float(p)
        self.xShift=float(dx*3.0/1000)
        self.yShift=float(dy*3.0/1000)
        
    def initAngle(self):
        for i in range (0,self.steps):
            self.phi.append(-90.0+i)
            self.x.append(0)
            self.y.append(0)
        
    def funcMirror(self):
        for i in range(len(self.phi)):
            self.x[i]=self.xShift+(self.radius*math.sin(math.radians(self.phi[i])))
            self.y[i]=self.yShift+(self.radius*self.ellipticity*math.sin(math.radians(self.phi[i]+self.phase)))

    def definePlot(self):
        fig=plt.figure(1)
        plt.clf()
        ax = plt.axes()
        ax.set_aspect(1)
        plt.plot (self.x,self.y,'b-',linewidth=3.0)
        plt.xlim(-3,3)
        plt.ylim(-3,3)
        plt.xlabel('x [a.u.]')
        plt.ylabel('y [a.u.]')
        plt.axis('off')
        plt.title('bfp-illumination')
        return fig
        

        