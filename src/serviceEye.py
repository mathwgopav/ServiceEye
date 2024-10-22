import os
import json
from datetime import datetime
import nest_asyncio
import httpx
import asyncio

nest_asyncio.apply()

# Function to load existing URLs from a JSON file
def load_urls(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        create_json_file(filename)
        return []

def format_url(url):
    new_url = url if url.startswith("https://") else "https://" + url
    print('Formatted', new_url)
    return new_url

def save_urls(filename, urls):
    with open(filename, 'w') as file:
        json.dump(urls, file, indent=4)

def add_url(filename, new_url):
    new_url = format_url(new_url)

    # Load existing URLs
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            urls = json.load(file)
    else:
        urls = []

    # Check for duplicates
    if new_url not in urls:
        urls.append(new_url)
        # Save the updated list back to the JSON file
        with open(filename, 'w') as file:
            json.dump(urls, file, indent=4)
        print(f"URL '{new_url}' added.")
    else:
        print("URL already exists.")

def create_json_file(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file, indent=4)
        print(f"JSON file '{filename}' created with an empty array.")
    else:
        print(f"JSON file '{filename}' already exists.")

def create_log_file(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write("")  # Optionally write a header or leave it empty
        print(f"Log file '{filename}' created.")
    else:
        print(f"Log file '{filename}' already exists.")

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_log(filename, message):
    if isinstance(message, list):
        message = '\n'.join(message)

    if os.path.exists(filename):
        with open(filename, 'a') as file:
            file.write(message + '\n')
    else:
        create_log_file(filename)
        save_log(filename, message)

# Class ServiceEye
class ServiceEye:
    def __init__(self):
        out_dir = './out/'
        os.makedirs(out_dir, exist_ok=True)
        
        self.filepath = os.path.join(out_dir, 'urls.json')
        self.logpath = os.path.join(out_dir, 'logs.txt')
        self.urls = load_urls(self.filepath)
        self.default_sleep_timer = 200

    async def ping(self, url):
        response_string = None
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    response_string = f"[{current_time()}]: A URL {url} está acessível. Status Code: {res.status_code}"
                else:
                    response_string = f"[{current_time()}]: A URL {url} respondeu com o código: {res.status_code}"

                return response_string

        except httpx.RequestError as e:
            response_string = f"[{current_time()}]: Erro ao acessar a URL {url}: {e}"
            return response_string

    def add_url(self, url):
        add_url(self.filepath, url)

    async def check_services_health(self):
        self.urls = load_urls(self.filepath)
        tasks = [self.ping(url) for url in self.urls]
        results = await asyncio.gather(*tasks)

        save_log(self.logpath, results)
        return results

    async def runner(self, timer=30):
        while True:
            res = await self.check_services_health()
            print(res)
            await asyncio.sleep(30)
