from matrix_lite import gpio
import time, os

debug = True
MOTOR = True
WAIT_TIME = 0.2
STEP_POWER_CHANGE = 20
FREQUENCY = 10000
FORWARD, REVERSE, STOP = "fwd", "rev", "stop"
FR, FL, RR, RL = "FR", "FL", "RR", "RL"
HALT = 'halt'
MOTOR_FIFO = '/home/pi/MOTOR_FIFO_DONT_TOUCH'

def start_fifo():
    if os.path.exists(MOTOR_FIFO) == False:
        os.mkfifo(MOTOR_FIFO)
    os.chmod(MOTOR_FIFO, 438)  # 438 is 0766 - let others write

def write_keypress_fifo(s):
    s = str(s)
    f = open(MOTOR_FIFO, "w")
    f.write(s)
    f.close()

class mpctrl():
	mgpio = {FR: (0,1), FL: (6,7), RR: (5,4), RL: (3,2)}
	cstate = None
	dstate = None
	tmp_halt = False
	all_mio = None
	stop_thread = False
	input_recvd = False

	def init():
		mpctrl.cstate = {FR: 0, FL: 0, RR: 0, RL: 0}
		mpctrl.dstate = {FR: 0, FL: 0, RR: 0, RL: 0}
		mpctrl.all_mio = mpctrl.mgpio[FR]+mpctrl.mgpio[FL]+mpctrl.mgpio[RR]+mpctrl.mgpio[RL]
		for i in mpctrl.all_mio:
			gpio.setFunction(i, 'PWM')
			gpio.setMode(i, "output")
	
	def stop():
		mpctrl.stop_thread = True

	def set_dstate(mm, val):
		if val < -100 or val > 100:
			print('ERROR: Allowed value for '+mm+' between -100 and 100 only')
			return False
		mpctrl.dstate[mm] = val

	def set_all_dstate(fr_val, fl_val, rr_val, rl_val):
		mpctrl.set_dstate(FR, fr_val)
		mpctrl.set_dstate(FL, fl_val)
		mpctrl.set_dstate(RR, rr_val)
		mpctrl.set_dstate(RL, rl_val)
		mpctrl.input_recvd = True

	def move_mtr(mm, speed):
		if speed >= 0:
			pin0 = {"pin":mpctrl.mgpio[mm][0], "percentage":abs(speed), "frequency":FREQUENCY}
			pin1 = {"pin":mpctrl.mgpio[mm][1], "percentage":0, "frequency":FREQUENCY}
		else:
			pin0 = {"pin":mpctrl.mgpio[mm][0], "percentage":0, "frequency":FREQUENCY}
			pin1 = {"pin":mpctrl.mgpio[mm][1], "percentage":abs(speed), "frequency":FREQUENCY}

		if debug:
			if debug: print(mm, ': ', pin0)
			if debug: print(mm, ': ', pin1)
		if MOTOR:
			gpio.setPWM(pin0)
			gpio.setPWM(pin1)

		if debug: print('updating cstate', mm, speed)
		mpctrl.cstate[mm] = speed

	def get_unit_change(current, dest, diff):
		if abs(diff) > STEP_POWER_CHANGE: 
			diff = STEP_POWER_CHANGE * int(diff/abs(diff))
		if diff >= 0 and (current + diff) > dest:
			return dest, diff
		elif diff < 0 and (current + diff) < dest:
			return dest, diff
		else: return current + diff, diff

	def get_power_change():
		dstate = mpctrl.dstate
		cstate = mpctrl.cstate
		if mpctrl.tmp_halt == True and mpctrl.get_motors_current_state() != HALT:
			dstate = {FR: 0, FL: 0, RR: 0, RL: 0}
		diff_fr = dstate[FR] - cstate[FR]
		diff_fl = dstate[FL] - cstate[FL]
		diff_rr = dstate[RR] - cstate[RR]
		diff_rl = dstate[RL] - cstate[RL]
		diff_total = abs(diff_fr) + abs(diff_fl) + abs(diff_rr) + abs(diff_rl)
		if debug: print('dstate:', mpctrl.dstate)
		if debug: print('tdstate:', dstate)
		if debug: print('cstate:', cstate)
		if debug: print('diffs:', diff_fr, diff_fl, diff_rr, diff_rl)
		if diff_total == 0:
			if debug: print('No change in motor power needed')
			return {'total_change': 0, 
					'diffs': (diff_fr, diff_fl, diff_rr, diff_rl),
					'change': {FR: 0, FL: 0, RR: 0, RL: 0}, 
					'exp_cstate': cstate}
		### add the STEP_POWER_CHANGE in destination direction maxing out to dstate
		fr_dt = mpctrl.get_unit_change(cstate[FR], dstate[FR], diff_fr)
		fl_dt = mpctrl.get_unit_change(cstate[FL], dstate[FL], diff_fl)
		rr_dt = mpctrl.get_unit_change(cstate[RR], dstate[RR], diff_rr)
		rl_dt = mpctrl.get_unit_change(cstate[RL], dstate[RL], diff_rl)
		return {'total_change': abs(fr_dt[1]) + abs(fl_dt[1]) + abs(rr_dt[1]) + abs(rl_dt[1]),
				'diffs': (diff_fr, diff_fl, diff_rr, diff_rl),
				'change': {FR: fr_dt[1], FL: fl_dt[1], RR: rr_dt[1], RL: rl_dt[1]}, 
				'exp_cstate': {FR: fr_dt[0], FL: fl_dt[0], RR: rr_dt[0], RL: rl_dt[0]}
				}

	def is_power_change_aligned(power_change):
		### if only total diff is same across all - can be removed later if nonuniform motor speeds required
		diff_values =  [abs(i) for i in power_change['diffs']]
		if debug: print('diffs;', diff_values)
		s_c = sorted(diff_values)
		if debug: print('s_c diffs;', s_c)
		if s_c[0] != s_c[-1]: return False

		### if only items getting changed are same independent of direction
		if debug: print('power_change', power_change)
		change = power_change['change']
		changed_values = []
		for mm in (FR, FL, RR, RL):
			if change[mm] != 0: changed_values.append(abs(change[mm]))
		## if only 1 motor changing
		if debug: print('changed_values;', changed_values)
		if len(changed_values) < 2: return True

		## if more than 1 motor changing by same value independent of direction
		## Sort the changes and check first and last value
		s_c = sorted(changed_values)
		if debug: print('s_c;', s_c)
		if s_c[0] == s_c[-1]: return True

		return False

	def get_motors_current_state():
		tot = 0
		for mm in (FR, FL, RR, RL):
			tot += abs(mpctrl.cstate[mm])
		if tot == 0: return HALT
		return None


	def run():
		while True:
			#### Wait for some time
			time.sleep(WAIT_TIME)

			if mpctrl.stop_thread: break
			if not mpctrl.input_recvd: continue
			
			### check if motors power needs to be changed
			### If power needs to be changed and all motors are not aligned (distance to destination is same) than set temp dest to zero power for all motors
			### Than identify change needed and update motor powers
			if debug: print('\n####################\ntmp_halt', mpctrl.tmp_halt)
			if debug: print('current_motor_state', mpctrl.get_motors_current_state())
			if mpctrl.tmp_halt == True and mpctrl.get_motors_current_state() == HALT:
				if debug: print('tmp halt finished, starting destination')
				mpctrl.tmp_halt = False
			power_change = mpctrl.get_power_change()
			if debug: print('power_change:', power_change)
			if power_change['total_change'] == 0:
				for mm in (FR, FL, RR, RL):
					mpctrl.move_mtr(mm, power_change['exp_cstate'][mm])
				mpctrl.input_recvd = False
				continue
			else:
				if mpctrl.is_power_change_aligned(power_change):
					### DO the power change and update cstate
					## exp_cstate in power change contains the desired state to reach destination
					if debug: print('\n###Next move')
					for mm in (FR, FL, RR, RL):
						mpctrl.move_mtr(mm, power_change['exp_cstate'][mm])

				else:
					if debug: print('Motors not aligned. Halting before destination')
					mpctrl.tmp_halt = True


			


