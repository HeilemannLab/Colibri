##
##  mainwindow.py
##  LAMA
##
##  Created by Sebastian Malkusch on 10.06.15.
##  <malkusch@chemie.uni-frankfurt.de>
##  Copyright (c) 2015 Single Molecule Biophysics. All rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import uic, QtGui
from PyQt4.QtCore import *
import colibriLib as clib
import gui_classes as guic
import galvoControl as gc
'''
try:
    import galvoControl as gc
except:
    import simGalvoControl as gc
'''
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

( Ui_MainWindow, QMainWindow ) = uic.loadUiType( 'gui.ui' )
    
class MainWindow ( QMainWindow ):
    """MainWindow inherits QMainWindow"""

    def __init__ ( self, parent = None ):
        QMainWindow.__init__( self, parent )
        self.toolbox = QtGui.QToolBox(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        #initialize settings
        self.settings=[clib.Settings(0), clib.Settings(1), clib.Settings(2), clib.Settings(3)]
        # initialize Galvo Control
        self.galvoControl = gc.GalvoDriver(self.settings[0])
        # GUI types
        self.frequencySB=guic.SliderBox(0.0, 500.0, 1)
        self.radiusSB=guic.SliderBox(0.0, 0.6, 0.001)
        self.ellipticitySB=guic.SliderBox(0.0, 2.5, 0.01)
        self.phaseSB=guic.SliderBox(0, 180.0, 1)
        self.xShiftSB=guic.SliderBox(-1000.0, 1000.0, 1)
        self.yShiftSB=guic.SliderBox(-1000.0, 1000.0, 1)
        self.bfp=guic.BFP()
        self.refreshGui()
        
        
        # Change sliders
        self.ui.horizontalSlider_1.valueChanged.connect(lambda: self.refreshColibri(0, 'frequency'))
        self.ui.horizontalSlider_2.valueChanged.connect(lambda: self.refreshColibri(0, 'radius'))
        self.ui.horizontalSlider_3.valueChanged.connect(lambda: self.refreshColibri(0, 'ellipticity'))
        self.ui.horizontalSlider_4.valueChanged.connect(lambda: self.refreshColibri(0, 'phase'))
        self.ui.horizontalSlider_5.valueChanged.connect(lambda: self.refreshColibri(0, 'x_shift'))
        self.ui.verticalSlider_1.valueChanged.connect(lambda: self.refreshColibri(0, 'y_shift'))
        #Change Boxes
        self.ui.doubleSpinBox_1.valueChanged.connect(lambda: self.refreshColibri(1, 'frequency'))
        self.ui.doubleSpinBox_2.valueChanged.connect(lambda: self.refreshColibri(1, 'radius'))
        self.ui.doubleSpinBox_3.valueChanged.connect(lambda: self.refreshColibri(1, 'ellipticity'))
        self.ui.doubleSpinBox_4.valueChanged.connect(lambda: self.refreshColibri(1, 'phase'))
        self.ui.doubleSpinBox_5.valueChanged.connect(lambda: self.refreshColibri(1, 'x_shift'))
        self.ui.doubleSpinBox_6.valueChanged.connect(lambda: self.refreshColibri(1, 'y_shift'))
        # Memorize
        self.ui.pushButton_01.clicked.connect(lambda: self.store(1))
        self.ui.pushButton_03.clicked.connect(lambda: self.store(2))
        self.ui.pushButton_05.clicked.connect(lambda: self.store(3))
        # Recall
        self.ui.pushButton_02.clicked.connect(lambda: self.recall(1))
        self.ui.pushButton_04.clicked.connect(lambda: self.recall(2))
        self.ui.pushButton_06.clicked.connect(lambda: self.recall(3))
        #load session
        self.ui.pushButton_07.clicked.connect(self.loadSettings)
        #save Session
        self.ui.pushButton_08.clicked.connect(self.saveSettings)
        #Start Storp Galvo
        self.ui.pushButton_09.clicked.connect(self.run)
        #Quit
        self.ui.quitButton.clicked.connect(self.quitColibri)
    # setters getters

    # functions
    def refreshColibri(self, changeType, changeKey):
        if changeType==0:
            self.refreshSliderSettings(changeKey)
        if changeType==1:
                self.refreshBoxSettings(changeKey)
        self.refreshGui()
        self.galvoControl.refresh(self.settings[0])
        
    def refreshSliderSettings(self, changeKey):
        if changeKey == 'frequency':
                self.settings[0].__setitem__('frequency',self.frequencySB.changeSliderValue(self.ui.horizontalSlider_1.value())[0])
        elif changeKey =='radius':
            self.settings[0].__setitem__('radius',self.radiusSB.changeSliderValue(self.ui.horizontalSlider_2.value())[0])
        elif changeKey =='ellipticity':
            self.settings[0].__setitem__('ellipticity',self.ellipticitySB.changeSliderValue(self.ui.horizontalSlider_3.value())[0])
        elif changeKey =='phase':
            self.settings[0].__setitem__('phase',self.phaseSB.changeSliderValue(self.ui.horizontalSlider_4.value())[0])
        elif changeKey =='x_shift':
            self.settings[0].__setitem__('x_shift',self.xShiftSB.changeSliderValue(self.ui.horizontalSlider_5.value())[0])
        elif changeKey =='y_shift':
            self.settings[0].__setitem__('y_shift',self.yShiftSB.changeSliderValue(self.ui.verticalSlider_1.value())[0])
    
    def refreshBoxSettings(self, changeKey):
        if changeKey == 'frequency':
            self.settings[0].__setitem__('frequency',self.frequencySB.changeBoxValue(self.ui.doubleSpinBox_1.value())[0])
        elif changeKey =='radius':
            self.settings[0].__setitem__('radius',self.radiusSB.changeBoxValue(self.ui.doubleSpinBox_2.value())[0])
        elif changeKey =='ellipticity':
            self.settings[0].__setitem__('ellipticity',self.ellipticitySB.changeBoxValue(self.ui.doubleSpinBox_3.value())[0])
        elif changeKey =='phase':
            self.settings[0].__setitem__('phase',self.phaseSB.changeBoxValue(self.ui.doubleSpinBox_4.value())[0])
        elif changeKey =='x_shift':
            self.settings[0].__setitem__('x_shift',self.xShiftSB.changeBoxValue(self.ui.doubleSpinBox_5.value())[0])
        elif changeKey =='y_shift':
            self.settings[0].__setitem__('y_shift',self.yShiftSB.changeBoxValue(self.ui.doubleSpinBox_6.value())[0])

    def refreshGui(self):
        self.ui.horizontalSlider_1.setValue(self.settings[0].__getitem__('frequency'))
        self.ui.doubleSpinBox_1.setValue(self.settings[0].__getitem__('frequency'))
        self.ui.horizontalSlider_2.setValue(self.settings[0].__getitem__('radius')*1000)
        self.ui.doubleSpinBox_2.setValue(self.settings[0].__getitem__('radius'))
        self.ui.horizontalSlider_3.setValue(self.settings[0].__getitem__('ellipticity')*100)
        self.ui.doubleSpinBox_3.setValue(self.settings[0].__getitem__('ellipticity'))
        self.ui.horizontalSlider_4.setValue(self.settings[0].__getitem__('phase'))
        self.ui.doubleSpinBox_4.setValue(self.settings[0].__getitem__('phase'))
        self.ui.horizontalSlider_5.setValue(self.settings[0].__getitem__('x_shift'))
        self.ui.doubleSpinBox_5.setValue(self.settings[0].__getitem__('x_shift'))
        self.ui.verticalSlider_1.setValue(self.settings[0].__getitem__('y_shift'))
        self.ui.doubleSpinBox_6.setValue(self.settings[0].__getitem__('y_shift'))
        self.plotBFP()

    def recall(self,i):
        '''i is the setting number we are recalling. settings[0] is always the current setting.'''
        self.settings[0].copy(self.settings[i])
        for key in self.settings[0].keys():
            self.refreshGui()

        
    def store(self,i):
        '''i is the setting number we are storing.  settings[0] is always the current setting.'''
        self.settings[i].copy(self.settings[0])
        
    def plotBFP(self):
        r=self.settings[0].__getitem__('radius')
        e=self.settings[0].__getitem__('ellipticity')
        p=self.settings[0].__getitem__('phase')
        dx=self.settings[0].__getitem__('x_shift')
        dy=self.settings[0].__getitem__('y_shift')
        self.bfp.setValues(r, e, p, dx, dy)
        self.bfp.funcMirror()
        figure=self.bfp.definePlot()
        scene = QtGui.QGraphicsScene()
        canvas = FigureCanvas(figure)
        canvas.setGeometry(0, 0, 189, 189)
        scene.addWidget(canvas)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.show()
  
  
    def loadSettings(self):
        self.settings[0].load()
        self.refreshGui()
    
    def saveSettings(self):
        self.settings[0].save()
        
    def run(self):
        self.galvoControl.startStop(self.settings[0])
        #print (self.galvoControl.operateSettings.__getitem__('frequency'))
        #print (self.galvoControl.operateSettings.__getitem__('radius'))
        #print (self.galvoControl.operateSettings.__getitem__('ellipticity'))
        #print (self.galvoControl.operateSettings.__getitem__('phase'))
        #print (self.galvoControl.operateSettings.__getitem__('x_shift'))
        #print (self.galvoControl.operateSettings.__getitem__('y_shift'))
        if self.galvoControl.stopped is True:
            self.ui.pushButton_09.setText('Start')
        else:
            self.ui.pushButton_09.setText('Stop')

        
    def quitColibri(self):
        raise SystemExit