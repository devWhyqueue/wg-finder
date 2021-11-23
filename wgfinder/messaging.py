import os

from twilio.rest import Client


def build_message(appointment_pairs):
    msg = f'Hi,\nthe Vaccinator found some appointment pairs for you!\nThese are your options:\n'
    for pair in appointment_pairs:
        msg += f'- {pair.centre}: First on {pair.first.date} at {pair.first.time},' \
               f'second one on {pair.second.date} at {pair.second.time}.\n'
    msg += '\nHappy vaccinating,\nThe Vaccinator'
    return msg


class SMSNotifier:
    def __init__(self, receiver):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)
        self.receiver = receiver

    def send_message(self, message):
        self.client.messages.create(from_='+19726274765', body=message, to=self.receiver)
