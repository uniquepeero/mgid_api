import requests
import json
import logging
import pickle
import os
import datetime

APIURL = 'https://api.mgid.com/v1'

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # w - перезаписывает файл. DEBUGOFF Удалить w при установке и повысить до INFO
fh = logging.FileHandler("logs.log", "w", "utf-8")
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
		"email": "advertcombo@gmail.com",
		"password": "letsbombnatiVE05"
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
			if response['id'] == camp_id:
				log.info(f'Site {uid} disabled in campaign {camp_id}')
			else:
				log.warning(f"Site {uid} in {camp_id} isn't disabled: {response}")
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
def check_sites(stat, profit=None):
	# Отформатированный список без camp id и даты
	f_stat = stat[list(stat.keys())[0]]
	f_stat = f_stat[list(f_stat.keys())[0]]
	log.debug(f_stat)
	#for key, value in f_stat:
	# Здесь нужно проверять наличие вложенных площадок и если они есть - в начале проходить циклом по ним
	# В циклах проверяем каждую площадку по прописанным условиям

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
					if (delta.seconds // 60) > 5040:
						log.debug('ПРОШЛО 3.5 ДНЯ')
						# По каждому тизеру из нынешних данных проверяем
						for key1, value1 in tsrs.items():
							# Находим разницу в конверсиях и тратах
							conv = value1['conversion']['buying_all'] - value['conversion']['buying_all']
							spent = value1['statistics']['spent'] - value['statistics']['spent']
							roi = (conv * profit - spent) / spent * 100
							if conv > highest_conv and roi > highest_roi:
								highest_conv = conv
								highest_roi = roi
								highest_id = value1['id']
							log.debug(f'(conv {conv} * profit {profit} - spent {spent}) / spent {spent} * 100 = {roi}')
						log.debug(f'{highest_conv} / {highest_roi} / {highest_id}')
						if highest_conv > 1:  # TODO Изменить 1 на нужное число
							# TODO Функция увеличения CPC тизера на определенное значение
							# TODO Удаление старого .data файла
							log.info(f'CPC Тизера {highest_id} увеличено на ')
							pass
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

#Запись
# time.strftime('%Y%m%d%H%M)
def store_data(name, time, cnv, roi, obj):
	name = f'{name}.data'

	if not os.path.exists(name):
		with open(name, 'rb') as f:
			pickle.dump(obj, f)

# Проверка тизеров по конкретным данным за определенный период
#def watch_teasers(tsrs):
	# Записываем данные наблюдаемых тизеров в файл в виде словаря. Дата - тизеры - их данные
	# Достаем из файла данные по тизерам. Проверяем текующую дату, если прошло 84 часа (3.5 дня) - повышаем ставку
	#pass

if __name__ == '__main__':
	# check_sites(site_stats(582530))

	log.debug('Started')
	check_teasers(user_teasers(582530), 5.97, 582530)
	#log.debug(f'{user_teasers(582530)}')
	#store_data()
	log.debug('Finished')


# TODO Функция проверки сайтов по заданным параметрам - check_sites
# TODO Функция проверки хороших площадок
# TODO Функция увеличения коэф. хороших площадок
# TODO Функция отслеживания изменений по хорошим площадкам \
#  - записали значения до увеличения коэфа и сравнили их через неделю
