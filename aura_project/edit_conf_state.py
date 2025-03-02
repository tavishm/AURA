import state_config
from op_cv_gif_view import write_in_fifo

emodict = {'listening':'listening',
	'sleeping':'sleeping',
	'working':'taking-note',
	'driving': 'driving',
	'DATE':'talking',
	'NXMED':'talking',
	'TIME':'talking',
	'LAUGH':'lol-laughing',
	'WHEREBOT':'talking',
	'WEATHER':'talking',
	'CMDPLAYSONG':'playing-music',
	'CMDPLAYONTV':'playing-music',
	'CMDPLAYNEWS':'talking',
	'DEFINATIONS':'talking',
	'GREET':'hi',
	'HOWRU':'hi',
	'WHATSUP':'hi',
	'EMERGENCY':'taking-note',
	'CWHOBOT':'hi',
	'CAREBOT': 'talking',
	'CSORRY':'lol-laughing',
	'PRAISE': 'lol-laughing',
	'CREATOR':'talking',
	'THANK':'hi',
	'BEFRIEND':'hi',
	'AGE':'talking',
	'OK':'hi',
	'BOTBUSY':'talking',
	'BOTSMARTER':'talking',
	'CANASKQUEST':'hi',
	'CWELCOME':'hi',
	'SODOI':'lol-laughing',
	'ANGRYATBOT':'weeping-crying',
	'CWHATBOTDO':'talking',
	'error':'weeping-cry',
}
def set_state(state, wf=True, conf=1):
	if conf==1:
		state_config.current_state = state
	elif conf==2:
		state_config.emo_state = state
	try:
		if wf:
			write_in_fifo(emodict[state])
	except:
		write_in_fifo("weeping-crying")

def tell_set():	return  state_config.emo_state
