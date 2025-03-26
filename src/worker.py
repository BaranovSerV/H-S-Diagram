from src.processor import ProcessorData
from src.loader import SaturationLoader, IsothermalLoader, IsobaricLoader
from src.request_api import SaturationAPI, IsothermalAPI, IsobaricAPI


class Worker:
    def __init__(self, ID: str):
        self.ID = ID

    def saturation(self, TLow_saturation, THigh_saturation, TInc_saturation):
        api = SaturationAPI()
        response_saturation = api.get_url(
            TLow_saturation, 
            THigh_saturation, 
            TInc_saturation,
            self.ID
        )

        T_saturation, S_saturation, H_saturation = ProcessorData.process_saturation_data(
            response_saturation
        )

        loader = SaturationLoader()
        loader.load_data(T_saturation, S_saturation, H_saturation)

        return T_saturation, S_saturation, H_saturation
    

    def isothermal(self, T_isothermal_array, PLow_isothermal, PHigh_isothermal, PInc_isothermal):
        api = IsothermalAPI()
        response_isothermal = [
            api.get_url(
                T, PLow_isothermal, PHigh_isothermal, PInc_isothermal, self.ID
            ) for T in T_isothermal_array
        ]

        T_isothermal, H_isothermal, S_isothermal = ProcessorData.process_isothermal_data(
            response_isothermal
        )
        
        loader = IsothermalLoader()
        loader.load_data(T_isothermal, H_isothermal, S_isothermal)

        return T_isothermal, H_isothermal, S_isothermal
    

    def isobaric(self, P_isobaric_array, TLow_isobaric, THigh_isobaric, TInc_isobaric):
        api = IsobaricAPI()
        response_isobaric = [
            api.get_url(
                P, 
                TLow_isobaric, 
                THigh_isobaric, 
                TInc_isobaric,
                self.ID
            ) for P in P_isobaric_array
        ]
        
        P_isobaric, H_isobaric, S_isobaric = ProcessorData.process_isobaric_data(
            response_isobaric
        )

        loader = IsobaricLoader()
        loader.load_data(P_isobaric, H_isobaric, S_isobaric)

        return P_isobaric, H_isobaric, S_isobaric