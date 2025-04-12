import numpy as np
from matplotlib import pyplot as plt

from src.worker_plotter import WokerPlotter
from config import *

"""Файл для удобного и быстрого построения H-S диаграммы после загрузки данных с сервера"""

# Границы графика
H_max = 490
S_max = 2.4

P_ON_GRAPH = [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1, 1.5,  2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 35, 45] # Изобары, которые будут подписываться на графике
T_ON_GRAPH = [-10, 0, 10, 20, 40, 70, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260] # Изотермы, которые будут подписываться на графике


worker_plotter = WokerPlotter(H_max, S_max)

(
    T_saturation, S_saturation, H_saturation,
    T_isothermal, S_isothermal, H_isothermal,
    P_isobaric, S_isobaric, H_isobaric, 
    V_isochoric, S_isochoric, H_isochoric,
    S_renkine, H_renkine, T_renkine, P_renkine
) = worker_plotter.plotter()

delta = 0.001

plt.subplots(figsize=(12, 8), dpi=300)

# Изотермы
for i in range(len(T_isothermal)):
    plt.plot(S_isothermal[i], H_isothermal[i], color='g', linewidth=0.2)
    if T_isothermal[i][0] in T_ON_GRAPH:
        if T_isothermal[i][0] > 160:
            plt.text(
                S_isothermal[i][0], 
                H_isothermal[i][0], 
                f"{T_isothermal[i][0]:.2f} °C", 
                fontsize=2, 
                rotation=35,
                color='black', 
                bbox=dict(facecolor='none', alpha=0.3, edgecolor='none')
            )
        else:
            plt.text(
                S_isothermal[i][0] - 0.1, 
                H_isothermal[i][0], 
                f"{T_isothermal[i][0]:.2f} °C", 
                fontsize=2, 
                rotation=35,
                color='black', 
                bbox=dict(facecolor='none', alpha=0.3, edgecolor='none')
            ) 

# Изобары
for i in range(len(P_isobaric)):
    plt.plot(S_isobaric[i], H_isobaric[i], color='r', linewidth=0.1)
    if P_isobaric[i][0] in P_ON_GRAPH:
        plt.text(
            S_isobaric[i][-10], 
            H_isobaric[i][-10], 
            f"{P_isobaric[i][0]}", 
            fontsize=2, 
            rotation=45,
            color='black', 
            bbox=dict(facecolor='none', alpha=0.3, edgecolor='none')
        )

# Линия насыщения
plt.plot(S_saturation, H_saturation, linewidth=0.8)
plt.ylabel("h, кДж/кг", fontsize=4)
plt.xlabel("s, кДж/(кг*К)", fontsize=4)
plt.title(f"H-S диаграмма {SUBSTANCE_NAME}", fontsize=6)


# Дополнительные данные

# Изохоры
# for i in range(len(V_isochoric)):
#     plt.plot(S_isochoric[i], H_isochoric[i], color='gray', linestyle="--",  linewidth=0.3)

# Цикл Ренкина
# Если данных о цикле еще нет, оставьте закоментированным
# plt.scatter(S_renkine, H_renkine, color='g', linewidth=0.5, s=2)
# for i in range(len(S_renkine)):
#     plt.text(
#             S_renkine[i] + delta, 
#             H_renkine[i] + delta, 
#             f"{i + 1}", 
#             fontsize=6, 
#             color='black', 
#             bbox=dict(facecolor='none', alpha=0.3, edgecolor='none')
#     )


x_ticks = np.arange(min(S_saturation), S_max,  step=0.02)  
y_ticks = np.arange(min(H_saturation), H_max, step=20) 

plt.xticks(x_ticks, fontsize=4)
plt.yticks(y_ticks, fontsize=4)
plt.grid(True, which='both', linewidth=0.2)  
plt.minorticks_on()  

plt.show()

