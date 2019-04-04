import requests
import json

APIURL = 'https://api.mgid.com/v1'

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
	response = requests.post(f'{APIURL}/auth/token', headers=headers, data=json.dumps(payload))
	if response.status_code == 200:
		return response.json()
	else:
		print('auth(): ' + str(response.status_code))

#Get specific campaign info if camp_id is provided or return all user campaigns. Returns in dict
def user_campaigns(camp_id=None):
	headers = {
		'Accept': 'application/json'
	}
	if camp_id is not None:
		url = f'''{APIURL}/goodhits/clients/{auth()['idAuth']}/campaigns/{camp_id}?token={auth()['token']}'''
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			print('user_campaigns(camp_id): ' + str(response.status_code))

	if camp_id is None:
		url = f'''{APIURL}/goodhits/clients/{auth()['idAuth']}/campaigns/?token={auth()['token']}'''
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			print('user_campaigns(None): ' + str(response.status_code))

#Get specific teaser info if teaser_id is provided or return all user teasers. Returns in dict
def user_teasers(teaser_id=None):
	headers = {
		'Accept': 'application/json'
	}
	if teaser_id is not None:
		response = requests.get(f'''{APIURL}/goodhits/clients/{auth()['idAuth']} \
			/teasers/{teaser_id}?token={auth()['token']}''', headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			print('user_teasers(teaser_id): ' + str(response.status_code))

	if teaser_id is None:
		response = requests.get(f'''{APIURL}/goodhits/clients/{auth()['idAuth']} \
			/teasers/?token=auth()['token']''', headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			print('user_teasers(None): ' + str(response.status_code))

#Exclude site from campaign and print result
def disable_sites(uid, camp_id):
	response = requests.patch(f'''{APIURL}/goodhits/clients/auth()['idAuth'] \
		/campaigns/{camp_id}?token={auth()['token']}&widgetsFilterUid=exclude,only,{uid}''').json()
	if response['id'] == camp_id:
		print('Site ' + str(uid) + 'disabled in campaign ' + str(camp_id))
	else:
		print(response)

#Get campaigns statistics by sites include conversions. Returns in dict
def site_stats(camp_id, uid=None, dateinterval=None):
	headers = {
		'Accept': 'application/json'
	}
	if uid is None:
		if dateinterval is None:

			response = requests.get(f'''{APIURL}/goodhits/campaigns/{camp_id} \
				/quality-analysis/?token={auth()['token']}''', headers=headers)
			if response.status_code == 200:
				return response.json()
			else:
				print('Site Stats: ' + str(response.status_code))
		else:
			response = requests.get(f'''{APIURL}/goodhits/campaigns/{camp_id} \
				/quality-analysis/?token={auth()['token']}&dateInterval={dateinterval}''', headers=headers)
			if response.status_code == 200:
				return response.json()
			else:
				print('Site Stats: ' + str(response.status_code))

	else:
		if dateinterval is None:
			response = requests.get(f'''{APIURL}/goodhits/campaigns/{camp_id} \
				/quality-analysis/{uid}?token={auth()['token']}''', headers=headers)
			if response.status_code == 200:
				return response.json()
			else:
				print('Site Stats: ' + str(response.status_code))
		else:
			response = requests.get(f'''{APIURL}/goodhits/campaigns/{camp_id} + \
				/quality-analysis/{uid}?token={auth()['token']} \ 
				&dateInterval={dateinterval}''', headers=headers)
			if response.status_code == 200:
				return response.json()
			else:
				print('Site Stats: ' + str(response.status_code))

# TODO Функция проверки сайтов по заданным параметрам

#print(site_stats(582530))
#print(user_campaigns(582530))
