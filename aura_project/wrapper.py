#!/usr/bin/python3.7
import urllib, re, requests, json, os, sys, index, time
from datetime import datetime
from datetime import date
#from gtts import gTTS
from shutil import copyfile
import edit_conf_state


def blockPrint():
	sys.stdout = open(os.devnull, 'w')

def enablePrint():
	sys.stdout = sys.__stdout__



def wthr_str(resp):
	txt = ''
	if 'sky' in resp['entity']: txt+='It is '+str(resp['entity']['sky'])+'. '

	jj = resp['entity']['str']
	if 'temp' in jj: txt += 'Temperature is '+str(resp['entity']['str']['temp'])+' degrees celcius. '
	if 'wind' in jj:
		if 'speed' in jj['wind']: txt += 'The wind speed is '+str(resp['entity']['str']['wind']['speed'])+' KMPH. '
		if 'deg' in jj['wind']: txt += 'Wind direction is '+str(resp['entity']['str']['wind']['deg'])+' degrees. '
	if 'humidity' in jj: txt += 'Humidity is '+str(resp['entity']['str']['humidity'])+' percent. '
	if 'visibility' in jj: txt += 'Visibility is '+str(resp['entity']['str']['visibility'])+' meters. '
	return txt


def speak_text(usr_txt, speak=False, offline=True):
	tts_fl = True
	blockPrint()
	print(usr_txt)
	if offline:
		out = index.fin_func(usr_txt)
	else:
		out = requests.get('mankash.co.in/matrix-server-bkd/index.py?text='+usr_txt.replace(' ', '+')).json()
	print(out)
	edit_conf_state.set_state(out['intent'],wf=False, conf=2)
	tvflag = False
	if out['intent'] == 'DATE':
		fin_txt = "it's "+date.today().strftime("%B %d, %Y")
	elif out['intent'] == 'TIME':
		fin_txt = "it's "+datetime.now().strftime('%I:%M %p')
	elif out['intent'] == 'WEATHER':
		fin_txt = wthr_str(out)
	elif out['intent'] == 'CMDPLAYSONG' or out['intent'] == 'CMDPLAYNEWS':
		tts_fl = False
#elif out['intent'] == 'EMERGENCY':

	elif out['intent'] == 'CMDPLAYONTV':
		fin_txt = 'playing'
		tvflag = True
	else:
		fin_txt = out['entity']['str'].lower()
	if tts_fl:
		os.system('python3.7 /home/pi/nlp/tts_b_c.py "'+fin_txt+'"')

	else:
		#url = 'http://mankash.co.in/'
		ffn = re.sub(r'\s+', '_', usr_txt)
		ffn = '/home/pi/nlp/output/'+ffn+'.mp3'
		if os.path.exists(ffn) and (time.time() - os.path.getmtime(ffn)) < 12*3600:
			copyfile(ffn, 'op.mp3')
		else:
			url = 'http://brahm.ai/'
			requests.get(url+'matrix-server-bkd/get_song_bt.py?text='+out['entity']['str'].lower().replace(' ', '+'))
			os.system('wget '+url+'matrix-server-bkd/op_me.mp3')
			copyfile('op_me.mp3', ffn)
			os.rename('op_me.mp3', 'op.mp3')
	if tvflag:
		query_string = urllib.parse.urlencode({"search_query" : out['entity']['str']})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		link="http://www.youtube.com/watch?v=" + search_results[0]
		os.system('catt cast '+link)
	
	if speak:
		os.system('omxplayer -o local op.mp3')
	enablePrint()
	
#print("Content-type:text/html\r\n\r\n")
#print('<html>')
#print('<head>')
#print('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
#print('<title>mp3</title>')
#print('<meta http-equiv="refresh" content="2; url=op.mp3" />')
#print('</head>')
#print('<body>')
#print('</body>')
#print('</html>')
