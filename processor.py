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
    def process_isothermal_data(response):
        parser = IsothermalParser()
        data = parser.parse(response)
        T, H, S = zip(*data)
        return (
            list(map(float, T)),
            list(map(float, H)),
            list(map(float, S))
        )


    @staticmethod
    def process_isobaric_data(response):
        parser = IsobaricParser()
        data = parser.parse(response)
        P, H, S = zip(*data)
        return (
            list(map(float, P)),
            list(map(float, H)),
            list(map(float, S))
        )