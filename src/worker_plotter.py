from src.loader import (
    SaturationLoader, 
    IsothermalLoader, 
    IsobaricLoader, 
    IsochoricLoader,
    RenkineLoader
)
from src.filter import (
    SaturationFilterData, 
    IsothermalFilterData, 
    IsobaricFilterData, 
    IsochoricFilterData
)


class WokerPlotter:
    def __init__(self, H_max, S_max):
        self.H_max = H_max
        self.S_max = S_max

    def plotter(self):
        saturation_loader = SaturationLoader()
        isothermal_loader = IsothermalLoader()
        isobaric_loader = IsobaricLoader()
        isochoric_loader = IsochoricLoader()
        renkine_loader = RenkineLoader()

        saturation_filter = SaturationFilterData(self.H_max, self.S_max)
        isothermal_filter = IsothermalFilterData(self.H_max,  self.S_max)
        isobaric_filter = IsobaricFilterData(self.H_max, self.S_max)
        isochoric_filter = IsochoricFilterData(self.H_max, self.S_max)

        (
            T_saturation_no_filter, 
            S_saturation_no_filer, 
            H_saturation_no_filter
        ) = saturation_loader.get_data()

        (
            T_isothermal_no_filter, 
            S_isothermal_no_filter, 
            H_isothermal_no_filter
        ) = isothermal_loader.get_data()

        (
            P_isobaric_no_filter, 
            S_isobaric_no_filter, 
            H_isobaric_no_filter,
            T_isobaric,
            D_isobaric
        ) = isobaric_loader.get_data()

        (
            V_isochoric_no_filter, 
            S_isochoric_no_filter, 
            H_isochoric_no_filter
        )  = isochoric_loader.get_data()

        T_saturation, S_saturation, H_saturation = saturation_filter.filter(
            T_saturation_no_filter, 
            S_saturation_no_filer, 
            H_saturation_no_filter
        )
        T_isothermal, S_isothermal, H_isothermal = isothermal_filter.filter(
            T_isothermal_no_filter, 
            S_isothermal_no_filter, 
            H_isothermal_no_filter
        )
        P_isobaric, S_isobaric, H_isobaric = isobaric_filter.filter(
            P_isobaric_no_filter, 
            S_isobaric_no_filter, 
            H_isobaric_no_filter 
        )
        V_isochoric, S_isochoric, H_isochoric = isochoric_filter.filter(
            V_isochoric_no_filter, 
            S_isochoric_no_filter, 
            H_isochoric_no_filter
        )

        S_renkine, H_renkine, T_renkine, P_renkine, V_renkine  = renkine_loader.get_data()

        return (
            T_saturation, S_saturation, H_saturation,
            T_isothermal, S_isothermal, H_isothermal,
            P_isobaric, S_isobaric, H_isobaric, T_isobaric, D_isobaric,
            V_isochoric, S_isochoric, H_isochoric,
            S_renkine, H_renkine, T_renkine, P_renkine, V_renkine
        )

