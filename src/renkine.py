import numpy as np
import pandas as pd
from IPython.display import display

from scipy.interpolate import interp1d
from src.loader import SaturationLoader, IsobaricLoader, IsothermalLoader, RenkineLoader
from src.searcher import ThermodynamicSearch


def linear_spline(x, x_list, y_list):
    n = len(x_list) - 1
    for i in range(n):
        if x_list[i] <= x <= x_list[i + 1]:
            return (
                y_list[i] + (y_list[i + 1] - y_list[i]) * 
                (x - x_list[i]) / (x_list[i + 1] - x_list[i])
            )
    raise ValueError(f"Точка {x} находится вне диапазона интерполяции")


class Renkine:
    def __init__(self, S_5_point, H_5_point):
        self.S_5_point = S_5_point
        self.H_5_point = H_5_point

        self.saturation_loader = SaturationLoader()
        self.isothermal_loader = IsothermalLoader()
        self.isobaric_loader = IsobaricLoader()

        self.T_saturation, self.S_saturation, self.H_saturation = self.saturation_loader.get_data()
        self.T_isothermal, self.S_isothermal, self.H_isothermal = self.isothermal_loader.get_data()
        self.P_isobaric, self.S_isobaric, self.H_isobaric = self.isobaric_loader.get_data()

    def renkine_data(self):
        self._point_5()
        self._point_6()
        self._point_1()
        self._point_2()
        self._point_3_and_4()

        loader = RenkineLoader()
        loader.load_data(
            [self.S_1_point, self.S_2_point, self.S_3_point, self.S_4_point, self.S_5_point, self.S_6_point],
            [self.H_1_point, self.H_2_point, self.H_3_point, self.H_4_point, self.H_5_point, self.H_6_point],
            [self.P_1_point, self.P_2_point, self.P_3_point, self.P_4_point, self.P_5_point, self.P_6_point],
            [self.T_1_point, self.T_2_point, self.T_3_point, self.T_4_point, self.T_5_point, self.T_6_point]
        )
        
        data = {
            "Точка": ["1", "2", "3", "4", "5", "6"],
            "P (бар)": [
                self.P_1_point, 
                self.P_2_point, 
                self.P_3_point, 
                self.P_4_point, 
                self.P_5_point, 
                self.H_6_point
            ],
            "T (°C)": [
                self.T_1_point,
                self.T_2_point,
                self.T_3_point,
                self.T_4_point,
                self.T_5_point,
                self.T_6_point
            ],
            "H (кДж/кг)": [
                self.H_1_point,
                self.H_2_point,
                self.H_3_point,
                self.H_4_point,
                self.H_5_point,
                self.H_6_point
            ],
            "S (кДж/кг·K)": [
                self.S_1_point,
                self.S_2_point,
                self.S_3_point,
                self.S_4_point,
                self.S_5_point,
                self.S_6_point
            ],
            "Техническое устройство": [
                "После конденсатора перед поступлением в насос ", 
                "После насоса перед котлом", 
                "В котле", 
                "После котла, перед перегревом в пароперегревателе", 
                "После перегрева, перед турбиной ", 
                "После турбины, перед конденсатором"
            ],
        }

        df = pd.DataFrame(data)
        display(df)

        return (
            self.S_1_point, self.H_1_point, self.P_1_point, self.T_1_point,
            self.S_2_point, self.H_2_point, self.P_2_point, self.T_2_point,
            self.S_3_point, self.H_3_point, self.P_3_point, self.T_3_point,
            self.S_4_point, self.H_4_point, self.P_4_point, self.T_4_point,
            self.S_5_point, self.H_5_point, self.P_5_point, self.T_5_point,
            self.S_6_point, self.H_6_point, self.P_6_point, self.T_6_point,
        )
    
    def renkine_params(self):
        A_nasos = self.H_2_point - self.H_1_point
        A_turbine = self.H_5_point - self.H_6_point
        n_RENKINE = (A_turbine - A_nasos) / (self.H_5_point - self.H_2_point)
        n_KARNO = 1 - (self.T_1_point + 273.15) / (self.T_5_point + 273.15)
        
        params = {
            "Параметр": ["Работа насоса кДж/кг", "Работа турбинык кДж/кг", "КПД Реникина", "КПД Карно"],
            "Значение": [A_nasos, A_turbine, n_RENKINE, n_KARNO]
        }
        df_params = pd.DataFrame(params)
        display(df_params)

    def _point_5(self):
        print(f"Расчет точки 5...")
        (
            self.index_5_isobar, 
            self.index_5_isotherm, 
            self.P_5_point, 
            self.T_5_point 
        ) = self._find_curve(self.S_5_point, self.H_5_point)
        print(f"Точка 5 расчитана")
        return self.S_5_point, self.H_5_point, self.P_5_point, self.T_5_point

    def _point_6(self):
        self.S_6_point = self.S_5_point
        self.H_6_point = linear_spline(self.S_5_point, self.S_saturation, self.H_saturation)
        
        print(f"Расчет точки 6...")
        (
            self.index_6_isobar, 
            self.index_6_isotherm, 
            self.P_6_point, 
            self.T_6_point 
        ) = self._find_curve(self.S_6_point, self.H_6_point)
        print(f"Точка 6 расчитана")
        return self.S_6_point, self.H_6_point, self.P_6_point, self.T_6_point

    def _point_1(self):
        self.T_1_point = self.T_6_point
        self.P_1_point = self.T_6_point

        print(f"Расчет точки 1...")
        self.S_1_point, self.H_1_point = self._get_nearest_point(
            self.S_saturation, 
            self.H_saturation, 
            self.S_isothermal[self.index_6_isotherm], 
            self.H_isothermal[self.index_6_isotherm]
        )
        print(f"Точка 1 расчитана")
        return self.S_1_point, self.H_1_point, self.P_1_point, self.T_1_point

    def _point_2(self):
        S = np.array(self.S_isobaric[self.index_5_isobar])
        H = np.array(self.H_isobaric[self.index_5_isobar])

        self.P_2_point = self.P_5_point
        self.S_2_point = self.S_1_point
        self.H_2_point = linear_spline(self.S_2_point, S, H)

        print(f"Расчет точки 2...")
        (
            self.index_2_isobar, 
            self.index_2_isotherm, 
            P, 
            self.T_2_point 
        ) = self._find_curve(self.S_2_point, self.H_2_point)
        print(f"Точка 2 расчитана")

        return self.S_2_point, self.H_2_point, self.P_2_point, self.T_2_point + 5

    def _point_3_and_4(self):
        self.P_3_point = self.P_5_point
        self.P_4_point = self.P_5_point

        print(f"Расчет точки 3 и 4...")
        max_index = np.argmax(self.H_saturation)

        self.S_3_point, self.H_3_point = self._get_nearest_point(
            self.S_saturation, self.H_saturation, 
            self.S_isobaric[self.index_5_isobar][:max_index], 
            self.H_isobaric[self.index_5_isobar][:max_index]
        )

        self.S_4_point, self.H_4_point = self._get_nearest_point(
            self.S_saturation, self.H_saturation, 
            self.S_isobaric[self.index_5_isobar][max_index:], 
            self.H_isobaric[self.index_5_isobar][max_index:]
        )

        (
            self.index_3_isobar, 
            self.index_3_isotherm, 
            P, 
            self.T_3_point 
        ) = self._find_curve(self.S_3_point, self.H_3_point)
        self.T_4_point = self.T_3_point

        print(f"Точка 3 и 4 расчитаны")
        return (
            self.S_3_point, self.H_3_point, self.P_3_point, self.T_3_point, 
            self.S_4_point, self.H_4_point, self.P_4_point, self.T_4_point
        )
    
    def _get_nearest_point(self, S_saturation, H_saturation, S_iso, H_iso):
        interp_func = interp1d(S_iso, H_iso, kind='linear', fill_value="extrapolate")

        min_distance = float('inf')
        nearest_point_S = None
        nearest_point_H = None

        for i in range(len(S_saturation)):
            H_isotherm_interp = interp_func(S_saturation[i])
            distance = abs(H_saturation[i] - H_isotherm_interp)

            if distance < min_distance:
                min_distance = distance
                nearest_point_S = S_saturation[i]
                nearest_point_H = H_saturation[i]

        return nearest_point_S, nearest_point_H
    
    def _find_curve(self, S_point, H_point):
        isothermal_search = ThermodynamicSearch(S_point, H_point, search_type='isothermal')
        isobaric_search = ThermodynamicSearch(S_point, H_point, search_type='isobaric')

        index_isobar, isobar = isobaric_search.find_curve()
        index_isotherm, isotherm = isothermal_search.find_curve()

        return index_isobar, index_isotherm, isobar, isotherm