import requests
import json
import logging
import pickle
import os
import datetime
import configparser

APIURL = 'https://api.mgid.com/v1'

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)  # w - перезаписывает файл.
fh = logging.FileHandler("logs.log", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

#Authenticate and get 'token', 'refreshToken', 'idAuth'. Returns in dict
def auth():
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	payload = {
		"email": EMAIL,
		"password": PASSWORD
	}
	try:
		response = requests.post(f'{APIURL}/auth/token', headers=headers, data=json.dumps(payload))
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			log.error(f'Response code error: {response.status_code}')
	except Exception as e:
		log.critical(f'Auth query error: {e}')

#Get specific campaign info if camp_id is provided or return all user campaigns. Returns in dict
def user_campaigns(camp_id=None):
	headers = {
		'Accept': 'application/json'
	}
	if camp_id is not None:
		url = f"{APIURL}/goodhits/clients/{auth()['idAuth']}/campaigns/{camp_id}?token={auth()['token']}"

		try:
			response = requests.get(url, headers=headers)
			if response.status_code == requests.codes.ok:
				return response.json()
			else:
				log.error(f'user_campaigns(camp_id): {response.status_code}')
		except Exception as e:
			log.critical(f'user_campaigns(camp_id): {e}')

	if camp_id is None:
		url = f"{APIURL}/goodhits/clients/{auth()['idAuth']}/campaigns/?token={auth()['token']}"
		try:
			response = requests.get(url, headers=headers)
			if response.status_code == requests.codes.ok:
				return response.json()
			else:
				log.error(f'user_campaigns(): {response.status_code}')
		except Exception as e:
			log.critical(f'user_campaigns(): {e}')

#Get specific ACTIVE teaser info if teaser_id is provided or return all user teasers. Returns in dict
def user_teasers(campaign=None, teaser_id=None):
	headers = {
		'Accept': 'application/json'
	}
	status = "&status=['active']"
	if campaign is None:
		if teaser_id is not None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
					/teasers/{teaser_id}?token={auth()['token']}{status}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(teaser_id): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(id): {e}')

		if teaser_id is None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
					/teasers/?token=auth()['token']{status}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(None): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(None): {e}')
	else:
		if teaser_id is not None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
					/teasers/{teaser_id}?token={auth()['token']}&campaign={campaign}{status}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(teaser_id): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(id): {e}')

		if teaser_id is None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
					/teasers/?token={auth()['token']}&campaign={campaign}{status}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(None): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(None): {e}')

#Exclude site from campaign and print result
def disable_sites(uid, camp_id):
	try:
		response = requests.patch(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
			/campaigns/{camp_id}?token={auth()['token']}&widgetsFilterUid=exclude,only,{uid}")
		if response.status_code == requests.codes.ok:
			response = response.json()
			if 'id' in response:
				if response['id'] == camp_id:
					log.info(f'Site {uid} disabled in campaign {camp_id}')
				else:
					log.warning(f"Site {uid} in {camp_id} isn't disabled: {response}")
			elif 'errors' in response:
				error = response['errors'][0]
				if error == '[ERROR_CURRENT_FILTER_TYPE_DIFFERENT_FIRST_SEND_OFF_FOR_FILTER_THAN_SEND_NEW_FILTER_TYPE]':
					response = requests.patch(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
							/campaigns/{camp_id}?token={auth()['token']}&widgetsFilterUid=exclude,except,{uid}")
					if response.status_code == requests.codes.ok:
						response = response.json()
						if 'id' in response:
							if response['id'] == camp_id:
								log.info(f'Site {uid} disabled in campaign {camp_id}')
							else:
								log.warning(f"Site {uid} in {camp_id} isn't disabled: {response}")
			else:
				log.error(f'disable sites: no id or errors in resp - {response}')
		else:
			log.error(f'disable_sites: {response.status_code}')
	except Exception as e:
		log.critical(f'disable_sites: {e}')

#Get campaigns statistics by sites include conversions. Returns in dict
def site_stats(camp_id, uid=None, dateinterval=None):
	headers = {
		'Accept': 'application/json'
	}
	if uid is None:
		if dateinterval is None:
			try:
				response = requests.get(f"{APIURL}/goodhits/campaigns/{camp_id} \
					/quality-analysis/?token={auth()['token']}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'site_stats(): {response.status_code}')
			except Exception as e:
				log.critical(f'site_stats(): {e}')
		else:
			try:
				response = requests.get(f"{APIURL}/goodhits/campaigns/{camp_id} \
					/quality-analysis/?token={auth()['token']}&dateInterval={dateinterval}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'site_stats(date): {response.status_code}')
			except Exception as e:
				log.critical(f'site_stats(date): {e}')

	else:
		if dateinterval is None:
			try:
				response = requests.get(f"{APIURL}/goodhits/campaigns/{camp_id} \
					/quality-analysis/{uid}?token={auth()['token']}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'site_stats(uid): {response.status_code}')
			except Exception as e:
				log.critical(f'site_stats(uid): {e}')
		else:
			try:
				response = requests.get(f"{APIURL}/goodhits/campaigns/{camp_id} \
					/quality-analysis/{uid}?token={auth()['token']} \
					&dateInterval={dateinterval}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'site_stats(uid,date): {response.status_code}')
			except Exception as e:
				log.critical(f'site_stats(uid,date): {e}')

# Проверяем сайты по заданным параметрам. Принимает словарь со статистикой по площадкам и доход конверсии
def check_sites(stat):
	# Отформатированный список без camp id и даты
	camp_id = list(stat.keys())[0]
	f_stat = stat[camp_id]
	f_stat = f_stat[list(f_stat.keys())[0]]
	#log.debug(f_stat)
	if len(f_stat) > 0:
		for key, value in f_stat.items():
			# Если есть вложеные площадки - проходим по ним
			if len(value['sources']) > 0:
				sources = value['sources']
				for key1, value1 in sources.items():
					if 'spent' in value1:
						if value1['spent'] > 10 and ('buy' and 'decision' not in value1):
							log.info(f'{camp_id} Site {key}s{key1} (spent {value1["spent"]} and leads not found) is ready to disable')
							disable_sites(f"{key}s{key1}", camp_id)
			if 'spent' in value:
				if value['spent'] > 10 and ('buy' and 'decision' not in value):
					log.info(f'{camp_id} Site {key} (spent {value["spent"]} and leads not found) is ready to disable')
					disable_sites(f"{key}", camp_id)

# Проверка тизеров по условиям. Принимает словарь тизеров от user_teasers.
def check_teasers(tsrs, profit, camp_id):
	highest_conv = 0
	highest_roi = -10
	highest_id = 0
	file = f'{camp_id}.data'
	# Если файла с названием РК нет -
	# - создаем и записываем туда словарь тизеров с ключом даты у каждого тизера
	if not os.path.exists(file):
		try:
			dict_todump = tsrs.copy()
			for key, value in dict_todump.items():
				value['date'] = datetime.datetime.today().strftime('%Y.%m.%d-%H:%M')
			with open(file, 'wb') as f:
				pickle.dump(dict_todump, f)
			del dict_todump
			log.debug(f'Успешно загружен в .data')
		except Exception as e:
			log.error(f'Dict dump: {e}')
	else:
		try:
			# Загружаем в словарь данные из файла
			with open(file, 'rb') as f:
				dict_fromdump = pickle.load(f)
			nowtime = datetime.datetime.now()
			# По каждому тизеру из старых данных проверяем
			for key, value in dict_fromdump.items():
				try:
					oldtime = datetime.datetime.strptime(value['date'], '%Y.%m.%d-%H:%M')
					delta = nowtime - oldtime
					log.debug(f'Delta {delta} = nowtime {nowtime} - oldtime {oldtime}')
					log.debug(f'Min Delta {delta.seconds // 60}')
					log.debug(f'Daya delta {delta.days}')  # Может быть здесь будет 3.5 - тогда исп-ть ее
					if delta.days > 3:
						log.debug('ПРОШЛО 4 ДНЯ')
						# По каждому тизеру из нынешних данных проверяем
						for key1, value1 in tsrs.items():
							# Находим разницу в конверсиях и тратах
							conv = value1['conversion']['buying_all'] - value['conversion']['buying_all']
							spent = value1['statistics']['spent'] - value['statistics']['spent']
							roi = (conv * profit - spent) / spent * 100
							#log.debug()
							if conv > highest_conv and roi > highest_roi:
								highest_conv = conv
								highest_roi = roi
								highest_id = value1['id']
							log.debug(f'(conv {conv} * profit {profit} - spent {spent}) / spent {spent} * 100 = {roi}')
						log.debug(f'{highest_conv} / {highest_roi} / {highest_id}')
						if highest_conv > 1:  # TODO Изменить 1 на нужное число
							# TODO Присваивать не только первое значение? Или среднее? Или страны будут только одни?
							current_cpc = tsrs[highest_id]['priceOfClickByLocations'][0]['priceOfClick']
							# Изменяем CPC. По стандарту на +0.5
							change_cpc(highest_id, current_cpc)
							# Удаляем старый файл
							if os.path.isfile(file):
								os.remove(file)
							else:
								log.error(f"{file} file not found for remove")
					else:
						log.debug('3.5 дня не прошло')
						break

				except Exception as e:
					log.error(f'dict_fromdump: {e}')
		except Exception as e:
			log.error(f'Dict load: {e}')

	for key, value in tsrs.items():
		# CTR TASK 1
		if value['statistics']['hits'] > 10000 and \
			value['statistics']['clicks'] > 100 and float(value['statistics']['ctr']) < 0.2:
			# DEBUGOFF ВКЛЮЧИТЬ ПРИ УСТАНОВКЕ
			#disable_teaser(key)
			log.debug(f'TEASER IS READY TO DISABLE(CTR TASK 1): {key}')
		# CLICKS TASK 1
		if value['statistics']['clicks'] > 100 and value['conversion']['buying_all'] == 0:
			# DEBUGOFF ВКЛЮЧИТЬ ПРИ УСТАНОВКЕ
			# disable_teaser(key)
			log.debug(f'TEASER IS READY TO DISABLE(CLICK TASK 1): {key}')

# Отключение тизера
def disable_teaser(tsr_id):
	try:
		response = requests.patch(f"{APIURL}/goodhits/clients/{auth()['idAuth']}/teasers/{tsr_id} \
			?token={auth()['token']}&whetherToBlockByClient=1")
		if response.status_code == requests.codes.ok:
			response = response.json()
			if response['id'] == tsr_id:
				log.info(f'Teaser {tsr_id} disabled')
			else:
				log.warning(f'action_teaser: {response}')
		else:
			log.error(f'action_teaser: {response.status_code}')

	except Exception as e:
		log.critical(f'action_teaser: {e}')

# Изменение цены за клик для тизера
def change_cpc(tsr_id, value, rate=0.5):
	try:
		response = requests.patch(f"{APIURL}/goodhits/clients/{auth()['idAuth']}\
		/teasers/{tsr_id}?token={auth()['token']}&priceOfClickByLocation={value + rate}")
		if response.status_code == requests.codes.ok:
			response = response.json()
			if response['id'] == tsr_id:
				log.info(f'Changed teaser {tsr_id} cpc {value} to {value + rate}')
			else:
				log.warning(f'change_cpc response: {response}')
		else:
			log.error(f'change_cpc: {response.status_code}')
	except Exception as e:
		log.critical(f'change_cpc: {e}')

if __name__ == '__main__':
	config = configparser.ConfigParser()
	if os.path.isfile('config.ini'):
		config.read('config.ini')
	else:
		log.critical('Config file (config.ini) not found')
	EMAIL = config['MGID']['email']
	PASSWORD = config['MGID']['password']
	log.info('Started')
	camplist = [582530, 585341, 584125, 584873, 584949, 584983, 585301, 585331, 585373, 587915, 587943]
	try:
		while True:
			for camp in camplist:
				log.debug(f'for in {camp}')
				check_sites(site_stats(camp))
	except Exception as err:
		log.critical(f'Main proccess error: {err}')
	finally:
		log.info('Finished')
	#log.debug(site_stats(584125))
	#log.debug(f'{user_teasers(582530)}')
	#check_teasers(user_teasers(582530), 6, 582530)


# TODO Функция проверки хороших площадок
# TODO Функция увеличения коэф. хороших площадок
# TODO Функция отслеживания изменений по хорошим площадкам \
#  - записали значения до увеличения коэфа и сравнили их через неделю
