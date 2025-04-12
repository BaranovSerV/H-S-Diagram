import numpy as np
from scipy.interpolate import interp1d
from sklearn.preprocessing import MinMaxScaler

from src.loader import IsothermalLoader, IsobaricLoader


class ThermodynamicSearch:
    def __init__(self, S_target, H_target, search_type):
        self.S_target = S_target
        self.H_target = H_target
        self.search_type = search_type
        
        self.loader = self._get_loader()
        self.data = self.loader.get_data()

        self.scaler_S = MinMaxScaler()
        self.scaler_H = MinMaxScaler()

        self._process_and_normalize_data()

        self.S_target_normalized = self.scaler_S.transform([[S_target]])[0][0]
        self.H_target_normalized = self.scaler_H.transform([[H_target]])[0][0]

    def _get_loader(self):
        if self.search_type == 'isothermal':
            return IsothermalLoader()
        elif self.search_type == 'isobaric':
            return IsobaricLoader()

    def _process_and_normalize_data(self):
        if self.search_type == 'isothermal':
            self.T_isothermal, self.S_isothermal, self.H_isothermal = self.data
            self.S_isothermal_flat = np.concatenate(self.S_isothermal)
            self.H_isothermal_flat = np.concatenate(self.H_isothermal)
            self.S_isothermal_normalized = self.scaler_S.fit_transform(self.S_isothermal_flat.reshape(-1, 1))
            self.H_isothermal_normalized = self.scaler_H.fit_transform(self.H_isothermal_flat.reshape(-1, 1))
        else:
            self.P_isobaric, self.S_isobaric, self.H_isobaric = self.data
            self.S_isobaric_flat = np.concatenate(self.S_isobaric)
            self.H_isobaric_flat = np.concatenate(self.H_isobaric)
            self.S_isobaric_normalized = self.scaler_S.fit_transform(self.S_isobaric_flat.reshape(-1, 1))
            self.H_isobaric_normalized = self.scaler_H.fit_transform(self.H_isobaric_flat.reshape(-1, 1))

    def distance(self, S1, H1, S2, H2):
        return np.sqrt((S1 - S2) ** 2 + (H1 - H2) ** 2)

    def _find_curve(self, S_data, H_data, curve_type):
        min_distance = float('inf')
        curve = None
        index = -1

        for i in range(len(S_data)):
            S_curve = S_data[i]
            H_curve = H_data[i]

            interp_func = interp1d(S_curve, H_curve, kind='linear', fill_value="extrapolate")
            H_interp = interp_func(S_curve)

            for j in range(len(S_curve)):
                S_curve_normalized = self.scaler_S.transform([[S_curve[j]]])[0][0]
                H_curve_normalized = self.scaler_H.transform([[H_interp[j]]])[0][0]

                distance = self.distance(self.S_target_normalized, self.H_target_normalized,
                                         S_curve_normalized, H_curve_normalized)

                if distance < min_distance:
                    min_distance = distance
                    index = i
                    if curve_type == 'isothermal':
                        curve = self.T_isothermal[i][0]  
                    elif curve_type == 'isobaric':
                        curve = self.P_isobaric[i][0]  

        return index, curve  

    def find_curve(self):
        if self.search_type == 'isothermal':
            return self._find_curve(self.S_isothermal, self.H_isothermal, 'isothermal')
        else:
            return self._find_curve(self.S_isobaric, self.H_isobaric, 'isobaric')
    