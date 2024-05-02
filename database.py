from deta import Deta
DETA_KEY ='LiMnnNNe_CsjwjLjLxwbkHLymBX6LD7pcfafWEm6D'

deta = Deta(DETA_KEY)

db = deta.Base("users_db")

def insert_user(username, name, password):
    return db.put({"key": username, "name": name, "password": password})

insert_user("sandeep007", "Sandeep Pratap", "san007")