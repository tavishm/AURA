#!/usr/bin/python3.7
#import mysql.connector
#from logdb import logdb
import os
from mtW2N import mtW2N
import nltk
from botPatterns import botPatterns as bpt
import re, requests, nlp_config, json
import datetime
import humanize
import op_cv_gif_view
#import cgi
#import cgitb
#cgitb.enable()
#form = cgi.FieldStorage()
#print("Content-type:text/html\r\n\r\n")
#print('<html>')
#print('<head>')
#print('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
#print('<title>Welcome to the chat site</title>')
#print('</head>')

def send_sms(mobile, name, line):
	url="http://cloud.smsindiahub.in/vendorsms/pushsms.aspx"
	params={'user':'baljits', 'password':'VeryBraVeryhmLongKey', 'sid':'BRHMAI', 'fl':0, 'gwid':2}
	params['msisdn'] = str(mobile)
	#params['msg'] = name+" needs urgent care. "+name+" told me: 'ffdd'\n\nYours faithfully,\nAura"
	params['msg'] = "Your dependent "+name+" needs urgent care. Please contact your dependent ASAP."
	r = requests.get(url=url, params=params)
	print('SMS sent response:', r.text)

def when_nex_med():
	rawdata = requests.get('http://brahm.ai/matrix-server-bkd/get_med.py?key=kanhamadeaappin1dayandthispasswordisquiteuniqueithinkbutaappin1dayisgreatanditisenoughrandomkanhaanywaypastethisrandomkeythankyoufullstopandpleasedontmodifythisatallthankyoufullstop').text

	## processing web response
	mdict = json.loads(rawdata)
	low_time = []
	for medn in mdict:
		info_array = mdict[medn]
		folu = int(info_array[1])
		freq = info_array[0]
		date_str = info_array[2]
		date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
		validity = date_obj+datetime.timedelta(days=folu)
		if datetime.datetime.now() < validity:
			time1rem = datetime.datetime.strptime('13:00', '%H:%M')
			if freq == 'once':
				if time1rem >  datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M"):
					timel = time1rem - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")
				else:
					timel = datetime.timedelta(days=1)-(datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M") - time1rem)
				low_time.append({medn:timel})



			elif freq=='twice':

				time1rem = datetime.datetime.strptime('10:00', '%H:%M')
				time2rem = datetime.datetime.strptime('18:00', '%H:%M')


				if time1rem >  datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M"):
					timel = time1rem - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")

				elif time2rem >  datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M"):
					timel = time2rem - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")
				else:
					timel = datetime.timedelta(days=1)-(datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M") - time1rem)
				low_time.append({medn:timel})



			elif freq =='thrice':


				time1rem = datetime.datetime.strptime('9:00', '%H:%M')
				time2rem = datetime.datetime.strptime('13:00', '%H:%M')
				time3rem = datetime.datetime.strptime('18:00', '%H:%M')

				if time1rem >  datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M"):
					timel = time1rem - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")


				elif time2rem >  datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M"):
					timel = time2rem - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")


				elif time3rem >  datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M"):
					timel = time3rem - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")
				else:
					timel = datetime.timedelta(days=1)-(datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M") - time1rem)


				low_time.append({medn:timel})
	
	time_left = datetime.timedelta(days=1)	
	fmedn = []
	for dicti in low_time:
		for medn2 in dicti:
			if dicti[medn2] < time_left:
				time_left = dicti[medn2]
				fmedn = [medn2]
			elif dicti[medn2] == time_left:
				fmedn.append(medn2)

	if len(fmedn) == 0:
		return 'please set medication reminders from the aura app.'
	else:
		return 'Please take '+' and '.join(fmedn)+' in '+humanize.naturaltime(-time_left)
						
					

def get_weather():
		import pyowm
		lat = 12.9716
		lng = 77.5946
		owm = pyowm.OWM('ec56199f1e5d0b09bdfebe911252c02d')
		observation = owm.weather_at_coords(float(lat), float(lng))
		w = observation.get_weather()
		temp = int(w.get_temperature()['temp']-273.15)
		wind = w.get_wind()
		sky = w.get_detailed_status()
		humid = w.get_humidity()
		visibility = w.get_visibility_distance()
		response = {'temp':temp, 'wind': wind, 'sky':sky, 'humidity':humid, 'visibility':visibility}
		return response

def define(text):
		ffn = re.sub(r'\s+', '_', text)
		ffn = 'output/'+ffn+'.txt'
		if os.path.exists(ffn):
			with open(ffn, 'r') as content_file:
				definition = content_file.read()
				return definition

		else:
			ttt = re.sub("(?i)^(.*(what|who|where)\s+(is|are|r)?\s the?|.*tell me about the?|.*define the?)", "", text)
			import wikipedia
			try:
				definition = wikipedia.summary(ttt, sentences=2)
				content_file = open(ffn, 'w')
				content_file.write(definition)
				content_file.close()
				return definition
			except:
				print(ttt)
				return 'I dont know about '+' '.join(ttt).lower()+'. I am still learning'

def preprocess(text):
		text = text.replace("?", "")
		text = text.replace("!", "")
		text = re.sub("(?i)(ha)+", 'ha', text)
		text = re.sub("(?i)(hah)+", 'ha', text)
		text = mtW2N.rep_w2n(text)
		textpu = text.split()
		text = text.upper()
		for (pattern, rep) in bpt.preprocess:
			text = re.sub("(?i)"+pattern, rep, text)
		return text

def parse(text):
	#tokenizing
	tokens = text.split()
	#making tager
	tager = nltk.RegexpTagger(bpt.taggrammar)
	#making chunker
	chunker = nltk.RegexpParser(bpt.chunkgrammar)
	#taging and chunking text
	tagtext = tager.tag(tokens)
	newtagtext = []
	for (word, tag) in tagtext:
		if tag == 'SELFTAG': newtagtext.append( (word,word))
		else: newtagtext.append( (word,tag))
#   print('tags',newtagtext)
	chunktext = chunker.parse(newtagtext)
	#main program
#   print(chunktext)
	return chunktext
def tv_sep(tree):
	tree = tree.leaves()
	dflag = False
	k = ''
	for el in tree:
		if el[1] == 'VIDST':
			dflag = False
		if dflag == True:
			k = k+el[0]+' '
		if el[1] == 'PLAY':
			dflag = True
	return k
def get_tree_sentence(tree): return ' '.join( [e[0] for e in tree.leaves()] )
def get_tree_sent_element(tree): return ' '.join([e for e in tree])
#def voice(text): os.system('echo "'+text+'" | festival --tts')
def intentresolution(tree, text):
	for st in tree:
		if type(st) == nltk.tree.Tree and st.label() == 'DATE':
			return(st.label(), '')
		if type(st) == nltk.tree.Tree and st.label() == 'NXMED':
			return(st.label(), when_nex_med())
		elif type(st) == nltk.tree.Tree and st.label() == 'TIME':
			return(st.label(), '')
		elif type(st) == nltk.tree.Tree and st.label() == 'LAUGH':
			return(st.label(), "Ha-ha-ha-ha-ha")
		elif type(st) == nltk.tree.Tree and st.label() == 'WHEREBOT':
			return(st.label(), "I am next to you, but you can't see me.")
		elif type(st) == nltk.tree.Tree and st.label() == 'WEATHER':
			return(st.label(), get_weather())
		elif type(st) == nltk.tree.Tree and st.label() == 'CMDPLAYSONG':
			return (st.label(),get_tree_sentence(st[1])+' song')
		elif type(st) == nltk.tree.Tree and st.label() == 'CMDPLAYONTV':
			return (st.label(),tv_sep(tree))
		elif type(st) == nltk.tree.Tree and st.label() == 'CMDPLAYNEWS':
			return(st.label(), 'shatak aaj tak')
		elif type(st) == nltk.tree.Tree and st.label() == 'DEFINATIONS':
			return(st.label(), define(text))
		elif type(st) == nltk.tree.Tree and st.label() == 'GREET':
			return(st.label(), 'hello.')
		elif type(st) == nltk.tree.Tree and st.label() == 'HOWRU':
			return(st.label(), 'I am fine, Thanks!')
		elif type(st) == nltk.tree.Tree and st.label() == 'WHATSUP':
			return(st.label(), 'Nothing Much.')
		elif type(st) == nltk.tree.Tree and st.label() == 'EMERGENCY':
			if nlp_config.ENABLE_SMS:
				send_sms(nlp_config.CT_PHONE, nlp_config.CT_NAME, text)
			return(st.label(), 'I have notified family members.')
		elif type(st) == nltk.tree.Tree and st.label() == 'CWHOBOT':
			return(st.label(), "I'm your day-to-day assistance robot.")
		elif type(st) == nltk.tree.Tree and st.label() == 'CAREBOT':
			return(st.label(), 'Yes.')
		elif type(st) == nltk.tree.Tree and st.label() == 'CSORRY':
			return(st.label(), "It's okay.")
		elif type(st) == nltk.tree.Tree and st.label() == 'PRAISE':
			return(st.label(), 'Thanks.')
		elif type(st) == nltk.tree.Tree and st.label() == 'CREATOR':
			return(st.label(), 'I was created by Tavish Mankash and Abhimanyu Mankash.')
		elif type(st) == nltk.tree.Tree and st.label() == 'THANK':
			return(st.label(), "you're welcome.")
		elif type(st) == nltk.tree.Tree and st.label() == 'BEFRIEND':
			return(st.label(), "Yes.")
		elif type(st) == nltk.tree.Tree and st.label() == 'AGE':
			return(st.label(), "I was born on Christmas, 2018.")
		elif type(st) == nltk.tree.Tree and st.label() == 'OK':
			return(st.label(), "okay.")
		elif type(st) == nltk.tree.Tree and st.label() == 'BOTBUSY':
			return(st.label(), "No, I am not busy. I am always free.")
		elif type(st) == nltk.tree.Tree and st.label() == 'BOTSMARTER':
			return(st.label(), "I can, but Tavish and Abhimanyu can make me smarter.It's not under my control.")
		elif type(st) == nltk.tree.Tree and st.label() == 'CANASKQUEST':
			return(st.label(), "Ok, What is it?")
		elif type(st) == nltk.tree.Tree and st.label() == 'CWELCOME':
			return(st.label(), "okay.")
		elif type(st) == nltk.tree.Tree and st.label() == 'CSODOI':
			return(st.label(), "So do I.")
		elif type(st) == nltk.tree.Tree and st.label() == 'ANGRYATBOT':
			return(st.label(), 'I am sorry.')
		elif type(st) == nltk.tree.Tree and st.label() == 'CWHATBOTDO':
			return(st.label(), "Here are some of the things I can do for you:\n1. play news. \n2. tell the weather.\n3. play music. \n4. Notify your family if anything bothers you.\n5. talk with you.\n6 You'll have to discover the rest yourself.")
		else:
			return('error', "Sorry, I couldn't understand what you meant.")
	return('error', "An error occoured")
#if 'text' in form:
#	text = form['text'].value
#else:
def fin_func(text):
	import sys
#text = sys.argv[1]
	if text ==None or len(text) == 0: text = 'wq'
	orig_text = text
#if 'uid' in form:
#	uid = form['uid'].value 
#else:
	uid = 'matrix'
#if 'lat' in form:
#	lat = form['lat'].value 
#else:
	lat = 12.9716
#if 'lng' in form :
#	lng = form['lng'].value 
#else:
	lng = '77.1025'
#if 'city' in form:
#	city = form['city'].value 
#else:
	city = 'bangalore'
	textpu = text
	textpu = textpu.split()
	text = preprocess(text)
	tree = parse(text)
	intent, entity = intentresolution(tree, text)
#print(intent)
#music
	response = {}
	divide = re.findall('(?i)(.*?)(plus|minus|into|by|divided by)(.*)',preprocess(text))
	if len(divide) > 0:
		divide = divide[0]
	if len(divide) == 3:
		d1 = divide[0].split()
		d2 = divide[2].split()
		no1 = int(d1[-1])
		no2 = int(d2[0])
		operator = divide[1].split()[0]
		if operator in ['PLUS']:
			calcout = no1+no2
		elif operator in ['MINUS']:
			calcout = no1-no2
		elif operator in ['BY', 'DIVIDED BY']:
			calcout = no1/no2
		else:
			calcout = no1*no2
		response = {'intent':'CALCULATE', 'entity':{'str': calcout}}
	else:
		response = {'intent':intent,'entity':{'str': entity}}

#	import json
#	response_str = json.dumps(response)
## log 
#logobj = logdb()
#logobj.insertlog(uid, orig_text, response_str, city)
#logobj.close()
#print('Content-Type: application/json\n');
#print(answer)
	return response
#print('<body>')
#print('</body>')
#print('</html>')

