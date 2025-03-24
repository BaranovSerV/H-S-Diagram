from request_api import SaturationAPI, IsothermalAPI, IsobaricAPI

class SubstanceData:
    def __init__(self, ID):
        self.ID = ID

    def get_saturation_data(self, TLow, THigh, TInc):
        api = SaturationAPI()
        return api.get_url(TLow=TLow, THigh=THigh, TInc=TInc, ID=self.ID)

    def get_isothermal_data(self, T, PLow, PHigh, PInc):
        api = IsothermalAPI()
        return api.get_url(T=T, PLow=PLow, PHigh=PHigh, PInc=PInc, ID=self.ID)

    def get_isobaric_data(self, P, TLow, THigh, TInc):
        api = IsobaricAPI()
        return api.get_url(P=P, TLow=TLow, THigh=THigh, TInc=TInc, ID=self.ID)
