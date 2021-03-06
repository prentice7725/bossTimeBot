# -*- coding: utf-8 -*- 

################ Server Ver. 28 (2021. 6. 23.) #####################

import sys, os, ctypes
import asyncio, discord, aiohttp
import random, re, datetime, time, logging
from discord.ext import tasks, commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from gtts import gTTS
from github import Github
import base64
import gspread, boto3
from oauth2client.service_account import ServiceAccountCredentials 
from io import StringIO
import urllib.request
from math import ceil, floor

##################### Loggin ###########################
log_stream = StringIO()    
logging.basicConfig(stream=log_stream, level=logging.WARNING)

#ilsanglog = logging.getLogger('discord')
#ilsanglog.setLevel(level = logging.WARNING)
#handler = logging.StreamHandler()
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#ilsanglog.addHandler(handler)
#####################################################

if not discord.opus.is_loaded():
	discord.opus.load_opus(ctypes.util.find_library('opus'))
	print("opus_loaded")

basicSetting = []
bossData = []
fixed_bossData = []

bossNum = 0
fixed_bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

fixed_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
fixed_bossFlag = []
fixed_bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

FixedBossDateData = []
indexFixedBossname = []

endTime = None

gc = None
credentials = None

regenembed = None
command = None
kill_Data = None
kill_Time = None
item_Data = None

tmp_racing_unit = None
setting_channel_name = None

boss_nick = {}

access_token = os.environ["BOT_TOKEN"]			
git_access_token = os.environ["GIT_TOKEN"]			
git_access_repo = os.environ["GIT_REPO"]			
git_access_repo_restart = os.environ["GIT_REPO_RESTART"]
try:	
	aws_key = os.environ["AWS_KEY"]			
	aws_secret_key = os.environ["AWS_SECRET_KEY"]			
except:
	aws_key = ""
	aws_secret_key = ""

g = Github(git_access_token)
repo = g.get_repo(git_access_repo)
repo_restart = g.get_repo(git_access_repo_restart)

def init():
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	global LoadChk
	
	global indexFixedBossname
	global FixedBossDateData

	global endTime
	
	global gc #??????
	global credentials #??????
	
	global regenembed
	global command
	global kill_Data
	global kill_Time
	global item_Data

	global tmp_racing_unit

	global boss_nick

	command = []
	tmp_bossData = []
	tmp_fixed_bossData = []
	FixedBossDateData = []
	indexFixedBossname = []
	kill_Data = {}
	tmp_kill_Data = []
	item_Data = {}
	tmp_item_Data = []
	f = []
	fb = []
	fk = []
	fc = []
	fi = []
	tmp_racing_unit = []
	boss_nick = {}
	
	inidata = repo.get_contents("test_setting.ini")
	file_data1 = base64.b64decode(inidata.content)
	file_data1 = file_data1.decode('utf-8')
	inputData = file_data1.split('\n')

	command_inidata = repo.get_contents("command.ini")
	file_data4 = base64.b64decode(command_inidata.content)
	file_data4 = file_data4.decode('utf-8')
	command_inputData = file_data4.split('\n')
	
	boss_inidata = repo.get_contents("boss.ini")
	file_data3 = base64.b64decode(boss_inidata.content)
	file_data3 = file_data3.decode('utf-8')
	boss_inputData = file_data3.split('\n')

	fixed_inidata = repo.get_contents("fixed_boss.ini")
	file_data2 = base64.b64decode(fixed_inidata.content)
	file_data2 = file_data2.decode('utf-8')
	fixed_inputData = file_data2.split('\n')

	kill_inidata = repo.get_contents("kill_list.ini")
	file_data5 = base64.b64decode(kill_inidata.content)
	file_data5 = file_data5.decode('utf-8')
	kill_inputData = file_data5.split('\n')

	item_inidata = repo.get_contents("item_list.ini")
	file_data6 = base64.b64decode(item_inidata.content)
	file_data6 = file_data6.decode('utf-8')
	item_inputData = file_data6.split('\n')

	for i in range(len(fixed_inputData)):
		FixedBossDateData.append(fixed_inputData[i])

	index_fixed = 0

	for value in FixedBossDateData:
		if value.find('bossname') != -1:
			indexFixedBossname.append(index_fixed)
		index_fixed = index_fixed + 1

	for i in range(inputData.count('\r')):
		inputData.remove('\r')

	for i in range(command_inputData.count('\r')):
		command_inputData.remove('\r')
		
	for i in range(boss_inputData.count('\r')):
		boss_inputData.remove('\r')

	for i in range(fixed_inputData.count('\r')):
		fixed_inputData.remove('\r')
	
	for i in range(kill_inputData.count('\r')):
		kill_inputData.remove('\r')

	for i in range(item_inputData.count('\r')):
		item_inputData.remove('\r')

	del(command_inputData[0])
	del(boss_inputData[0])
	del(fixed_inputData[0])
	del(kill_inputData[0])
	del(item_inputData[0])

#	for data in boss_inputData:
#		if "kakaoOnOff" in data:
#			raise Exception("[boss.ini] ???????????? [kakaoOnOff]??? ???????????????.")

