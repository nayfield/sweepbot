import slack
import requests
import re

exec(open('config/slackcred.py').read())


def notify_mods(wc, user, why):
    print('Signoff', user, 'because:', why)
    msg = 'Signoff: <@{}> {}'.format(user, why)
    wc.chat_postMessage(channel=OUT_CHAN, text=msg)
    #     web_client.chat_postMessage(channel=channel_id, text=response)
    return True


@slack.RTMClient.run_on(event="message")
def modbot_message(**payload):
    """message trigger"""
    data = payload["data"]
    web_client = payload["web_client"]

    # Ignore things I am sending
    if data['user'] == SUID:
        return True

    # Ignore things not in the channels I monitor
    if data['channel'] not in IN_CHANS:
        return True

    # Ignore threads
    if 'thread_ts' in data:
        return True

    match = False
    for k in PHRASES:
        if k in data['text']:
            match = True
    if not match:
        return True

    notify_mods(web_client, data['user'], 'said '+data['text'])
    return True

@slack.RTMClient.run_on(event="reaction_added")
def modbot_react(**payload):
    """
    This function triggers when someone sends
    a message on the slack
    """
    data = payload["data"]
    web_client = payload["web_client"]

    # Ignore things I am sending
    if data['user'] == SUID:
        print('i see me')
        return True

    # Ignore things not in the channels I monitor
    if data['item']['channel'] not in IN_CHANS:
        return True

    # Ignore threads
    # This does not work for reactions.  need to use webapi.
#    if 'thread_ts' in data:
#        return True


    if data['user'] not in MODS:
        # return True
        pass
    if data['reaction'] not in EMOJIS:
        return true

    # double check user / item_user
    reason = 'Reaction {}  tagged by Mod  <@{}>'.format(data['reaction'], data['user'])
    notify_mods(web_client, data['item_user'], reason)
    return True

try:
    rtm_client = slack.RTMClient(token=TOKEN)
    print("Bot is up and running!")
    rtm_client.start()
except Exception as err:
    print(err)