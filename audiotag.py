# -*- coding: utf-8 -*-
import requests
import json
import time
import sys
import os


apikey   = 'censored';
api_url  = 'https://audiotag.info/api'

def build_name(splited):
	return os.path.join(splited[0], splited[1])

def	get_token(filename):
	payload  = {'action': 'identify', 'apikey': apikey}
	result = requests.post(api_url, data=payload, files = {'file': open(filename, 'rb')})
	json_object = json.loads(result.text);
	token = json_object['token']
	return (token)

def def_song(path):
	token = get_token(path)
	n = 1;
	while n < 10:
		time.sleep(0.5);
		print('request:%d'%(n));
		n+=1;
		payload = {'action': 'get_result', 'token': token, 'apikey': apikey}
		result = requests.post(api_url,data = payload)
		print(result.text);
		json_object = json.loads(result.text);
		print(json_object);
		if json_object['success'] == True and json_object['result'] != 'wait' and json_object['result'] != 'not found' :
			name = json_object['data'][0]['tracks'][0][1]
			name += ' - '
			name += json_object['data'][0]['tracks'][0][0]
			return (name)
	return 'bad'

def get_splited_names(name):
	text_file = open(name, 'r')
	lines = text_file.read().split('\n')
	split_arr = list()
	for line in lines:
		split_arr.append(line.split('/'))
	return split_arr

# filename = 'f14486176.mp3'
# pretty_print = json.dumps(json_object, indent=4, sort_keys=True)
# print(pretty_print.encode().decode('utf-8'));

splited_names = get_splited_names('names.txt')
for song in splited_names:
	print(song)
	song_path = build_name(song)
	defined_song = def_song(build_name(song))
	if (defined_song != 'bad'):
		new_name = song[0] + '/' + defined_song + '.mp3'
		os.rename(song_path, new_name)
		just_name = new_name.split('/')
		os.replace(new_name, 'renamed/' + just_name[1])
		print(new_name)
	else:
		print('could not rename!')
		just_name = song_path.split('/')
		os.replace(song_path, 'not_found/' + just_name[1])

#song_name = def_song(build_name(splited_names[0]))
print(song_name)


# for line in split_arr:
# 	print(line)

#os.rename(splited[1] + '/' + splited[2], splited[1] + '/a' + splited[2])
