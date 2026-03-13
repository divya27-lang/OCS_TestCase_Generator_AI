
import json
import requests


def get_offer(address, msisdn):
    retries = 0
    url = address + f'/tmf-api/ServiceActivationAndConfiguration/v3/service/{msisdn}?serviceType=Mobile Subscriber&fields=Account&fields=Offerings'
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    r = requests.get(url, headers=headers, auth=('api-user', 'password'), verify=False)
    offer_dict = {}
    while retries < 5 and r.status_code == 500:
        r = requests.get(url, headers=headers, auth=('api-user', 'password'), verify=False)
        retries = retries + 1

    if r.status_code == 200:
        for entry in json.loads(r.text)['serviceCharacteristic']:
            if entry['name'] == 'Offerings':
                for entry1 in entry['value']:
                    if entry1['OfferingID'] in [201000005]:
                        return True
                        # offer_dict['offers'] = entry1['OfferingID']
        return False
                        #to put something like flag
                        #offer_dict['Offer_id'] = entry['OfferingID']


    else:
        return False