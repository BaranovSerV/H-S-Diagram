import os
import json
from abc import ABC, abstractmethod

import numpy as np


DIRECTORY = "data"


class Loader(ABC):
    @abstractmethod
    def load_data(self, *args, **kwargs):
        """Метод для загрузк  данных при получении их с сервера"""
        pass


    @abstractmethod
    def get_data(self):
        """Метод для получение сохраненных данных"""
        pass


class SaturationLoader(Loader):
    def load_data(self, T_saturation, S_saturation, H_saturation):
        print("Сохранение данных линии насыщения...")

        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "saturation_data.json")

        data = {
            "T_saturation": T_saturation.tolist(),
            "S_saturation": S_saturation.tolist(),
            "H_saturation": H_saturation.tolist()
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print("Данные успешно сохранены")


    def get_data(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "saturation_data.json") 
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        T_saturation = data["T_saturation"]
        S_saturation = data["S_saturation"]
        H_saturation = data["H_saturation"]

        return T_saturation, S_saturation, H_saturation
    

class IsothermalLoader(Loader):
    def load_data(self, T_isothermal, H_isothermal, S_isothermal):
        print("Сохранение данных изотерм...")

        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isothermal_data.json")

        T_isothermal = np.array(T_isothermal, dtype=object)
        H_isothermal = np.array(H_isothermal, dtype=object)
        S_isothermal = np.array(S_isothermal, dtype=object)

        data = {
            "T_isothermal": T_isothermal.tolist(),
            "S_isothermal": S_isothermal.tolist(),
            "H_isothermal": H_isothermal.tolist()
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print("Данные успешно сохранены")


    def get_data(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isothermal_data.json") 
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        T_isothermal = data["T_isothermal"]
        S_isothermal = data["S_isothermal"]
        H_isothermal = data["H_isothermal"]

        return T_isothermal, S_isothermal, H_isothermal
    

class IsobaricLoader(Loader):
    def load_data(self, P_isobaric, H_isobaric, S_isobaric):
        print("Данных данных изобар...")

        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isobaric_data.json")

        P_isobaric = np.array(P_isobaric, dtype=object)
        H_isobaric = np.array(H_isobaric, dtype=object)
        S_isobaric = np.array(S_isobaric, dtype=object)

        data = {
            "P_isobaric": P_isobaric.tolist(),
            "S_isobaric": S_isobaric.tolist(),
            "H_isobaric": H_isobaric.tolist()
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print("Данные успешно сохранены")


    def get_data(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isobaric_data.json") 
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        P_isobaric = data["P_isobaric"]
        S_isobaric = data["S_isobaric"]
        H_isobaric = data["H_isobaric"]

        return P_isobaric, S_isobaric, H_isobaric