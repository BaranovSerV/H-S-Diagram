from abc import ABC, abstractmethod

from requests import Response
from bs4 import BeautifulSoup


class ParserData(ABC):
    @abstractmethod
    def parse(self):
        """
        Метод для обработки полученной информации от сервера, 
        который находит нужные таблицы и берет из нужных столбцов данные 
        """
        pass    


class SaturationParser(ParserData):
    def __init__(self):
        self.liquid_index = 0
        self.steam_index = 1


    def parse(self, response: Response):
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table", {"class": "small"})  

        liquid_table = tables[self.liquid_index]
        steam_table = tables[self.steam_index]
        return self._parse_table(liquid_table), self._parse_table(steam_table)
    
         
    def _parse_table(self, table): 
        rows = table.find_all("tr")[1:]  
        data = []
        
        for row in rows:
            cols = row.find_all("td")
            values = [col.text.strip() for col in cols]
            if values:
                temperature = values[0]  
                enthalpy = values[5]    
                entropy = values[6]     
                data.append((temperature, enthalpy, entropy))
        return data
    

class IsothermalParser(ParserData):
    def parse(self, response: Response):
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table", {"class": "small"})  
        return self._parse_table(table[0])
         
    
    def _parse_table(self, table):

        rows = table.find_all("tr")[1:]  
        data = []
        
        for row in rows:
            cols = row.find_all("td")
            values = [col.text.strip() for col in cols]
            if values:
                temperature = values[0]  
                enthalpy = values[5]    
                entropy = values[6]     
                data.append((temperature, enthalpy, entropy))
        return data
    

class IsobaricParser(ParserData):
    def parse(self, response: Response):
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table", {"class": "small"})  
        return self._parse_table(table[0]) 


    def _parse_table(self, table):
        rows = table.find_all("tr")[1:]  
        data = []
        
        for row in rows:
            cols = row.find_all("td")
            values = [col.text.strip() for col in cols]
            if values:
                pressure = values[1]  
                enthalpy = values[5]    
                entropy = values[6]     
                data.append((pressure, enthalpy, entropy))
        return data


class IsochoricParser(ParserData):
    def parse(self, response: Response):
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table", {"class": "small"})  
        return self._parse_table(table[1]) 


    def _parse_table(self, table):
        rows = table.find_all("tr")[1:]  
        data = []
        
        for row in rows:
            cols = row.find_all("td")
            values = [col.text.strip() for col in cols]
            if values:
                pressure = values[4]  
                enthalpy = values[5]    
                entropy = values[6]     
                data.append((pressure, enthalpy, entropy))
        return data