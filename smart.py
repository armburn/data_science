

# libraries :
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import sys
import os

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureWidget

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#
import settings
    

pd.options.mode.chained_assignment = None


class VALUES:
    def __init__(self, L_str, mode='statistique'):
        self.L_str = L_str
        self.selected_A = L_str[0]
        self.selected_B = L_str[0]
        self.mode = mode
      
class TheBrain:
    
    def __init__(self, db_name, Map, VAL, Ngrid):
        self.df = self.open_file(db_name)
        self.Ngrid = Ngrid
        self.val = None
        self.Map = Map
        self.VAL = VAL
        self.pos_0 = self.Map.get_pos()
        self.shape_0 = [self.Map.get_x_span(), self.Map.get_y_span()]
        self.scale = settings.scale_start
        self.threshold = settings.thresh_start
        self.prepare_grid()
        if settings.cheat:
            self.prepare_all_corr()
        
    def open_file(self, db_name):
        extension = db_name.split('.')[-1]
        if extension == 'csv':
            df = pd.read_csv(db_name)
        elif extension == 'xlsx' or extension == 'xls':
            df = pd.read_excel(db_name)
        elif extension == 'ods':
            df = pd.read_excel(db_name, engine='odf')
        else:
            raise ValueError("Extension de la base de donnée non prise en charge")
        return df
    
    def set_scale(self, new_scale):
        self.scale = new_scale
    def set_threshold(self, new_threshold):
        self.threshold = new_threshold
    def set_dot_size(self, new_size):
        self.Map.dot_size = new_size
    def rescale_Map(self):
        self.Map.set_x_span(self.shape_0[0] * self.scale)
        self.Map.set_y_span(self.shape_0[1] * self.scale)
    def extract_data(self):
        cond = self.df['population'] > self.threshold
        x = np.array(self.df['longitude'][cond])
        y = np.array(self.df['latitude'][cond])
        val = np.array(self.val[cond])
        return x, y, val
    
    def find_closest_city(self, pos, do_cond = 1):
        if do_cond == 1:
            cond = self.df['population'] > self.threshold
            x = self.df['longitude'][cond]
            y = self.df['latitude'][cond]
        else:
            x = self.df['longitude']
            y = self.df['latitude']
        m = (x-pos[0])*(x-pos[0]) + (y-pos[1])*(y-pos[1])
        return m.idxmin()
    def get_pos_info(self):
        i_city = self.find_closest_city(self.Map.get_pos())
        city = self.df["nom_commune_postal"].iloc()[i_city]
        # mode a :
        val_city = self.val[i_city]
        msg = f"Position : x = {self.Map.pos[0]}, "+ \
                         f"y = {self.Map.pos[1]} \t"+ \
                         f"Ville la plus proche : {city}, "+ \
                         f"VAL = {val_city}"
        return msg
    
    def prepare_grid(self):
        # on divise les coordonnées en N par N intervalles :
        self.df['x_grid'] = pd.cut(self.df['longitude'], bins=self.Ngrid)
        self.df['y_grid'] = pd.cut(self.df['latitude'], bins=self.Ngrid)
        # on enregistre les cases non vides :
        self.X_unique = self.df['x_grid'].unique()
        self.Y_unique = self.df['y_grid'].unique()
    def make_correlation(self):
        path = "correlations\\Ngrid_" + str(self.Ngrid)
        # indépendance de l'ordre : (1 seul file est utilisé)
        file1 = self.VAL.selected_A + '_' + self.VAL.selected_B + '.csv'
        file2 = self.VAL.selected_B + '_' + self.VAL.selected_A + '.csv'
        do_exist, file = self.check_files(path, file1, file2)
        # on efface les valeurs (ou on créé une colonne) :
        if do_exist:
            self.df['corr'] = pd.read_csv(file, na_values="\\N")
        else:
            self.df['corr'] = 0
            for x in self.X_unique:
                for y in self.Y_unique:
                    cond = (self.df.x_grid == x) & (self.df.y_grid == y)
                    M = self.df[cond][[self.VAL.selected_A, self.VAL.selected_B]].corr()
                    if np.isnan(M.iloc()[0][1]):
                        pass
                    else:
                        self.df['corr'][cond] = M.iloc()[0][1]
            print(file)
            self.df['corr'].to_csv(file, index=False, sep=",", na_rep="\\N")
    def check_files(self, path, file1, file2):
        script_rep = os.getcwd()
        project_rep = os.path.dirname(script_rep)
        path = project_rep + "\\correlations\\Ngrid_" + str(self.Ngrid)
        self.create_path(path)
        if os.path.exists(path + "\\" + file1):
            return True, path + "\\" + file1
        elif os.path.exists(path + "\\" + file2):
            return True, path + "\\" + file2
        else:
            return False, path + "\\" + file1
    def create_path(self, path):
        L = path.split("\\")
        new_path = L.pop(0)
        while new_path != path:
            if os.path.exists(new_path):
                new_path = new_path + "\\" + L.pop(0)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
    def prepare_all_corr(self):
        L = self.VAL.L_str.copy()
        for i in range(len(self.VAL.L_str)):
            for j in range(len(L)):
                self.VAL.selected_A = self.VAL.L_str[i]
                self.VAL.selected_B = L[j]
                self.make_correlation()
            L.pop(0)
        self.VAL.selected_A = self.VAL.L_str[0]
        self.VAL.selected_B = self.VAL.L_str[0]
            
    def update_val(self):
        if self.VAL.mode == 'statistique':
            val = self.df[self.VAL.selected_A].iloc()[:]
        elif self.VAL.mode == 'corrélation':
            self.make_correlation()
            val = self.df['corr']
        self.val = val
    

class MyMap:
    # x = longitude
    # y = latitude
    def __init__(self, pos, x_span, y_span):
        self.pos = pos # center of the map
        self.x_span = x_span
        self.y_span = y_span
        # on garde en memoire les données cartopy et geojson :
        self.feature_ocean = cfeature.OCEAN.with_scale('50m')
        self.feature_coast = cfeature.COASTLINE.with_scale('50m')
        self.feature_borders = cfeature.BORDERS.with_scale('50m')
        self.departements = gpd.read_file("contour-des-departements.geojson")
        self.departements = self.departements['geometry']
        self.dot_size = settings.dot_start
    def load_border(self):
        self.x_min = self.pos[0] - self.x_span/2
        self.x_max = self.pos[0] + self.x_span/2
        self.y_min = self.pos[1] - self.y_span/2
        self.y_max = self.pos[1] + self.y_span/2
    def get_border(self):
        self.load_border()
        return [self.x_min, self.x_max, self.y_min, self.y_max]    
    def get_axis(self, Nx=settings.Ngrad_x, Ny=settings.Ngrad_y):
        self.load_border()
        x_axis = np.linspace(self.x_min, self.x_max, Nx)
        y_axis = np.linspace(self.y_min, self.y_max, Ny)
        return [x_axis, y_axis]
    def get_pos(self):
        return self.pos
    def get_x_span(self):
        return self.x_span
    def get_y_span(self):
        return self.y_span
    def set_pos(self, new_pos):
        self.pos = new_pos
    def set_x_span(self, new_x_span):
        self.x_span = new_x_span
    def set_y_span(self, new_y_span):
        self.y_span = new_y_span

if __name__ == '__main__':
    pass