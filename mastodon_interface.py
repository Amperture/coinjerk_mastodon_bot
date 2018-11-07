import requests
import qrcode
import pprint

from io import BytesIO

from config_handler import config, save_config

API_PATH_GET_NOTIFICATIONS = '/api/v1/notifications'
API_PATH_POST_STATUS = '/api/v1/statuses'
API_PATH_POST_MEDIA = '/api/v1/media'

headers = {}
headers['Authorization'] = 'Bearer ' + config['mastodon']['access_token']

def check_notifications(): #{{{
    data = {}
    data['since_id'] = config['latest_notification']

    response = _mastodon_API_get(API_PATH_GET_NOTIFICATIONS, data)

    if response.status_code == 200 and response.json():
        latest_notification_id = response.json()[0]['id']
        config['mastodon']['latest_notification'] = latest_notification_id
        save_config(config)
        return response.json()
    elif response.status_code == 200:
        print("No new notifications")
        return False
    elif not response.status_code == 200:
        print("Something went wrong with the check!")
# }}}

def get_qr_link(text): #{{{
    link = _mastodon_upload_qr(text)
    return link
#}}}

def send_toot(toot_dict): #{{{
    text = toot_dict['text']
    _mastodon_push_message(text, 'public')
#}}}

def send_reply(toot_dict): #{{{
    text = toot_dict['text']
    replyTo = toot_dict['reply_to']
    _mastodon_push_message(text, 'public', replyTo = replyTo, files = None)
#}}}

def send_reply_qr_code(toot_dict): # {{{
    text = toot_dict['text']
    qr_data = toot_dict['qr']
    replyTo = toot_dict['reply_to']
    qr_media_id = [ _mastodon_upload_qr(qr_data) ]
    _mastodon_push_message(
            text, 
            'public', 
            replyTo = replyTo, 
            files = qr_media_id
    )
#}}}

def process_commands(commands): #{{{
    # Build Switch Case Setup for toots.
    switch = {
        'reply_qr' : send_reply_qr_code,
        'reply'    : send_reply,
        'public'   : send_toot,
    }
    for command in commands:
        switch[ command['type'] ](command)
#}}}

def _mastodon_upload_qr(toSend): #{{{
    img = qrcode.make(toSend)
    byte_io = BytesIO()
    img.save(byte_io, 'png')
    byte_io.seek(0)

    data = {
            'file' : byte_io

            #'files[]': (
                #'1.png', byte_io, 'image/png'
            #)
    }

    response = requests.post(
            url = config['mastodon']['host_instance'] + API_PATH_POST_MEDIA,
            files = data,
            headers = headers
    )

    if response.status_code == 200:
        qr_json = response.json()
        pprint.pprint(qr_json)
        return qr_json['id']
    else:
        print("Failed to upload QR Code.")
        pprint.pprint(response.json())
        pprint.pprint(response.status_code)
        return False
#}}}

def _mastodon_push_message(text, visibility, replyTo = None, files = [] ):#{{{
    data = {}
    data['visibility'] = visibility
    data['status'] = text
    data['in_reply_to_id'] = replyTo
    data['media_ids[]'] = files
    print("Data: ", data)

    response = requests.post(
            url = config['mastodon']['host_instance'] + API_PATH_POST_STATUS,
            data = data,
            headers = headers
    )

    if response.status_code == 200:
        print("Success!!")
        return True
    else:
        print("Fail...")
        return False
#}}}

def _mastodon_API_get(api_path, data):#{{{
    response = requests.get(
            url = config['mastodon']['host_instance'] + api_path,
            data = data,
            headers = headers
    )
    if response.status_code == 200:
        print("Success!!")
        return response
    else:
        print("Fail...")
        return False
#}}}
