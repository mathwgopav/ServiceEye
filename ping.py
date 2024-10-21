import requests as rq

def ping(url):
    try:
        res = rq.get(url)
        if res.status_code == 200:
          print(f"A URL {url} está acessível. Status Code: {res.status_code}")
        else:
            print(f"A URL {url} respondeu com o código: {res.status_code}")
    except rq.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {e}")  

url = input("Digite a url: ")
urlTratada = url if url.startswith("https://") else "https://" + url 

ping(urlTratada)