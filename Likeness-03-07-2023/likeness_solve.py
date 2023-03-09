import requests
import time

url = "http://puzzler7.imaginaryctf.org:11000/"

for i in range(100):
    r = requests.get(url, params = {"lastname" : i * "_"})
    print(f"====================")
    print(f"{i}: {r.text}")
    time.sleep(0.2)