import json
import http.client
import mimetypes

clientId = ""
clientSecret = ""
tenantId = ""
resource = ""
subscriptionId = ""
loginUrl = ""
firstPart = 'grant_type=client_credentials&client_id='
secondPart = '&client_secret='
ThirdPart = '&resource=https%3A//management.azure.com/'
emergencyEvent = "statusActiveEvent"
value = ""

with open('configuretion.json') as json_file:
	data = json.load(json_file)
	for p in data['userConfiguration']:
		clientId +=  p['clientId']
		clientSecret += p['clientSecret']
		tenantId += p['tenantId']
		resource += p['resource']
		subscriptionId += p['subscriptionId']
		loginUrl += p['loginUrl']

conn = http.client.HTTPSConnection(loginUrl)


payload = '{}{}{}{}{}'.format(firstPart, clientId, secondPart, clientSecret, ThirdPart)

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'x-ms-gateway-slice=prod; stsservicecookie=ests; fpc=AsY9Nkg6w4VBvqtpzR428ifYAfKIAQAAAChmMdYOAAAA'
}


requestUrl = "/{}/oauth2/token".format(tenantId)

try:
	conn.request("POST", requestUrl, payload, headers)
except Exception as e:
	raise e
	print(e)
	print("Http error, server not found. Something went wrong with request")


res = conn.getresponse()
data = res.read()


#get Access token
try:
	responseFromPostReq = data.decode("utf-8")
	resp_dict = json.loads(responseFromPostReq)
	accessToken = resp_dict["access_token"]
except KeyError as e:
	raise e
	print("Something went wrong exctracting token from json")

#save to plain file
def saveDataToFile(data):
	try:
		with open('data.json', 'a') as json_file:
			json.dump(data, json_file)
	except Exception as e:
		raise e
		print("Error while dumping gathered data")


def getAvailabilityStatus(accessToken, subscriptionId):
	conn = http.client.HTTPSConnection("management.azure.com")
	payload = ''
	headers = {
	  'Authorization': 'Bearer {}'.format(accessToken)
	}
	requestUrl = "/subscriptions/{}/providers/Microsoft.ResourceHealth/availabilityStatuses?api-version=2018-07-01-preview&$expand=recommendedactions".format(subscriptionId)
	try:
		conn.request("GET",requestUrl , payload, headers)
		res = conn.getresponse()
	except requests.exceptions.RequestException as e:
		raise e
		print("Availability Status api could not connect")
	data = res.read()
	responseFromApi = data.decode("utf-8")
	saveDataToFile(responseFromApi)	


def getEmergingIssues(accessToken, emergencyEvent):
	conn = http.client.HTTPSConnection("management.azure.com")
	payload = ''
	headers = {
	  'Authorization': 'Bearer {}'.format(accessToken)
	}
	requestUrl = "https://management.azure.com/providers/Microsoft.ResourceHealth/emergingIssues/default?api-version=2018-07-01".format(emergencyEvent)
	try:
		conn.request("GET", requestUrl, payload, headers)
		res = conn.getresponse()
	except requests.exceptions.RequestException as e:
		raise e
		print("Availability Status api could not connect")
	data = res.read()
	responseFromApi = data.decode("utf-8")
	saveDataToFile(responseFromApi)


def GetEvents(accessToken, subscriptionId):
	conn = http.client.HTTPSConnection("management.azure.com")
	payload = ''
	requestUrl = "/subscriptions/{}/providers/Microsoft.ResourceHealth/events?api-version=2018-07-01".format(subscriptionId)
	headers = {
	  'Authorization': 'Bearer {}'.format(accessToken)
	}
	try:
		conn.request("GET", requestUrl, payload, headers)
		res = conn.getresponse()
	except requests.exceptions.RequestException as e:
		raise e
		print("Availability Status api could not connect")
	data = res.read()
	responseFromApi = data.decode("utf-8")
	saveDataToFile(responseFromApi)


getAvailabilityStatus(accessToken, subscriptionId)
getEmergingIssues(accessToken, emergencyEvent)
GetEvents(accessToken, subscriptionId)