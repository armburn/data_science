

# libraries :
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureWidget
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# 
from smart import *
from search_window import SearchWindow
import ext

        
class MaFenetre(QWidget):
    def __init__(self, Brain):
        super().__init__()
        self.Brain = Brain        
        self.setWindowTitle('Correlacum')
        self.resize(settings.width, settings.height)
        self.Brain.update_val()
        self.create_plot_object()
        self.create_puzzle_pieces()
        self.update_figure()
        self.make_puzzle()
        
    def create_plot_object(self):
        self.map_fig = plt.figure(figsize=(10, 4))
        self.map_fig.subplots_adjust(left=0.05, right=0.98, top=1, bottom=0)
        self.map_ax = self.map_fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.cbar_fig = plt.figure(figsize=(1, 4))
        self.cbar_ax = self.cbar_fig.add_axes([0.1, 0.1, 0.5, 0.8])  
    def create_puzzle_pieces(self):
        self.line_1 = self.create_line_1(self.mode_changed,
                                         self.Brain.VAL.L_str,
                                         self.changed_A,
                                         self.changed_B)
        self.line_2 = self.create_line_2(self.map_fig, 
                                         self.cbar_fig, 
                                         self.on_click)
        
        self.line_3 = self.create_line_3(self.Brain.get_pos_info,
                                         self.open_search_window)
        self.line_4 = self.create_line_4(self.scale_changed, 
                                         self.threshold_changed, 
                                         self.dot_changed)
    def make_puzzle(self):
        self.parent_layout = QVBoxLayout()
        self.layout1H = QHBoxLayout() # ligne 1
        self.layout2H = QHBoxLayout() # ligne 2
        self.layout3H = QHBoxLayout() # ligne 3
        self.layout4V = QVBoxLayout() # ligne 4
        self.layout1H.addWidget(self.line_1.mode_selecter)
        self.layout1H.addLayout(self.line_1.value_selecter_per_mode)
        self.layout2H.addWidget(self.line_2.map_widget)
        self.layout2H.addWidget(self.line_2.cbar_widget)
        self.layout3H.addWidget(self.line_3.label)
        self.layout3H.addWidget(self.line_3.spacer)
        self.layout3H.addWidget(self.line_3.search_button)
        self.layout4V.addLayout(self.line_4.scale_slider.layout)
        self.layout4V.addLayout(self.line_4.threshold_slider.layout)
        self.layout4V.addLayout(self.line_4.dot_slider.layout)
        self.parent_layout.addLayout(self.layout1H)
        self.parent_layout.addLayout(self.layout2H)
        self.parent_layout.addLayout(self.layout3H)
        self.parent_layout.addLayout(self.layout4V)
        # strech horizontal sur ligne 2 :
        self.layout2H.setStretch(0, 7)
        self.layout2H.setStretch(1, 1)
        # strech horizontal sur ligne 3 :
        self.layout3H.setStretch(0, 5)
        self.layout3H.setStretch(1, 1)
        self.layout3H.setStretch(2, 1)
        # strech vertical sur ligne 2 :
        self.parent_layout.setStretch(0, 1)
        self.parent_layout.setStretch(1, 7)
        self.parent_layout.setStretch(2, 1)
        self.parent_layout.setStretch(3, 1)
        self.setLayout(self.parent_layout)    
    class create_line_1:
        def __init__(self, mode_changed, L_str, changed_A, changed_B):
            self.mode_selecter = QComboBox()
            self.mode_selecter.addItems(['statistique', 'corrélation'])
            self.mode_selecter.currentTextChanged.connect( mode_changed )
                # stackedLayout permet de changer le layout avec un callback
            self.value_selecter_per_mode = QStackedLayout()
            mode_stat = QWidget()
            mode_corr = QWidget()
            layout_stat = QHBoxLayout()
            layout_corr = QHBoxLayout()
                # version statistique du stackedLayout :
            stat_label = QLabel('VAL = ')
            stat_label.setAlignment(Qt.AlignCenter)
            stat_selecter = QComboBox()
            stat_selecter.addItems( L_str )
            stat_selecter.currentTextChanged.connect( changed_A )
            stat_spacer = QWidget()
            layout_stat.addWidget(stat_label)
            layout_stat.addWidget(stat_selecter)
            layout_stat.addWidget(stat_spacer)
            mode_stat.setLayout(layout_stat)
            self.value_selecter_per_mode.addWidget(mode_stat)
                # version corrélation du stackedLayout :
            corr_label = QLabel('VAL = local corr between')
            corr_label.setAlignment(Qt.AlignCenter)
            corr_selecter_A = QComboBox()
            corr_selecter_A.addItems( L_str )
            corr_selecter_A.currentTextChanged.connect( changed_A )
            corr_selecter_B = QComboBox()
            corr_selecter_B.addItems( L_str )
            corr_selecter_B.currentTextChanged.connect( changed_B )
            layout_corr.addWidget(corr_label)
            layout_corr.addWidget(corr_selecter_A)
            layout_corr.addWidget(corr_selecter_B)
            mode_corr.setLayout(layout_corr)
            self.value_selecter_per_mode.addWidget(mode_corr)
    class create_line_2:
        def __init__(self, map_fig, cbar_fig, on_click):
            self.map_widget = FigureWidget(map_fig)
            self.cbar_widget = FigureWidget(cbar_fig)
            map_fig.canvas.mpl_connect('button_press_event', on_click)       
    class create_line_3:
        def __init__(self, get_pos_info, open_search_window):
            msg = get_pos_info()
            self.label = QLabel(msg)
            self.spacer = QWidget()
            self.search_button = QPushButton("Rechercher")
            self.search_button.clicked.connect(open_search_window)
    class create_line_4:
        def __init__(self, scale_changed, threshold_changed, dot_changed):
            self.scale_slider = ext.smart_slider("Scale = ",
                                                 settings.scale_min,
                                                 settings.scale_max,
                                                 settings.scale_start,
                                                 settings.scale_N,
                                                 scale_changed )
            self.threshold_slider = ext.smart_slider("Threshold on population = ",
                                                    settings.thresh_min,
                                                    settings.thresh_max,
                                                    settings.thresh_start,
                                                    settings.thresh_N,
                                                    threshold_changed )
            self.dot_slider = ext.smart_slider("Dot size = ", 
                                               settings.dot_min,
                                               settings.dot_max,
                                               settings.dot_start,
                                               settings.dot_N,
                                               dot_changed )
    def update_figure(self):
        x, y, val = self.Brain.extract_data()
        self.map_ax.clear()
        self.cbar_ax.clear()
        border = self.Brain.Map.get_border()
        self.map_ax.set_extent(border)
        self.map_ax.add_feature(self.Brain.Map.feature_coast)
        self.map_ax.add_feature(self.Brain.Map.feature_ocean)
        self.map_ax.add_feature(self.Brain.Map.feature_borders, linestyle=':')
        self.map_ax.add_geometries(self.Brain.Map.departements, crs=ccrs.PlateCarree(),
                               edgecolor=settings.dep_color, facecolor='none', 
                               linewidth=settings.dep_linewidth, 
                               linestyle=settings.dep_linestyle)
        center = self.Brain.Map.get_pos()
        self.map_ax.plot(center[0], center[1], 
                         settings.center_color, 
                         linewidth=settings.center_linewidth)
        scatter = self.map_ax.scatter(x ,y , c=val,
                             cmap=settings.colormap[self.Brain.VAL.mode], 
                             norm=settings.cmap_norm[self.Brain.VAL.mode], marker='o',
                             s = self.Brain.Map.dot_size)
        axis = self.Brain.Map.get_axis()
        self.map_ax.set_xticks(axis[0])
        self.map_ax.set_yticks(axis[1])
        cbar = plt.colorbar(scatter, cax=self.cbar_ax)
        cbar.set_label('Valeurs de VAL')
        self.line_2.map_widget.draw_idle()
        self.line_2.cbar_widget.draw_idle()        
    # CALLBACKS :
    def on_click(self, event):
        if event.inaxes == self.map_ax:
            x, y = self.map_ax.projection.transform_point(event.xdata, event.ydata, ccrs.PlateCarree())
            self.Brain.Map.set_pos((x, y))
            self.update_info_and_fig()
    def mode_changed(self, s):
        self.Brain.VAL.mode = s
        self.line_1.value_selecter_per_mode.setCurrentIndex(self.line_1.mode_selecter.currentIndex())
        self.Brain.update_val()
        self.update_info_and_fig()
    def changed_A(self, s): 
        self.Brain.VAL.selected_A = s
        self.Brain.update_val()
        self.update_info_and_fig()
    def changed_B(self, s): 
        self.Brain.VAL.selected_B = s
        self.Brain.update_val()
        self.update_info_and_fig()
    def scale_changed(self, i):
        self.Brain.set_scale(self.line_4.scale_slider.i_to_val(i) )
        self.Brain.rescale_Map()
        self.update_figure()
        self.line_4.scale_slider.update_label(self.Brain.scale)   
    def threshold_changed(self, i):
        self.Brain.set_threshold(self.line_4.threshold_slider.i_to_val(i) )
        self.line_4.threshold_slider.update_label(self.Brain.threshold)
        self.update_figure()    
    def dot_changed(self, i):
        self.Brain.set_dot_size(self.line_4.dot_slider.i_to_val(i) )
        self.line_4.dot_slider.update_label(self.Brain.Map.dot_size)
        self.update_figure()
        
    def update_info_and_fig(self):
        msg = self.Brain.get_pos_info()
        self.line_3.label.setText(msg)
        self.update_figure()
        
    def open_search_window(self):
        self.search_window = SearchWindow(self.Brain, self.update_info_and_fig)
        self.search_window.show()
        
    def closeEvent(self, event):
        if hasattr(self, 'search_window') and self.search_window:
            self.search_window.close()
        event.accept()


if __name__ == '__main__': 
    pass
