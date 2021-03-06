[I2C]
ADDR_B = 0x38
ADDR_A = 0x21

[ADC]
THRESHOLD_VOLTAGE = 2.5
POLLING_DELAY = 0.05

[BTN]
MODE = 3
#0 - Polling
#1 - Polling with software debounce
#2 - Polling with hardware and software debounce
#3 - Interrupt-based
IDLE_POLLING_DELAY = 0.05
DEBOUNCE_POLLING_DELAY = 0.005
DEBOUNCE_STABLE_PERIOD = 0.1
INT_PIN = 15
[PID]
KP = 6.0
KD = -0.6
KI = 1.0
TARGET_LUMINOSITY = 1.1
MAX_OUTPUT = 10.0
MIN_OUTPUT = 1.0
