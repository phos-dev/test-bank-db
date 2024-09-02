import random
import uuid
import pandas as pd
from faker import Faker

fake = Faker("pt_BR")
pd.options.display.max_rows = 9999

########## Clientes

bank_client = {
    "id": [],
    "name": [],
    "birthdate": [],
    "gender": [],
    "address": [],
}

# Seed bank clients table
bank_client_len = 5
bank_client["id"] = [
    str(uuid.UUID(int=random.getrandbits(128), version=4))
    for x in range(0, bank_client_len)
]
bank_client["gender"] = [
    random.choice(["male", "female"]) for x in range(0, bank_client_len)
]
bank_client["name"] = [
    (
        fake.first_name_male()
        if bank_client["gender"][x] == "male"
        else fake.first_name_female()
    )
    for x in range(0, bank_client_len)
]
bank_client["address"] = [fake.address() for x in range(0, bank_client_len)]
bank_client["birthdate"] = [fake.date_of_birth() for x in range(0, bank_client_len)]

pd.DataFrame(bank_client).to_csv("./bank_customer.csv")

########## Cartão de Crédito

bank_cards = {
    "id": [],
    "client_id": [],
    "number": [],
    "security_code": [],
    "provider": [],
    "expiration_date": [],
    # "limit": []
}

total_cards_len = 10
bank_cards["id"] = [
    str(uuid.UUID(int=random.getrandbits(128), version=4))
    for x in range(0, total_cards_len)
]
bank_cards["expiration_date"] = [
    fake.credit_card_expire() for x in range(0, total_cards_len)
]
bank_cards["provider"] = [
    fake.credit_card_provider() for x in range(0, total_cards_len)
]
bank_cards["number"] = [fake.credit_card_number() for x in range(0, total_cards_len)]
bank_cards["security_code"] = [
    fake.credit_card_security_code() for x in range(0, total_cards_len)
]
bank_cards["client_id"] = [
    random.choice(bank_client["id"]) for x in range(0, total_cards_len)
]

pd.DataFrame(bank_cards).to_csv("./bank_cards.csv")

########## Contas

bank_accounts = {"id": [], "client_id": [], "type": [], "balance": [], "currency": []}
bank_accounts_len = bank_client_len + 2
pending_client_ids = set(bank_client["id"])

bank_accounts["id"] = [
    str(uuid.UUID(int=random.getrandbits(128), version=4))
    for x in range(0, bank_accounts_len)
]

for accountIndex in range(0, bank_accounts_len):
    client_id = None
    if len(pending_client_ids) > 0:
        client_id = random.choice(list(pending_client_ids))
        pending_client_ids.remove(client_id)
    else:
        client_id = random.choice(bank_client["id"])
    bank_accounts["client_id"].insert(accountIndex, client_id)

bank_accounts["type"] = [
    random.choice(["pj", "pf"]) for _ in range(0, len(bank_accounts["id"]))
]
bank_accounts["balance"] = [
    random.randint(-2000, 130000) / 100 for _ in range(0, len(bank_accounts["id"]))
]
bank_accounts["currency"] = [
    fake.currency_symbol() for _ in range(0, len(bank_accounts["id"]))
]

pd.DataFrame(bank_accounts).to_csv("./bank_accounts.csv")

########## Transações

bank_transactions = {
    "id": [],
    "value": [],
    "from_account": [],
    "to_account": [],
    "date": [],
    "method": [],
    "method_id": [],
}

bank_transactions_len = 5

bank_transactions["id"] = [
    str(uuid.UUID(int=random.getrandbits(128), version=4))
    for _ in range(0, bank_transactions_len)
]
bank_transactions["value"] = [
    random.randint(-2000, 130000) / 100 for _ in range(0, bank_transactions_len)
]
bank_transactions["from_account"] = [
    random.choice(bank_accounts["id"]) for _ in range(0, bank_transactions_len)
]

for transactionIndex in range(0, bank_transactions_len):
    to_account = random.choice(bank_accounts["id"])
    while to_account == bank_transactions["from_account"][transactionIndex]:
        to_account = random.choice(bank_accounts["id"])

    bank_transactions["to_account"].insert(transactionIndex, to_account)

bank_transactions["date"] = [
    fake.date_of_birth() for _ in range(0, bank_transactions_len)
]
bank_transactions["method"] = [
    random.choice(["ted", "doc", "pix", "credit_card"])
    for _ in range(0, bank_transactions_len)
]


for transactionIndex in range(0, bank_transactions_len):
    method = bank_transactions["method"][transactionIndex]
    method_id = None

    if method == "pix":
        method_id = random.choice([fake.phone_number(), fake.cnpj(), fake.cpf()])
    elif method == "credit_card":  # Get origin client credit_card
        account_client_id = [
            bank_accounts["client_id"][bank_accounts["id"].index(account_id)]
            for account_id in bank_accounts["id"]
            if account_id
            == bank_transactions["from_account"][
                transactionIndex
            ]  # Current transaction account id
        ]
        account_client_id = account_client_id[0]
        client_cards = [
            bank_cards["id"][bank_cards["client_id"].index(client_id)]
            for client_id in bank_cards["client_id"]
            if client_id == account_client_id
        ]
        method_id = random.choice(client_cards)

    bank_transactions["method_id"].insert(transactionIndex, method_id)

pd.DataFrame(bank_transactions).to_csv("./bank_transactions.csv")
