from concurrent.futures import ThreadPoolExecutor
import requests


def get_cat(num):
    response = requests.get('https://aws.random.cat/meow').json().get('file')
    with open(f'cats/cat{num}.jpg', 'wb') as file:
        file.write(requests.get(response).content)


def multithreading():
    with ThreadPoolExecutor(max_workers=4) as executor:
        for count in range(1, 51):
            executor.submit(get_cat, count)


if __name__ == '__main__':
    multithreading()