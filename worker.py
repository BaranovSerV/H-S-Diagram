from data import SubstanceData
from processor import ProcessorData

class Worker:
    def __init__(self, ID: str):
        self.substance_data = SubstanceData(ID)

    def saturation(self, TLow_saturation, THigh_saturation, TInc_saturation):
        response_saturation = self.substance_data.get_saturation_data(
            TLow_saturation, 
            THigh_saturation, 
            TInc_saturation
        )

        T_saturation, S_saturation, H_saturation = ProcessorData.process_saturation_data(
            response_saturation
        )
        return T_saturation, S_saturation, H_saturation
    

    def isothermal(self, T_isothermal_array, PLow_isothermal, PHigh_isothermal, PInc_isothermal):
        response_isothermal = [
            self.substance_data.get_isothermal_data(
                T, PLow_isothermal, PHigh_isothermal, PInc_isothermal
            ) for T in T_isothermal_array
        ]

        T_isothermal, H_isothermal, S_isothermal = ProcessorData.process_isothermal_data(
            response_isothermal
        )
        return T_isothermal, H_isothermal, S_isothermal
    
    def isobaric(self, P_isobaric_array, TLow_isobaric, THigh_isobaric, TInc_isobaric):
        response_isobaric = [
            self.substance_data.get_isobaric_data(
                P, 
                TLow_isobaric, 
                THigh_isobaric, 
                TInc_isobaric
            ) for P in P_isobaric_array
        ]
        
        P_isobaric, H_isobaric, S_isobaric = ProcessorData.process_isobaric_data(
            response_isobaric
        )
        return P_isobaric, H_isobaric, S_isobaric