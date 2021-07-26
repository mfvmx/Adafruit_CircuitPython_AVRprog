# Write your code here :-)
from time import monotonic, sleep
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

x = 0
testVoltageHigh = 4.0 # 11.0
testVoltageLow = 1.0
blinkTimeH = 0.79
blinkTimeL = 0.73
testTimerBlink = 3.3

nowStart = monotonic()
current = monotonic()
blinkTimeOn = monotonic()
test1 = True
# P5 always 12V
batP5 = 0
batU9 = 1
batP10 = 2
batU18 = 3
# B12 always Ground
BP3 = DigitalInOut(board.A1)
B6 = 4
B17 = 5
B12 = 6
BP6 = 7
RF = 8
LF = 9
LR = 10
RR = 11
LS = 12
RS = 13
LD = 14
RD = 15
MuxPins = []
buttonTB = DigitalInOut(board.SDA)
ledTB = DigitalInOut(board.SCL)
LTswitch = DigitalInOut(board.D2)
RTswitch = DigitalInOut(board.D3)
BKswitch = DigitalInOut(board.D4)
HZswitch = DigitalInOut(board.D5)
hornIn = DigitalInOut(board.D6)
hornOut = DigitalInOut(board.D7)
selectPins = [board.D8, board.D9, board.D11, board.D12]
for i in range(0, len(selectPins)):
    led = DigitalInOut(selectPins[i])
    led.direction = Direction.OUTPUT
    MuxPins.append(led)

hornIn.switch_to_input(pull=Pull.DOWN)
hornOut.direction = Direction.OUTPUT
BP3.switch_to_input(pull=Pull.UP)
LTswitch.direction = Direction.OUTPUT
RTswitch.direction = Direction.OUTPUT
BKswitch.direction = Direction.OUTPUT
HZswitch.direction = Direction.OUTPUT
ledTB.direction = Direction.OUTPUT
buttonTB.switch_to_input(pull=Pull.DOWN)
LTswitch.value = 0
RTswitch.value = 0
BKswitch.value = 0
HZswitch.value = 0

def selectMuxPin(pin):
    if pin > 15:
        return
    for i in range(4):
        if pin & (1 << i):
            MuxPins[i].value = True
        else:
            MuxPins[i].value = False

def batt_voltage(pin):
    selectMuxPin(pin)
    sleep(0.0001)
    Zin = AnalogIn(board.A0)
    gvlt = (Zin.value * 15.0) / 65536
    Zin.deinit()
    sleep(0.0001)
    return gvlt

def ground_voltage(pin):
    GroundIn = DigitalInOut(board.A0)
    GroundIn.switch_to_input(pull=Pull.UP)
    selectMuxPin(pin)
    sleep(0.0001)
    gv = GroundIn.value
    GroundIn.deinit()
    sleep(0.0001)
    return gv

def testHorn():
    hornOut.value = 0
    if hornIn.value == 1:
        print("Test Horn Failed")
        return 0
    hornOut.value = 1
    if hornIn.value == 1:
        print("Test Horn Passed")
        hornOut.value = 0
        return 1
    print("Test Horn Failed")
    hornOut.value = 0
    return 0

def testBatt():
    # print("Voltage Pin#" , "batP5" , batt_voltage(batP5) , "batU9" , batt_voltage(batU9) , "batP10" , batt_voltage(batP10) , "batU18" , batt_voltage(batU18))
    if (batt_voltage(batU9) > testVoltageHigh) and (batt_voltage(batP5) > testVoltageHigh) and (batt_voltage(batP10) > testVoltageHigh) and (batt_voltage(batU18) > testVoltageHigh) :
        print("Test 12V Passed")
        return 1
    print("Test 12V Failed")
    return 0

def testGround():
    # print("Voltage Pin#" , "B12" , ground_voltage(B12) , "BP3" , BP3.value , "B6" , ground_voltage(B6) , "B17" , ground_voltage(B17) , "BP6" , ground_voltage(BP6))
    if BP3.value is False and ground_voltage(B12) is False and ground_voltage(B6) is False and ground_voltage(B17) is False and ground_voltage(BP6) is False :
        print("Test Grounds Passed")
        return 1
    print("Test Grounds Failed")
    return 0