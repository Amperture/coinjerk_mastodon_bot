
def sort_mentions(mentions):
    sendback = []
    for x in mentions:
        if x['type'] == 'mention':
            y = x['status']
            #pprint.pprint(y)
            print('From: ' + y['account']['acct']) 
            print('Text: ' + y['content']) 
            print('Toot ID: ' + y['id']) 

            if "do your best" in y['content'].lower():
                print("He wants me to do my best!")
                reply = {
                    'type'     : 'reply',
                    'reply_to' : y['id'],
                    'text'     : "@{} I'm going to do my best!" \
                            .format(y['account']['acct'])
                }
                sendback.append(reply)

            #{{{ Marco
            if "marco" in y['content'].lower():
                print("He wants to play Marco Polo!")
                reply = {
                    'type'     : 'reply',
                    'reply_to' : y['id'],
                    'text'     : "@{} Polo!" \
                            .format(y['account']['acct'])
                }
                sendback.append(reply)
            #}}} Marco
            #{{{ Test QR
            if "testqr" in y['content'].lower():
                print("He wants to see a QR Code!")
                reply = {
                    'type'     : 'reply_qr',
                    'reply_to' : y['id'],
                    'text'     : "@{} Did I make a good QR Code?" \
                            .format(y['account']['acct']),
                    'qr'     : (
                    "bitcoin:bc1qve9xjmxugte40d9a26vd0us0xc3rekutsseg5k")
                }
                sendback.append(reply)
            #}}} Test QR
    return sendback