#	for data in fixed_inputData:
#			if "kakaoOnOff" in data:
#				raise Exception("[fixed_boss.ini] ???????????? [kakaoOnOff]??? ???????????????.")

	############## ????????? ?????? ?????? ????????? #####################
	try:
		basicSetting.append(inputData[0][11:])     #basicSetting[0] : timezone
		basicSetting.append(inputData[8][15:])     #basicSetting[1] : before_alert
		basicSetting.append(inputData[10][11:])     #basicSetting[2] : mungChk1
		basicSetting.append(inputData[9][16:])     #basicSetting[3] : before_alert1
		basicSetting.append(inputData[14][14:16])  #basicSetting[4] : restarttime ???
		basicSetting.append(inputData[14][17:])    #basicSetting[5] : restarttime ???
		basicSetting.append(inputData[1][15:])     #basicSetting[6] : voice??????????????? ID
		basicSetting.append(inputData[2][14:])     #basicSetting[7] : text??????????????? ID
		basicSetting.append(inputData[3][16:])     #basicSetting[8] : ????????? ?????? ID
		basicSetting.append(inputData[13][14:])    #basicSetting[9] : !??? ?????? ???
		basicSetting.append(inputData[17][11:])    #basicSetting[10] : json ?????????
		basicSetting.append(inputData[4][17:])     #basicSetting[11] : ?????? ?????? ID
		basicSetting.append(inputData[16][12:])    #basicSetting[12] : sheet ??????
		basicSetting.append(inputData[15][16:])    #basicSetting[13] : restart ??????
		basicSetting.append(inputData[18][12:])    #basicSetting[14] : ?????? ??????
		basicSetting.append(inputData[19][12:])    #basicSetting[15] : ?????? ???
		basicSetting.append(inputData[20][13:])    #basicSetting[16] : ?????? ???
		basicSetting.append(inputData[12][13:])     #basicSetting[17] : ???????????????
		basicSetting.append(inputData[5][14:])     #basicSetting[18] : kill?????? ID
		basicSetting.append(inputData[6][16:])     #basicSetting[19] : racing ?????? ID
		basicSetting.append(inputData[7][14:])     #basicSetting[20] : item ?????? ID
		basicSetting.append(inputData[21][12:])     #basicSetting[21] : voice_use
		basicSetting.append(inputData[11][11:])     #basicSetting[22] : mungChk2
	except:
		raise Exception("[test_setting.ini] ?????????????????????")

	############## ????????? ????????? ????????? #####################
	for i in range(len(command_inputData)):
		tmp_command = command_inputData[i][12:].rstrip('\r')
		fc = tmp_command.split(', ')
		command.append(fc)
		fc = []
		#command.append(command_inputData[i][12:].rstrip('\r'))     #command[0] ~ [24] : ?????????

	################## ?????? ?????? ###########################
	for i in range(len(kill_inputData)):
		tmp_kill_Data.append(kill_inputData[i].rstrip('\r'))
		fk.append(tmp_kill_Data[i][:tmp_kill_Data[i].find(' ')])
		fk.append(tmp_kill_Data[i][tmp_kill_Data[i].find(' ')+1:])
		try:
			kill_Data[fk[0]] = int(fk[1])
		except:
			pass
		fk = []

	for i in range(len(item_inputData)):
		tmp_item_Data.append(item_inputData[i].rstrip('\r'))
		fi.append(tmp_item_Data[i][:tmp_item_Data[i].find(' ')])
		fi.append(tmp_item_Data[i][tmp_item_Data[i].find(' ')+1:])
		try:
			item_Data[fi[0]] = int(fi[1])
		except:
			pass
		fi = []

	tmp_killtime = datetime.datetime.now().replace(hour=int(5), minute=int(0), second = int(0))
	kill_Time = datetime.datetime.now()

	if tmp_killtime < kill_Time :
		kill_Time = tmp_killtime + datetime.timedelta(days=int(1))
	else:
		kill_Time = tmp_killtime
	
	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	try:
		if basicSetting[6] != "":
			basicSetting[6] = int(basicSetting[6])
			
		if basicSetting[7] != "":
			basicSetting[7] = int(basicSetting[7])
		
		if basicSetting[8] != "":
			basicSetting[8] = int(basicSetting[8])
			
		if basicSetting[11] != "":
			basicSetting[11] = int(basicSetting[11])

		if basicSetting[18] != "":
			basicSetting[18] = int(basicSetting[18])

		if basicSetting[19] != "":
			basicSetting[19] = int(basicSetting[19])

		if basicSetting[20] != "":
			basicSetting[20] = int(basicSetting[20])
	except ValueError:
		raise Exception("[test_setting.ini] ?????????????????????")
	
	tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
	
	if int(basicSetting[13]) == 0 :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		endTime = endTime + datetime.timedelta(days=int(1000))
	else :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		if endTime < tmp_now :			
			endTime = endTime + datetime.timedelta(days=int(basicSetting[13]))
	
	bossNum = int(len(boss_inputData)/6)

	fixed_bossNum = int(len(fixed_inputData)/6) 
	
	for i in range(bossNum):
		tmp_bossData.append(boss_inputData[i*6:i*6+6])

	for i in range(fixed_bossNum):
		tmp_fixed_bossData.append(fixed_inputData[i*6:i*6+6]) 
		
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()

	tmp_boss_name_list : list = []
	tmp_nick : list = []

	############## ???????????? ?????? ????????? #####################
	for j in range(bossNum):
		tmp_nick = []
		tmp_len = tmp_bossData[j][1].find(':')
		tmp_boss_name_list = tmp_bossData[j][0][11:].split(", ")
		f.append(tmp_boss_name_list[0])         #bossData[0] : ?????????
		if len(tmp_boss_name_list) > 1:
			for nick in tmp_boss_name_list[1:]:
				tmp_nick.append(nick)
			boss_nick[tmp_boss_name_list[0]] = tmp_nick
		f.append(tmp_bossData[j][1][10:tmp_len])  #bossData[1] : ???
		f.append(tmp_bossData[j][2][13:])         #bossData[2] : ???/?????????
		f.append(tmp_bossData[j][3][20:])         #bossData[3] : ?????? ????????????
		f.append(tmp_bossData[j][4][13:])         #bossData[4] : ??? ????????????
		f.append(tmp_bossData[j][1][tmp_len+1:])  #bossData[5] : ???
		f.append('')                              #bossData[6] : ?????????
		f.append(tmp_bossData[j][5][11:])		  #bossData[8] : ?????????????????????
		bossData.append(f)
		f = []
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('99:99:99')
		tmp_bossDateString.append('9999-99-99')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)
		
	tmp_fixed_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

	############## ???????????? ?????? ????????? #####################	
	for j in range(fixed_bossNum):
		try:
			tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
			tmp_fixedGen_len = tmp_fixed_bossData[j][2].find(':')
			fb.append(tmp_fixed_bossData[j][0][11:])                  #fixed_bossData[0] : ?????????
			fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])     #fixed_bossData[1] : ???
			fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])     #fixed_bossData[2] : ???
			fb.append(tmp_fixed_bossData[j][4][20:])                  #fixed_bossData[3] : ?????? ????????????
			fb.append(tmp_fixed_bossData[j][5][13:])                  #fixed_bossData[4] : ??? ????????????
			fb.append(tmp_fixed_bossData[j][2][12:tmp_fixedGen_len])  #fixed_bossData[5] : ?????????-???
			fb.append(tmp_fixed_bossData[j][2][tmp_fixedGen_len+1:])  #fixed_bossData[6] : ?????????-???
			fb.append(tmp_fixed_bossData[j][3][12:16])                #fixed_bossData[7] : ?????????-???	
			fb.append(tmp_fixed_bossData[j][3][17:19])                #fixed_bossData[8] : ?????????-???
			fb.append(tmp_fixed_bossData[j][3][20:22])                #fixed_bossData[9] : ?????????-???
			fixed_bossData.append(fb)
			fb = []
			fixed_bossFlag.append(False)
			fixed_bossFlag0.append(False)
			fixed_bossTime.append(tmp_fixed_now.replace(year = int(fixed_bossData[j][7]), month = int(fixed_bossData[j][8]), day = int(fixed_bossData[j][9]), hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
			if fixed_bossTime[j] < tmp_fixed_now :
				while fixed_bossTime[j] < tmp_fixed_now :
					fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(hours=int(fixed_bossData[j][5]), minutes=int(fixed_bossData[j][6]), seconds = int(0))
			if  tmp_fixed_now + datetime.timedelta(minutes=int(basicSetting[1])) <= fixed_bossTime[j] < tmp_fixed_now + datetime.timedelta(minutes=int(basicSetting[3])):
				fixed_bossFlag0[j] = True
			if fixed_bossTime[j] < tmp_fixed_now + datetime.timedelta(minutes=int(basicSetting[1])):
				fixed_bossFlag[j] = True
				fixed_bossFlag0[j] = True
		except:
			raise Exception(f"[fixed_boss.ini] ?????? {tmp_fixed_bossData[j][0][11:]} ?????? ????????? ???????????????.")

	################# ????????? ?????? ######################

	emo_inidata = repo.get_contents("emoji.ini")
	emoji_data1 = base64.b64decode(emo_inidata.content)
	emoji_data1 = emoji_data1.decode('utf-8')
	emo_inputData = emoji_data1.split('\n')

	for i in range(len(emo_inputData)):
		tmp_emo = emo_inputData[i][8:].rstrip('\r')
		if tmp_emo != "":
			tmp_racing_unit.append(tmp_emo)
	
	################# ???????????? ?????? ?????? ######################
	regenData = []
	regenTime = []
	regenbossName = []
	outputTimeHour = []
	outputTimeMin = []

	for i in range(bossNum):
		if bossData[i][2] == "1":
			f.append(bossData[i][0] + "R")
		else:
			f.append(bossData[i][0])
		f.append(bossData[i][1] + bossData[i][5])
		regenData.append(f)
		regenTime.append(bossData[i][1] + bossData[i][5])
		f = []
		
	regenTime = sorted(list(set(regenTime)))
	
	for j in range(len(regenTime)):
		for i in range(len(regenData)):
			if regenTime[j] == regenData[i][1] :
				f.append(regenData[i][0])
		regenbossName.append(f)
		try:
			outputTimeHour.append(int(regenTime[j][:2]))
			outputTimeMin.append(int(regenTime[j][2:]))
		except ValueError:
			raise Exception(f"[boss.ini] ?????? {f} gentime??? ??????????????? ????????????.")
		f = []

	regenembed = discord.Embed(
			title='----- ????????????????????? -----',
			description= ' ')
	for i in range(len(regenTime)):
		if outputTimeMin[i] == 0 :
			regenembed.add_field(name=str(outputTimeHour[i]) + '??????', value= '```'+ ', '.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
		else :
			regenembed.add_field(name=str(outputTimeHour[i]) + '??????' + str(outputTimeMin[i]) + '???', value= '```' + ','.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
	regenembed.set_footer(text = 'R : ???????????? ')

	##########################################################

	if basicSetting[10] !="":
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #??????
		credentials = ServiceAccountCredentials.from_json_keyfile_name(basicSetting[10], scope) #??????

init()

channel = ''

#mp3 ?????? ????????????(gTTS ??????, ???????????????)
async def MakeSound(saveSTR, filename):
	if aws_key != "" and aws_secret_key != "":
		polly = boto3.client("polly", aws_access_key_id = aws_key, aws_secret_access_key = aws_secret_key, region_name = "eu-west-1")

		s = '<speak><prosody rate="' + str(95) + '%">' +  saveSTR + '</prosody></speak>'

		response = polly.synthesize_speech(
			TextType = "ssml",
			Text=s,
			OutputFormat="mp3",
			VoiceId="Seoyeon")

		stream = response.get("AudioStream")

		with open(f"./{filename}.mp3", "wb") as mp3file:
			data = stream.read()
			mp3file.write(data)
	else:	
		tts = gTTS(saveSTR, lang = 'ko')
		tts.save(f"./{filename}.wav")

#mp3 ?????? ????????????	
async def PlaySound(voiceclient, filename):
	if basicSetting[21] != "1":
		return
        
	# source = discord.FFmpegPCMAudio(filename)
	source = discord.FFmpegOpusAudio(filename)
	try:
		voiceclient.play(source)
	except discord.errors.ClientException:
		while voiceclient.is_playing():
			await asyncio.sleep(1)
	while voiceclient.is_playing():
		await asyncio.sleep(1)
	voiceclient.stop()
	# source.cleanup()
	return

#my_bot.db ????????????
async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungFlag
	global bossMungCnt

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22
					
	datelist1 = bossTime
	
	datelist = list(set(datelist1))

	information1 = '----- ??????????????? -----\n'
	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' or bossMungFlag[i] == True :
					if bossMungFlag[i] == True :
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (????????? ' + str(bossMungCnt[i]) + '???)' + ' * ' + bossData[i][6] + '\n'
						else : 
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (???????????? ' + str(bossMungCnt[i]) + '???)' + ' * ' + bossData[i][6] + '\n'
					else:
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (????????? ' + str(bossMungCnt[i]) + '???)' + ' * ' + bossData[i][6] + '\n'
						else : 
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (???????????? ' + str(bossMungCnt[i]) + '???)' + ' * ' + bossData[i][6] + '\n'
						
	try :
		contents = repo.get_contents("my_bot.db")
		repo.update_file(contents.path, "bossDB", information1, contents.sha)
	except Exception as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#my_bot.db ????????????
async def dbLoad():
	global LoadChk
	
	contents1 = repo.get_contents("my_bot.db")
	file_data = base64.b64decode(contents1.content)
	file_data = file_data.decode('utf-8')
	beforeBossData = file_data.split('\n')
	
	if len(beforeBossData) > 1:	
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				startPos = beforeBossData[i+1].find('-')
				endPos = beforeBossData[i+1].find('(')
				if beforeBossData[i+1][startPos+2:endPos] == bossData[j][0] :
				#if beforeBossData[i+1].find(bossData[j][0]) != -1 :
					tmp_mungcnt = 0
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')
					tmp_msglen = beforeBossData[i+1].find('*')

					
					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
					
					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

					tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					if bossData[j][7] == "1":
						tmp_now_chk = tmp_now + datetime.timedelta(minutes = int(basicSetting[2]))
					else:
						tmp_now_chk = tmp_now + datetime.timedelta(minutes = int(basicSetting[22]))

					if tmp_now_chk < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while tmp_now_chk < now2 :
							tmp_now_chk = tmp_now_chk + deltaTime
							tmp_now = tmp_now + deltaTime
							tmp_mungcnt = tmp_mungcnt + 1

					if tmp_now_chk > now2 > tmp_now: #??????.
						bossMungFlag[j] = True
						tmp_bossTime[j] = tmp_now
						tmp_bossTimeString[j] = tmp_bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = tmp_bossTime[j].strftime('%Y-%m-%d')
						bossTimeString[j] = '99:99:99'
						bossDateString[j] = '9999-99-99'
						bossTime[j] = tmp_bossTime[j] + datetime.timedelta(days=365)
					else:
						tmp_bossTime[j] = bossTime[j] = tmp_now
						tmp_bossTimeString[j] = bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')
						
					if  now2 + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[j] < now2 + datetime.timedelta(minutes=int(basicSetting[3])):
						bossFlag0[j] = True
					if tmp_bossTime[j] < now2 + datetime.timedelta(minutes=int(basicSetting[1])):
						bossFlag[j] = True
						bossFlag0[j] = True
			
					bossData[j][6] = beforeBossData[i+1][tmp_msglen+2:len(beforeBossData[i+1])]

					if beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3] != 0 and beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] == ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					elif beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] != ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] + beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					else:
						bossMungCnt[j] = 0

		global FixedBossDateData
		global fixed_bossFlag
		global fixed_bossFlag0
		global fixed_bossTime
		global fixed_bossData

		FixedBossDateData = []
		fixed_bossFlag = []
		fixed_bossFlag0 = []
		fixed_bossTime = []
		fixed_bossData = []
		tmp_fixed_bossData = []
		fb = []
	
		fixed_inidata = repo.get_contents("fixed_boss.ini")
		file_data2 = base64.b64decode(fixed_inidata.content)
		file_data2 = file_data2.decode('utf-8')
		fixed_inputData = file_data2.split('\n')

		for i in range(len(fixed_inputData)):
			FixedBossDateData.append(fixed_inputData[i])

		del(fixed_inputData[0])

		for i in range(fixed_inputData.count('\r')):
			fixed_inputData.remove('\r')

		fixed_bossNum = int(len(fixed_inputData)/6)

		for i in range(fixed_bossNum):
			tmp_fixed_bossData.append(fixed_inputData[i*6:i*6+6]) 
			
		for j in range(fixed_bossNum):
			for i in range(len(tmp_fixed_bossData[j])):
				tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()
					
		tmp_fixed_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

		############## ???????????? ?????? ????????? #####################	
		for j in range(fixed_bossNum):
			try:
				tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
				tmp_fixedGen_len = tmp_fixed_bossData[j][2].find(':')
				fb.append(tmp_fixed_bossData[j][0][11:])                  #fixed_bossData[0] : ?????????
				fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])     #fixed_bossData[1] : ???
				fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])     #fixed_bossData[2] : ???
				fb.append(tmp_fixed_bossData[j][4][20:])                  #fixed_bossData[3] : ?????? ????????????
				fb.append(tmp_fixed_bossData[j][5][13:])                  #fixed_bossData[4] : ??? ????????????
				fb.append(tmp_fixed_bossData[j][2][12:tmp_fixedGen_len])  #fixed_bossData[5] : ?????????-???
				fb.append(tmp_fixed_bossData[j][2][tmp_fixedGen_len+1:])  #fixed_bossData[6] : ?????????-???
				fb.append(tmp_fixed_bossData[j][3][12:16])                #fixed_bossData[7] : ?????????-???	
				fb.append(tmp_fixed_bossData[j][3][17:19])                #fixed_bossData[8] : ?????????-???
				fb.append(tmp_fixed_bossData[j][3][20:22])                #fixed_bossData[9] : ?????????-???
				fixed_bossData.append(fb)
				fb = []
				fixed_bossFlag.append(False)
				fixed_bossFlag0.append(False)
				fixed_bossTime.append(tmp_fixed_now.replace(year = int(fixed_bossData[j][7]), month = int(fixed_bossData[j][8]), day = int(fixed_bossData[j][9]), hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
				if fixed_bossTime[j] < tmp_fixed_now :
					while fixed_bossTime[j] < tmp_fixed_now :
						fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(hours=int(fixed_bossData[j][5]), minutes=int(fixed_bossData[j][6]), seconds = int(0))
				if  tmp_fixed_now + datetime.timedelta(minutes=int(basicSetting[1])) <= fixed_bossTime[j] < tmp_fixed_now + datetime.timedelta(minutes=int(basicSetting[3])):
					fixed_bossFlag0[j] = True
				if fixed_bossTime[j] < tmp_fixed_now + datetime.timedelta(minutes=int(basicSetting[1])):
					fixed_bossFlag[j] = True
					fixed_bossFlag0[j] = True
			except:
				raise Exception(f"[fixed_boss.ini] ??????????????? {tmp_fixed_bossData[j][0]} ????????????")

		LoadChk = 0
		print ("<???????????? ??????>")
	else:
		LoadChk = 1
		print ("???????????? ????????? ????????????.")

#???????????? ????????????
async def FixedBossDateSave():
	global fixed_bossData
	global fixed_bossTime
	global fixed_bossNum
	global FixedBossDateData
	global indexFixedBossname

	for i in range(fixed_bossNum):
		FixedBossDateData[indexFixedBossname[i] + 3] = 'startDate = '+ fixed_bossTime[i].strftime('%Y-%m-%d') + '\n'

	FixedBossDateDataSTR = ""
	for j in range(len(FixedBossDateData)):
		pos = len(FixedBossDateData[j])
		tmpSTR = FixedBossDateData[j][:pos-1] + '\r\n'
		FixedBossDateDataSTR += tmpSTR

	contents = repo.get_contents("fixed_boss.ini")
	repo.update_file(contents.path, "bossDB", FixedBossDateDataSTR, contents.sha)

#???????????????		
async def LadderFunc(number, ladderlist, channelVal):
	result_ladder = random.sample(ladderlist, number)
	lose_member = [item for item in ladderlist if item not in result_ladder]
	result_ladderSTR = ','.join(map(str, result_ladder))
	embed = discord.Embed(title  = "???? ?????????! ?????? ????????? ???!",color=0x00ff00)
	embed.add_field(name = "???? ?????????", value =  f"```fix\n{', '.join(ladderlist)}```", inline=False)
	embed.add_field(name = "???? ??????", value =  f"```fix\n{', '.join(result_ladder)}```")
	embed.add_field(name = "???? ??????", value =  f"```{', '.join(lose_member)}```")
	await channelVal.send(embed=embed, tts=False)

#data?????????
async def init_data_list(filename, first_line : str = "-----------"):
	try :
		contents = repo.get_contents(filename)
		repo.update_file(contents.path, "deleted list " + str(filename), first_line, contents.sha)
		print ('< ??????????????????????????? >')
	except Exception as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#data??????
async def data_list_Save(filename, first_line : str = "-----------",  save_data : dict = {}):

	output_list = first_line+ '\n'
	for key, value in save_data.items():
		output_list += str(key) + ' ' + str(value) + '\n'

	try :
		contents = repo.get_contents(filename)
		repo.update_file(contents.path, "updated " + str(filename), output_list, contents.sha)
	except Exception as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#??????(??????) ?????? 
async def get_guild_channel_info(bot):
	text_channel_name : list = []
	text_channel_id : list = []
	voice_channel_name : list = []
	voice_channel_id : list = []
	
	for guild in bot.guilds:
		for text_channel in guild.text_channels:
			text_channel_name.append(text_channel.name)
			text_channel_id.append(str(text_channel.id))
		for voice_channel in guild.voice_channels:
			voice_channel_name.append(voice_channel.name)
			voice_channel_id.append(str(voice_channel.id))
	return text_channel_name, text_channel_id, voice_channel_name, voice_channel_id

class taskCog(commands.Cog): 
	def __init__(self, bot):
		self.bot = bot
		self.checker = True

		self.main_task.start()

	@tasks.loop(seconds=1.0, count=1)
	async def main_task(self):
		boss_task = asyncio.get_event_loop().create_task(self.boss_check())
		await boss_task

	@main_task.before_loop
	async def before_tast(self):
		await self.bot.wait_until_ready()

	################ ????????? ################ 
	@commands.command(name=command[8][0], aliases=command[8][1:])
	async def command_task_list(self, ctx : commands.Context):
		if ctx.message.channel.id != basicSetting[7]:
			return

		for t in asyncio.Task.all_tasks():
			# print(t._coro.__name__)
			if t._coro.__name__ == f"boss_check":
				if t.done():
					try:
						t.exception()
					except asyncio.CancelledError:
						continue
					continue
				t.cancel()
		# await ctx.send( '< BOT????????????????????? >', tts=False)
		try:
			file = discord.File("./??????.JPG")
			await ctx.send(file = file)
		except:
			await ctx.send( '< BOT????????????????????? >', tts=False)
		print("??????!")
		await dbSave()
		await data_list_Save("kill_list.ini", "-----????????????-----", kill_Data)
		await data_list_Save("item_list.ini", "-----???????????????-----", item_Data)

		for vc in self.bot.voice_clients:
			if vc.guild.id == int(ctx.guild.id):
				if vc.is_playing():
					vc.stop()
			await vc.disconnect(force=True)

		if basicSetting[21] != "1":
			print("BOT???????????????")
			await dbLoad()
			await self.bot.get_channel(channel).send( '< BOT??????????????? >', tts=False)

		self.checker = True

		boss_task = asyncio.Task(self.boss_check())
		return

	async def boss_check(self):
		await self.bot.wait_until_ready()

		global channel
		global endTime
			
		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime
		
		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global fixed_bossFlag
		global fixed_bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global endTime
		global kill_Time
		
		if chflg == 1 : 
			if len(self.bot.voice_clients) == 0 :
				if basicSetting[21] == "1":
					try:
						await self.bot.get_channel(basicSetting[6]).connect(reconnect=True, timeout=5)
						if self.bot.voice_clients[0].is_connected() :
							await self.bot.get_channel(channel).send( '< BOT?????? >', tts=False)
							self.checker = True
							print("BOT??????")
					except:
						await self.bot.get_channel(channel).send( '< voice?????????????????????????????? >', tts=False)
						self.checker = False
						print("?????????")
						pass
					await dbLoad()

		while True:
			############ ????????????! ############
			if log_stream.getvalue().find("Awaiting") != -1:
				log_stream.truncate(0)
				log_stream.seek(0)
				await self.bot.get_channel(channel).send( '< Discord??????????????? >', tts=False)
				await dbSave()
				break
			
			log_stream.truncate(0)
			log_stream.seek(0)
			##################################

			now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
			priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
			priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
			tmp_aftr1 = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))
			tmp_aftr2 = now+datetime.timedelta(minutes=int(0-int(basicSetting[22])))

			if channel != '':			
				################ ????????? ????????? ################ 
				if endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M:%S'):
					await dbSave()
					#await FixedBossDateSave()
					await data_list_Save("kill_list.ini", "-----????????????-----", kill_Data)
					await data_list_Save("item_list.ini", "-----???????????????-----", item_Data)
					print("??????????????????!")
					endTime = endTime + datetime.timedelta(days = int(basicSetting[13]))
					for voice_client in self.bot.voice_clients:
						if voice_client.is_playing():
							voice_client.stop()
						await voice_client.disconnect(force=True)
					await asyncio.sleep(2)

					inidata_restart = repo_restart.get_contents("restart.txt")
					file_data_restart = base64.b64decode(inidata_restart.content)
					file_data_restart = file_data_restart.decode('utf-8')
					inputData_restart = file_data_restart.split('\n')

					if len(inputData_restart) < 3:	
						contents12 = repo_restart.get_contents("restart.txt")
						repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
					else:
						contents12 = repo_restart.get_contents("restart.txt")
						repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)

				############# ????????????! ###########
				if len(self.bot.voice_clients) == 0 and self.checker and basicSetting[21] == "1":
					try:
						await self.bot.get_channel(basicSetting[6]).connect(reconnect=True, timeout=5)
						print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} : ?????? ?????? ?????? ???????????????!")
					except discord.errors.ClientException as e:
						print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} : ?????? ?????? ?????? ???????????? ?????? ?????? ?????? ?????? ?????? ?????? : {e}")
						self.checker = False
						pass
					except Exception as e:
						print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} : ?????? ?????? ?????? ???????????? ?????? ?????? ?????? ???????????? ?????? : {e}")
						self.checker = False
						pass
					if not self.bot.voice_clients[0].is_connected():
						print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} : ?????? ?????? ?????? ????????????!")
						await self.bot.get_channel(channel).send( '< ?????? ?????? ????????? ?????????????????????. ?????? ??? ?????? ?????? ????????? ??????????????????! >')
						self.checker = False
						pass
				
				################ ??? ?????? ????????? ################ 
				if kill_Time.strftime('%Y-%m-%d ') + kill_Time.strftime('%H:%M') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M'):
					kill_Time = kill_Time + datetime.timedelta(days=int(1))
					await init_data_list('kill_list.ini', '-----????????????-----')

				################ ?????? ?????? ?????? ################ 
				for i in range(fixed_bossNum):
					if int(basicSetting[3]) == 0:
						fixed_bossFlag0[i] = True
					if int(basicSetting[1]) == 0:
						fixed_bossFlag[i] = True
					################ before_alert1 ################ 
					if fixed_bossTime[i] <= priv0 and fixed_bossTime[i] > priv:
						if basicSetting[3] != '0':
							if fixed_bossFlag0[i] == False:
								fixed_bossFlag0[i] = True
								await self.bot.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[3] + '?????? ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
								try:
									if basicSetting[21] == "1":
										await PlaySound(self.bot.voice_clients[0], './sound/' + fixed_bossData[i][0] + '??????1.mp3')
								except:
									pass

					################ before_alert ################ 
					if fixed_bossTime[i] <= priv and fixed_bossTime[i] > now and fixed_bossFlag0[i] == True :
						if basicSetting[1] != '0' :
							if fixed_bossFlag[i] == False:
								fixed_bossFlag[i] = True
								await self.bot.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[1] + '?????? ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
								try:
									if basicSetting[21] == "1":
										await PlaySound(self.bot.voice_clients[0], './sound/' + fixed_bossData[i][0] + '??????.mp3')
								except:
									pass
					
					################ ?????? ??? ?????? ?????? ################
					if fixed_bossTime[i] <= now and fixed_bossFlag[i] == True and fixed_bossFlag0[i] == True :
						fixed_bossTime[i] = fixed_bossTime[i]+datetime.timedelta(hours=int(fixed_bossData[i][5]), minutes=int(fixed_bossData[i][6]), seconds = int(0))
						fixed_bossFlag0[i] = False
						fixed_bossFlag[i] = False
						embed = discord.Embed(
								description= "```" + fixed_bossData[i][0] + fixed_bossData[i][4] + "```" ,
								color=0x00ff00
								)
						await self.bot.get_channel(channel).send(embed=embed, tts=False)
						try:
							if basicSetting[21] == "1":
								await PlaySound(self.bot.voice_clients[0], './sound/' + fixed_bossData[i][0] + '???.mp3')
						except:
							pass

				################ ?????? ?????? ?????? ################ 
				for i in range(bossNum):
					if int(basicSetting[3]) == 0:
						bossFlag0[i] = True
					if int(basicSetting[1]) == 0:
						bossFlag[i] = True
					################ before_alert1 ################ 
					if bossTime[i] <= priv0 and bossTime[i] > priv:
						if basicSetting[3] != '0':
							if bossFlag0[i] == False:
								bossFlag0[i] = True
								if bossData[i][6] != '' :
									await self.bot.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '??????' + bossData[i][3] + " [" +  bossTimeString[i] + "]" + '\n<' + bossData[i][6] + '>```', tts=False)
								else :
									await self.bot.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '??????' + bossData[i][3] + " [" +  bossTimeString[i] + "]```", tts=False)
								try:
									if basicSetting[21] == "1":
										await PlaySound(self.bot.voice_clients[0], './sound/' + bossData[i][0] + '??????1.mp3')
								except:
									pass

					################ before_alert ################
					if bossTime[i] <= priv and bossTime[i] > now and bossFlag0[i] == True:
						if basicSetting[1] != '0' :
							if bossFlag[i] == False:
								bossFlag[i] = True
								if bossData[i][6] != '' :
									await self.bot.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '??????' + bossData[i][3] + " [" +  bossTimeString[i] + "]" + '\n<' + bossData[i][6] + '>```', tts=False)
								else :
									await self.bot.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '??????' + bossData[i][3] + " [" +  bossTimeString[i] + "]```", tts=False)
								try:
									if basicSetting[21] == "1":
										await PlaySound(self.bot.voice_clients[0], './sound/' + bossData[i][0] + '??????.mp3')
								except:
									pass

					################ ?????? ??? ?????? ?????? ################ 
					if bossTime[i] <= now and bossFlag0[i] == True and bossFlag[i] == True :
						#print ('if ', bossTime[i])
						bossMungFlag[i] = True
						tmp_bossTime[i] = bossTime[i]
						tmp_bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						tmp_bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
						bossTimeString[i] = '99:99:99'
						bossDateString[i] = '9999-99-99'
						bossTime[i] = now+datetime.timedelta(days=365)
						if bossData[i][6] != '' :
							embed = discord.Embed(
									description= "```" + bossData[i][0] + bossData[i][4] + '\n<' + bossData[i][6] + '>```' ,
									color=0x00ff00
									)
						else :
							embed = discord.Embed(
									description= "```" + bossData[i][0] + bossData[i][4] + "```" ,
									color=0x00ff00
									)
						await self.bot.get_channel(channel).send(embed=embed, tts=False)
						try:
							if basicSetting[21] == "1":
								await PlaySound(self.bot.voice_clients[0], './sound/' + bossData[i][0] + '???.mp3')
						except:
							pass

					################ ?????? ?????? ??? ?????? ################ 
					if bossMungFlag[i] == True:
						if bossData[i][7] == "1":
							aftr = tmp_aftr1
						else:
							aftr = tmp_aftr2
						if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
							if basicSetting[2] != '0' and basicSetting[22] != '0' and bossFlag[i] == True and bossFlag0[i] == True and bossMungFlag[i] == True :
								if int(basicSetting[17]) <= bossMungCnt[i] and int(basicSetting[17]) != 0:
									bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
									tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
									bossTimeString[i] = '99:99:99'
									bossDateString[i] = '9999-99-99'
									tmp_bossTimeString[i] = '99:99:99'
									tmp_bossDateString[i] = '9999-99-99'
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									bossMungCnt[i] = 0
									if bossData[i][2] == '0':
										await self.bot.get_channel(channel).send(f'```?????????????????? {basicSetting[17]}????????????????????? [{bossData[i][0]}] ????????????????????????```', tts=False)
										print ('????????????????????? <' + bossData[i][0] + ' ?????????>')
									else:
										await self.bot.get_channel(channel).send(f'```????????????????????? {basicSetting[17]}????????????????????? [{bossData[i][0]}] ????????????????????????```', tts=False)
										print ('???????????????????????? <' + bossData[i][0] + ' ?????????>')
									#await dbSave()
									
								else:
									################ ????????? ?????? ################
									if bossData[i][2] == '0':
										bossFlag[i] = False
										bossFlag0[i] = False
										bossMungFlag[i] = False
										bossMungCnt[i] = bossMungCnt[i] + 1
										tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
										tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
										tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
										await self.bot.get_channel(channel).send("```" +  bossData[i][0] + ' ???????????????```', tts=False)
										embed = discord.Embed(
											description= '```' + bossData[i][0] + '???????????????' + bossTimeString[i] + '?????????```',
											color=0xff0000
											)
										await self.bot.get_channel(channel).send(embed=embed, tts=False)
										try:
											if basicSetting[21] == "1":
												await PlaySound(self.bot.voice_clients[0], './sound/' + bossData[i][0] + '?????????.mp3')
										except:
											pass
									################ ??? ?????? ################
									else :
										bossFlag[i] = False
										bossFlag0[i] = False
										bossMungFlag[i] = False
										bossMungCnt[i] = bossMungCnt[i] + 1
										tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
										tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
										tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
										await self.bot.get_channel(channel).send("```" + bossData[i][0] + ' ??????????????????```')
										embed = discord.Embed(
											description= '```' + bossData[i][0] + '???????????????' + bossTimeString[i] + '?????????```',
											color=0xff0000
											)
										await self.bot.get_channel(channel).send(embed=embed, tts=False)
										try:
											if basicSetting[21] == "1":
												await PlaySound(self.bot.voice_clients[0], './sound/' + bossData[i][0] + '???.mp3')
										except:
											pass

			await asyncio.sleep(1) # task runs every 60 seconds

		self.checker = False
		
		for voice_client in self.bot.voice_clients:
			if voice_client.is_playing():
				voice_client.stop()
			await voice_client.disconnect(force=True)

		for t in asyncio.Task.all_tasks():
			if t._coro.__name__ == f"boss_check":
				print("-------------")
				if t.done():
					try:
						t.exception()
					except asyncio.CancelledError:
						continue
					continue
				t.cancel()
		await dbSave()
		await data_list_Save("kill_list.ini", "-----????????????-----", kill_Data)
		await data_list_Save("item_list.ini", "-----???????????????-----", item_Data)

		boss_task = asyncio.Task(self.boss_check())

