from matrix_lite import gpio

FREQUENCY = 10000
FR, FL, RR, RL = "FR", "FL", "RR", "RL"
mgpio = {FR: (0,1), FL: (6,7), RR: (5,4), RL: (3,2)}
all_mio = mgpio[FR]+mgpio[FL]+mgpio[RR]+mgpio[RL]

for i in all_mio:
	gpio.setFunction(i, 'PWM')
	gpio.setMode(i, "output")

for mm in [FR, FL, RR, RL]:
	pin0 = {"pin":mgpio[mm][0], "percentage":0, "frequency":FREQUENCY}
	pin1 = {"pin":mgpio[mm][1], "percentage":0, "frequency":FREQUENCY}
	gpio.setPWM(pin0)
	gpio.setPWM(pin1)


