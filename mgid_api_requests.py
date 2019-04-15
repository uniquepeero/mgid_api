import requests
import json
import logging

APIURL = 'https://api.mgid.com/v1'

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs.log", "w", "utf-8")  # w - перезаписывает файл. TODO Удалить при установке
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
		log.critical(f'Auth query error: {e} - {response.status_code}')

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
			log.critical(f'user_campaigns(camp_id): {e} - {response.status_code}')

	if camp_id is None:
		url = f"{APIURL}/goodhits/clients/{auth()['idAuth']}/campaigns/?token={auth()['token']}"
		try:
			response = requests.get(url, headers=headers)
			if response.status_code == requests.codes.ok:
				return response.json()
			else:
				log.error(f'user_campaigns(): {response.status_code}')
		except Exception as e:
			log.critical(f'user_campaigns(): {e} - {response.status_code}')

#Get specific teaser info if teaser_id is provided or return all user teasers. Returns in dict
def user_teasers(campaign=None, teaser_id=None):
	headers = {
		'Accept': 'application/json'
	}
	if campaign is None:
		if teaser_id is not None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
				/teasers/{teaser_id}?token={auth()['token']}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(teaser_id): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(id): {e} - {response.status_code}')

		if teaser_id is None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
					/teasers/?token=auth()['token']", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(None): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(None): {e} - {response.status_code}')
	else:
		if teaser_id is not None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
				/teasers/{teaser_id}?token={auth()['token']}&campaign={campaign}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(teaser_id): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(id): {e} - {response.status_code}')

		if teaser_id is None:
			try:
				response = requests.get(f"{APIURL}/goodhits/clients/{auth()['idAuth']} \
					/teasers/?token={auth()['token']}&campaign={campaign}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'user_teasers(None): {response.status_code}')
			except Exception as e:
				log.critical(f'user_teasers(None): {e} - {response.status_code}')

#Exclude site from campaign and print result
def disable_sites(uid, camp_id):
	try:
		response = requests.patch(f"{APIURL}/goodhits/clients/auth()['idAuth'] \
			/campaigns/{camp_id}?token={auth()['token']}&widgetsFilterUid=exclude,only,{uid}")
		if response.status_code == requests.codes.ok:
			response = response.json()
			if response['id'] == camp_id:
				log.info(f'Site {uid} disabled in campaign {camp_id}')
			else:
				log.warning(f"Site isn't disabled: {response}")
		else:
			log.error(f'disable_sites: {response.status_code}')
	except Exception as e:
		log.critical(f'disable_sites: {e} - {response.status_code}')

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
				log.critical(f'site_stats(): {e} - {response.status_code}')
		else:
			try:
				response = requests.get(f"{APIURL}/goodhits/campaigns/{camp_id} \
					/quality-analysis/?token={auth()['token']}&dateInterval={dateinterval}", headers=headers)
				if response.status_code == requests.codes.ok:
					return response.json()
				else:
					log.error(f'site_stats(date): {response.status_code}')
			except Exception as e:
				log.critical(f'site_stats(date): {e} - {response.status_code}')

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
				log.critical(f'site_stats(uid): {e} - {response.status_code}')
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
				log.critical(f'site_stats(uid,date): {e} - {response.status_code}')

# Проверяем сайты по заданным параметрам. Принимает словарь со статистикой по площадкам и доход конверсии
def check_sites(stat, profit=None):
	# Отформатированный список без camp id и даты
	f_stat = stat[list(stat.keys())[0]]
	f_stat = f_stat[list(f_stat.keys())[0]]
	log.debug(f_stat)
	# for key, value in f_stat:
	# Здесь нужно проверять наличие вложенных площадок и если они есть - в начале проходить циклом по ним
	# В циклах проверяем каждую площадку по прописанным условиям


check_sites(site_stats(582530))
#log.debug(f'{user_teasers(582530)}')

# TODO Функция проверки сайтов по заданным параметрам - check_sites
# TODO Функция проверки хороших площадок
# TODO Функция увеличения коэф. хороших площадок
# TODO Функция отслеживания изменений по хорошим площадкам \
#  - записали значения до увеличения коэфа и сравнили их через неделю
