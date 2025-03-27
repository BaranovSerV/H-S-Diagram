from abc import ABC, abstractmethod

import requests


BASE_URL = "https://webbook.nist.gov/cgi/fluid.cgi" # URL сайта с данными

class RequestAPI(ABC):
    @abstractmethod
    def get_url(self):
        """Метод для получения данных с сайта"""
        pass


class SaturationAPI(RequestAPI):
    def get_url(
        self, 
        TLow: float,
        THigh: float,
        TInc: float,
        ID: str
    ):
        url = (
            f"{BASE_URL}?TLow={TLow}&THigh={THigh}&TInc={TInc}&Digits=5&ID={ID}" \
            "&Action=Load&Type=SatP&TUnit=C&PUnit=bar&DUnit=mol%2Fl&HUnit=kJ%2F" \
            "kg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
        )
        print("Получение данных о линии насыщения...")
        response = requests.get(url)
        if response.status_code == 200:
            print("Данные получены успешно")
            return response
        else:
            print(f"Ошибка запроса")
    

class IsothermalAPI(RequestAPI):
    def get_url(
        self,
        T: float,
        PLow: float,
        PHigh: float,
        PInc: float,
        ID: str
    ):
        url = (
            f"{BASE_URL}?T={T}&PLow={PLow}&PHigh={PHigh}&PInc={PInc}&Digits=5&ID={ID}"
            "&Action=Load&Type=IsoTherm&TUnit=C&PUnit=bar&DUnit=mol%2Fl&HUnit=kJ%2Fkg"
            "&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
        )
        
        print(f"Получение данных о изотерме {T}°C...")
        response = requests.get(url)
        if response.status_code == 200:
            print("Данные получены успешно")
            return response
        else:
            print(f"Ошибка запроса")


class IsobaricAPI(RequestAPI):
    def get_url(
        self,
        P: float,
        TLow: float,
        THigh: float,
        TInc: float,
        ID: str
    ):
        url = (
            f"{BASE_URL}?P={P}&TLow={TLow}&THigh={THigh}&TInc={TInc}&Digits=5&ID={ID}"
            "&Action=Load&Type=IsoBar&TUnit=C&PUnit=bar&DUnit=mol%2Fl&HUnit=kJ%2Fkg"
            "&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
        )
        print(f"Получение данных о изобаре {P} бар...")
        response = requests.get(url)
        if response.status_code == 200:
            print("Данные получены успешно")
            return response
        else:
            print(f"Ошибка запроса")


class IsochoricAPI(RequestAPI):
    def get_url(
        self,
        D,
        TLow,
        THigh,
        TInc,
        ID
    ):
        url = (
            f"{BASE_URL}?D={D}&TLow={TLow}&THigh={THigh}&TInc={TInc}&Digits=5&ID={ID}"
            "&Action=Load&Type=IsoChor&TUnit=C&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&"
            "Unit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"
        )
        
        print(f"Получение данных о изохоре {D} кг/m^3...")
        response = requests.get(url)
        if response.status_code == 200:
            print("Данные получены успешно")
            return response
        else:
            print(f"Ошибка запроса")
