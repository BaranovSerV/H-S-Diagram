import numpy as np

from src.loader import SaturationLoader, IsobaricLoader, IsothermalLoader
from src.searcher import ThermodynamicSearch
from src.utils import linear_spline

class Renkine:
    def __init__(self):
        self.saturation_loader = SaturationLoader()
        self.isothermal_loader = IsothermalLoader()
        self.isobaric_loader = IsobaricLoader()

        self.T_saturation, self.S_saturation, self.H_saturation = self.saturation_loader.get_data()
        self.T_isothermal, self.S_isothermal, self.H_isothermal = self.isothermal_loader.get_data()
        (
            self.P_isobaric, 
            self.S_isobaric, 
            self.H_isobaric, 
            self.T_isobaric, 
            self.V_isobaric 
        ) = self.isobaric_loader.get_data()
        self.max_index = np.argmax(self.H_saturation) # Индекс критической точки

    def _get_nearest_point(self, S_saturation, H_saturation, S_iso, H_iso):
        min_distance = float('inf')
        nearest_point_S = None
        nearest_point_H = None

        for i in range(len(S_saturation)):
            H_iso_interp = linear_spline(S_saturation[i], S_iso, H_iso)
            if H_iso_interp is not None:
                distance = abs(H_saturation[i] - H_iso_interp)
            else:
                distance = float("inf")

            if distance < min_distance:
                min_distance = distance
                nearest_point_S = S_saturation[i]
                nearest_point_H = H_saturation[i]

        return nearest_point_S, nearest_point_H
    
    def _find_curve_isobaric(self, S_point, H_point):
        isobaric_search = ThermodynamicSearch(S_point, H_point, search_type='isobaric')

        index_isobar, isobar = isobaric_search.find_curve()

        return index_isobar, isobar
     
    def _find_curve_isothermal(self, S_point, H_point):
        isothermal_search = ThermodynamicSearch(S_point, H_point, search_type='isothermal')

        index_isotherm, isotherm = isothermal_search.find_curve()

        return index_isotherm, isotherm
    