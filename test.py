import os
from config import APP_STATIC

for filename in os.listdir(APP_STATIC):
    print(filename)
