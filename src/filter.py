from abc import ABC, abstractmethod


class FilterData(ABC):
    """Фильтрация данных насыщения по заданным диапазонам энтальпии и энтропии"""

    def __init__(self, h_max: float, s_max: float):
        self.h_max = h_max
        self.s_max = s_max

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass


class SaturationFilterData(FilterData):
    def filter(
        self, 
        T_saturation, 
        S_saturation, 
        H_saturation
    ):
        filtered_T = []
        filtered_S = []
        filtered_H = []
        for i in range(len(T_saturation)):
            if (
                H_saturation[i] <= self.h_max and
                S_saturation[i] <= self.s_max
            ):
                filtered_T.append(T_saturation[i])
                filtered_S.append(S_saturation[i])
                filtered_H.append(H_saturation[i])

        return filtered_T, filtered_S, filtered_H


class IsothermalFilterData(FilterData):
    def filter(self, T_isothermal, S_isothermal, H_isothermal):
        filtered_T = []
        filtered_S = []
        filtered_H = []

        for t, s_row, h_row in zip(T_isothermal, S_isothermal, H_isothermal):
            s_filtered_row = []
            h_filtered_row = []

            for s, h in zip(s_row, h_row):
                if  h <= self.h_max and s <= self.s_max:
                    s_filtered_row.append(s)
                    h_filtered_row.append(h)

            if s_filtered_row:  # добавлять только непустые ряды
                filtered_T.append(t)
                filtered_S.append(s_filtered_row)
                filtered_H.append(h_filtered_row)

        return filtered_T, filtered_S, filtered_H


class IsobaricFilterData(FilterData):
    def filter(self, P_isobaric, S_isobaric, H_isobaric):
        filtered_P = []
        filtered_S = []
        filtered_H = []

        for p, s_row, h_row in zip(P_isobaric, S_isobaric, H_isobaric):
            s_filtered_row = []
            h_filtered_row = []

            for s, h in zip(s_row, h_row):
                if h <= self.h_max and s <= self.s_max:
                    s_filtered_row.append(s)
                    h_filtered_row.append(h)

            if s_filtered_row:
                filtered_P.append(p)
                filtered_S.append(s_filtered_row)
                filtered_H.append(h_filtered_row)

        return filtered_P, filtered_S, filtered_H

    

class IsochoricFilterData(FilterData):
    def filter(self, V_isochoric, S_isochoric, H_isochoric):
        filtered_V = []
        filtered_S = []
        filtered_H = []

        for v_row, s_row, h_row in zip(V_isochoric, S_isochoric, H_isochoric):
            v_filtered_row = []
            s_filtered_row = []
            h_filtered_row = []

            for v, s, h in zip(v_row, s_row, h_row):
                if h <= self.h_max and s <= self.s_max:
                    v_filtered_row.append(v)
                    s_filtered_row.append(s)
                    h_filtered_row.append(h)

            if v_filtered_row:
                filtered_V.append(v_filtered_row)
                filtered_S.append(s_filtered_row)
                filtered_H.append(h_filtered_row)

        return filtered_V, filtered_S, filtered_H


