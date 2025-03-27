import numpy as np
from matplotlib import pyplot as plt

from src.loader import SaturationLoader, IsobaricLoader, IsothermalLoader, IsochoricLoader


"""Файл для удобного и быстрого построения H-S диаграммы после загрузки данных с сервера"""


SUBSTANCE_NAME = "Trichlorofluoromethane (R11)" # Название вашего вещества

saturation_loader = SaturationLoader()
isothermal_loader = IsothermalLoader()
isobaric_loader = IsobaricLoader()
isochoric_loader = IsochoricLoader()

T_saturation, S_saturation, H_saturation = saturation_loader.get_data()
T_isothermal, S_isothermal, H_isothermal = isothermal_loader.get_data()
P_isobaric, S_isobaric, H_isobaric = isobaric_loader.get_data()
V_isochoric, S_isochoric, H_isochoric = isochoric_loader.get_data()

P_ON_GRAPH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45] # Изобары, которые будут подписываться на графике


plt.subplots(figsize=(12, 8), dpi=200)

# Изохоры
for i in range(len(V_isochoric)):
    plt.plot(S_isochoric[i], H_isochoric[i], color='gray', linestyle="--",  linewidth=0.3)


# Изотермы
for i in range(len(T_isothermal)):
    plt.plot(S_isothermal[i], H_isothermal[i], color='g', linewidth=0.2)
    plt.text(
        S_isothermal[i][0], 
        H_isothermal[i][0], 
        f"{T_isothermal[i][0]:.2f} °C", 
        fontsize=3, 
        color='black', 
        bbox=dict(facecolor='none', alpha=0.3, edgecolor='none')
    )

# Изобары
for i in range(len(P_isobaric)):
    plt.plot(S_isobaric[i], H_isobaric[i], color='r', linewidth=0.1)
    if P_isobaric[i][0] in P_ON_GRAPH:
        plt.text(
            S_isobaric[i][-1], 
            H_isobaric[i][-1], 
            f"{int(P_isobaric[i][0])}", 
            fontsize=4, 
            color='black', 
            bbox=dict(facecolor='none', alpha=0.3, edgecolor='none')
        )

# Линия насыщения
plt.plot(S_saturation, H_saturation, linewidth=0.8)
plt.ylabel("h, кДж/кг")
plt.xlabel("s, кДж/(кг*К)")
plt.title(f"H-S диаграмма {SUBSTANCE_NAME}")

# Необходиммо установить границы для оси X и Y
x_ticks = np.arange(0.5, 2.8,  step=0.2)  
y_ticks = np.arange(100, 660, step=20) 

plt.xticks(x_ticks, fontsize=6)
plt.yticks(y_ticks, fontsize=6)
plt.grid(True, which='both', linewidth=0.2)  
plt.minorticks_on()  

plt.show()