class mainCog(commands.Cog): 
	def __init__(self, bot):
		self.bot = bot

	################ ????????? ?????? ################ 	
	@commands.has_permissions(manage_messages=True)
	@commands.command(name=command[0][0], aliases=command[0][1:])
	async def join_(self, ctx):
		global basicSetting
		global chflg

		if basicSetting[7] == "":
			channel = ctx.message.channel.id #???????????? ????????? ?????? ID

			print ('[ ', basicSetting[7], ' ]')
			print ('] ', ctx.message.channel.name, ' [')

			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith("textchannel ="):
					inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
					basicSetting[7] = channel
					#print ('======', inputData_text[i])
			
			result_textCH = '\n'.join(inputData_textCH)
			
			#print (result_textCH)
			
			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			await ctx.send(f"< ??????????????? [{ctx.message.channel.name}] ???????????? >", tts=False)
			
			print('< ??????????????? [' + ctx.guild.get_channel(basicSetting[7]).name + '] ????????????>')
			if basicSetting[6] != "" and basicSetting[21] == "1":
				try:
					await ctx.guild.get_channel(basicSetting[6]).connect(reconnect=True, timeout=5)
					print('< ???????????? [' + ctx.guild.get_channel(basicSetting[6]).name + '] ????????????>')
				except:
					print('< ???????????? [' + ctx.guild.get_channel(basicSetting[6]).name + '] ????????????! >')
					pass
			if basicSetting[8] != "":
				if str(basicSetting[8]) in channel_id:
					print('< ??????????????? [' + ctx.guild.get_channel(int(basicSetting[8])).name + '] ???????????? >')
				else:
					basicSetting[8] = ""
					print(f"??????????????? ID ??????! [{command[28][0]} ?????????] ???????????? ????????? ????????????.")
			if basicSetting[11] != "":
				if str(basicSetting[11]) in channel_id:
					print('< ???????????? [' + ctx.guild.get_channel(int(basicSetting[11])).name + '] ????????????>')
				else:
					basicSetting[11] = ""
					print(f"???????????? ID ??????! [{command[28][0]} ??????] ???????????? ????????? ????????????.")
			if basicSetting[18] != "":
				if str(basicSetting[18]) in channel_id:
					print('< ???????????? [' + ctx.guild.get_channel(int(basicSetting[18])).name + '] ????????????>')
				else:
					basicSetting[18] = ""
					print(f"???????????? ID ??????! [{command[28][0]} ??????] ???????????? ????????? ????????????.")
			if basicSetting[19] != "":
				if str(basicSetting[19]) in channel_id:
					print('< ???????????? [' + ctx.guild.get_channel(int(basicSetting[19])).name + '] ????????????>')
				else:
					basicSetting[19] = ""
					print(f"???????????? ID ??????! [{command[28][0]} ??????] ???????????? ????????? ????????????.")
			if basicSetting[20] != "":
				if str(basicSetting[20]) in channel_id:
					print('< ??????????????? [' + ctx.guild.get_channel(int(basicSetting[20])).name + '] ????????????>')
				else:
					basicSetting[20] = ""
					print(f"??????????????? ID ??????! [{command[28][0]} ?????????] ???????????? ????????? ????????????.")
			if int(basicSetting[13]) != 0 :
				print('< ????????? ????????? ?????? ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + ' >')
				print('< ????????? ????????? ?????? ' + basicSetting[13] + '??? >')
			else :
				print('< ????????? ????????? ???????????? >')

			chflg = 1
		else:
			curr_guild_info = None
			for guild in self.bot.guilds:
				for text_channel in guild.text_channels:
					if basicSetting[7] == text_channel.id:
						curr_guild_info = guild

			emoji_list : list = ["???", "???"]
			guild_error_message = await ctx.send(f"?????? **[{curr_guild_info.name}]** ?????? **[{setting_channel_name}]** ????????? ????????? ????????? ???????????? ????????????.\n?????? ????????? ????????? ????????? ?????? ???????????? ??? ????????? ?????????????????? ??? ??? ???????????????.\n(10????????? ???????????? ?????? ?????? ????????? ???????????????.)", tts=False)

			for emoji in emoji_list:
				await guild_error_message.add_reaction(emoji)

			def reaction_check(reaction, user):
				return (reaction.message.id == guild_error_message.id) and (user.id == ctx.author.id) and (str(reaction) in emoji_list)
			try:
				reaction, user = await self.bot.wait_for('reaction_add', check = reaction_check, timeout = 10)
			except asyncio.TimeoutError:
				return await ctx.send(f"????????? ??????????????????. **[{curr_guild_info.name}]** ?????? **[{setting_channel_name}]** ???????????? ??????????????????!")

			if str(reaction) == "???":
				if ctx.voice_client is not None:
					await ctx.voice_client.disconnect(force=True)
				basicSetting[6] = ""
				basicSetting[7] = int(ctx.message.channel.id)

				print ('[ ', basicSetting[7], ' ]')
				print ('] ', ctx.message.channel.name, ' [')

				inidata_textCH = repo.get_contents("test_setting.ini")
				file_data_textCH = base64.b64decode(inidata_textCH.content)
				file_data_textCH = file_data_textCH.decode('utf-8')
				inputData_textCH = file_data_textCH.split('\n')
				
				for i in range(len(inputData_textCH)):
					if inputData_textCH[i].startswith("textchannel ="):
						inputData_textCH[i] = 'textchannel = ' + str(basicSetting[7]) + '\r'
				
				result_textCH = '\n'.join(inputData_textCH)
				
				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

				return await ctx.send(f"????????? ????????? **[{ctx.author.guild.name}]** ?????? **[{ctx.message.channel.name}]** ????????? ?????? ?????????????????????.\n< ???????????? ?????? ??? [{command[5][0]}] ????????? ?????? ????????? >")
			else:
				return await ctx.send(f"????????? ?????? ????????? ?????????????????????.\n**[{curr_guild_info.name}]** ?????? **[{setting_channel_name}]** ???????????? ??????????????????!")

	################ ????????? ?????? ?????? ################ 	
	@commands.command(name=command[1][0], aliases=command[1][1:])
	async def menu_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			command_list = ''
			#command_list += ','.join(command[2]) + '\n'     #!????????????
			#command_list += ','.join(command[3]) + '\n'     #!????????????
			#command_list += ','.join(command[4]) + ' [?????????]\n'     #!????????????
			#command_list += ','.join(command[5]) + ' ??? ???????????? ?????? ??????\n'     #!??????
			#command_list += ','.join(command[6]) + '\n'     #!????????????
			command_list += ','.join(command[7]) + '??????????????????\n'     #!?????????
			#command_list += ','.join(command[8]) + '\n'     #!??????
			#command_list += ','.join(command[9]) + '\n'     #!?????????
			#command_list += ','.join(command[10]) + '\n'     #!?????????
			#command_list += ','.join(command[11]) + ' [??????] [??????]\n'     #!??????
			#command_list += ','.join(command[12]) + ' [???????????????] [?????????1] [?????????2]...\n'     #!?????????
			#command_list += ','.join(command[27]) + ' [?????????1] [?????????2]...(?????? 12???)\n'     #!??????
			#command_list += ','.join(command[41]) + ' [????????????] (????????????/???) *(??????)\n'    #!????????????
			#command_list += ','.join(command[35]) + ' [????????????] (???????????????)\n'     #!?????????
			#command_list += ','.join(command[36]) + ' [???????????????] [???????????????] (???????????????)\n'     #!?????????
			#command_list += ','.join(command[13]) + ' [?????????]\n'     #!??????
			command_list += ','.join(command[14]) + ' 0000, 00:00 ????????????????????????????????????????????????\n'     #!????????????
			#command_list += ','.join(command[40]) + ' ?????? ' + ','.join(command[40]) + ' 0000, 00:00\n'     #!?????????
			#command_list += ','.join(command[43]) + f' [00:00:00 : ?????????(??????) ...]\n??? ????????? ?????? ?????? ??????\nex){command[43][0]} + 12:34:00 : {bossData[0][0]}\n+ 10:56:00 : {bossData[1][0]}\n+ (+1d) 12:12:00 : {bossData[2][0]}...\n'     #!?????????
			#command_list += ','.join(command[44]) + f' [00:00:00 : ?????????(??????) ...]\n??? [00:00:00 ?????????] ????????? ?????????(??????)??? ???????????? ??????\nex){command[44][0]} + 12:34:00 : {bossData[0][0]}\n10:56:00 : {bossData[1][0]}\n+ (+1d) 12:12:00 : {bossData[2][0]}...\n'     #!????????????
			#command_list += ','.join(command[45]) + ' [??????(00:00)] [????????????(??????)] [?????????1] [?????????2] [?????????3] ...\n'     #!????????????
			command_list += ','.join(command[15]) + '??????????????????????????????\n'     #!q
			#command_list += ','.join(command[16]) + ' [??????]\n'     #!v
			#command_list += ','.join(command[17]) + '\n'     #!??????
			#command_list += ','.join(command[18]) + '\n'     #!????????????
			#command_list += ','.join(command[24]) + '\n'     #!????????????
			#command_list += ','.join(command[25]) + '\n'     #!????????? ??????
			#command_list += ','.join(command[25]) + ' [?????????]\n'     #!???
			#command_list += ','.join(command[26]) + ' [?????????]\n'     #!?????????
			#command_list += ','.join(command[33]) + ' [?????????] ?????? ' + ','.join(command[33]) + ' [?????????] [??????]\n'     #!?????????
			#command_list += ','.join(command[29]) + '\n'     #!????????? ?????? ?????????
			#command_list += ','.join(command[30]) + '\n'     #!????????? ?????? ??????
			#command_list += ','.join(command[30]) + ' [?????????] ?????? ' + ','.join(command[30]) + ' [?????????] [??????]\n'     #!????????? ?????? ??????
			#command_list += ','.join(command[31]) + ' [?????????]\n'     #!????????? ???????????? ??????
			#command_list += ','.join(command[32]) + ' [?????????] ?????? ' + ','.join(command[32]) + ' [?????????] [??????]\n'     #!????????? ??????
			#command_list += ','.join(command[19]) + '\n'     #!??????
			#command_list += ','.join(command[19]) + ' [????????????]\n'     #!??????
			#command_list += ','.join(command[20]) + '\n'     #!????????????
			#command_list += ','.join(command[21]) + ' [??????]\n'     #!??????
			#command_list += ','.join(command[28]) + ' ?????????, ??????, ??????, ??????, ?????????\n'     #!????????????
			#command_list += ','.join(command[42]) + ' ?????????, ??????, ??????, ??????, ?????????\n'     #!????????????
			#command_list += ','.join(command[34]) + ' ??? ???????????????\n\n'     #???????????????
			command_list += ','.join(command[22]) + ' ???????????????????????????\n'     #?????????
			command_list += ','.join(command[23]) + ' ???????????????????????????\n'     #!?????????
			command_list += '[?????????]END ????????? [?????????]????????? 0000, 00:00  ?????????????????????\n'  
			command_list += '[?????????] END ????????? [?????????] ????????? 0000, 00:00  ?????????????????????\n'   
			command_list += '[?????????]???????????? ????????? [?????????] ???????????? 0000, 00:00  ??????????????????\n'     
			command_list += '[?????????]?????? ????????? [?????????] ?????? 0000, 00:00  ??????????????????\n' 
			#command_list += '[?????????]?????? [??????]\n'
			embed = discord.Embed(
					title = "----- List -----",
					description= '```' + command_list + '```',
					color=0xff00ff
					)
			#embed.add_field(
			#		name="----- ???????????? -----",
			#		value= '```- [?????????]???/???/??????  [??????] : ???????????? ?????? ??? ?????? ??????!! ?????? ??????\n- [?????????]??? ???????????? ???????????? ?????????????????????.\n  ex)' + bossData[0][0] + '??? => ' +  ', ' + bossData[0][0] + ' ??? => ' + '```'
			#		)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ ????????? ?????? ???????????? ################ 
	@commands.command(name=command[2][0], aliases=command[2][1:])
	async def setting_(self, ctx):	
		#print (ctx.message.channel.id)
		if ctx.message.channel.id == basicSetting[7]:
			setting_val = '??????????????? : Server Ver. 28 (2021. 6. 23.)\n'
			if basicSetting[6] != "" :
				setting_val += '???????????? : ' + self.bot.get_channel(basicSetting[6]).name + '\n'
			setting_val += '??????????????? : ' + self.bot.get_channel(basicSetting[7]).name +'\n'
			if basicSetting[8] != "" :
				setting_val += '??????????????? : ' + self.bot.get_channel(int(basicSetting[8])).name + '\n'
			if basicSetting[11] != "" :
				setting_val += '???????????? : ' + self.bot.get_channel(int(basicSetting[11])).name + '\n'
			if basicSetting[18] != "" :
				setting_val += '???????????? : ' + self.bot.get_channel(int(basicSetting[18])).name + '\n'
			if basicSetting[19] != "" :
				setting_val += '???????????? : ' + self.bot.get_channel(int(basicSetting[19])).name + '\n'
			if basicSetting[20] != "" :
				setting_val += '??????????????? : ' + self.bot.get_channel(int(basicSetting[20])).name + '\n'
			setting_val += '?????????????????????1 : ' + basicSetting[1] + ' ??? ???\n'
			setting_val += '?????????????????????2 : ' + basicSetting[3] + ' ??? ???\n'
			setting_val += '?????????????????????1 : ' + basicSetting[2] + ' ??? ???\n'
			setting_val += '?????????????????????2 : ' + basicSetting[22] + ' ??? ???\n'
			if basicSetting[21] == "0":
				setting_val += '????????????????????? : ????????????\n'
			else:
				setting_val += '????????????????????? : ?????????\n'
			embed = discord.Embed(
					title = "----- ???????????? -----",
					description= f'```{setting_val}```',
					color=0xff00ff
					)
			#embed.add_field(
			#		name="----- Special Thanks to. -----",
			#		value= '```??????, ??????, ?????????, ??????, ??????, ??????, D.H.Kim, K.H.Sim, ??????, ????????????, D.H.Oh, Bit, ??????, ??????, ?????????, ??????, ??????, B.Park```'
			#		)
			await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ?????? ?????? ?????? ################ 
	@commands.command(name=command[3][0], aliases=command[3][1:])
	async def chChk_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			channel_name, channel_id, channel_voice_name, channel_voice_id = await get_guild_channel_info(self.bot)

			ch_information = []
			cnt = 0
			ch_information.append("")

			ch_voice_information = []
			cntV = 0
			ch_voice_information.append("")

			for guild in self.bot.guilds:
				ch_information[cnt] = f"{ch_information[cnt]}????  {guild.name}  ????\n"
				for i in range(len(channel_name)):
					for text_channel in guild.text_channels:
						if channel_id[i] == str(text_channel.id):
							if len(ch_information[cnt]) > 900 :
								ch_information.append("")
								cnt += 1
							ch_information[cnt] = f"{ch_information[cnt]}[{channel_id[i]}] {channel_name[i]}\n"

				ch_voice_information[cntV] = f"{ch_voice_information[cntV]}????  {guild.name}  ????\n"
				for i in range(len(channel_voice_name)):
					for voice_channel in guild.voice_channels:
						if channel_voice_id[i] == str(voice_channel.id):
							if len(ch_voice_information[cntV]) > 900 :
								ch_voice_information.append("")
								cntV += 1
							ch_voice_information[cntV] = f"{ch_voice_information[cntV]}[{channel_voice_id[i]}] {channel_voice_name[i]}\n"
					
			######################

			if len(ch_information) == 1 and len(ch_voice_information) == 1:
				embed = discord.Embed(
					title = "----- ?????? ?????? -----",
					description = '',
					color=0xff00ff
					)
				embed.add_field(
					name="< ????????? ?????? >",
					value= '```' + ch_information[0] + '```',
					inline = False
					)
				embed.add_field(
					name="< ????????? ?????? >",
					value= '```' + ch_voice_information[0] + '```',
					inline = False
					)

				await ctx.send( embed=embed, tts=False)
			else :
				embed = discord.Embed(
					title = "----- ?????? ?????? -----\n< ????????? ?????? >",
					description= '```' + ch_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(ch_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send( embed=embed, tts=False)
				embed = discord.Embed(
					title = "< ?????? ?????? >",
					description= '```' + ch_voice_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(ch_voice_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_voice_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send( embed=embed, tts=False)
		else:
			return

	################ ????????????????????? ################ 
	@commands.command(name=command[4][0], aliases=command[4][1:])
	async def chMove_(self, ctx):
		global basicSetting
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			channel = None
			for i in range(len(channel_name)):
				if  channel_name[i] == msg:
					channel = int(channel_id[i])
					
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('textchannel ='):
					inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
					basicSetting[7] = int(channel)
			
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)
			
			await ctx.send( f"????????? ????????? < {ctx.message.channel.name} >?????? < {self.bot.get_channel(channel).name} > ??? ?????????????????????.", tts=False)
			await self.bot.get_channel(channel).send( f"< {self.bot.get_channel(channel).name} ???????????? >", tts=False)
		else:
			return

	################ ????????? ???????????? ?????? ################ 
	@commands.has_permissions(manage_messages=True)
	@commands.command(name=command[5][0], aliases=command[5][1:])
	async def connectVoice_(self, ctx):
		global basicSetting

		if ctx.message.channel.id == basicSetting[7]:
			if basicSetting[21] != "1":
				return await ctx.send('```???????????? ???????????? ????????? ???????????? ????????????.```', tts=False)

			if ctx.voice_client is None:
				if ctx.author.voice:
					try:
						await ctx.author.voice.channel.connect(reconnect=True, timeout=5)
					except:
						await ctx.send('??????????????? ????????? ?????????????????????.', tts=False)	
						pass
				else:
					await ctx.send('??????????????? ?????? ??????????????????.', tts=False)
					return
			else:
				if ctx.voice_client.is_playing():
					ctx.voice_client.stop()

				await ctx.voice_client.move_to(ctx.author.voice.channel)

			voice_channel = ctx.author.voice.channel

			print ('< ', basicSetting[6], ' >')
			print ('> ', self.bot.get_channel(voice_channel.id).name, ' <')

			if basicSetting[6] == "":
				inidata_voiceCH = repo.get_contents("test_setting.ini")
				file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
				file_data_voiceCH = file_data_voiceCH.decode('utf-8')
				inputData_voiceCH = file_data_voiceCH.split('\n')

				for i in range(len(inputData_voiceCH)):
					if inputData_voiceCH[i].startswith('voicechannel ='):
						inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
						basicSetting[6] = int(voice_channel.id)

				result_voiceCH = '\n'.join(inputData_voiceCH)

				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

			elif basicSetting[6] != int(voice_channel.id):
				inidata_voiceCH = repo.get_contents("test_setting.ini")
				file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
				file_data_voiceCH = file_data_voiceCH.decode('utf-8')
				inputData_voiceCH = file_data_voiceCH.split('\n')

				for i in range(len(inputData_voiceCH)):
					if inputData_voiceCH[i].startswith('voicechannel ='):
						inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
						basicSetting[6] = int(voice_channel.id)

				result_voiceCH = '\n'.join(inputData_voiceCH)

				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

			await ctx.send('< ???????????? [' + self.bot.get_channel(voice_channel.id).name + '] ????????????>', tts=False)
		else:
			return


	################ my_bot.db??? ????????? ???????????? ???????????? ################
	@commands.command(name=command[6][0], aliases=command[6][1:])
	async def loadDB_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await dbLoad()

			if LoadChk == 0:
				await ctx.send('<???????????? ??????>', tts=False)
			else:
				await ctx.send('<???????????? ????????? ????????????.>', tts=False)
		else:
			return

	################ ????????? ?????? ????????? ################
	@commands.command(name=command[7][0], aliases=command[7][1:])
	async def initVal_(self, ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime
		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global fixed_bossFlag
		global fixed_bossFlag0
		global bossMungFlag
		global bossMungCnt

		global FixedBossDateData
		global indexFixedBossname
			
		if ctx.message.channel.id == basicSetting[7]:
			basicSetting = []
			bossData = []
			fixed_bossData = []

			bossTime = []
			tmp_bossTime = []
			fixed_bossTime = []

			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []

			bossFlag = []
			bossFlag0 = []
			fixed_bossFlag = []
			fixed_bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []

			FixedBossDateData = []
			indexFixedBossname = []
			
			init()

			await dbSave()

			await ctx.send('<???????????????????????????>', tts=False)
			print ("< ????????? ?????? >")
		else:
			return

	################ ????????? ????????? ################ 
	@commands.command(name=command[9][0], aliases=command[9][1:])
	async def restart_(self, ctx):
		global basicSetting
		global bossTimeString
		global bossDateString

		if ctx.message.channel.id == basicSetting[7]:
			if basicSetting[2] != '0' and basicSetting[22] != '0':
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
			await dbSave()
			await data_list_Save("kill_list.ini", "-----????????????-----", kill_Data)
			await data_list_Save("item_list.ini", "-----???????????????-----", item_Data)
			for voice_client in self.bot.voice_clients:
				if voice_client.is_playing():
					voice_client.stop()
				await voice_client.disconnect(force=True)
			print("????????????????????????!")
			await asyncio.sleep(2)

			inidata_restart = repo_restart.get_contents("restart.txt")
			file_data_restart = base64.b64decode(inidata_restart.content)
			file_data_restart = file_data_restart.decode('utf-8')
			inputData_restart = file_data_restart.split('\n')

			if len(inputData_restart) < 3:	
				contents12 = repo_restart.get_contents("restart.txt")
				repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
			else:
				contents12 = repo_restart.get_contents("restart.txt")
				repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)
		else:
			return

	################ ????????? ???????????? ?????? ################ 
	@commands.command(name=command[10][0], aliases=command[10][1:])
	async def nocheckBoss_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')
			
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1800 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','

			if len(tmp_boss_information) == 1:
				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- ??????????????? -----",
						description= tmp_boss_information[0],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
			else:
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- ??????????????? -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"							
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)
		else:
			return

	################ ?????? ?????? ?????? ################ 
	@commands.command(name=command[11][0], aliases=command[11][1:])
	async def bunbae_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			separate_money = []
			separate_money = msg.split(" ")
			num_sep = floor(int(separate_money[0]))
			cal_tax1 = floor(float(separate_money[1])*0.05)
			
			real_money = floor(floor(float(separate_money[1])) - cal_tax1)
			cal_tax2 = floor(real_money/num_sep) - floor(float(floor(real_money/num_sep))*0.95)
			if num_sep == 0 :
				await ctx.send('```?????? ????????? 0?????????. ????????? ????????????.```', tts=False)
			else :
				embed = discord.Embed(
					title = "----- ????????????! -----",
					description= '```1??? ?????? : ' + str(cal_tax1) + '\n1??? ????????? : ' + str(real_money) + '\n????????? ????????????????????? : ' + str(floor(real_money/num_sep)) + '\n2??? ?????? : ' + str(cal_tax2) + '\n?????? ???????????? : ' + str(floor(float(floor(real_money/num_sep))*0.95)) + '```',
					color=0xff00ff
					)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ????????? ?????? ?????? ################ 
	@commands.command(name=command[12][0], aliases=command[12][1:])
	async def ladder_(self, ctx : commands.Context, *, args : str = None):
		if basicSetting[8] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[8]:
			if not args:
				return await ctx.send(f'```????????? [??????] [?????????1] [?????????2] ... ????????? ?????????????????? ????????????.```')

			ladder = args.split()

			try:
				num_cong = int(ladder[0])  # ?????? ??????
				del(ladder[0])
			except ValueError:
				return await ctx.send(f'```?????? ????????? ????????? ??????????????????\nex)!????????? 1 ??? ??? ??? ...```')

			if num_cong >= len(ladder):
				return await ctx.send(f'```??????????????? ??? ????????? ????????? ????????????. ????????? ????????????```')
			
			if len(ladder) > 20:
				await LadderFunc(num_cong, ladder, ctx)
				return

			input_dict : dict = {}
			ladder_description : list = []
			ladder_data : list = []
			output_list : list = []
			result :dict = {}

			for i in range(len(ladder)):
				input_dict[f"{i+1}"] = ladder[i]
				if i < num_cong:
					output_list.append("o")
				else:
					output_list.append("x")

			for i in range(len(ladder)+1):
				tmp_list = []
				if i%2 != 0:
					sample_list = ["| |-", "| | "]
				else:
					sample_list = ["| | ", "|-| "]
				for i in range(len(ladder)//2):
					value = random.choice(sample_list)
					tmp_list.append(value)
				ladder_description.append(tmp_list)

			tmp_result = list(input_dict.keys())
			input_data : str = ""

			for i in range(len(tmp_result)):
				if int(tmp_result[i]) < 9:
					input_data += f"{tmp_result[i]} "
				else:
					input_data += f"{tmp_result[i]}"
			input_value_data = " ".join(list(input_dict.values()))

			for i in range(len(ladder_description)):
				if (len(ladder) % 2) != 0:
					ladder_data.append(f"{''.join(ladder_description[i])}|\n")
				else:
					ladder_data.append(f"{''.join(ladder_description[i])[:-1]}\n")
				
				random.shuffle(output_list)

			output_data = list(" ".join(output_list))

			for line in reversed(ladder_data):
				for i, x in enumerate(line):
					if i % 2 == 1 and x == '-':
						output_data[i-1], output_data[i+1] = output_data[i+1], output_data[i-1]

			for i in range(output_data.count(" ")):
				output_data.remove(" ")

			for i in range(len(tmp_result)):
				result[tmp_result[i]] = output_data[i]
			result_str : str = ""
			join_member : list = []
			win_member : list = []
			lose_member : list = []

			for x, y in result.items():
				join_member.append(f"{x}:{input_dict[f'{x}']}")
				if y == "o":
					win_member.append(f"{input_dict[f'{x}']}")
				else :
					lose_member.append(f"{input_dict[f'{x}']}")

			embed = discord.Embed(title  = "???? ?????????! ?????? ????????? ???!",
				color=0x00ff00
				)
			embed.description = f"||```{input_data}\n{''.join(ladder_data)}{' '.join(output_list)}```||"
			embed.add_field(name = "???? ?????????", value =  f"```fix\n{', '.join(join_member)}```", inline=False)
			embed.add_field(name = "???? ??????", value =  f"```fix\n{', '.join(win_member)}```")
			embed.add_field(name = "???? ??????", value =  f"```{', '.join(lose_member)}```")
			return await ctx.send(embed = embed)
		else:
			return

	################ ???????????? ################ 
	@commands.command(name=command[13][0], aliases=command[13][1:])
	async def jungsan_(self, ctx):
		if basicSetting[11] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[11]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			if basicSetting[10] !="" and basicSetting[12] !="" and basicSetting[14] !="" and basicSetting[15] !="" and basicSetting[16] !=""  :
				SearchID = msg
				gc = gspread.authorize(credentials)
				wks = gc.open(basicSetting[12]).worksheet(basicSetting[14])

				wks.update_acell(basicSetting[15], SearchID)

				result = wks.acell(basicSetting[16]).value

				embed = discord.Embed(
						description= '```' + SearchID + ' ?????? ?????? ???????????? ' + result + ' ????????? ?????????.```',
						color=0xff00ff
						)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ???????????? ?????? ?????? ################
	@commands.command(name=command[14][0], aliases=command[14][1:])
	async def allBossInput_(self, ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99':
					tmp_msg = msg
					if len(tmp_msg) > 3 :
						if tmp_msg.find(':') != -1 :
							chkpos = tmp_msg.find(':')
							hours1 = tmp_msg[chkpos-2:chkpos]
							minutes1 = tmp_msg[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(tmp_msg)-2
							hours1 = tmp_msg[chkpos-2:chkpos]
							minutes1 = tmp_msg[chkpos:chkpos+2]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = now2
						
					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 1

					if tmp_now > now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(-1))
						
					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							bossMungCnt[i] = bossMungCnt[i] + 1
						now2 = tmp_now
						bossMungCnt[i] = bossMungCnt[i] - 1
					else :
						now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								
					tmp_bossTime[i] = bossTime[i] = nextTime = now2
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

			await dbSave()
			await dbLoad()
			await dbSave()
			
			await ctx.send('<?????????????????????????????????>', tts=False)
			print ("<?????? ?????? ?????? ??????>")
		else:
			return

	################ ??????????????? ?????? ?????? ################
	@commands.command(name=command[40][0], aliases=command[40][1:])
	async def mungBossInput_(self, ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(bossNum):
				if bossData[i][2] == "1" and bossTimeString[i] == '99:99:99':
					tmp_msg = msg
					if len(tmp_msg) > 3 :
						if tmp_msg.find(':') != -1 :
							chkpos = tmp_msg.find(':')
							hours1 = tmp_msg[chkpos-2:chkpos]
							minutes1 = tmp_msg[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(tmp_msg)-2
							hours1 = tmp_msg[chkpos-2:chkpos]
							minutes1 = tmp_msg[chkpos:chkpos+2]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = now2
						
					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 1

					if tmp_now > now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(-1))
						
					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							bossMungCnt[i] = bossMungCnt[i] + 1
						now2 = tmp_now
						bossMungCnt[i] = bossMungCnt[i] - 1
					else :
						now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								
					tmp_bossTime[i] = bossTime[i] = nextTime = now2
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

			await dbSave()
			await dbLoad()
			await dbSave()
			
			await ctx.send('<????????? ?????? ?????? ??????>', tts=False)
			print ("<????????? ?????? ?????? ??????>")
		else:
			return

	################ ?????? ????????? ???????????? ?????? ################ 
	@commands.command(name=command[15][0], aliases=command[15][1:])
	async def nearTimeBoss_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			checkTime = datetime.datetime.now() + datetime.timedelta(days=1, hours = int(basicSetting[0]))
			
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			sorted_datelist = []

			for i in range(bossNum):
				if bossMungFlag[i] != True and bossTimeString[i] != '99:99:99' :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			for i in range(bossNum):
				if bossMungFlag[i] != True :
					aa.append(bossData[i][0])		                 #output_bossData[0] : ?????????
					aa.append(bossTime[i])                           #output_bossData[1] : ??????
					aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : ??????(00:00:00)
					ouput_bossData.append(aa)
				aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : ?????????
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : ??????
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : ??????(00:00:00)
				ouput_bossData.append(aa)
				aa = []

			tmp_sorted_datelist = sorted(datelist)

			for i in range(len(tmp_sorted_datelist)):
				if checkTime > tmp_sorted_datelist[i]:
					sorted_datelist.append(tmp_sorted_datelist[i])
			
			if len(sorted_datelist) == 0:
				await ctx.send( '<???????????????????????????????????????>', tts=False)
			else : 
				result_lefttime = ''
				
				if len(sorted_datelist) > int(basicSetting[9]):
					for j in range(int(basicSetting[9])):
						for i in range(len(ouput_bossData)):
							if sorted_datelist[j] == ouput_bossData[i][1]:
								leftTime = ouput_bossData[i][1] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

								total_seconds = int(leftTime.total_seconds())
								hours, remainder = divmod(total_seconds,60*60)
								minutes, seconds = divmod(remainder,60)

								result_lefttime += ouput_bossData[i][0] + '?????????????????? %02d:%02d:%02d ?????????????????? ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
				else :
					for j in range(len(sorted_datelist)):
						for i in range(len(ouput_bossData)):						
							if sorted_datelist[j] == ouput_bossData[i][1]:
								leftTime = ouput_bossData[i][1] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

								total_seconds = int(leftTime.total_seconds())
								hours, remainder = divmod(total_seconds,60*60)
								minutes, seconds = divmod(remainder,60)

								result_lefttime +=  ouput_bossData[i][0] + '?????????????????? %02d:%02d:%02d ?????????????????? ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
				embed = discord.Embed(
					description= result_lefttime,
					color=0xff0000
					)
				await ctx.send( embed=embed, tts=False)
		else:
			return

	################ ???????????? ?????? ??? ?????? ################ 			
	@commands.command(name=command[16][0], aliases=command[16][1:])
	async def playText_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			if basicSetting[21] != "1":
				return await ctx.send('```???????????? ???????????? ????????? ???????????? ????????????.```', tts=False)

			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			try:
				await MakeSound(ctx.message.author.display_name +'??????, ' + sayMessage, './sound/say')
			except:
				await ctx.send( f"```???????????? ????????? ?????????????????????.!(amazon polly ????????? ??? ?????? ???????????????!)```")
				return
			await ctx.send("```< " + ctx.author.display_name + " >?????? \"" + sayMessage + "\"```", tts=False)
			try:
				if aws_key != "" and aws_secret_key != "":
					await PlaySound(ctx.voice_client, './sound/say.mp3')
				else:
					await PlaySound(ctx.voice_client, './sound/say.wav')
			except:
				await ctx.send( f"```???????????? ????????? ?????????????????????. ????????? ????????? ????????? ??????????????? ?????? ?????? ?????? ???????????????.!```")
				return
		else:  
			return

	################ ???????????? ?????? ################
	@commands.command(name=command[17][0], aliases=command[17][1:])
	async def regenTime_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send(embed=regenembed, tts=False)
		else:
			return
			
	################ ???????????? ?????? ################ 
	@commands.command(name=command[18][0], aliases=command[18][1:])
	async def currentTime_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			curruntTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
			embed = discord.Embed(
				title = '??????????????? ' + curruntTime.strftime('%H') + '??? ' + curruntTime.strftime('%M') + '??? ' + curruntTime.strftime('%S')+ '??? ?????????.',
				color=0xff00ff
				)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ ?????? ??????/?????? ################ 
	@commands.command(name=command[19][0], aliases=command[19][1:])
	async def notice_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content.split(" ")
			if len(msg) > 1:
				sayMessage = " ".join(msg[1:])
				contents = repo.get_contents("notice.ini")
				repo.update_file(contents.path, "notice ??????", sayMessage, contents.sha)
				await ctx.send( '< ?????? ???????????? >', tts=False)
			else:
				notice_initdata = repo.get_contents("notice.ini")
				notice = base64.b64decode(notice_initdata.content)
				notice = notice.decode('utf-8')
				if notice != '' :
					embed = discord.Embed(
							description= str(notice),
							color=0xff00ff
							)
				else :
					embed = discord.Embed(
							description= '```????????? ????????? ????????????.```',
							color=0xff00ff
							)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ?????? ?????? ################ 
	@commands.command(name=command[20][0], aliases=command[20][1:])
	async def noticeDel_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			contents = repo.get_contents("notice.ini")
			repo.update_file(contents.path, "notice ??????", '', contents.sha)
			await ctx.send( '< ?????? ???????????? >', tts=False)
		else:
			return

	################ ??? ??????????????? ?????? ################ 
	@commands.command(name=command[21][0], aliases=command[21][1:])
	async def botStatus_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=sayMessage, type=1), afk = False)
			await ctx.send( '< ??????????????? ???????????? >', tts=False)
		else:
			return

	################ ???????????? ?????? ################ 
	@commands.command(name=command[22][0], aliases=command[22][1:])
	async def bossTime_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_time_delta = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1000 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : ?????????
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : ??????

						tmp_time_delta = (tmp_bossTime[i].date() - (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).date()).days
						if tmp_time_delta == 0:
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))
						else:
							if tmp_time_delta > 0:
								aa.append(f"(+{tmp_time_delta}d) {tmp_bossTime[i].strftime('%H:%M:%S')}")
							else:
								aa.append(f"({tmp_time_delta}d) {tmp_bossTime[i].strftime('%H:%M:%S')}")

						tmp_time_delta = 0

						# aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : ??????(00:00:00) -> ????????? : aa.append(tmp_bossTime[i].strftime('%H:%M'))  
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : ??????

						tmp_time_delta = (tmp_bossTime[i].date() - (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).date()).days
						if tmp_time_delta == 0:
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))
						else:
							if tmp_time_delta > 0:
								aa.append(f"(+{tmp_time_delta}d) {tmp_bossTime[i].strftime('%H:%M:%S')}")
							else:
								aa.append(f"({tmp_time_delta}d) {tmp_bossTime[i].strftime('%H:%M:%S')}")

						tmp_time_delta = 0

						# aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : ??????(00:00:00) -> ????????? : aa.append(bossTime[i].strftime('%H:%M'))  
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : ???/????????? ??????
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : ???/???????????????
					aa.append(bossData[i][6])	                         #output_bossData[6] : ?????????
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : ?????????
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : ??????
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : ??????(00:00:00) -> ????????? : aa.append(fixed_bossTime[i].strftime('%H:%M'))
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : ???/????????? ??????
				aa.append(0)                                         #output_bossData[5] : ???/???????????????
				aa.append("")                                        #output_bossData[6] : ?????????
				ouput_bossData.append(aa)
				aa = []

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (????????? ' + str(ouput_bossData[i][5]) + '???)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (???????????? ' + str(ouput_bossData[i][5]) + '???)' + ' ' + ouput_bossData[i][6] + '\n'

			if len(boss_information) == 1 and len(tmp_boss_information) == 1:
				###########################
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- ??????????????? -----",
						description= boss_information[0],
						color=0x0000ff
						)
				embed.add_field(
						name="----- ??????????????? -----",
						value= tmp_boss_information[0],
						inline = False
						)				
				await ctx.send( embed=embed, tts=False)
			else : 
				###########################??????????????????
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- ??????????????? -----",
						description= boss_information[0],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(boss_information)-1):
					if len(boss_information[i+1]) != 0:
						boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
					else :
						boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)
				###########################?????????????????????
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- ??????????????? -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"							
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)

			await dbSave()
			await data_list_Save("kill_list.ini", "-----????????????-----", kill_Data)
			await data_list_Save("item_list.ini", "-----???????????????-----", item_Data)
		else:
			return

	################ ???????????? ??????(??????????????????) ################ 
	@commands.command(name=command[23][0], aliases=command[23][1:])
	async def bossTime_fixed_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			fixed_datelist = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1800 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : ?????????
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : ??????

						if (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).strftime('%Y-%m-%d') == tmp_bossTime[i].strftime('%Y-%m-%d'):
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))
						else:
							aa.append(f"[{tmp_bossTime[i].strftime('%Y-%m-%d')}] {tmp_bossTime[i].strftime('%H:%M:%S')}")

						# aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : ??????(00:00:00) -> ????????? : aa.append(tmp_bossTime[i].strftime('%H:%M'))
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : ??????

						if (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).strftime('%Y-%m-%d') == bossTime[i].strftime('%Y-%m-%d'):
							aa.append(bossTime[i].strftime('%H:%M:%S'))
						else:
							aa.append(f"[{bossTime[i].strftime('%Y-%m-%d')}] {bossTime[i].strftime('%H:%M:%S')}")
							
						# aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : ??????(00:00:00) -> ????????? : aa.append(bossTime[i].strftime('%H:%M'))
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : ???/????????? ??????
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : ???/???????????????
					aa.append(bossData[i][6])	                         #output_bossData[6] : ?????????
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				fixed_datelist.append(fixed_bossTime[i])

			fixed_datelist = list(set(fixed_datelist))

			fixedboss_information = []
			cntF = 0
			fixedboss_information.append('')
					
			for timestring1 in sorted(fixed_datelist):
				if len(fixedboss_information[cntF]) > 1800 :
					fixedboss_information.append('')
					cntF += 1
				for i in range(fixed_bossNum):
					if timestring1 == fixed_bossTime[i]:
						if (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).strftime('%Y-%m-%d') == fixed_bossTime[i].strftime('%Y-%m-%d'):
							tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M:%S') #????????? : tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M')
						else:
							tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M:%S') #????????? : tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M')
						fixedboss_information[cntF] = fixedboss_information[cntF] + tmp_timeSTR + ' : ' + fixed_bossData[i][0] + '\n'

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (????????? ' + str(ouput_bossData[i][5]) + '???)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (???????????? ' + str(ouput_bossData[i][5]) + '???)' + ' ' + ouput_bossData[i][6] + '\n'

			###########################??????????????????
			if len(fixedboss_information[0]) != 0:
				fixedboss_information[0] = "```diff\n" + fixedboss_information[0] + "\n```"
			else :
				fixedboss_information[0] = '``` ```'
	
			embed = discord.Embed(
					title = "----- ?????????????????? -----",
					description= fixedboss_information[0],
					color=0x0000ff
					)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(fixedboss_information)-1):
				if len(fixedboss_information[i+1]) != 0:
					fixedboss_information[i+1] = "```diff\n" + fixedboss_information[i+1] + "\n```"
				else :
					fixedboss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= fixedboss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			###########################??????????????????
			if len(boss_information[0]) != 0:
				boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
			else :
				boss_information[0] = '``` ```'

			embed = discord.Embed(
					title = "----- ??????????????? -----",
					description= boss_information[0],
					color=0x0000ff
					)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(boss_information)-1):
				if len(boss_information[i+1]) != 0:
					boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
				else :
					boss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= boss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			###########################?????????????????????
			if len(tmp_boss_information[0]) != 0:
				if len(tmp_boss_information) == 1 :
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
			else :
				tmp_boss_information[0] = '``` ```'

			embed = discord.Embed(
				title = "----- ??????????????? -----",
				description= tmp_boss_information[0],
				color=0x0000ff
				)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(tmp_boss_information)-1):
				if len(tmp_boss_information[i+1]) != 0:
					if i == len(tmp_boss_information)-2:
						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
					else:
						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
				else :
					tmp_boss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= tmp_boss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			await dbSave()
			await data_list_Save("kill_list.ini", "-----????????????-----", kill_Data)
			await data_list_Save("item_list.ini", "-----???????????????-----", item_Data)
		else:
			return

	################ ???????????? ################ 
	@commands.command(name=command[24][0], aliases=command[24][1:])
	async def killInit_(self, ctx):
		if basicSetting[18] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data

			kill_Data = {}
			
			await init_data_list('kill_list.ini', '-----????????????-----')
			return await ctx.send( '< ??? ?????? ??????????????? >', tts=False)
		else:
			return

	################ ????????? ?????? ??? ??????################ 
	@commands.command(name=command[25][0], aliases=command[25][1:]) 
	async def killList_(self, ctx, *, args : str = None):
		if basicSetting[18] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data

			if not args:
				kill_output = ''
				for key, value in kill_Data.items():
					kill_output += ':skull_crossbones: ' + str(key) + ' : ' + str(value) + '??? ??????!\n'

				if kill_output != '' :
					embed = discord.Embed(
							description= str(kill_output),
							color=0xff00ff
							)
				else :
					embed = discord.Embed(
							description= '????????? ??? ????????? ????????????. ???????????????!',
							color=0xff00ff
							)
				return await ctx.send(embed=embed, tts=False)

			if args in kill_Data:
				kill_Data[args] += 1
			else:
				kill_Data[args] = 1
					
			embed = discord.Embed(
					description= ':skull_crossbones: ' + args + ' ??????! [' + str(kill_Data[args]) + '???]\n',
					color=0xff00ff
					)
			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ????????? ################ 
	@commands.command(name=command[26][0], aliases=command[26][1:])
	async def killDel_(self, ctx, *, args : str = None):
		if basicSetting[18] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data
			
			if not args:
				return await ctx.send( '```????????? ??? ???????????? ??????????????????!\n```', tts=False)
			
			if args in kill_Data:
				del kill_Data[args]
				return await ctx.send( ':angel: ' + args + ' ????????????!', tts=False)
			else :				
				return await ctx.send( '```??? ????????? ???????????? ?????? ????????????!\n```', tts=False)
		else:
			return

	################ ??? ?????? ################ 
	@commands.command(name=command[33][0], aliases=command[33][1:]) 
	async def killSubtract_(self, ctx, *, args : str = None):
		if basicSetting[18] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data

			if not args:
				return await ctx.send(f'{command[33][0]} [?????????] ?????? {command[33][0]} [?????????] [??????] ????????? ?????? ??????????????????!', tts = False)

			input_data = args.split()
			
			if len(input_data) == 1:
				kill_name = args
				count = 1
			elif len(input_data) == 2:
				kill_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'[??????]??? ????????? ??????????????????')
			else:
				return await ctx.send(f'{command[33][0]} [?????????] ?????? {command[33][0]} [?????????] [??????] ????????? ?????? ??????????????????!', tts = False)

			if kill_name in kill_Data:
				if kill_Data[kill_name] < int(count):
					return await ctx.send( f"????????? ??? ??????[{str(kill_Data[kill_name])}???]?????? ?????? ??????[{str(count)}???]??? ????????????. ??? ????????? ?????? ????????? ????????????.", tts=False)
				else:
					kill_Data[kill_name] -= int(count)
			else:
				return await ctx.send( '```??? ????????? ???????????? ?????? ????????????!\n```', tts=False)
					
			embed = discord.Embed(
					description= f':angel: [{kill_name}] [{str(count)}???] ?????? ??????! [?????? : {str(kill_Data[kill_name])}???]\n',
					color=0xff00ff
					)
			
			if kill_Data[kill_name] == 0:
				del kill_Data[kill_name]

			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ?????? ################ 
	@commands.command(name=command[27][0], aliases=command[27][1:])
	async def race_(self, ctx):
		if basicSetting[19] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[19]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			race_info = []
			fr = []
			racing_field = []
			str_racing_field = []
			cur_pos = []
			race_val = []
			random_pos = []
			racing_result = []
			output = ':camera: :camera: :camera: ????????? ?????????! :camera: :camera: :camera:\n'
			#racing_unit = [':giraffe:', ':elephant:', ':tiger2:', ':hippopotamus:', ':crocodile:',':leopard:',':ox:', ':sheep:', ':pig2:',':dromedary_camel:',':dragon:',':rabbit2:'] #????????????
			#racing_unit = [':red_car:', ':taxi:', ':bus:', ':trolleybus:', ':race_car:', ':police_car:', ':ambulance:', ':fire_engine:', ':minibus:', ':truck:', ':articulated_lorry:', ':tractor:', ':scooter:', ':manual_wheelchair:', ':motor_scooter:', ':auto_rickshaw:', ':blue_car:', ':bike:', ':helicopter:', ':steam_locomotive:']  #????????????
			#random.shuffle(racing_unit) 
			racing_member = msg.split(" ")

			racing_unit = []

			emoji = discord.Emoji
			emoji = ctx.message.guild.emojis

			for j in range(len(tmp_racing_unit)):
				racing_unit.append(':' + tmp_racing_unit[j] + ':')
				for i in range(len(emoji)):
					if emoji[i].name == tmp_racing_unit[j].strip(":"):
						racing_unit[j] = '<:' + tmp_racing_unit[j] + ':' + str(emoji[i].id) + '>'

			random.shuffle(racing_unit)

			field_size = 60
			tmp_race_tab = 35 - len(racing_member)
			if len(racing_member) <= 1:
				await ctx.send('????????? ????????? 2????????? ????????????.')
				return
			elif len(racing_member) >= 13:
				await ctx.send('????????? ????????? 12??? ???????????????.')
				return
			else :
				race_val = random.sample(range(tmp_race_tab, tmp_race_tab+len(racing_member)), len(racing_member))
				random.shuffle(race_val)
				for i in range(len(racing_member)):
					fr.append(racing_member[i])
					fr.append(racing_unit[i])
					fr.append(race_val[i])
					race_info.append(fr)
					fr = []
					for i in range(field_size):
						fr.append(" ")
					racing_field.append(fr)
					fr = []

				for i in range(len(racing_member)):
					racing_field[i][0] = "|"
					racing_field[i][field_size-2] = race_info[i][1]
					if len(race_info[i][0]) > 5:
						racing_field[i][field_size-1] = "| " + race_info[i][0][:5] + '..'
					else:
						racing_field[i][field_size-1] = "| " + race_info[i][0]
					str_racing_field.append("".join(racing_field[i]))
					cur_pos.append(field_size-2)
				
				for i in range(len(racing_member)):
					output +=  str_racing_field[i] + '\n'

				result_race = await ctx.send(output + ':traffic_light: 3??? ??? ????????? ???????????????!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 2??? ??? ????????? ???????????????!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 1??? ??? ????????? ???????????????!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':checkered_flag:  ?????? ??????!')								

				for i in range(len(racing_member)):
					test = random.sample(range(2,field_size-2), race_info[i][2])
					while len(test) != tmp_race_tab + len(racing_member)-1 :
						test.append(1)
					test.append(1)
					test.sort(reverse=True)
					random_pos.append(test)

				for j in range(len(random_pos[0])):
					if j%2 == 0:
						output =  ':camera: :camera_with_flash: :camera: ????????? ?????????! :camera_with_flash: :camera: :camera_with_flash:\n'
					else :
						output =  ':camera_with_flash: :camera: :camera_with_flash: ????????? ?????????! :camera: :camera_with_flash: :camera:\n'
					str_racing_field = []
					for i in range(len(racing_member)):
						temp_pos = cur_pos[i]
						racing_field[i][random_pos[i][j]], racing_field[i][temp_pos] = racing_field[i][temp_pos], racing_field[i][random_pos[i][j]]
						cur_pos[i] = random_pos[i][j]
						str_racing_field.append("".join(racing_field[i]))

					await asyncio.sleep(1) 

					for i in range(len(racing_member)):
						output +=  str_racing_field[i] + '\n'
					
					await result_race.edit(content = output + ':checkered_flag:  ?????? ??????!')
				
				for i in range(len(racing_field)):
					fr.append(race_info[i][0])
					fr.append((race_info[i][2]) - tmp_race_tab + 1)
					racing_result.append(fr)
					fr = []

				result = sorted(racing_result, key=lambda x: x[1])

				result_str = ''
				for i in range(len(result)):
					if result[i][1] == 1:
						result[i][1] = ':first_place:'
					elif result[i][1] == 2:
						result[i][1] = ':second_place:'
					elif result[i][1] == 3:
						result[i][1] = ':third_place:'
					elif result[i][1] == 4:
						result[i][1] = ':four:'
					elif result[i][1] == 5:
						result[i][1] = ':five:'
					elif result[i][1] == 6:
						result[i][1] = ':six:'
					elif result[i][1] == 7:
						result[i][1] = ':seven:'
					elif result[i][1] == 8:
						result[i][1] = ':eight:'
					elif result[i][1] == 9:
						result[i][1] = ':nine:'
					elif result[i][1] == 10:
						result[i][1] = ':keycap_ten:'
					else:
						result[i][1] = ':x:'
					result_str += result[i][1] + "  " + result[i][0] + "  "
					
				#print(result)
				await asyncio.sleep(1)
				return await result_race.edit(content = output + ':tada: ?????? ??????!\n' + result_str)
		else:
			return

	################ ???????????? ################ 	
	@commands.command(name=command[28][0], aliases=command[28][1:])
	async def set_channel_(self, ctx):
		global basicSetting

		msg = ctx.message.content[len(ctx.invoked_with)+1:]
		channel = ctx.message.channel.id #???????????? ????????? ?????? ID

		if channel == basicSetting[7] and msg in ["?????????", "??????", "??????", "??????", "?????????"]:
			return await ctx.send(f'????????? ????????? `{msg} ??????`??? `??????`??? ??? ????????????.', tts=False)

		if msg == '?????????' : #????????? ?????? ??????
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('ladderchannel'):
					inputData_textCH[i] = 'ladderchannel = ' + str(channel) + '\r'
					basicSetting[8] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ??????????????? [{ctx.message.channel.name}] ???????????? >')
			return await ctx.send(f'< ??????????????? [{ctx.message.channel.name}] ???????????? >', tts=False)
		elif msg == '??????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('jungsanchannel'):
					inputData_textCH[i] = 'jungsanchannel = ' + str(channel) + '\r'
					basicSetting[11] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ???????????? [{ctx.message.channel.name}] ???????????? >')
			return await ctx.send(f'< ???????????? [{ctx.message.channel.name}] ???????????? >', tts=False)			
		elif msg == '??????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('killchannel'):
					inputData_textCH[i] = 'killchannel = ' + str(channel) + '\r'
					basicSetting[18] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ???????????? [{ctx.message.channel.name}] ???????????? >')
			return await ctx.send(f'< ???????????? [{ctx.message.channel.name}] ???????????? >', tts=False)
		elif msg == '??????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('racingchannel'):
					inputData_textCH[i] = 'racingchannel = ' + str(channel) + '\r'
					basicSetting[19] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ???????????? [{ctx.message.channel.name}] ???????????? >')
			return await ctx.send(f'< ???????????? [{ctx.message.channel.name}] ???????????? >', tts=False)
		elif msg == '?????????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('itemchannel'):
					inputData_textCH[i] = 'itemchannel = ' + str(channel) + '\r'
					basicSetting[20] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ??????????????? [{ctx.message.channel.name}] ???????????? >')
			return await ctx.send(f'< ??????????????? [{ctx.message.channel.name}] ???????????? >', tts=False)
		else :
			return await ctx.send(f'```????????? ???????????? ??????????????????.```', tts=False)

	################ ???????????? ################ 	
	@commands.command(name=command[42][0], aliases=command[42][1:])
	async def remove_channel_(self, ctx):
		global basicSetting
		if ctx.message.channel.id != basicSetting[7]:
			return

		msg = ctx.message.content[len(ctx.invoked_with)+1:]
		channel = ctx.message.channel.id #???????????? ????????? ?????? ID

		if msg == '?????????' : #????????? ?????? ??????
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			ch_name = ctx.guild.get_channel(int(basicSetting[8]))
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('ladderchannel'):
					inputData_textCH[i] = 'ladderchannel = \r'
					basicSetting[8] = ""
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ??????????????? [{ch_name}] ???????????? >')
			return await ctx.send(f'< ??????????????? [{ch_name}] ???????????? >', tts=False)
		elif msg == '??????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			ch_name = ctx.guild.get_channel(int(basicSetting[11]))
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('jungsanchannel'):
					inputData_textCH[i] = 'jungsanchannel = \r'
					basicSetting[11] = ""
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ???????????? [{ch_name}] ???????????? >')
			return await ctx.send(f'< ???????????? [{ch_name}] ???????????? >', tts=False)			
		elif msg == '??????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			ch_name = ctx.guild.get_channel(int(basicSetting[18]))
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('killchannel'):
					inputData_textCH[i] = 'killchannel = \r'
					basicSetting[18] = ""
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ???????????? [{ch_name}] ???????????? >')
			return await ctx.send(f'< ???????????? [{ch_name}] ???????????? >', tts=False)
		elif msg == '??????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			ch_name = ctx.guild.get_channel(int(basicSetting[19]))
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('racingchannel'):
					inputData_textCH[i] = 'racingchannel = \r'
					basicSetting[19] = ""
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ???????????? [{ch_name}] ???????????? >')
			return await ctx.send(f'< ???????????? [{ch_name}] ???????????? >', tts=False)
		elif msg == '?????????' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			ch_name = ctx.guild.get_channel(int(basicSetting[20]))
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('itemchannel'):
					inputData_textCH[i] = 'itemchannel = \r'
					basicSetting[20] = ""
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< ??????????????? [{ch_name}] ???????????? >')
			return await ctx.send(f'< ??????????????? [{ch_name}] ???????????? >', tts=False)
		else :
			return await ctx.send(f'```????????? ???????????? ??????????????????.```', tts=False)

	################ ?????????????????? ?????? ################ 
	@commands.command(name=command[29][0], aliases=command[29][1:])
	async def itemInit_(self, ctx):
		if basicSetting[20] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data

			item_Data = {}

			await init_data_list('item_list.ini', '-----????????? ??????-----')
			return await ctx.send( '< ????????? ?????? ??????????????? >', tts=False)
		else:
			return

	################ ????????? ?????? ?????? ??? ?????? ################ 
	@commands.command(name=command[30][0], aliases=command[30][1:]) 
	async def itemList_(self, ctx, *, args : str = None):
		if basicSetting[20] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data
			
			if not args:
				sorted_item_list = sorted(item_Data.items(), key=lambda x: x[0])

				embed_list : list = []
				embed_index : int = 0
				embed_cnt : int = 0
				embed = discord.Embed(title = '', description = f'`{self.bot.user.name}\'s ??????`', color = 0x00ff00)
				
				embed_list.append(embed)

				if len(sorted_item_list) > 0 :
					for item_id, count in sorted_item_list:
						embed_cnt += 1
						if embed_cnt > 24 :
							embed_cnt = 0
							embed_index += 1
							tmp_embed = discord.Embed(
								title = "",
								description = "",
								color=0x00ff00
								)
							embed_list.append(tmp_embed)
						embed_list[embed_index].add_field(name = item_id, value = count)
					embed_list[len(embed_list)-1].set_footer(text = f"?????? ????????? ??????  :  {len(item_Data)}???")
					if len(embed_list) > 1:
						for embed_data in embed_list:
							await asyncio.sleep(0.1)
							await ctx.send(embed = embed_data)
						return
					else:
						return await ctx.send(embed=embed, tts=False)
				else :
					embed.add_field(name = '\u200b\n', value = '????????? ???????????????.\n\u200b')
					return await ctx.send(embed=embed, tts=False)

			input_data = args.split()
			
			if len(input_data) == 1:
				item_name = args
				count = 1
			elif len(input_data) == 2:
				item_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'????????? [??????]??? ????????? ??????????????????')
			else:
				return await ctx.send(f'{command[30][0]} [????????????] ?????? {command[30][0]} [????????????] [??????] ????????? ?????? ??????????????????!', tts = False)	

			if item_name in item_Data:
				item_Data[item_name] += int(count)
			else:
				item_Data[item_name] = int(count)
					
			embed = discord.Embed(
					description= f':inbox_tray: **[{item_name}] [{str(count)}???]** ?????? ??????! [?????? : {str(item_Data[item_name])}???]\n',
					color=0xff00ff
					)
			return await ctx.send(embed=embed, tts=False)

		else:
			return

	################ ????????? ?????? ################ 
	@commands.command(name=command[31][0], aliases=command[31][1:])
	async def itemDel_(self, ctx, *, args : str = None):
		if basicSetting[20] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data

			if not args:
				return await ctx.send( f'{command[31][0]} [????????????] ????????? ?????? ??????????????????!', tts = False)

			if args in item_Data:
				del item_Data[args]
				embed = discord.Embed(
					description= ':outbox_tray: ' + args + ' ????????????!',
					color=0xff00ff
					)
				return await ctx.send(embed=embed, tts=False)
			else :				
				return await ctx.send( '```????????? ????????? ???????????? ?????? ????????????!\n```', tts=False)
		else:
			return

	################ ????????? ?????? ################ 
	@commands.command(name=command[32][0], aliases=command[32][1:]) 
	async def itemSubtract_(self, ctx, *, args : str = None):
		if basicSetting[20] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data

			if not args:
				return await ctx.send(f'{command[32][0]} [????????????] ?????? {command[32][0]} [????????????] [??????] ????????? ?????? ??????????????????!', tts = False)

			input_data = args.split()
			
			if len(input_data) == 1:
				item_name = args
				count = 1
			elif len(input_data) == 2:
				item_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'????????? [??????]??? ????????? ??????????????????')
			else:
				return await ctx.send(f'{command[32][0]} [????????????] ?????? {command[32][0]} [????????????] [??????] ????????? ?????? ??????????????????!', tts = False)	

			if item_name in item_Data:
				if item_Data[item_name] < int(count):
					return await ctx.send( f"????????? ????????? ??????[{str(item_Data[item_name])}???]?????? ?????? ??????[{str(count)}???]??? ????????????. ?????? ????????? ?????? ????????? ????????????.", tts=False)
				else:
					item_Data[item_name] -= int(count)
			else:
				return await ctx.send( '```????????? ????????? ???????????? ?????? ????????????!\n```', tts=False)
					
			embed = discord.Embed(
					description= f':outbox_tray: **[{item_name}] [{str(count)}???]** ?????? ??????! [?????? : {str(item_Data[item_name])}???]\n',
					color=0xff00ff
					)
			
			if item_Data[item_name] == 0:
				del item_Data[item_name]

			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ?????? ????????? ################ 		
	@commands.has_permissions(manage_messages=True)
	@commands.command(name=command[34][0], aliases=command[34][1:])
	async def leaveGuild_(self, ctx):
		if ctx.message.channel.id == basicSetting[7]:
			guild_list : str = ""
			guild_name : str = ""

			for i, gulid_name in enumerate(self.bot.guilds):
				guild_list += f"`{i+1}.` {gulid_name}\n"

			embed = discord.Embed(
				title = "----- ?????? ?????? -----",
				description = guild_list,
				color=0x00ff00
				)
			await ctx.send(embed = embed)

			try:
				await ctx.send(f"```????????? ?????? ????????? [??????]??? ???????????? ????????? ?????????```")
				message_result : discord.Message = await self.bot.wait_for("message", timeout = 10, check=(lambda message: message.channel == ctx.message.channel and message.author == ctx.message.author))
			except asyncio.TimeoutError:
				return await ctx.send(f"```?????? ?????? ????????? ??????????????????! ????????? ???????????? ???????????? ?????????```")
				
			try:
				guild_name = self.bot.guilds[int(message_result.content)-1].name
				await self.bot.get_guild(self.bot.guilds[int(message_result.content)-1].id).leave()
				return await ctx.send(f"```[{guild_name}] ???????????? ???????????????.!```")
			except ValueError:
				return			

	################ ????????? ????????? ################ 
	@commands.command(name=command[35][0], aliases=command[35][1:])
	async def tax_check(self, ctx, *, args : str = None):
		if basicSetting[20] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			if not args:
				return await ctx.send(f"**{command[35][0]} [????????????] (???????????????)** ???????????? ?????? ????????????\n??? ?????????????????? ???????????? 5%?????????.")
			
			input_money_data : list = args.split()
			len_input_money_data = len(input_money_data)

			try:
				for i in range(len_input_money_data):
					input_money_data[i] = int(input_money_data[i])
			except ValueError:
				return await ctx.send(f"**[????????????] (???????????????)**??? ????????? ?????? ????????????.")

			if len_input_money_data < 1 or len_input_money_data > 3:
				return await ctx.send(f"**{command[35][0]} [????????????] (???????????????)** ???????????? ?????? ????????????\n??? ?????????????????? ???????????? 5%?????????.")
			elif len_input_money_data == 2:
				tax = input_money_data[1]
			else:
				tax = 5

			price_first_tax = int(input_money_data[0] * ((100-tax)/100))
			price_second_tax = int(price_first_tax * ((100-tax)/100))
			price_rev_tax = int((input_money_data[0] * 100)/(100-tax)+0.5)

			embed = discord.Embed(
					title = f"????  ????????? ???????????? (?????? {tax}% ??????) ",
					description = f"",
					color=0x00ff00
					)
			embed.add_field(name = "?????? ????????? ??????", value = f"```????????? : {price_rev_tax}\n????????? : {input_money_data[0]}\n??? ??? : {price_rev_tax-input_money_data[0]}```")
			embed.add_field(name = "?????? 1??? ??????", value = f"```????????? : {input_money_data[0]}\n????????? : {price_first_tax}\n??? ??? : {input_money_data[0]-price_first_tax}```")
			embed.add_field(name = "?????? 2??? ??????", value = f"```????????? : {price_first_tax}\n????????? : {price_second_tax}\n??? ??? : {price_first_tax-price_second_tax}```")
			return await ctx.send(embed = embed)
		else:
			return

	################ ????????? ????????? ################ 
	@commands.command(name=command[36][0], aliases=command[36][1:])
	async def payback_check(self, ctx, *, args : str = None):
		if basicSetting[20] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			if not args:
				return await ctx.send(f"**{command[36][0]} [???????????????] [????????????] (???????????????)** ???????????? ?????? ????????????\n??? ?????????????????? ???????????? 5%?????????.")
			
			input_money_data : list = args.split()
			len_input_money_data = len(input_money_data)

			try:
				for i in range(len_input_money_data):
					input_money_data[i] = int(input_money_data[i])
			except ValueError:
				return await ctx.send(f"**[????????????] (???????????????)**??? ????????? ?????? ????????????.")

			if len_input_money_data < 2 or len_input_money_data > 4:
				return await ctx.send(f"**{command[36][0]} [???????????????] [????????????] (???????????????)** ???????????? ?????? ????????????\n??? ?????????????????? ???????????? 5%?????????.")
			elif len_input_money_data == 3:
				tax = input_money_data[2]
			else:
				tax = 5

			price_reg_tax = int(input_money_data[0] * ((100-tax)/100))
			price_real_tax = int(input_money_data[1] * ((100-tax)/100))

			reault_payback = price_reg_tax - price_real_tax
			reault_payback1= price_reg_tax - input_money_data[1]

			embed = discord.Embed(
					title = f"????  ????????? ????????????1 (?????? {tax}% ??????) ",
					description = f"**```fix\n{reault_payback}```**",
					color=0x00ff00
					)
			embed.add_field(name = "?????? ?????????", value = f"```????????? : {input_money_data[0]}\n????????? : {price_reg_tax}\n??? ??? : {input_money_data[0]-price_reg_tax}```")
			embed.add_field(name = "??????? ?????????", value = f"```????????? : {input_money_data[1]}\n????????? : {price_real_tax}\n??? ??? : {input_money_data[1]-price_real_tax}```")
			await ctx.send(embed = embed)

			embed2 = discord.Embed(
					title = f"????  ????????? ????????????2 (?????? {tax}% ??????) ",
					description = f"**```fix\n{reault_payback1}```**",
					color=0x00ff00
					)
			embed2.add_field(name = "?????? ?????????", value = f"```????????? : {input_money_data[0]}\n????????? : {price_reg_tax}\n??? ??? : {input_money_data[0]-price_reg_tax}```")
			embed2.add_field(name = "??????? ?????????", value = f"```????????? : {input_money_data[1]}```")
			return await ctx.send(embed = embed2)
		else:
			return

	@commands.command(name=command[37][0], aliases=command[37][1:])
	async def command_rock_paper_scissors_game(self, ctx : commands.Context):
		if basicSetting[19] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id != basicSetting[7] and ctx.message.channel.id != basicSetting[19]:
			return

		message_rock_paper_scissors : discord.message.Message = await ctx.send("????????? ?????? ????????????..")
		reaction_emoji : list = ["??????", "???", "???"]

		for emoji in reaction_emoji:
			await message_rock_paper_scissors.add_reaction(emoji)

		def reaction_check(reaction, user):
			return (reaction.message.id == message_rock_paper_scissors.id) and (user.id == ctx.author.id) and (str(reaction) in reaction_emoji)
		try:
			reaction_result, user = await self.bot.wait_for('reaction_add', check = reaction_check, timeout = int(basicSetting[5]))
		except asyncio.TimeoutError:
			return await ctx.send(f"????????? ??????????????????. ")
		
		bot_result : str = random.choice(reaction_emoji)
		result_rock_paper_scissors : str = ""
		
		if reaction_result is None:
			result_rock_paper_scissors = f"??? ???????"
		elif str(reaction_result) == bot_result:
			result_rock_paper_scissors = f"??? {bot_result} : {reaction_result} {ctx.author.mention}\n?????????????!"
		elif str(reaction_result) == "??????" and bot_result == "???":
			result_rock_paper_scissors = f"??? {bot_result} : {reaction_result} {ctx.author.mention}\n?????????????"
		elif str(reaction_result) == "???" and bot_result == "??????":
			result_rock_paper_scissors = f"??? {bot_result} : {reaction_result} {ctx.author.mention}\n?????????????"
		elif str(reaction_result) == "???" and bot_result == "???":
			result_rock_paper_scissors = f"??? {bot_result} : {reaction_result} {ctx.author.mention}\n?????????????"
		else:
			result_rock_paper_scissors = f"??? {bot_result} : {reaction_result} {ctx.author.mention}\n??????????.."

		return await ctx.send(result_rock_paper_scissors)

	################ ??????????????? ################ 
	@commands.command(name=command[38][0], aliases=command[38][1:])
	async def command_voice_use(self, ctx : commands.Context):
		if ctx.message.channel.id != basicSetting[7]:
			return

		inidata_voice_use = repo.get_contents("test_setting.ini")
		file_data_voice_use = base64.b64decode(inidata_voice_use.content)
		file_data_voice_use = file_data_voice_use.decode('utf-8')
		inputData_voice_use = file_data_voice_use.split('\n')
		
		for i in range(len(inputData_voice_use)):
			if inputData_voice_use[i].startswith("voice_use ="):
				inputData_voice_use[i] = f"voice_use = 1\r"
				basicSetting[21] = "1"
		
		result_voice_use = '\n'.join(inputData_voice_use)
		
		contents = repo.get_contents("test_setting.ini")
		repo.update_file(contents.path, "test_setting", result_voice_use, contents.sha)

		if basicSetting[6] != "":
			try:
				await self.bot.get_channel(basicSetting[6]).connect(reconnect=True, timeout=5)
			except:
				await ctx.send( '< ???????????? ?????? ??????! >', tts=False)
				pass
			if self.bot.voice_clients[0].is_connected() :
				print("????????? ?????? ?????? ??????!")
				return await ctx.send(f"```???????????? ??????????????? ?????????????????????.!```")

		return await ctx.send(f"```????????? ?????? ????????? ?????? ???????????????!\n< ???????????? ?????? ??? [{command[5][0]}] ????????? ?????? ????????? >```")

	################ ?????????????????? ################ 
	@commands.command(name=command[39][0], aliases=command[39][1:])
	async def command_voice_not_use(self, ctx : commands.Context):
		if ctx.message.channel.id != basicSetting[7]:
			return

		for vc in self.bot.voice_clients:
			if vc.guild.id == int(ctx.guild.id):
				if vc.is_playing():
					vc.stop()
			await vc.disconnect(force=True)

		inidata_voice_use = repo.get_contents("test_setting.ini")
		file_data_voice_use = base64.b64decode(inidata_voice_use.content)
		file_data_voice_use = file_data_voice_use.decode('utf-8')
		inputData_voice_use = file_data_voice_use.split('\n')
		
		for i in range(len(inputData_voice_use)):
			if inputData_voice_use[i].startswith("voice_use ="):
				inputData_voice_use[i] = f"voice_use = 0\r"
				basicSetting[21] = "0"
		
		result_voice_use = '\n'.join(inputData_voice_use)
		
		contents = repo.get_contents("test_setting.ini")
		repo.update_file(contents.path, "test_setting", result_voice_use, contents.sha)
		return await ctx.send(f"```???????????? ???????????? ????????? ?????????????????????.!```")

	################ ???????????? ################ 
	@commands.command(name=command[41][0], aliases=command[41][1:])
	async def command_randombox_game(self, ctx : commands.Context, *, args : str = None):
		if basicSetting[19] != "" and ctx.message.channel.id == basicSetting[7]:
			return

		if ctx.message.channel.id != basicSetting[7] and ctx.message.channel.id != basicSetting[19]:
			return

		if not args:
			return await ctx.send(f'```????????? [????????????] (????????????/???) *(??????) ????????? ?????????????????? ????????????.```')

		memo_data : str = ""
		waiting_time : int = 30

		if args.find("*") == -1:
			input_game_data = args.split()
		else:
			input_game_data = args[:args.find("*")-1].split()
			memo_data = args[args.find("*")+1:]

		try:
			num_cong = int(input_game_data[0])  # ?????? ??????
			if num_cong <= 0:
				return await ctx.send(f'```??????????????? 0?????? ????????? ????????????. ????????? ????????????```')
		except ValueError:
			return await ctx.send('```??????????????? ????????? ?????? ????????????\nex)!???????????? 1```')

		if len(input_game_data) >= 2:
			waiting_time : int = 30
			try:
				waiting_time = int(input_game_data[1])  # ????????????
				if waiting_time <= 0 :
					return await ctx.send(f'```??????????????? 0?????? ????????? ????????????. ????????? ????????????```')
			except ValueError:
				return await ctx.send(f'```????????????(???)??? ????????? ?????? ????????????\nex)!???????????? 1 60```')

		reaction_emoji : list = ["???", "???"]

		embed = discord.Embed(title  = f"???? ????????????! ?????? ????????? ???! (???????????? : {waiting_time}???)", description = f"????????? ???????????? ?????? ??????????????????!", timestamp =datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=int(basicSetting[0])))),
			color=0x00ff00
			)
		if memo_data != "":
			embed.add_field(name = "???? ??????", value =  f"```{memo_data}```", inline=False)

		game_message : discord.message.Message = await ctx.send(embed = embed)

		for emoji in reaction_emoji:
			await game_message.add_reaction(emoji)
		
		cache_msg = await ctx.fetch_message(game_message.id)

		for i in range(waiting_time):
			embed.title = f"???? ????????????! ?????? ????????? ???! (???????????? : {waiting_time - i}???)"			
			await game_message.edit(embed=embed)
			cache_msg = await ctx.fetch_message(game_message.id)
			if cache_msg.reactions[1].count >= 2:
				tmp_users = await cache_msg.reactions[1].users().flatten()
				for user in tmp_users:
					if user.id == ctx.author.id:
						embed.title = f"???? ????????????! ??????! ????"
						embed.description = ""
						await game_message.edit(embed=embed)	
						return await ctx.send(f"```????????? ?????????????????????.!```")
			await asyncio.sleep(1)

		if cache_msg.reactions[0].count == 1:
			embed.title = f"???? ????????????! ?????? ??????! ????"
			embed.description = ""
			await game_message.edit(embed=embed)
			return await ctx.send(f"```???????????? ?????? ????????? ?????????????????????.!```")

		if num_cong >= cache_msg.reactions[0].count-1:
			embed.title = f"???? ????????????! ?????? ??????! ????"
			embed.description = ""
			await game_message.edit(embed=embed)		
			return await ctx.send(f'```??????????????? ??????????????? ????????? ????????????. ????????? ????????????```')

		participant_users = await cache_msg.reactions[0].users().flatten()

		del_index : int = 0
		for i, user in enumerate(participant_users):
			if self.bot.user.id == user.id:
				del_index = i
		del participant_users[del_index]

		user_name_list : list = []
		for user in participant_users:
			user_name_list.append(user.mention)

		for _ in range(num_cong + 5):
			random.shuffle(user_name_list)

		result_users = None
		for _ in range(num_cong + 5):
			result_users = random.sample(user_name_list, num_cong)

		lose_user = list(set(user_name_list)-set(result_users))

		embed.title = f"???? ????????????! ????????????! ????"
		embed.description = ""
		embed.add_field(name = f"???? ????????? ({len(user_name_list)}???)", value =  f"{', '.join(user_name_list)}", inline=False)
		embed.add_field(name = f"???? ?????? ({num_cong}???)", value =  f"{', '.join(result_users)}")
		if len(lose_user) != 0:
			embed.add_field(name = f"???? ?????? ({len(lose_user)}???)", value =  f"{', '.join(lose_user)}")
		return await game_message.edit(embed=embed)

	################ ????????? ################ 
	@commands.command(name=command[43][0], aliases=command[43][1:])
	async def multi_boss_cut(self, ctx, *, args : str = None):
		if ctx.message.channel.id != basicSetting[7]:
			return

		if not args:
			return await ctx.send('```???????????? ????????? ??????????????????```', tts=False)

		boss_data_list : list = args.split("\n")
		boss_data_dict : dict = {}
		result_boss_name : list = []

		for boss_data in boss_data_list:
			tmp_boss_name = boss_data[boss_data.rfind(": ")+1:].strip()
			if tmp_boss_name.find(" ") != -1:
				tmp_boss_name = tmp_boss_name[:tmp_boss_name.find(" ")].strip()
			tmp_boss_time = boss_data[:boss_data.rfind(" : ")].strip()
			try:
				if list(tmp_boss_time).count(":") > 1:
					tmp_hour = int(tmp_boss_time[tmp_boss_time.find(":")-2:tmp_boss_time.find(":")])
					tmp_minute = int(tmp_boss_time[tmp_boss_time.find(":")+1:tmp_boss_time.rfind(":")])
					tmp_second = int(tmp_boss_time[tmp_boss_time.rfind(":")+1:])
				else:
					tmp_hour = int(tmp_boss_time[tmp_boss_time.find(":")-2:tmp_boss_time.find(":")])
					tmp_minute = int(tmp_boss_time[tmp_boss_time.rfind(":")+1:])
					tmp_second = 0
				if tmp_hour > 23 or tmp_hour < 0 or tmp_minute > 60 or tmp_second > 60:
					return await ctx.send(f"**[{tmp_boss_name}]**??? ????????? ??????(00:00:00 ~ 23:59:59)??? ??????????????????.")
			except:
				return await ctx.send(f"**[{tmp_boss_name}]**??? ????????? ??????(00:00:00 ~ 23:59:59)??? ??????????????????. ")

			if "@" != boss_data[0]:
				boss_data_dict[tmp_boss_name] = {"hour" : tmp_hour, "minute" : tmp_minute, "second" : tmp_second}

		for i in range(bossNum):
			if bossData[i][0] in boss_data_dict:
				curr_now = datetime.datetime.now()
				now2 = datetime.datetime.now()
				tmp_now = datetime.datetime.now()
				tmp_now = tmp_now.replace(hour=int(boss_data_dict[bossData[i][0]]["hour"]), minute=int(boss_data_dict[bossData[i][0]]["minute"]), second=int(boss_data_dict[bossData[i][0]]["second"]))
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 0

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))
					
				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							
				tmp_bossTime[i] = bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
				if  curr_now + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < curr_now + datetime.timedelta(minutes=int(basicSetting[3])):
					bossFlag0[i] = True
				if tmp_bossTime[i] < curr_now + datetime.timedelta(minutes=int(basicSetting[1])):
					bossFlag[i] = True
					bossFlag0[i] = True
				result_boss_name.append(bossData[i][0])

		return await ctx.send(f"```[{', '.join(result_boss_name)}] ?????? [?????????]??? ?????????????????????. [{command[22][0]}]?????? ??????????????? ??????????????????```", tts=False)

	################ ???????????? ################ 
	@commands.command(name=command[44][0], aliases=command[44][1:])
	async def multi_boss_predict(self, ctx, *, args : str = None):
		if ctx.message.channel.id != basicSetting[7]:
			return
			
		if not args:
			return await ctx.send('```???????????? ????????? ??????????????????```', tts=False)

		boss_data_list : list = args.split("\n")
		boss_data_dict : dict = {}
		result_boss_name : list = []

		for boss_data in boss_data_list:
			tmp_boss_name = boss_data[boss_data.rfind(": ")+1:].strip()
			if tmp_boss_name.find(" ") != -1:
				tmp_boss_name = tmp_boss_name[:tmp_boss_name.find(" ")].strip()
			tmp_boss_time = boss_data[:boss_data.rfind(" : ")].strip()
			try:
				if list(tmp_boss_time).count(":") > 1:
					tmp_hour = int(tmp_boss_time[tmp_boss_time.find(":")-2:tmp_boss_time.find(":")])
					tmp_minute = int(tmp_boss_time[tmp_boss_time.find(":")+1:tmp_boss_time.rfind(":")])
					tmp_second = int(tmp_boss_time[tmp_boss_time.rfind(":")+1:])
				else:
					tmp_hour = int(tmp_boss_time[tmp_boss_time.find(":")-2:tmp_boss_time.find(":")])
					tmp_minute = int(tmp_boss_time[tmp_boss_time.rfind(":")+1:])
					tmp_second = 0
				if tmp_hour > 23 or tmp_hour < 0 or tmp_minute > 60 or tmp_second > 60:
					return await ctx.send(f"**[{tmp_boss_name}]**??? ????????? ??????(00:00:00 ~ 23:59:59)??? ??????????????????. ")
			except:
				return await ctx.send(f"**[{tmp_boss_name}]**??? ????????? ??????(00:00:00 ~ 23:59:59)??? ??????????????????. ")

			if "@" != boss_data[0]:
				boss_data_dict[tmp_boss_name] = {"hour" : tmp_hour, "minute" : tmp_minute, "second" : tmp_second}

		for i in range(bossNum):
			if bossData[i][0] in boss_data_dict:
				now2 = datetime.datetime.now()
				tmp_now = datetime.datetime.now()
				tmp_now = tmp_now.replace(hour=int(boss_data_dict[bossData[i][0]]["hour"]), minute=int(boss_data_dict[bossData[i][0]]["minute"]), second=int(boss_data_dict[bossData[i][0]]["second"]))
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 0

				if tmp_now < now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(1))
							
				tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

				if  now2 + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < now2 + datetime.timedelta(minutes=int(basicSetting[3])):
					bossFlag0[i] = True
				if tmp_bossTime[i] < now2 + datetime.timedelta(minutes=int(basicSetting[1])):
					bossFlag[i] = True
					bossFlag0[i] = True
				result_boss_name.append(bossData[i][0])

		return await ctx.send(f"```[{', '.join(result_boss_name)}] ?????? [????????????]??? ?????????????????????. [{command[22][0]}]?????? ??????????????? ??????????????????```", tts=False)

	################ ???????????? ################ 
	@commands.command(name=command[45][0], aliases=command[45][1:])
	async def multi_boss_delta_add(self, ctx, *, args : str = None):
		if ctx.message.channel.id != basicSetting[7]:
			return

		if not args:
			return await ctx.send(f"```[{command[45][0]}] [??????(00:00)] [????????????(??????)] [?????????1] [?????????2] [?????????3] ... ???????????? ??????????????????```", tts=False)

		input_data_list : list = []
		input_data_list = args.split()
		result_boss_name : list = []

		if len(input_data_list) < 3:
			return await ctx.send(f"```[{command[45][0]}] [??????(00:00)] [????????????(??????)] [?????????1] [?????????2] [?????????3] ... ???????????? ??????????????????```", tts=False)

		try:
			input_hour = int(input_data_list[0][:input_data_list[0].find(":")])
			input_minute = int(input_data_list[0][input_data_list[0].find(":")+1:])
			input_delta_time = int(input_data_list[1])
		except:
			return await ctx.send(f"?????? ??? ??????????????? ????????? ??????????????????. ")

		boss_name_list : list = input_data_list[2:]

		if input_hour > 23 or input_hour < 0 or input_minute > 60:
			return await ctx.send(f"????????? ??????(00:00:00 ~ 23:59:59)??? ??????????????????.")

		for i in range(bossNum):
			if bossData[i][0] in boss_name_list:
				curr_now = datetime.datetime.now()
				now2 = datetime.datetime.now()
				tmp_now = datetime.datetime.now()
				tmp_now = tmp_now.replace(hour=int(input_hour), minute=int(input_minute), second=0) + datetime.timedelta(hours=int(input_delta_time))
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 0

				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = tmp_now
							
				tmp_bossTime[i] = bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

				if  curr_now + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < curr_now + datetime.timedelta(minutes=int(basicSetting[3])):
					bossFlag0[i] = True
				if tmp_bossTime[i] < curr_now + datetime.timedelta(minutes=int(basicSetting[1])):
					bossFlag[i] = True
					bossFlag0[i] = True
				result_boss_name.append(bossData[i][0])
					
		return await ctx.send(f"```[{', '.join(list(result_boss_name))}] ?????? [????????????]??? ?????????????????????. [{command[27][0]}]?????? ??????????????? ??????????????????```", tts=False)

	################ ?????????????? ################ 
	@commands.command(name='!??????')
	async def brother1_(self, ctx):
		if basicSetting[21] != "1":
			return await ctx.send('```???????????? ???????????? ????????? ???????????? ????????????.```', tts=False)
		return await PlaySound(ctx.voice_client, './sound/??????.mp3')

	@commands.command(name='!??????')
	async def sister_(self, ctx):
		if basicSetting[21] != "1":
			return await ctx.send('```???????????? ???????????? ????????? ???????????? ????????????.```', tts=False)
		return await PlaySound(ctx.voice_client, './sound/??????.mp3')

	@commands.command(name='!???')
	async def brother2_(self, ctx):
		if basicSetting[21] != "1":
			return await ctx.send('```???????????? ???????????? ????????? ???????????? ????????????.```', tts=False)
		return await PlaySound(ctx.voice_client, './sound/???.mp3')
	
	@commands.command(name='!TJ', aliases=['!tj'])
	async def TJ_(self, ctx):
		if basicSetting[21] != "1":
			return await ctx.send('```???????????? ???????????? ????????? ???????????? ????????????.```', tts=False)
		resultTJ = random.randrange(1,9)
		return await PlaySound(ctx.voice_client, './sound/TJ' + str(resultTJ) +'.mp3')

