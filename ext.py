

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class smart_slider:
    def __init__(self, msg, val_min, val_max, val_0, Nstep, callback):
        self.msg = msg
        self.val_min = val_min
        self.val_max = val_max
        self.Nstep = Nstep
        self.layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(self.Nstep)
        slider.setValue(self.val_to_i(val_0))
        slider.valueChanged.connect(callback)
        self.label = QLabel(self.msg + str(val_0))
        self.layout.addWidget(self.label)
        self.layout.addWidget(slider)      
    def update_label(self, val):
        self.label.setText(self.msg + f"{val:.2f}")  
    def val_to_i(self, val):
        return round( (val-self.val_min)/(self.val_max-self.val_min)*self.Nstep )
    def i_to_val(self, i):
        return self.val_min + i/self.Nstep * (self.val_max-self.val_min)