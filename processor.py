import numpy as np
from parser import SaturationParser, IsothermalParser, IsobaricParser

class ProcessorData:
    @staticmethod
    def process_saturation_data(response):
        parser = SaturationParser()
        liquid_data, steam_data = parser.parse(response)

        S_saturation = np.concatenate((
            np.array([d[2] for d in liquid_data], dtype=float),
            np.array([d[2] for d in steam_data][::-1], dtype=float)
        ))

        H_saturation = np.concatenate((
            np.array([d[1] for d in liquid_data], dtype=float),
            np.array([d[1] for d in steam_data][::-1], dtype=float)
        ))

        T_saturation = np.concatenate((
            np.array([d[0] for d in liquid_data], dtype=float),
            np.array([d[0] for d in steam_data][::-1], dtype=float)
        ))

        return T_saturation, S_saturation, H_saturation


    @staticmethod
    def process_isothermal_data(responses):
        T_isothermal, H_isothermal, S_isothermal = [], [], [] 
        parser = IsothermalParser()
    
        for response in responses:
            data = parser.parse(response)
            T, H, S = zip(*data)

            T_isothermal.append(list(map(float, T)))
            H_isothermal.append(list(map(float, H)))
            S_isothermal.append(list(map(float, S)))

        return T_isothermal, H_isothermal, S_isothermal


    @staticmethod
    def process_isobaric_data(responses):
        P_isobaric, H_isobaric, S_isobaric = [], [], []
        parser = IsobaricParser()
        for response in responses:
            data = parser.parse(response)
            P, H, S = zip(*data)

            P_isobaric.append(list(map(float, P)))
            H_isobaric.append(list(map(float, H)))
            S_isobaric.append(list(map(float, S)))

        return P_isobaric, H_isobaric, S_isobaric