class IlsangDistributionBot(commands.AutoShardedBot):
	def __init__(self):
		super().__init__(command_prefix=[""], help_command=None)

	def run(self):
		super().run(access_token, reconnect=True)

	async def on_ready(self):
		global basicSetting

		global channel
	
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global chkvoicechannel
		global chflg
		
		global endTime
		global setting_channel_name
				
		print("Logged in as ") #????????? ?????? ?????????, ???????????? ???????????????.
		print(self.user.name)
		print(self.user.id)
		print("===========")

		channel_name, channel_id, channel_voice_name, channel_voice_id = await get_guild_channel_info(self)

		await dbLoad()

		if str(basicSetting[7]) in channel_id:

			channel = basicSetting[7]

			setting_channel_name = self.get_channel(basicSetting[7]).name

			now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

			print('< ???????????? [' + now.strftime('%Y-%m-%d ') + now.strftime('%H:%M:%S') + '] >')
			print('< ??????????????? [' + self.get_channel(basicSetting[7]).name + '] ????????????>')
			if basicSetting[21] == "1" and str(basicSetting[6]) in channel_voice_id:
				try:
					await self.get_channel(basicSetting[6]).connect(reconnect=True, timeout=5)
					print('< ???????????? [' + self.get_channel(basicSetting[6]).name + '] ???????????? >')
				except:
					print('< ???????????? [' + self.get_channel(basicSetting[6]).name + '] ???????????? >')
					pass			
			elif basicSetting[21] == "1" and str(basicSetting[6]) not in channel_voice_id:
				print(f"????????? ???????????? ?????? ????????? ?????? ????????????. ???????????? ?????? ??? **[{command[5][0]}]** ????????? ?????? ???????????? ?????????????????? ????????????.")
				await self.get_channel(int(basicSetting[7])).send(f"????????? ???????????? ?????? ????????? ?????? ????????????. ???????????? ?????? ??? **[{command[5][0]}]** ????????? ?????? ???????????? ?????????????????? ????????????.")
			if basicSetting[8] != "":
				if str(basicSetting[8]) in channel_id:
					print('< ??????????????? [' + self.get_channel(int(basicSetting[8])).name + '] ???????????? >')
				else:
					basicSetting[8] = ""
					print(f"??????????????? ID ??????! [{command[28][0]} ?????????] ???????????? ????????? ????????????.")
			if basicSetting[11] != "":
				if str(basicSetting[11]) in channel_id:
					print('< ???????????? [' + self.get_channel(int(basicSetting[11])).name + '] ????????????>')
				else:
					basicSetting[11] = ""
					print(f"???????????? ID ??????! [{command[28][0]} ??????] ???????????? ????????? ????????????.")
			if basicSetting[18] != "":
				if str(basicSetting[18]) in channel_id:
					print('< ???????????? [' + self.get_channel(int(basicSetting[18])).name + '] ????????????>')
				else:
					basicSetting[18] = ""
					print(f"???????????? ID ??????! [{command[28][0]} ??????] ???????????? ????????? ????????????.")
			if basicSetting[19] != "":
				if str(basicSetting[19]) in channel_id:
					print('< ???????????? [' + self.get_channel(int(basicSetting[19])).name + '] ????????????>')
				else:
					basicSetting[19] = ""
					print(f"???????????? ID ??????! [{command[28][0]} ??????] ???????????? ????????? ????????????.")
			if basicSetting[20] != "":
				if str(basicSetting[20]) in channel_id:
					print('< ??????????????? [' + self.get_channel(int(basicSetting[20])).name + '] ????????????>')
				else:
					basicSetting[20] = ""
					print(f"??????????????? ID ??????! [{command[28][0]} ?????????] ???????????? ????????? ????????????.")
			if int(basicSetting[13]) != 0 :
				print('< ????????? ????????? ?????? ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + ' >')
				print('< ????????? ????????? ?????? ' + basicSetting[13] + '??? >')
			else :
				print('< ????????? ????????? ???????????? >')
			chflg = 1
		else:
			basicSetting[6] = ""
			basicSetting[7] = ""
			print(f"????????? ?????? ?????? ????????? ?????? ????????????. **[{command[0][0]}]** ????????? ?????? ???????????? ?????????????????? ????????????.")

		# ?????????????????? ?????? ????????? ?????? ????????? ?????????????????? ???????????? ????????? ????????????.
		# ??? ????????? ???????????? ?????? ????????? ???????????? ???????????? ??? ????????????.
		await self.change_presence(status=discord.Status.online, activity=discord.Game(name=command[1][0], type=1), afk=False)

	async def on_message(self, msg):
		await self.wait_until_ready()
		if msg.author.bot: #?????? ???????????? ??????????????? ?????? ????????????
			return None #???????????? ?????? ???????????????.

		ori_msg = msg

		global channel
		
		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global chflg
		global LoadChk
		
		global indexFixedBossname
		global FixedBossDateData
		
		global gc #??????
		global credentials	#??????

		global regenembed
		global command
		global kill_Data
		
		id = msg.author.id #id?????? ???????????? ???????????? ??????????????? ID??? ????????????.
		
		if chflg == 1 :
			if self.get_channel(basicSetting[7]).id == msg.channel.id:
				channel = basicSetting[7]
				message = msg

				for command_str in ["END", "end", "SKIP", "?????????", "?????????", "????????????", "??????", "??????","??????", "??????", "???"]:
					if command_str in message.content:
						tmp_msg : str = ""
						for key, value in boss_nick.items():
							if message.content[:message.content.find(command_str)].strip() in value:
								message.content = message.content.replace(message.content[:message.content.find(command_str)], key)

				hello = message.content

				for i in range(bossNum):
					################ ?????? ????????? ################ 
					if message.content.upper().startswith(bossData[i][0] +'END') or message.content.upper().startswith(bossData[i][0] +' END') or message.content.startswith(bossData[i][0] +'?????????') or message.content.startswith(bossData[i][0] +' ?????????') or message.content.startswith(bossData[i][0] +'?????????') or message.content.startswith(bossData[i][0] +' ?????????') or message.content.startswith(bossData[i][0] +'???'):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''

						curr_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_msg = bossData[i][0] +'END'
						if len(hello) > len(tmp_msg) + 3 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = now2

						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0

						if tmp_now > now2 :
							tmp_now = tmp_now + datetime.timedelta(days=int(-1))
							
						if tmp_now < now2 : 
							deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							while now2 > tmp_now :
								tmp_now = tmp_now + deltaTime
								bossMungCnt[i] = bossMungCnt[i] + 1
							now2 = tmp_now
							bossMungCnt[i] = bossMungCnt[i] - 1
						else :
							now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
									
						tmp_bossTime[i] = bossTime[i] = nextTime = now2
						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

						if  curr_now + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < curr_now + datetime.timedelta(minutes=int(basicSetting[3])):
							bossFlag0[i] = True
						if tmp_bossTime[i] < curr_now + datetime.timedelta(minutes=int(basicSetting[1])):
							bossFlag[i] = True
							bossFlag0[i] = True

						embed = discord.Embed(
								description= '```'+ bossData[i][0] + ' ???????????????' + bossTimeString[i] + '?????????```',
								color=0xff0000
								)
						await self.get_channel(channel).send(embed=embed, tts=False)

					################ ????????????????????? ################ 

					if message.content.startswith(bossData[i][0] +'????????????') or message.content.startswith(bossData[i][0] +' ????????????') or message.content.startswith(bossData[i][0] +'SKIP') or message.content.startswith(bossData[i][0] +' SKIP'):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''
							
						tmp_msg = bossData[i][0] +'????????????'
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

						if len(hello) > len(tmp_msg) + 3 :
							temptime = tmp_now
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos] 
								minutes1 = hello[chkpos+1:chkpos+3]					
								temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]					
								temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							
							bossMungCnt[i] = 0
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False

							if temptime > tmp_now :
								temptime = temptime + datetime.timedelta(days=int(-1))

							if temptime < tmp_now :
								deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								while temptime < tmp_now :
									temptime = temptime + deltaTime
									bossMungCnt[i] = bossMungCnt[i] + 1

							tmp_bossTime[i] = bossTime[i] = temptime				
							tmp_bossTimeString[i] = bossTimeString[i] = temptime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = temptime.strftime('%Y-%m-%d')
							if  tmp_now + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < tmp_now + datetime.timedelta(minutes=int(basicSetting[3])):
								bossFlag0[i] = True
							if tmp_bossTime[i] < tmp_now + datetime.timedelta(minutes=int(basicSetting[1])):
								bossFlag[i] = True
								bossFlag0[i] = True

							embed = discord.Embed(
									description= '```'+ bossData[i][0] + ' ?????????????????????' + bossTimeString[i] + '?????????```',
									color=0xff0000
									)
							await self.get_channel(channel).send(embed=embed, tts=False)
						else:
							if tmp_bossTime[i] < tmp_now :

								nextTime = tmp_bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1

								tmp_bossTime[i] = bossTime[i] = nextTime				
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								if  tmp_now + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < tmp_now + datetime.timedelta(minutes=int(basicSetting[3])):
									bossFlag0[i] = True
								if tmp_bossTime[i] < tmp_now + datetime.timedelta(minutes=int(basicSetting[1])):
									bossFlag[i] = True
									bossFlag0[i] = True

								embed = discord.Embed(
									description= '```'+ bossData[i][0] + ' ?????????????????????' + bossTimeString[i] + '?????????```',
										color=0xff0000
										)
								await self.get_channel(channel).send(embed=embed, tts=False)
							else:
								await self.get_channel(channel).send('```' + bossData[i][0] + '????????????????????????????????????. ?????? ' + bossData[i][0] + '????????? [' + tmp_bossTimeString[i] + '] ?????????```', tts=False)

						
				################ ?????? ?????? ?????? ?????? ################ 

					if message.content.startswith(bossData[i][0] +'??????')  or message.content.startswith(bossData[i][0] +' ??????'):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''
							
						tmp_msg = bossData[i][0] +'??????'
						if len(hello) > len(tmp_msg) + 4 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = 0

							if tmp_now < now2 :
								tmp_now = tmp_now + datetime.timedelta(days=int(1))

							tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							if  now2 + datetime.timedelta(minutes=int(basicSetting[1])) <= tmp_bossTime[i] < now2 + datetime.timedelta(minutes=int(basicSetting[3])):
								bossFlag0[i] = True
							if tmp_bossTime[i] < now2 + datetime.timedelta(minutes=int(basicSetting[1])):
								bossFlag[i] = True
								bossFlag0[i] = True		
									
							embed = discord.Embed(
									description= '```'+ bossData[i][0] + '??????????????????' + bossTimeString[i] + '?????????```',
									color=0xff0000
									)
							await self.get_channel(channel).send(embed=embed, tts=False)
						else:
							await self.get_channel(channel).send('```' + bossData[i][0] +'?????????????????????????????????????????????```', tts=False)
							
					################ ???????????? ?????? ################
						
					if message.content == bossData[i][0] +'DEL' or message.content == bossData[i][0] +' DEL':
						bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
						tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
						bossTimeString[i] = '99:99:99'
						bossDateString[i] = '9999-99-99'
						tmp_bossTimeString[i] = '99:99:99'
						tmp_bossDateString[i] = '9999-99-99'
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0
						await self.get_channel(channel).send('<' + bossData[i][0] + '????????????????????????????????????>', tts=False)
						await dbSave()
						print ('<' + bossData[i][0] + '????????????????????????????????????>')
					
					################ ???????????? ?????? ################ 

					if message.content.startswith(bossData[i][0] +'???????????? '):
						
						tmp_msg = bossData[i][0] +'???????????? '
						
						bossData[i][6] = hello[len(tmp_msg):]
						await self.get_channel(channel).send('< ' + bossData[i][0] + ' [ ' + bossData[i][6] + ' ] ????????????????????????>', tts=False)
						
					if message.content.startswith(bossData[i][0] +'????????????'):
						
						bossData[i][6] = ''
						await self.get_channel(channel).send('< ' + bossData[i][0] + ' ????????????????????????>', tts=False)

		await self.process_commands(ori_msg)

	async def on_command_error(self, ctx : commands.Context, error : commands.CommandError):
		if isinstance(error, CommandNotFound):
			return
		elif isinstance(error, MissingRequiredArgument):
			return
		elif isinstance(error, discord.ext.commands.MissingPermissions):
			return await ctx.send(f"**[{ctx.message.content.split()[0]}]** ????????????????????????")
		elif isinstance(error, discord.ext.commands.CheckFailure):
			return await ctx.send(f"**[{ctx.message.content.split()[0]}]** ????????????????????????")
		raise error

	async def close(self):
		await super().close()
		print("BossTimeBot Finish.")

ilsang_distribution_bot : IlsangDistributionBot = IlsangDistributionBot()
ilsang_distribution_bot.add_cog(mainCog(ilsang_distribution_bot))
ilsang_distribution_bot.add_cog(taskCog(ilsang_distribution_bot))
ilsang_distribution_bot.run()
