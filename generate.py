import random
import uuid

import pandas as pd
from faker import Faker

fake = Faker()


pd.options.display.max_rows = 9999

df = pd.read_csv("bank_customer.csv")

users_ids = list(df["_id"])
m = {
    "transaction_id": [],
    "client_id": [],
    "amount": [],
    "date": [],
    "target_account": [],
}

transactions_len = 1000

for x in range(1, transactions_len):
    m["transaction_id"] = [str(uuid.uuid1()) for x in range(0, transactions_len)]
    m["amount"] = [
        round(random.uniform(1, 500000), 2) for x in range(0, transactions_len)
    ]
    m["date"] = [fake.date_time().isoformat() for x in range(0, transactions_len)]
    m["client_id"] = [random.choice(users_ids) for x in range(0, transactions_len)]
    m["target_account"] = [random.choice(users_ids) for x in range(0, transactions_len)]


d = pd.DataFrame(m)

d.to_csv("./bank_transactions.csv")
print(m)
