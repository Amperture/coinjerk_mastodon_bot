from html2text import html2text

#{{{ Commands
def do_your_best(mention): #{{{
    #print("He wants me to do my best!")
    reply = {
        'type'     : 'reply',
        'reply_to' : mention['status']['id'],
        'text'     : ("@{} I'm going to do my best! " \
                + "You should too!").format(mention['account']['acct'])
    }
    return reply
#}}}
def testqr(mention): #{{{
    #print("He wants to see a QR Code!")
    reply = {
        'type'     : 'reply_qr',
        'reply_to' : mention['status']['id'],
        'text'     : "@{} Did I make a good QR Code?" \
                .format(mention['account']['acct']),
        'qr'     : (
        "bitcoin:bc1qve9xjmxugte40d9a26vd0us0xc3rekutsseg5k")
    }
    return reply
#}}}
def marco(mention): #{{{
    #print("He wants to play Marco Polo!")
    reply = {
        'type'     : 'reply',
        'reply_to' : mention['status']['id'],
        'text'     : "@{} Polo!" \
                .format(mention['account']['acct'])
    }
    return reply
#}}}
command_list = {#{{{
        'do your best' : do_your_best,
        'marco' : marco,
        'testqr' : testqr
        }#}}}
#}}}

def sort_mentions(notifications):#{{{
    sendback = []
    mentions = (x for x in notifications if x['type'] == 'mention')

    for mention in mentions:
        for key in command_list.keys():
            print(html2text(mention['status']['content']))
            print(key.lower())
            if key in mention['status']['content']:
                reply = command_list[key](mention)
                sendback.extend(reply) if type(reply) is list \
                    else sendback.append(reply)
    return sendback
#}}}
