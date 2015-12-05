import types

class userSettings:
    def __init__(self):
        self._vco = None
        self._testSignal = None
        self._scrod = None
        self._bunchMarkerA = None
        self._bunchMarkerB = None

    @property
    def vco(self):
        return self._vco

    @property
    def testSignal(self):
        return self._testSignal

    @property
    def scrod(self):
        return self._scrod

    @property
    def bunchMarkerA(self):
        return self._bunchMarkerA

    @property
    def bunchMarkerB(self):
        return self._bunchMarkerB

    @vco.setter
    def vco(self, enabled):
        assert type(enabled) == types.BooleanType, "vco requires a boolean"
        self._vco = enabled

    @testSignal.setter
    def testSignal(self, on):
        assert type(on) == types.BooleanType, "testSignal requires a boolean"
        self._testSignal = on

    @scrod.setter
    def scrod(self, choice):
        assert type(choice) == types.StringType, "scrod requires a string"
        assert choice.lower() == "a" or choice.lower() == "b", "scrod is either A or B"
        
        self._scrod = choice.lower()

    @bunchMarkerA.setter
    def bunchMarkerA(self, value):
        assert type(value) == types.IntType, "bunchMarkerA must be an integer"
        assert value >= 0 and value <= 5280, "bunchMarkerA must be in the range 0 to 5280"
        self._bunchMarkerA = value
   
    @bunchMarkerB.setter
    def bunchMarkerB(self, value):
        assert type(value) == types.IntType, "bunchMarkerB must be an integer"
        assert value >= 0 and value <= 5280, "bunchMarkerB must be in the range 0 to 5280"
        self._bunchMarkerB = value
