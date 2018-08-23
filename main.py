#!/usr/bin/python3
import os
import sys
import vlc
import time

inputs = [
	'\'/\'',
	'\'*\'',
	
	'\'7\'',
	'\'8\'',
	'\'9\'',
	
	'\'4\'',
	'\'5\'',
	'\'6\'',
	 
	'\'1\'',
	'\'2\'',
	'\'3\'',
	
	'\'0\'',
	'\'.\'',
]
special = [
	'\'+\'',
	'\'-\'',
	'\'\\x7f\'', # Backspace
	'\'\\r\'', # Return
	'\'\\x1b[H\'', # Home
	'\'\\x1b[F\'', # End
	'\'\\x1b[5\'', # PageUp
	'\'\\x1b[6\'', # PageDown
	'\'\\x1b[2\'', # Ins
	'\'\\x1b[3~\'', # Del
]

#instance = vlc.Instance('--input-repeat=999999')
instance = vlc.Instance()
player = instance.media_player_new()
currentPresetIndex = 0
numPresets = 0


def loadPresets():
	''' Get all the Presets in the current directory '''
	l = []
	for file in sorted(os.listdir(os.getcwd())):
	    if file.endswith(".preset"):
	        print("Preset Found:", os.path.join(os.getcwd(), file))
	        l.append(os.path.join(os.getcwd(), file))
	return l


def getPresetTracks(preset):
	''' Get all the links inside of a preset track '''
	l = []
	with open(preset) as file:
		for line in file:
			 # Need to get rid of those pesky \n's
			print(str(len(l)) + ': ', line[:-1])
			l.append(line[:-1])
	return l


def isYouTubeAudio(link):
	import re
	if re.match(r'http[s]:\/\/www\.youtube\.com/watch\?v=([\w-]{11})', link) == None:
		return False
	else:
		return True
	

def getYouTubeAudioTrack(link):
	''' Get Audio track of a link '''
	import pafy

	video = pafy.new(link)
	bestaudio = video.getbestaudio()

	# print(bestaudio.url)
	return bestaudio.url


def playQuick(num):
	''' Make quick sound '''
	l = ['up.mp3', 'down.mp3', 'preset_change.mp3', 'startup.mp3']
	s = instance.media_new(os.path.join(os.getcwd(), l[num]))
	player.set_media(s)
	player.play()
	if num == 3:
		time.sleep(4)
	else:
		time.sleep(1)
	player.stop()


def switchPresets(readyPresets):
	#playQuick(2)
	
	print("Ready to swap the preset. Loaded presets:")
	i = 0
	for link in readyPresets:
		print(i, "-", link)
		i += 1

	newPreset = input("What would you like your preset to be?: ")
	
	if newPreset.isdigit() and int(newPreset) < len(presetList):
		# Number preset. We're goood
		numPre = int(newPreset)
		print("New Preset: ", numPre)
		#playQuick(0)
		return numPre
	else:
		# It's a character. Stop
		print("Invalid preset. Skipping.")
		playQuick(1)
		return None
		
		
def playFile():
	with open("url.txt") as file:
		for line in file:
			print("Contents: " + line)
			playTrack(line[:-1])
			

def playTrack(track):
	''' Play an audio track indefinetly. Also awaits response so it can detect a change in information '''
	from readchar import readkey

	# Load and add media file
	media = instance.media_new(track)
	player.set_media(media)

	# Play
	player.play()

	# Pause before getting the status, to update everything
	print(str(player.get_state()) + "          ", end='\r')
	sys.stdout.flush()
	time.sleep(1)
	
	print(str(player.get_state()) + "          ")


if __name__ == '__main__':
	presetList = loadPresets()
	numPresets = len(presetList)
	preset = getPresetTracks(presetList[currentPresetIndex])
	
	# Start Up and initial setup
	active = False
	
	playQuick(0)

	import readchar

	keyInput = '\'0\''
	# Start Main loop
	print("Ready for input")
	while keyInput not in inputs or keyInput not in special:
		keyInput = repr(readchar.readkey())
		# print("Got key: " + keyInput)
		
		# Sanitize input
		if keyInput in inputs:
			sanitized = inputs.index(keyInput)

			player.stop()
			active = True

			if sanitized < len(preset):
				if isYouTubeAudio(preset[sanitized]):
					playTrack(getYouTubeAudioTrack(preset[sanitized]))
				else:
					playTrack(preset[sanitized])
			else:
				playQuick(1)


		# Special Characters
		elif keyInput == '\'+\'':
			currentPresetIndex += 1
			if currentPresetIndex == numPresets:
				currentPresetIndex = 0
			preset = getPresetTracks(presetList[currentPresetIndex])
				
		elif keyInput == '\'-\'':
			currentPresetIndex -= 1
			if currentPresetIndex == -1:
				currentPresetIndex = numPresets - 1
			preset = getPresetTracks(presetList[currentPresetIndex])
				
		elif keyInput == '\'\\x7f\'': # Backspace
			currentPresetIndex = 0
			preset = getPresetTracks(presetList[currentPresetIndex])
			
		elif keyInput == '\'\\r\'': # Return
			active = False
			player.stop()

		elif keyInput == '\'\\x1b[H\'': # Home (reboot)
			print("Home")
			os.system('sudo reboot')

		elif keyInput == '\'\\x1b[F\'': # End (exit app)
			print("End")
			exit()

		elif keyInput == '\'\\x1b[5\'': # PageUp (ifup)
			print("PageUp")
			os.system('sudo ifup wlan0')

		elif keyInput == '\'\\x1b[6\'': # PageDown (ifdown)
			print("PageDown")
			os.system('sudo ifdown wlan0')

		elif keyInput == '\'\\x1b[2\'': # Ins (unused)
			print("Ins")

		elif keyInput == '\'\\x1b[3~\'': # Del
			print("Del")
			playFile()

		elif keyInput == '\'x\'':
			# End case
			exit() 

