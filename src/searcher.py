import numpy as np
from scipy.interpolate import interp1d

from src.loader import IsothermalLoader, IsobaricLoader
from src.utils import linear_spline


class ThermodynamicSearch:
    def __init__(self, S_target, H_target, search_type):
        self.S_target = S_target
        self.H_target = H_target
        self.search_type = search_type
        
        self.loader = self._get_loader()
        self.data = self.loader.get_data()

        self._process_and_normalize_data()

    def _get_loader(self):
        if self.search_type == 'isothermal':
            return IsothermalLoader()
        elif self.search_type == 'isobaric':
            return IsobaricLoader()
        

    def _find_curve(self, S_data, H_data, curve_type):
        min_distance = float('inf')
        curve = None
        index = -1

        for i in range(len(S_data)):
            S_curve = S_data[i]
            H_curve = H_data[i]

            H_i = linear_spline(self.S_target, S_curve, H_curve)
            if H_i is not None:
                distance = np.abs(H_i - self.H_target)
            else:
                distance = float("inf")

            if distance < min_distance:
                min_distance = distance
                index = i
                if curve_type == 'isothermal':
                    curve = self.T_isothermal[i]
                elif curve_type == 'isobaric':
                    curve = self.P_isobaric[i] 

        return index, curve  
        
    def find_curve(self):
        if self.search_type == 'isothermal':
            return self._find_curve(self.S_isothermal, self.H_isothermal, 'isothermal')
        else:
            return self._find_curve(self.S_isobaric, self.H_isobaric, 'isobaric')
        
    def _process_and_normalize_data(self):
        if self.search_type == 'isothermal':
            self.T_isothermal, self.S_isothermal, self.H_isothermal = self.data
        else:
            self.P_isobaric, self.S_isobaric, self.H_isobaric, self.T_isobaric, self.V_isobaric = self.data
