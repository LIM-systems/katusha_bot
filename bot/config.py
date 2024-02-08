import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

ADM_ID = int(os.environ.get('ADM_ID'))
DEV_ID = int(os.environ.get('DEV_ID'))
DAYS = (
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    )