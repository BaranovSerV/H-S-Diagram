import os
import json
from abc import ABC, abstractmethod

import numpy as np

from config import *

DIRECTORY = f"data/{ID}"


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

        if not os.path.exists(file_path):
            return [], [], []

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

        if not os.path.exists(file_path):
            return [], [], []

        with open(file_path, "r") as f:
            data = json.load(f)
        
        T_isothermal = data["T_isothermal"]
        S_isothermal = data["S_isothermal"]
        H_isothermal = data["H_isothermal"]

        return T_isothermal, S_isothermal, H_isothermal
    

class IsobaricLoader(Loader):
    def load_data(self, P_isobaric, H_isobaric, S_isobaric, T_isobaric, V_isobaric):
        print("Данных данных изобар...")

        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isobaric_data.json")

        P_isobaric = np.array(P_isobaric, dtype=object)
        H_isobaric = np.array(H_isobaric, dtype=object)
        S_isobaric = np.array(S_isobaric, dtype=object)
        T_isobaric = np.array(T_isobaric, dtype=object)
        V_isobaric = np.array(V_isobaric, dtype=object)

        data = {
            "P_isobaric": P_isobaric.tolist(),
            "S_isobaric": S_isobaric.tolist(),
            "H_isobaric": H_isobaric.tolist(),
            "T_isobaric": T_isobaric.tolist(),
            "V_isobaric": V_isobaric.tolist()
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print("Данные успешно сохранены")


    def get_data(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isobaric_data.json") 

        if not os.path.exists(file_path):
            return [], [], [], [], []

        with open(file_path, "r") as f:
            data = json.load(f)
        
        P_isobaric = data["P_isobaric"]
        S_isobaric = data["S_isobaric"]
        H_isobaric = data["H_isobaric"]
        T_isobaric = data["T_isobaric"]
        V_isobaric = data["V_isobaric"]

        return P_isobaric, S_isobaric, H_isobaric, T_isobaric, V_isobaric
    

class IsochoricLoader(Loader):
    def load_data(self, V_isochoric, H_isochoric, S_isochoric):
        print("Данных данных изохор...")

        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isochoric_data.json")

        V_isochoric = np.array(V_isochoric, dtype=object)
        H_isochoric = np.array(H_isochoric, dtype=object)
        S_isochoric = np.array(S_isochoric, dtype=object)

        data = {
            "V_isochoric": V_isochoric.tolist(),
            "S_isochoric": S_isochoric.tolist(),
            "H_isochoric": H_isochoric.tolist()
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print("Данные успешно сохранены")


    def get_data(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "isochoric_data.json") 

        if not os.path.exists(file_path):
            return [], [], []

        with open(file_path, "r") as f:
            data = json.load(f)
        
        V_isochoric = data["V_isochoric"]
        S_isochoric = data["S_isochoric"]
        H_isochoric = data["H_isochoric"]

        return V_isochoric, S_isochoric, H_isochoric
    
    
class RenkineLoader(Loader):
    def load_data(self, S_renkine, H_renkine, P_renkine, T_renkine, V_renkine):
        print("Сохранение данных цикла Ренкина...")

        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "renkine_data.json")

        H_renkine = np.array(H_renkine, dtype=object)
        S_renkine = np.array(S_renkine, dtype=object)
        T_renkine = np.array(T_renkine, dtype=object)
        P_renkine = np.array(P_renkine, dtype=object)
        V_renkine = np.array(V_renkine, dtype=object)
        data = {
            "T_renkine": T_renkine.tolist(),
            "S_renkine": S_renkine.tolist(),
            "H_renkine": H_renkine.tolist(),
            "P_renkine": P_renkine.tolist(),
            "V_renkine": V_renkine.tolist()
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print("Данные успешно сохранены")


    def get_data(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        file_path = os.path.join(DIRECTORY, "renkine_data.json") 
        
        if not os.path.exists(file_path):
            return [], [], [], [], []

        with open(file_path, "r") as f:
            data = json.load(f)
        
        S_renkine = data["S_renkine"]
        H_renkine = data["H_renkine"]
        T_renkine = data["T_renkine"]
        P_renkine = data["P_renkine"]
        V_renkine = data["V_renkine"]

        return S_renkine, H_renkine, T_renkine, P_renkine, V_renkine