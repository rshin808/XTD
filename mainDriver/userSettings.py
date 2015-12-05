import types

class userSettings:
    def __init__(self):
        self._osc = None
        self._testSignal = None
        self._jtag = None
        self._bunchMarkerA = None
        self._bunchMarkerB = None

    @property
    def osc(self):
        return self._input

    @property
    def testSignal(self):
        return self._testSignal

    @property
    def jtag(self):
        return self._jtag

    @property
    def bunchMarkerA(self):
        return self._bunchMarkerA

    @property
    def bunchMarkerB(self):
        return self._bunchMarkerB

    @osc.setter
    def osc(self, enabled):
        assert type(enabled) == types.BooleanType, "osc requires a boolean"
        self._osc = enabled

    @testSignal.setter
    def testSignal(self, on):
        assert type(on) == types.BooleanType, "testSignal requires a boolean"
        self._testSignal = on

    @jtag.setter
    def jtag(self, choice):
        assert type(choice) == types.BooleanType, "scrod requires a boolean"
        #assert choice.lower() == "a" or choice.lower() == "b", "scrod is either A or B"
        #self._jtag = choice.lower()
        self._jtag = A

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
