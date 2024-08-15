import threading
import queue
import requests

q = queue.Queue()
valid_proxies=[]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"}

with open("proxy-list.txt",'r') as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)
        
def check_proxies():
    global q 
    while not q.empty():
        proxy = q.get()
        try:
            print(f"Using proxy : {proxy}")
            res = requests.get("https://www.ambitionbox.com/list-of-companies?page=1", proxies = {"http" : proxy, "https" : proxy},  headers = headers)

        except: 
            
            continue
        if res.status_code == 200:
            
            print("PROXY SUCCESSFULL")
            with open("valid_proxies.txt", "a") as f:
                f.write(proxy + "\n")
            print(proxy)
            
for _ in range(10):
    threading.Thread(target=check_proxies).start()