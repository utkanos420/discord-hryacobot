# Пока что это просто пример работы
import random

chance_of_common_hryak = 80
chance_of_uncommon_hryak = 20

def generate_drop():

    random_number = random.randint(1, 100)

    if random_number <= chance_of_common_hryak:
        return {"hryak_type": "common", "message": "Выпал обычный хряк!"}
    else:
        return {"hryak_type": "uncommon", "message": "Выпал необычный хряк!"}

