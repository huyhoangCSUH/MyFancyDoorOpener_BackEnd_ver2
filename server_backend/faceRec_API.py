import requests
import json
import base64
import os

def enroll(photo):
    url = "https://api.kairos.com/enroll"

    headr = {
        'Content-type': 'application/json',
        'app_id': '38280dd7',
        'app_key': 'c96e8bcc7ddd1559b54a5e1dc81c809b'
    }

    payload = {
        'image': base64.b64encode(open(photo).read()),
        'subject_id': 'Huy',
        'gallery_name': 'HuyHoang'
    }

    r = requests.post(url, headers=headr, data=json.dumps(payload))

    response = json.loads(r.content)
    print response


def verify(photo):
    url = "https://api.kairos.com/verify"


    headr = {
        'Content-type': 'application/json',
        'app_id': '38280dd7',
        'app_key': 'c96e8bcc7ddd1559b54a5e1dc81c809b'
    }

    payload = {
        'image': base64.b64encode(open(photo).read()),
        'subject_id': 'Huy',
        'gallery_name': 'HuyHoang'
    }

    r = requests.post(url, headers=headr, data=json.dumps(payload))

    response = json.loads(r.content)
    print response


def recognize(photo):
    url = "https://api.kairos.com/recognize"
    userhome = os.path.expanduser('~')
    path_for_files = userhome + "/MyFancyDoorOpener_BackEnd_ver2/server_backend"
    headr = {
        'Content-type': 'application/json',
        'app_id': '38280dd7',
        'app_key': 'c96e8bcc7ddd1559b54a5e1dc81c809b'
    }

    payload = {
        'image': base64.b64encode(open(photo).read()),
        'gallery_name': 'HuyHoang'
    }

    r = requests.post(url, headers=headr, data=json.dumps(payload))

    response = json.loads(r.content)
    person_name = 'Unidentified!'
    print response

    if 'images' in response:
        if 'subject_id' in response['images'][0]['transaction']:
            person_name = response['images'][0]['transaction']['subject_id']

    #print person_name
    return person_name

#photofile = '/Users/huyhoang/PycharmProjects/MyFancyDoorOpener_BackEnd_ver2/server_backend/training-data/person0/9.jpg'
#recognize(photofile)
