from api import Api
import json


accounts = []
CEND = '\33[0m'
CRED = '\33[31m'
CGREEN = '\33[32m'


if __name__ == '__main__':
    VALIDATE = True
    tokens = []
    with open('accounts.json') as file:
        accounts_file = json.load(file)
        for token in list(accounts_file.keys()):
            tokens.append(token)

    with open("tokens.txt", "r+") as file:
        for line in file:
            if line not in list(tokens) and len(line) > 0:
                tokens.append(line.strip())
        file.truncate(0)

    json_accounts = {}
    for token in tokens:
        account = Api(token, VALIDATE)
        if account.valid:
            accounts.append(account)
            json_accounts[account.token] = account.dump_json()

    with open('accounts.json', 'w') as file:
        json.dump(json_accounts, file, indent=4)
        print(CGREEN + "Dumped accounts" + CEND)
