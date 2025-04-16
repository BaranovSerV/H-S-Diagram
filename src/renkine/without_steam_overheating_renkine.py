import pandas as pd
from IPython.display import display, Math

from src.loader import RenkineLoader
from src.renkine import Renkine
from src.utils import linear_spline

class WithoutSteamOverheatingRenkine(Renkine):
    """Не стандартный цикл Ренкина, состоящий из 6 точек без перегревом пара"""
    def __init__(self, S_5_point, H_5_point):
        super().__init__()
        self.S_5_point = S_5_point
        self.H_5_point = H_5_point


    def _formulas(self):
        formula_A_nasos = r"\begin{align}l_{\text{насоса}} = h_2 - h_1\end{align}"
        formula_A_turbine = r"\begin{align}l_{\text{турбины}} = h_4 - h_5\end{align}"
        formula_n_RENKINE = r"\begin{align}\eta_{\text{Ренкина}} = \frac{l_{\text{турбины}} - l_{\text{насоса}}}{h_4 - h_2}\end{align}"
        formula_n_KARNO = r"\begin{align}\eta_{\text{Карно}} = 1 - \frac{T_1}{T_4}\end{align}"

        display(Math(formula_A_nasos))
        display(Math(formula_A_turbine))
        display(Math(formula_n_RENKINE))
        display(Math(formula_n_KARNO))

    def _process_data(self):
        self.S = [self.S_1_point, self.S_2_point, self.S_3_point, self.S_4_point]
        
        # for s in self.S_ren:
            # self.S.append(s)
        
        self.S.append(self.S_5_point)
        self.S.append(self.S_6_point)
        self.S.append(self.S_1_point)

        self.T = [self.T_1_point, self.T_2_point, self.T_3_point, self.T_4_point]
        
        # for t in self.T_ren:
        #     self.T.append(t)
    
        self.T.append(self.T_5_point)
        self.T.append(self.T_6_point)
        self.T.append(self.T_1_point)


    def renkine_data(self):
        self._point_5()
        self._point_4()
        self._point_6()
        self._point_3()
        self._point_1()
        self._point_2()
        self._process_data()

        self.S_RENKINE = [self.S_1_point, self.S_2_point, self.S_3_point, self.S_4_point, self.S_5_point, self.S_6_point]
        self.H_RENKINE = [self.H_1_point, self.H_2_point, self.H_3_point, self.H_4_point, self.H_5_point, self.H_6_point]
        self.P_RENKINE = [self.P_1_point, self.P_2_point, self.P_3_point, self.P_4_point, self.P_5_point, self.P_6_point]
        self.T_RENKINE = [self.T_1_point, self.T_2_point, self.T_3_point, self.T_4_point, self.T_5_point, self.T_6_point]
        self.V_RENKINE = [self.V_1_point, self.V_2_point, self.V_3_point, self.V_4_point, self.V_5_point, self.V_6_point]

        loader = RenkineLoader()
        loader.load_data(
            self.S_RENKINE,
            self.H_RENKINE,
            self.P_RENKINE,
            self.T_RENKINE,
            self.V_RENKINE,
        )
        
        data = {
            "Точка": ["1", "2", "3", "4", "5", "6"],
            "v (м^3/кг)": [
                self.V_1_point, 
                self.V_2_point, 
                self.V_3_point, 
                self.V_4_point, 
                self.V_5_point, 
                self.V_6_point,
            ],
            "P (бар)": [
                self.P_1_point, 
                self.P_2_point, 
                self.P_3_point, 
                self.P_4_point, 
                self.P_5_point, 
                self.P_6_point
            ],
            "T (°C)": [
                self.T_1_point,
                self.T_2_point,
                self.T_3_point,
                self.T_4_point,
                self.T_5_point,
                self.T_6_point
            ],
            "h (кДж/кг)": [
                self.H_1_point,
                self.H_2_point,
                self.H_3_point,
                self.H_4_point,
                self.H_5_point,
                self.H_6_point
            ],
            "s (кДж/кг·K)": [
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
                "После котла", 
                "После турбины", 
                "После турбины"
            ],
        }

        df = pd.DataFrame(data)
        display(df)

        return (
            self.S_RENKINE, self.T_RENKINE, self.S, self.T
        )

    def renkine_params(self):
        A_nasos = self.H_2_point - self.H_1_point
        A_turbine = self.H_4_point - self.H_5_point
        n_RENKINE = (A_turbine - A_nasos) / (self.H_4_point - self.H_2_point)
        n_KARNO = 1 - (self.T_1_point + 273.15) / (self.T_4_point + 273.15)
        
        self._formulas()

        params = {
            "Параметр": ["Работа насоса кДж/кг", "Работа турбины кДж/кг", "КПД Ренкина", "КПД Карно"],
            "Значение": [A_nasos, A_turbine, n_RENKINE, n_KARNO]
        }
        df_params = pd.DataFrame(params)
        display(df_params)

    def _point_5(self):
        print(f"Расчет точки 5...")

        self.index_5_isobar, self.P_5_point = self._find_curve_isobaric(self.S_5_point, self.H_5_point)
        self.index_5_isotherm, self.T_5_point = self._find_curve_isothermal(self.S_5_point, self.H_5_point)

        self.V_5_point = linear_spline(
            self.S_5_point, 
            self.S_isobaric[self.index_5_isobar], 
            self.V_isobaric[self.index_5_isobar]
        )

        print(f"Точка 5 расчитана")

        return self.S_5_point, self.H_5_point, self.P_5_point, self.T_5_point, self.V_5_point


    def _point_4(self):
        print(f"Расчет точки 4...")
        
        self.S_4_point = self.S_5_point

        self.H_4_point = linear_spline(
            self.S_5_point, 
            self.S_saturation[self.max_index:], 
            self.H_saturation[self.max_index:]
        )
        
        self.index_4_isobar, self.P_4_point = self._find_curve_isobaric(self.S_4_point, self.H_4_point)
        self.index_4_isotherm, self.T_4_point = self._find_curve_isothermal(self.S_4_point, self.H_4_point)

        self.V_4_point = linear_spline(
            self.S_4_point, 
            self.S_isobaric[self.index_4_isobar], 
            self.V_isobaric[self.index_4_isobar]
        )

        print(f"Точка 4 расчитана")

        return self.S_4_point, self.H_4_point, self.P_4_point, self.T_4_point, self.V_4_point


    def _point_6(self):
        print(f"Расчет точки 6...")

        self.index_6_isobar, self.P_6_point = self.index_5_isobar, self.P_5_point

        self.S_6_point, self.H_6_point = self._get_nearest_point(
            self.S_saturation[self.max_index:], 
            self.H_saturation[self.max_index:], 
            self.S_isobaric[self.index_6_isobar], 
            self.H_isobaric[self.index_6_isobar],
        )

        self.index_6_isotherm, self.T_6_point = self._find_curve_isothermal(self.S_6_point, self.H_6_point)

        self.V_6_point = linear_spline(
            self.S_6_point, 
            self.S_isobaric[self.index_6_isobar], 
            self.V_isobaric[self.index_6_isobar]
        )

        print(f"Точка 6 расчитана")

        return self.S_6_point, self.H_6_point, self.P_6_point, self.T_6_point, self.V_6_point
    

    def _point_1(self):
        print(f"Расчет точки 1...")

        self.index_1_isotherm, self.T_1_point = self.index_6_isotherm, self.T_6_point
        self.index_1_isobar, self.P_1_point = self.index_6_isobar, self.P_6_point

        self.S_1_point, self.H_1_point = self._get_nearest_point(
            self.S_saturation[:self.max_index], 
            self.H_saturation[:self.max_index], 
            self.S_isothermal[self.index_1_isotherm], 
            self.H_isothermal[self.index_1_isotherm]
        )

        self.V_1_point = linear_spline(
            self.S_1_point, 
            self.S_isobaric[self.index_1_isobar], 
            self.V_isobaric[self.index_1_isobar]
        )

        print(f"Точка 1 расчитана")
        
        return self.S_1_point, self.H_1_point, self.P_1_point, self.T_1_point, self.V_1_point  


    def _point_3(self):
        print(f"Расчет точки 3...")

        self.index_3_isotherm, self.T_3_point = self.index_4_isotherm, self.T_4_point
        self.index_3_isobar, self.P_3_point = self.index_4_isobar, self.P_4_point
        
        self.S_3_point, self.H_3_point = self._get_nearest_point(
            self.S_saturation[:self.max_index], 
            self.H_saturation[:self.max_index], 
            self.S_isothermal[self.index_4_isotherm], 
            self.H_isothermal[self.index_4_isotherm]
        )

        self.V_3_point = linear_spline(
            self.S_3_point, 
            self.S_isobaric[self.index_3_isobar], 
            self.V_isobaric[self.index_3_isobar]
        )

        print(f"Точка 3 расчитана")
        
        return self.S_3_point, self.H_3_point, self.P_3_point, self.T_3_point, self.V_3_point
    

    def _point_2(self):
        print(f"Расчет точки 2...")

        self.index_2_isobar, self.P_2_point = self.index_4_isobar, self.P_4_point
        self.S_2_point = self.S_1_point
        
        self.H_2_point = linear_spline(
            self.S_2_point, 
            self.S_isobaric[self.index_4_isobar], 
            self.H_isobaric[self.index_4_isobar]
        )

        
        self.T_2_point = linear_spline(
            self.S_2_point, 
            self.S_isobaric[self.index_2_isobar], 
            self.T_isobaric[self.index_2_isobar]
        )

        self.V_2_point = linear_spline(
            self.S_2_point, 
            self.S_isobaric[self.index_2_isobar], 
            self.V_isobaric[self.index_2_isobar]
        )

        print(f"Точка 2 расчитана")

        return self.S_2_point, self.H_2_point, self.P_2_point, self.T_2_point, self.V_2_point

